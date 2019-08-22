/* Udacity Homework 3
HDR Tone-mapping

Background HDR
==============

A High Dynamic Range (HDR) image contains a wider variation of intensity
and color than is allowed by the RGB format with 1 byte per channel that we
have used in the previous assignment.

To store this extra information we use single precision floating point for
each channel.  This allows for an extremely wide range of intensity values.

In the image for this assignment, the inside of church with light coming in
through stained glass windows, the raw input floating point values for the
channels range from 0 to 275.  But the mean is .41 and 98% of the values are
less than 3!  This means that certain areas (the windows) are extremely bright
compared to everywhere else.  If we linearly map this [0-275] range into the
[0-255] range that we have been using then most values will be mapped to zero!
The only thing we will be able to see are the very brightest areas - the
windows - everything else will appear pitch black.

The problem is that although we have cameras capable of recording the wide
range of intensity that exists in the real world our monitors are not capable
of displaying them.  Our eyes are also quite capable of observing a much wider
range of intensities than our image formats / monitors are capable of
displaying.

Tone-mapping is a process that transforms the intensities in the image so that
the brightest values aren't nearly so far away from the mean.  That way when
we transform the values into [0-255] we can actually see the entire image.
There are many ways to perform this process and it is as much an art as a
science - there is no single "right" answer.  In this homework we will
implement one possible technique.

Background Chrominance-Luminance
================================

The RGB space that we have been using to represent images can be thought of as
one possible set of axes spanning a three dimensional space of color.  We
sometimes choose other axes to represent this space because they make certain
operations more convenient.

Another possible way of representing a color image is to separate the color
information (chromaticity) from the brightness information.  There are
multiple different methods for doing this - a common one during the analog
television days was known as Chrominance-Luminance or YUV.

We choose to represent the image in this way so that we can remap only the
intensity channel and then recombine the new intensity values with the color
information to form the final image.

Old TV signals used to be transmitted in this way so that black & white
televisions could display the luminance channel while color televisions would
display all three of the channels.


Tone-mapping
============

In this assignment we are going to transform the luminance channel (actually
the log of the luminance, but this is unimportant for the parts of the
algorithm that you will be implementing) by compressing its range to [0, 1].
To do this we need the cumulative distribution of the luminance values.

Example
-------

input : [2 4 3 3 1 7 4 5 7 0 9 4 3 2]
min / max / range: 0 / 9 / 9

histo with 3 bins: [4 7 3]

cdf : [4 11 14]


Your task is to calculate this cumulative distribution by following these
steps.

*/

#include "utils.h"


// GPU Kernels *************

__global__ void find_max_kernel(float * d_out, const float * d_in)
{
	// sdata is allocated in the kernel call: 3rd arg to <<<b, t, shmem>>>
	extern __shared__ float sdata[];

	const int threadGId = blockIdx.x * blockDim.x + threadIdx.x;
	const int threadLId = threadIdx.x;

	// load shared mem from global mem
	sdata[threadLId] = d_in[threadGId];
	__syncthreads();            // make sure entire block is loaded!

								// do reduction in shared mem
	for (unsigned int blockHalfSize = blockDim.x / 2; blockHalfSize > 0; blockHalfSize >>= 1) {
		if (threadLId < blockHalfSize) {
			sdata[threadLId] = max(sdata[threadLId], sdata[threadLId + blockHalfSize]);
		}
		__syncthreads();        // make sure all adds at one stage are done!
	}

	// only thread 0 writes result for this block back to global mem
	if (threadLId == 0)
	{
		d_out[blockIdx.x] = sdata[0];
	}
}

__global__ void find_min_kernel(float * d_out, const float * d_in)
{
	// sdata is allocated in the kernel call: 3rd arg to <<<b, t, shmem>>>
	extern __shared__ float sdata[];

	const int threadGId = blockIdx.x * blockDim.x + threadIdx.x;
	const int threadLId = threadIdx.x;

	// load shared mem from global mem
	sdata[threadLId] = d_in[threadGId];
	__syncthreads();            // make sure entire block is loaded!

								// do reduction in shared mem
	for (unsigned int blockHalfSize = blockDim.x / 2; blockHalfSize > 0; blockHalfSize >>= 1) {
		if (threadLId < blockHalfSize) {
			sdata[threadLId] = min(sdata[threadLId], sdata[threadLId + blockHalfSize]);
		}
		__syncthreads();        // make sure all adds at one stage are done!
	}

	// only thread 0 writes result for this block back to global mem
	if (threadLId == 0)
	{
		d_out[blockIdx.x] = sdata[0];
	}
}

__global__ void calc_histogram_kernel(const float* const d_in,
	float* d_minArray,
	float* d_maxArray,
	size_t* d_numBins,
	unsigned int * d_bincount) {

	const int threadGId = blockIdx.x * blockDim.x + threadIdx.x;

	const float range = *d_maxArray - *d_minArray;
	float item = d_in[threadGId];

	int bin = (item - *d_minArray) / range * *d_numBins;
	//printf("BlockDim: %d BlockInd: %d ThreadG: %d Item: %f Bin: %d\n", blockDim.x, blockIdx.x, threadGId, item, bin);

	atomicAdd(&(d_bincount[bin]), 1);
}

__global__ void calc_cdf_kernel(unsigned int* const d_cdf,
	size_t ArraySize) {

	const int threadGId = blockIdx.x * blockDim.x + threadIdx.x;

	for (int s = 1; s <= ArraySize; s *= 2) {
		int spot = threadGId - s;

		unsigned int val = 0;
		if (spot >= 0)
			val = d_cdf[spot];
		__syncthreads();
		if (spot >= 0)
			d_cdf[threadGId] += val;
		__syncthreads();
	}
}




void find_max(const float* const d_logLuminance,
	float &max_logLum,
	const size_t ArraySize) {

	// declare GPU memory pointers
	float *d_intermediate, *d_out;

	size_t ARRAY_BYTES = sizeof(float)*ArraySize;

	// Allocate memory on GPU
	checkCudaErrors(cudaMalloc((void **)&d_intermediate, ARRAY_BYTES / 2));
	checkCudaErrors(cudaMalloc((void **)&d_out, sizeof(float)));


	const int maxThreadsPerBlock = 1024;
	int threads = maxThreadsPerBlock;
	int blocks = ArraySize / maxThreadsPerBlock;

	// Launch the first kernel to find the min and max
	find_max_kernel << <blocks, threads, threads * sizeof(float) >> > (d_intermediate, d_logLuminance);

	// Call cudaDeviceSynchronize(), then call checkCudaErrors() immediately after
	// launching your kernel to make sure that you didn't make any mistakes.
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());

	threads = blocks;
	blocks = 1;
	// Launch the second kernel to find the min and max
	find_max_kernel << <blocks, threads, threads * sizeof(float) >> > (d_out, d_intermediate);
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());

	// Get max value from GPU memory
	checkCudaErrors(cudaMemcpy(&max_logLum, d_out, sizeof(float), cudaMemcpyDeviceToHost));

	// free GPU memory allocation
	checkCudaErrors(cudaFree(d_intermediate));
	checkCudaErrors(cudaFree(d_out));

}

void find_min(const float* const d_logLuminance,
	float &min_logLum,
	const size_t ArraySize) {

	// declare GPU memory pointers
	float *d_intermediate, *d_out;

	size_t ARRAY_BYTES = sizeof(float)*ArraySize;

	// Allocate memory on GPU
	checkCudaErrors(cudaMalloc((void **)&d_intermediate, ARRAY_BYTES / 2));
	checkCudaErrors(cudaMalloc((void **)&d_out, sizeof(float)));


	const int maxThreadsPerBlock = 1024;
	int threads = maxThreadsPerBlock;
	int blocks = ArraySize / maxThreadsPerBlock;

	// Launch the first kernel to find the min and max
	find_min_kernel << <blocks, threads, threads * sizeof(float) >> > (d_intermediate, d_logLuminance);

	// Call cudaDeviceSynchronize(), then call checkCudaErrors() immediately after
	// launching your kernel to make sure that you didn't make any mistakes.
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());

	threads = blocks;
	blocks = 1;
	// Launch the second kernel to find the min and max
	find_min_kernel << <blocks, threads, threads * sizeof(float) >> > (d_out, d_intermediate);
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());

	// Get max value from GPU memory
	checkCudaErrors(cudaMemcpy(&min_logLum, d_out, sizeof(float), cudaMemcpyDeviceToHost));

	// free GPU memory allocation
	checkCudaErrors(cudaFree(d_intermediate));
	checkCudaErrors(cudaFree(d_out));

}

void calc_histogram(const float* const d_logLuminance,
	unsigned int *h_bincount,
	float &min_logLum,
	float &max_logLum,
	const size_t numBins,
	const size_t ArraySize) {

	// declare GPU memory pointers
	float *d_minArray, *d_maxArray;
	size_t *d_numBins;
	unsigned int *d_bincount;

	// Allocate memory on GPU
	checkCudaErrors(cudaMalloc((void **)&d_minArray, sizeof(float)));
	checkCudaErrors(cudaMalloc((void **)&d_maxArray, sizeof(float)));
	checkCudaErrors(cudaMalloc((void **)&d_numBins, sizeof(size_t)));
	checkCudaErrors(cudaMalloc((void **)&d_bincount, sizeof(unsigned int)*numBins));

	// Copy from host to device
	checkCudaErrors(cudaMemcpy(d_minArray, &min_logLum, sizeof(float), cudaMemcpyHostToDevice));
	checkCudaErrors(cudaMemcpy(d_maxArray, &max_logLum, sizeof(float), cudaMemcpyHostToDevice));
	checkCudaErrors(cudaMemcpy(d_numBins, &numBins, sizeof(size_t), cudaMemcpyHostToDevice));

	const int maxThreadsPerBlock = 1024;
	int threads = maxThreadsPerBlock;
	int blocks = ArraySize / maxThreadsPerBlock;

	calc_histogram_kernel << <blocks, threads >> > (d_logLuminance, d_minArray, d_maxArray, d_numBins, d_bincount);
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());


	// Get bincount value from GPU memory
	checkCudaErrors(cudaMemcpy(h_bincount, d_bincount, sizeof(unsigned int)*numBins, cudaMemcpyDeviceToHost));

	// free GPU memory allocation
	checkCudaErrors(cudaFree(d_minArray));
	checkCudaErrors(cudaFree(d_maxArray));
	checkCudaErrors(cudaFree(d_numBins));
	checkCudaErrors(cudaFree(d_bincount));

}


void calc_cdf(unsigned int *h_bincount,
	const size_t numBins,
	size_t ArraySize,
	unsigned int* const d_cdf) {

	unsigned int * d_bincount;

	// Allocate memory on GPU
	checkCudaErrors(cudaMalloc((void **)&d_bincount, sizeof(unsigned int)*numBins));

	// Copy from host to device
	checkCudaErrors(cudaMemcpy(d_cdf, h_bincount, sizeof(unsigned int)*numBins, cudaMemcpyHostToDevice));

	const int maxThreadsPerBlock = 1024;
	int threads = maxThreadsPerBlock;
	int blocks = ArraySize / maxThreadsPerBlock;

	calc_cdf_kernel << <blocks, threads >> > (d_cdf, ArraySize);
	cudaDeviceSynchronize(); checkCudaErrors(cudaGetLastError());

}




void your_histogram_and_prefixsum(const float* const d_logLuminance,
	unsigned int* const d_cdf,
	float &min_logLum,
	float &max_logLum,
	const size_t numRows,
	const size_t numCols,
	const size_t numBins)
{
	//TODO
	/*Here are the steps you need to implement
	1) find the minimum and maximum value in the input logLuminance channel
	store in min_logLum and max_logLum
	2) subtract them to find the range
	3) generate a histogram of all the values in the logLuminance channel using
	the formula: bin = (lum[i] - lumMin) / lumRange * numBins
	4) Perform an exclusive scan (prefix sum) on the histogram to get
	the cumulative distribution of luminance values (this should go in the
	incoming d_cdf pointer which already has been allocated for you)       */


	const size_t arraySize = numRows*numCols;

	find_max(d_logLuminance, max_logLum, arraySize);
	find_min(d_logLuminance, min_logLum, arraySize);

	float range = max_logLum - min_logLum;

	printf("Max: %f Min: %f Range: %f\n", max_logLum, min_logLum, range);

	// Allocate memory for histogram
	unsigned int *h_bincount = (unsigned int *)malloc(sizeof(unsigned int)*numBins);

	calc_histogram(d_logLuminance, h_bincount, min_logLum, max_logLum, numBins, arraySize);

	calc_cdf(h_bincount, numBins, arraySize, d_cdf);


	/*unsigned int *h_cdf = (unsigned int *)malloc(sizeof(unsigned int)*numBins);
	cudaMemcpy(h_cdf, d_cdf, sizeof(unsigned int) * 100, cudaMemcpyDeviceToHost);

	for (int i = 0; i < 100; i++)
		printf("Hst out %d\n", h_bincount[i]);

	for (int i = 0; i < 100; i++)
		printf("Cdf out %d\n", h_cdf[i]);*/

}

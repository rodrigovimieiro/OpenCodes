
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "gputimer.h"

#include <stdio.h>

const int N = 512;		// matrix size is NxN
const int K = 16;	    	// TODO, set K to the correct value and tile size will be KxK


							// to be launched with one thread per element, in KxK threadblocks
							// thread (x,y) in grid writes element (i,j) of output matrix 
__global__ void
transpose_parallel_per_element(float in[], float out[])
{
	//TODO
	const int thread_2D_posX = blockIdx.x * blockDim.x + threadIdx.x;
	const int thread_2D_posY  = blockIdx.y * blockDim.y + threadIdx.y;

	out[thread_2D_posY + thread_2D_posX*N] = in[thread_2D_posX + thread_2D_posY*N]; // out(j,i) = in(i,j)

}


// to be launched on a single thread
__global__ void
transpose_serial(float in[], float out[])
{
	for (int j = 0; j < N; j++)
		for (int i = 0; i < N; i++)
			out[j + i*N] = in[i + j*N]; // out(j,i) = in(i,j)
}

// to be launched with one thread per row of output matrix
__global__ void
transpose_parallel_per_row(float in[], float out[])
{
	int i = threadIdx.x;

	for (int j = 0; j < N; j++)
		out[j + i*N] = in[i + j*N]; // out(j,i) = in(i,j)
}






//The following functions and kernels are for your reference
void transpose_CPU(float in[], float out[])
{
	for (int j = 0; j < N; j++)
		for (int i = 0; i < N; i++)
			out[j + i*N] = in[i + j*N]; // out(j,i) = in(i,j)
}

// fill a matrix with sequential numbers in the range 0..N-1
void fill_matrix(float *mat)
{
	for (int j = 0; j < N * N; j++)
		mat[j] = (float)j;
}

int compare_matrices(float *gpu, float *ref)
{
	int result = 0;

	for (int j = 0; j < N; j++)
		for (int i = 0; i < N; i++)
			if (ref[i + j*N] != gpu[i + j*N])
			{
				// printf("reference(%d,%d) = %f but test(%d,%d) = %f\n",
				// i,j,ref[i+j*N],i,j,test[i+j*N]);
				result = 1;
			}
	return result;
}






int main(int argc, char **argv)
{
	int numbytes = N * N * sizeof(float);

	float *in = (float *)malloc(numbytes);
	float *out = (float *)malloc(numbytes);
	float *gold = (float *)malloc(numbytes);

	fill_matrix(in);
	transpose_CPU(in, gold);

	float *d_in, *d_out;

	cudaMalloc(&d_in, numbytes);
	cudaMalloc(&d_out, numbytes);
	cudaMemcpy(d_in, in, numbytes, cudaMemcpyHostToDevice);

	GpuTimer timer;


	// Serial
	/*timer.Start();
	transpose_serial << <1, 1 >> >(d_in, d_out);
	timer.Stop();
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_serial: %g ms.\nVerifying transpose...%s\n",
		timer.Elapsed(), compare_matrices(out, gold) ? "Failed" : "Success");*/

	// 1 Thread per row
	timer.Start();
	transpose_parallel_per_row << <1, N >> >(d_in, d_out);
	timer.Stop();
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_parallel_per_row: %g ms.\nVerifying transpose...%s\n",
		timer.Elapsed(), compare_matrices(out, gold) ? "Failed" : "Success");


	/*
	* Now time each kernel and verify that it produces the correct result.
	*
	* To be really careful about benchmarking purposes, we should run every kernel once
	* to "warm" the system and avoid any compilation or code-caching effects, then run
	* every kernel 10 or 100 times and average the timings to smooth out any variance.
	* But this makes for messy code and our goal is teaching, not detailed benchmarking.
	*/

	dim3 threads(K, K);	// TODO, you need to define the correct threads per block
	dim3 blocks(N/K, N/K); // TODO, you need to define the correct blocks per grid

	timer.Start();
	transpose_parallel_per_element << <blocks, threads >> >(d_in, d_out);
	timer.Stop();
	cudaMemcpy(out, d_out, numbytes, cudaMemcpyDeviceToHost);
	printf("transpose_parallel_per_element: %g ms.\nVerifying transpose...%s\n",
		timer.Elapsed(), compare_matrices(out, gold) ? "Failed" : "Success");

	cudaFree(d_in);
	cudaFree(d_out);
}
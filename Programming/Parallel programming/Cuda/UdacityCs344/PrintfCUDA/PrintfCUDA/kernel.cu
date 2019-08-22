
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

// Block index Printf (Rodrigo)

#include <stdio.h>

#define NUM_BLOCKS 16
#define BLOCK_WIDTH 1

__global__ void hello()
{
	printf("Hello world! I'm a thread in block %d\n", blockIdx.x);
}


int main(int argc, char **argv)
{
	// launch the kernel
	hello << <NUM_BLOCKS, BLOCK_WIDTH >> >();

	// force the printf()s to flush
	cudaDeviceSynchronize();

	printf("That's all!\n");

	return 0;
}

// Block Thread Printf (Rodrigo)


/*#include <stdio.h>

#define NUM_BLOCKS 1
#define BLOCK_WIDTH 256

__global__ void hello()
{
	printf("Hello world! I'm thread %d\n", threadIdx.x);
}


int main(int argc, char **argv)
{
	// launch the kernel
	hello << <NUM_BLOCKS, BLOCK_WIDTH >> >();

	// force the printf()s to flush
	cudaDeviceSynchronize();

	printf("That's all!\n");

	return 0;
}*/
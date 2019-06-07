#include <stdio.h>
#include <omp.h>

int main()
{
	// Here goes your serial code
	printf("Serial Hello World!!\n");

#pragma omp parallel num_threads(4)
	{
		// Here goes your parrallel code
		printf("Parallel Hello World!!\n");
	}

	return 0;
}

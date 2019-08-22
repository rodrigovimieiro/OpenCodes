#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define nThreads 4

double sharedSum[nThreads];

int main(int argc, char **argv)
{
	// Here goes your serial code

	unsigned long nIte;

	nIte = atoi(argv[1]);

	printf("N iterations: %d\n", nIte);



#pragma omp parallel num_threads(nThreads)
	{
		// Here goes your parrallel code

		unsigned int threadId, rangeInit, rangeFinal;
		double numerator = -1;

		threadId = omp_get_thread_num();

		rangeInit = (nIte / nThreads)*threadId;
		rangeFinal = (nIte / nThreads)*(threadId + 1);

		//printf("Thread %d - RangeI: %d RangeF:%d \n",threadId,rangeInit,rangeFinal);

		if (threadId == nThreads - 1) // Last thread get the rest of iterations
		{
			rangeFinal = nIte;
		}

		if ((rangeInit % 2) == 0)
			numerator = 1;

		sharedSum[threadId] = 0;
		for (unsigned long i = rangeInit; i<rangeFinal; i++)
		{
			sharedSum[threadId] += numerator / (2.0*i + 1.0);
			numerator = -numerator;
		}

		//printf("Sharedsum: %f \n",sharedSum[threadId]);

	}

	double sum=0;

	for (int i = 0; i<nThreads; i++)
		sum += sharedSum[i];

	sum = sum * 4;

	printf("Pi: %f\n", sum);

	return 0;
}
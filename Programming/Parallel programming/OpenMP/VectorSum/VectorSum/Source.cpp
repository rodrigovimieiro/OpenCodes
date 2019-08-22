#include<stdio.h>
#include<stdlib.h>
#include<omp.h>

// g++-9 findPerfectNumber.cpp -o findPerfectNumber -fopenmp

int main(void) {

	int vectorSize, sum = 0;
	int *pVector;

	fscanf_s(stdin, "%d\n", &vectorSize);

	pVector = (int*)malloc(vectorSize * sizeof(int));

	for (int i = 0; i<vectorSize; i++)
		fscanf_s(stdin, "%d", &(pVector[i]));


#pragma omp parallel reduction(+:sum)
	{
#pragma omp for schedule(auto)
		for (int i = 0; i<vectorSize; i++)
			sum += pVector[i];
	}


	printf("%d", sum);
	free(pVector);
}

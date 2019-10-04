#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// g++-9 findPerfectNumber.cpp -o findPerfectNumber -fopenmp

int main(int argc, char **argv) {

	int range = atoi(argv[1]);

#pragma omp parallel
	{
#pragma omp for schedule(auto)
		for (int i = 1; i < range; i++)
		{
			int soma = 0;
			for (int j = 1; j < i; j++)
			{
				if (i%j == 0)
				{
					soma += j;
				}
			}
			if (soma == i)
			{
				printf("%d ", i);
			}
		}

	}

	return 0;
}

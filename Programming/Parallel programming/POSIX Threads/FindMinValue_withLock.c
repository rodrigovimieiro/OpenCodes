#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define N 450000000
#define P 8

unsigned int posInit[P], posFinal[P],arg_in[P];
signed int A[N], min_global,min_local_global[P];
sem_t  mutex;

void * findMin(int * arg_in);


int main(void) {
	
	pthread_t *min_handle;
	
	min_handle = (pthread_t *)malloc(P * sizeof(pthread_t ));
	
	srand(time(NULL));   // Initialization, should only be called once.
	
	sem_init (&mutex, 0 , 1);
	
	printf("\n\n***************\n\n");
	
	for (int i = 0; i < N; i++) {
	    //A[i] = (N - 1) - i;
	    A[i] = rand();
	}
	
	min_global = A[0];
	
	int div = N/P;
	
	//printf("div:%d\n",div);
	
	for(int k = 0;k < P; k++){
		posInit[k] = k*div;
		posFinal[k] = ((k+1)*div)-1;
		//printf("PosInit: %d Posfinal: %d \n",posInit[k],posFinal[k]);
	}	
	posFinal[P-1] = N-1;
	
	
	for(int k = 0;k < P; k++){
		arg_in[k] = k;
		if (pthread_create(&min_handle[k], 0, (void *) findMin, (void *) &arg_in[k]) != 0) { 
			printf("Error creating thread! Exiting! \n");
			exit(0);
		}
		
	}
	
	for(int k = 0;k < P; k++){
		pthread_join(min_handle[k], NULL);
	}
	
	printf("\n min = %d, N = %d \n", min_global, N);
	
	printf("\n\n***************\n\n");

	fflush(0);
	
	return 0;
} // fim main()

void * findMin(int * arg_in)
{
	
	int tid = arg_in[0];
	
	signed int min_local = A[posInit[tid]]; 

	for (int ind = posInit[tid]+1; ind<= posFinal[tid]; ind++) 
	    if (A[ind] < min_local) 
			min_local = A[ind]; 

	printf("I am thread: %d, PosInit: %d Posfinal: %d, with min value: %d\n", tid,posInit[tid],posFinal[tid], min_local);
	
	sem_wait(&mutex);
	if(min_local < min_global)
		min_global = min_local;
	sem_post(&mutex);
	
}
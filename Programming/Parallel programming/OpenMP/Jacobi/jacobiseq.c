// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: October, 2019
rodrigo.vimieiro@gmail.com
=========================================================================

Compile it -> gcc jacobiseq.c -o jacobiseq.bin

*/
// ---------------------------------------------------------------------------------------

#include "jacobiseq.h"

/*
*** MAIN ***
*/
int main(int argc,char **argv){

    unsigned int rank, nTreads;
    unsigned int nIter;

    // Test if the arguments are correct
    if(argc==3){

        char *p;

        errno = 0;

        rank = (unsigned int) strtol(argv[1], &p, 10);
        nTreads = (unsigned int) strtol(argv[2], &p, 10);

        // https://stackoverflow.com/a/9748431/8682939
        // Check for errors: e.g., the string does not represent an integer
        // or the integer is larger than int
        if (errno != 0 || *p != '\0' || rank > INT_MAX) {
            // Put here the handling of the error, like exiting the program with
            // an error message
            printf("*** Error: Please, give the program its correct input: <rank, nThreads> ***\n");
            return 0;
        }

    }
    else{
        printf("*** Error: Please, give the program its correct input: <rank, nThreads> ***\n");
        return 0;
    }



    const float epsilon = PRECISION;

    float b_hat[rank];

    // Memory allocation for matrix A, x and b
	float* const A = (float*)malloc(rank*rank * sizeof(float));
    float* const x = (float*)malloc(rank * sizeof(float));
    float* const b = (float*)malloc(rank * sizeof(float));

    clock_t wtime = clock();

    // Initialization, should only be called once.
	srand(time(NULL));


    // Generate random numebers 0-10 to place on matrix A
    generateRandNumbers(A,b,rank,nTreads);
            
/*     A[0] = 4;A[1] = 2;A[2] = 1;
    A[3] = 1;A[4] = 3;A[5] = 1;
    A[6] = 2;A[7] = 3;A[8] = 6;

    b[0] = 7;b[1] = -8;b[2] = 6; */
    
    
    printf("\n\n***************\n\n");

    // Show preliminary informations
    if(showAuxInf){

        printf("\nMatrix rank: %d \n",rank);

        printf("\nNumber of threads: %d \n",nTreads);

        printf("\nA = [\n");
        for(int j = 0; j < rank; j++){
            for(int i = 0; i < rank; i++)
                printf("%.2f ",A[i*rank+j]); 
            printf("\n");
        }
        printf("]\n");

        printf("\nb = [");
        for(int i = 0; i < rank; i++)
                    printf("%.2f ",b[i]); 
        printf("]\n");

    }

    // Test if matrix A will converge
    if(convergenceTest(A,rank,nTreads) == false){
        printf("\n******* The matrix A might not converge. *******\n\n");
        return 0;
    }

    // Solve Ax=b through Jacobi method
    solveJacobi(A,x,b,rank,epsilon,&nIter,nTreads);


    // Solve b with calculated x
    for(int i = 0; i < rank; i++){
        b_hat[i] = 0;
        for(int j = 0; j < rank; j++)
                b_hat[i] += A[i*rank+j] * x[j]; 
    }

    double finalTime = (double)(clock() - wtime) / CLOCKS_PER_SEC;
    
    // print informations
    printf("\nx = [");
    for(int i = 0; i < rank; i++)
                printf("%.2f ",x[i]); 
    printf("]\n");

    printf("\nb# = [");
    for(int i = 0; i < rank; i++)
                printf("%.2f ",b_hat[i]); 
    printf("]\n");

    printf("\nTempo: %f \n",finalTime); 

    printf("\n\n***************\n\n");


    write2file(finalTime,nIter,nTreads);

    // Free all allocated variables
    free(A);
    free(x);
    free(b);
}

// Test if matrix A will converge
int convergenceTest(float* const A,
                    unsigned int rank,
                    unsigned int nTreads){

    float alpha[rank];
    unsigned int convergence=0;    

    // Calculate alpha to test convergence
    for(int k = 0; k < rank; k++){

        alpha[k] = 0;

        for(int j = 0; j < rank; j++){
            if(j != k){
                alpha[k] += fabs(A[k*rank+j]) / fabs(A[k*rank+k]); 
            }
        }
        
        if(alpha[k] < 1)
            convergence++;

    }

    // Show alpha
    if(showAuxInf){
            printf("\n");
            for(int k = 0; k < rank; k++)
                printf("Alpha%d:%.2f \n",k,alpha[k]);
    }

    if (convergence == rank)
        return true;
    else
        return false;

}

// Solve Ax=b through Jacobi method
void solveJacobi(float* const A,
                 float* const x,
                 float* const b,
                 unsigned int rank,
                 const float epsilon,
                 unsigned int *nIter,
                 unsigned int nTreads){

    float x_k[rank];
    float iterate = true;
    unsigned int iterN = 0;

    // Generate x0
    for(int i=0; i<rank; i++)
        x_k[i] = b[i] / A[i*rank+i];

    // Show x0
    if(showAuxInf){
        printf("\nx0 = [");
        for(int i = 0; i < rank; i++)
                    printf("%.2f ",x_k[i]); 
        printf("]\n");
    }

    while(iterate){

        iterN++;

        // Calculate x^{k+1}
        for(int i=0; i<rank; i++){

            float sum = 0;
            for(int j=0; j<rank; j++){
                if(j != i)
                    sum += -A[i*rank+j] * x_k[j];
            }

            x[i] = (b[i] + sum) / A[i*rank+i];

        }

        // Show x^{k+1}
        if(showAuxInf){
            printf("x%d = [",iterN);
            for(int i = 0; i < rank; i++)
                        printf("%.2f ",x[i]); 
            printf("]\n");
        }

        // Calculate difference x^{k+1} - x^{k}
        unsigned int stop = 0;
        for(int i=0; i<rank; i++)
            if(fabs(x[i] - x_k[i]) < epsilon)
                stop++;

        if(stop == rank)
            // Iteration stop!!
            iterate = false;
        else
            // Iteration continues...
            // Place x^{k+1} into x^{k}
            for(int i=0; i<rank; i++)
                x_k[i] = x[i];  

    }  

    nIter[0] =  iterN; 

    return;

}
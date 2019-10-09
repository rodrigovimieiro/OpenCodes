// Generate random numebers
void generateRandNumbers(double* const A,
                         double* const b,
                         unsigned int rank,
                         unsigned int nTreads){

    double sum;
    
    // Generate random numebers 0-10 to place on matrix A
    //#pragma omp parallel for schedule(static) num_threads(nTreads)
    for(int i = 0; i < rank; i++){
        b[i] = (double) ((double)rand()/(double)(RAND_MAX/10));
         sum = 0;
        for(int j = 0; j < rank; j++){
            A[i*rank+j] = (double) ((double)rand()/(double)(RAND_MAX/10));
            sum += A[i*rank+j];
        }
        A[i*rank+i] = sum;
    }

}
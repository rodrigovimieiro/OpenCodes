// Generate random numebers
void generateRandNumbers(float* const A,
                         float* const b,
                         unsigned int rank,
                         unsigned int nTreads){

    float sum;
    
    // Generate random numebers 0-10 to place on matrix A
    //#pragma omp parallel for schedule(static) num_threads(nTreads)
    for(int i = 0; i < rank; i++){
        b[i] = (float) ((double)rand()/(double)(RAND_MAX/10));
         sum = 0;
        for(int j = 0; j < rank; j++){
            A[i*rank+j] = (float) ((double)rand()/(double)(RAND_MAX/10));
            sum += A[i*rank+j];
        }
        A[i*rank+i] = sum;
    }

}
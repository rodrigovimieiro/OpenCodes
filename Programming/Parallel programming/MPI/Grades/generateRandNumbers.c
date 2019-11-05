// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: November, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
*/
// ---------------------------------------------------------------------------------------


// Generate random numebers
void generateRandNumbers(unsigned int* const A,
                         unsigned int m,
                         unsigned int n,
                         unsigned int k){

    // Generate random numebers 0-100 to place on matrix A
    for(int l = 0; l < k; l++)
        for(int i = 0; i < m; i++)
            for(int j = 0; j < n; j++)
                    A[(l*m*n)+i*n+j] = (unsigned int) ((double)rand()/(double)(RAND_MAX/100));
        
}
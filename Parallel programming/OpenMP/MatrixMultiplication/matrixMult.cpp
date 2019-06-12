#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

// g++-9 matrixMult.cpp -o matrixMult -fopenmp

int main(int argc,char **argv){
    /*
    Não modifique este trecho de código
    *************************************************************************************
    */
    int **A,**B,**C;
    int i,j,k,dim;
    
    printf("Entre com a dimensao das matrizes: \n");
    fscanf(stdin, "%d", &dim); //Lê a dimensão das matrizes
    A=(int **)malloc(dim * sizeof(int *));
    B=(int **)malloc(dim * sizeof(int *)); 
    C=(int **)malloc(dim * sizeof(int *)); 
    for (i=0; i<dim; i++){ 
         A[i] = (int *)malloc(dim * sizeof(int));  //Aloca a matriz A do tamanho lido
         B[i] = (int *)malloc(dim * sizeof(int));  //Aloca a matriz B do tamanho lido
         C[i] = (int *)malloc(dim * sizeof(int));  //Aloca a matriz C do tamanho lido
    } 
    
    printf("Entre com os dados da matriz A: \n");
    for(i=0;i<dim;i++){
        for(j=0;j<dim;j++){
                fscanf(stdin, "%d ",&(A[i][j])); //Lê a matriz A
        }
    }
    printf("Entre com os dados da matriz B: \n");
    for(i=0;i<dim;i++)
        for(j=0;j<dim;j++)
            fscanf(stdin, "%d ",(&B[i][j])); //Lê a matriz B
    
    /************************************************************************************
    Modifique a partir daqui
    */

 	//#pragma omp parallel
    //{
    	//#pragma omp for schedule(auto)
    	for(i=0;i<dim;i++){
        	for(j=0;j<dim;j++)
            	for(k=0;k<dim;k++)
                	C[i][j]+=A[i][k]*B[k][j]; //Faz a multiplicação das matrizes
    	}
    //}

    /*
    *************************************************************************************
    Não modifique este trecho de código
    */
    for(i=0;i<dim;i++){
        for(j=0;j<dim;j++){
            printf("%d ",C[i][j]); //Imprime o resultado
        }
        printf("\n");
    }
    for (i=0; i<dim; i++){ 
        free(A[i]);
        free(B[i]);
        free(C[i]);
    }

    free(A);
    free(B);
    free(C);
}

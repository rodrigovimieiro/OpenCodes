#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int main(int argc,char **argv){
    /*
    Não modifique este trecho de código
    *************************************************************************************
    */
    int *A,*B,resultado=0;
    int i,dim;
    fscanf(stdin, "%d\n", &dim); //Lê a dimensão dos vetores
    //Aloca os vetores
    A=(int *)malloc(dim * sizeof(int));
    B=(int *)malloc(dim * sizeof(int)); 
    
    for(i=0;i<dim;i++)
        fscanf(stdin, "%d ",&(A[i])); //Lê o vetor A
    for(i=0;i<dim;i++)
        fscanf(stdin, "%d ",&(B[i])); //Lê o vetor B
    
    /************************************************************************************
    Modifique a partir daqui
    */

	#pragma omp parallel reduction(+:resultado)
	{
		#pragma omp for schedule(auto)
		    for(i=0;i<dim;i++){
        		resultado+=A[i]*B[i]; //Faz a multiplicação das matrizes
    		}
	}


    /*
    *************************************************************************************
    Não modifique este trecho de código
    */
    
    printf("%d ",resultado); //Imprime o resultado

    free(A);
    free(B);
}

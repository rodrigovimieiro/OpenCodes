#include <stdlib.h>
#include <stdio.h>

int main(int argc,char **argv){
    /*
    Não modifique este trecho de código
    *************************************************************************************
    */
    int *vetor,i,maximum=0,tam;
    fscanf(stdin, "%d\n", &tam); //Lê a dimensão do vetor
    vetor=(int*)malloc(tam*sizeof(int)); //Aloca o vetor da dimensão lida
    for(i=0;i<tam;i++)
        fscanf(stdin, "%d\n", &(vetor[i])); //Lê os elementos do vetor
    
    /************************************************************************************
    Modifique a partir daqui
    */
    maximum=vetor[0];
    
    #pragma omp parallel reduction(max:maximum)
	{
		#pragma omp for schedule(auto)
		for(i=1;i<tam;i++){
        	if(vetor[i]>maximum)
            	maximum=vetor[i];
	}
    
    
    }

   /*
    *************************************************************************************
    Não modifique este trecho de código
    */
    printf("%d",maximum); //Imprime o vetor ordenado
    free(vetor); //Desaloca o vetor lido
    return 0;
}
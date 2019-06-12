// compilar com -lm

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// g++-9 operacoes_retangulos_seq.cpp -o operacoes_retangulos_seq -fopenmp

// variaveis globais
int *base,*altura;
int *perimetro, *area;
double *diagonal;

void ret_perimetro (int dim)
{
    int i;
    for (i = 0; i < dim; i++)
    {
        perimetro[i] = (base[i]*2) + (altura[i]*2);
    }
}

void ret_area (int dim)
{
    int i;
    for (i = 0; i < dim; i++)
    {
        area[i] = base[i] * altura[i];
    }
}

void ret_diagonal(int dim)
{
    double num;
    int i;
	
    for (i = 0; i < dim; i++){
        num = (base[i]*2) + (altura[i]*2);
        diagonal[i] = sqrt(num);
    }
}

int main()
{
   /*
    Não modifique este trecho de código
    *************************************************************************************
    */
    int i,dim;
    fscanf(stdin, "%d\n", &dim); //Lê a dimensão dos vetores
    //Aloca os vetores
    base=(int *)malloc(dim * sizeof(int));
    altura=(int *)malloc(dim * sizeof(int)); 
	
	perimetro = (int *)malloc(dim * sizeof(int));
	area = (int *)malloc(dim * sizeof(int));
	diagonal =(double *)malloc(dim * sizeof(double));
    
    for(i = 0; i < dim; i++)
        fscanf(stdin, "%d ",&(base[i])); //Lê o vetor base
    for(i = 0; i < dim; i++)
        fscanf(stdin, "%d ",&(altura[i])); //Lê o vetor altura

	
/*    for (i = 0; i < dim; i++){
        printf("%d, %d\n", base[i], altura[i]);
		fflush(0);
    }*/
    
    /************************************************************************************
    Modifique a partir daqui
    */
    
    #pragma omp parallel
    {
    	#pragma omp sections
    	{
    		#pragma omp section
    		{
    			ret_perimetro(dim);
    		}
    		#pragma omp section
    		{
    			ret_area(dim);
    		}
    		#pragma omp section
    		{
    			ret_diagonal(dim);
    		}
    	}
    }

    for (i = 0; i < dim; i++)
    {
    	printf("base[%d]=%d, alt[%d]=%d, per[%d]=%d, area[%d]=%d, diag[%d]=%.2f\n", i, base[i], i, altura[i], i, perimetro[i], i, area[i], i, diagonal[i]);
	fflush(0);
    }
    
    return 0;
}
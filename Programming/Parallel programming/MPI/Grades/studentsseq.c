// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: November, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
*/
// ---------------------------------------------------------------------------------------


#include "studentsseq.h"

/*
*** MAIN ***
*/

int main(int argc,char **argv){

    unsigned int nRegions,nCity,nStudent,seed; 

    // Test if the arguments are correct
    if(argc==5){

        char *p;

        nRegions    = (unsigned int) strtol(argv[1], &p, 10);
        nCity       = (unsigned int) strtol(argv[2], &p, 10);
        nStudent    = (unsigned int) strtol(argv[3], &p, 10);
        seed        = (unsigned int) strtol(argv[4], &p, 10);

        // https://stackoverflow.com/a/9748431/8682939
        // Check for errors: e.g., the string does not represent an integer
        // or the integer is larger than int
        if (errno != 0 || *p != '\0' || nRegions > INT_MAX || nCity > INT_MAX || nStudent > INT_MAX|| seed > INT_MAX) {
            // Put here the handling of the error, like exiting the program with
            // an error message
            printf("*** Error: Please, give the program its correct input: <lin, col,seed> ***\n");
            return 0;
        }

    }
    else{
        printf("*** Error: Please, give the program its correct input: <lin, col,seed> ***\n");
        return 0;
    }

    // Memory allocation for matrix mGrades (nCity X nStudent X nRegions)
	unsigned int* const mGrades = (unsigned int*)malloc(nCity*nStudent*nRegions* sizeof(unsigned int));
    // Memory allocation for City metrics (nRegions X nCity)
    unsigned int* const mMaxGradesCity = (unsigned int*)malloc(nRegions*nCity* sizeof(unsigned int));
    unsigned int* const mMinGradesCity = (unsigned int*)malloc(nRegions*nCity* sizeof(unsigned int));
    double* const mMedianGradesCity = (double*)malloc(nRegions*nCity* sizeof(double));
    double* const mMeanGradesCity = (double*)malloc(nRegions*nCity* sizeof(double));
    double* const mStdGradesCity = (double*)malloc(nRegions*nCity* sizeof(double));
    // Memory allocation for Regions metrics (nRegions)
    unsigned int* const mMaxGradesRegions = (unsigned int*)malloc(nRegions* sizeof(unsigned int));
    unsigned int* const mMinGradesRegions = (unsigned int*)malloc(nRegions* sizeof(unsigned int));
    double* const mMedianGradesRegions = (double*)malloc(nRegions* sizeof(double));
    double* const mMeanGradesRegions = (double*)malloc(nRegions* sizeof(double));
    double* const mStdGradesRegions = (double*)malloc(nRegions* sizeof(double));
    // Memory allocation for Country metrics (1)
    unsigned int* const mMaxGradesCountry = (unsigned int*)malloc(1* sizeof(unsigned int));
    unsigned int* const mMinGradesCountry = (unsigned int*)malloc(1* sizeof(unsigned int));
    double* const mMedianGradesCountry = (double*)malloc(1* sizeof(double));
    double* const mMeanGradesCountry = (double*)malloc(1* sizeof(double));
    double* const mStdGradesCountry = (double*)malloc(1* sizeof(double));

    unsigned int bestRegion, bestCity[nRegions];
    

    // Initialization, should only be called once.
	srand(seed);

    // Generate random numebers 0-100 to place on matrix A
    generateRandNumbers(mGrades,nCity,nStudent,nRegions);

    


    clock_t wtime = clock();

    // Run over cities of each region
    for(int l = 0; l < nRegions; l++)
            for(int i = 0; i < nCity; i++){
                findMax(&mGrades[(l*nCity*nStudent)+i*nStudent], &mMaxGradesCity[l*nCity+i], &bestRegion, nStudent);
                findMin(&mGrades[(l*nCity*nStudent)+i*nStudent], &mMinGradesCity[l*nCity+i], nStudent);
                findMean(&mGrades[(l*nCity*nStudent)+i*nStudent], &mMeanGradesCity[l*nCity+i], nStudent);
                calcStd(&mGrades[(l*nCity*nStudent)+i*nStudent], mMeanGradesCity[l*nCity+i], &mStdGradesCity[l*nCity+i], nStudent);
                findMedian(&mGrades[(l*nCity*nStudent)+i*nStudent], &mMedianGradesCity[l*nCity+i], nStudent);
            }

    double masterTime_city = (double)(clock() - wtime) / CLOCKS_PER_SEC;

    // Run over regions
    for(int l = 0; l < nRegions; l++){
        findMax(&mMaxGradesCity[l*nCity],&mMaxGradesRegions[l], &bestCity[l], nCity);
        findMin(&mMinGradesCity[l*nCity],&mMinGradesRegions[l], nCity);
        findMeanF(&mMeanGradesCity[l*nCity],&mMeanGradesRegions[l] , nCity);
        calcStd(&mGrades[l*nCity*nStudent], mMeanGradesRegions[l], &mStdGradesRegions[l], nCity*nStudent);
        findMedian(&mGrades[(l*nCity*nStudent)], &mMedianGradesRegions[l], nCity*nStudent);

    }

    double masterTime_region = (double)(clock() - wtime) / CLOCKS_PER_SEC;

    // Over country
    findMax(&mMaxGradesRegions[0],&mMaxGradesCountry[0], &bestRegion, nRegions);
    findMin(&mMinGradesRegions[0],&mMinGradesCountry[0], nRegions);
    findMeanF(&mMeanGradesRegions[0],&mMeanGradesCountry[0], nRegions);
    calcStd(&mGrades[0], mMeanGradesCountry[0], &mStdGradesCountry[0], nCity*nStudent*nRegions);
    findMedian(&mGrades[0], &mMedianGradesCountry[0], nCity*nStudent*nRegions);


    double masterTime = (double)(clock() - wtime) / CLOCKS_PER_SEC;



    // Show all information

    if(showAuxInfo){

        // Show preliminary information
        for(int l = 0; l < nRegions; l++){
            printf("\nRegion: %d ------------ \n",l);
            for(int i = 0; i < nCity; i++){
                for(int j = 0; j < nStudent; j++)
                        printf("%02d ",mGrades[(l*nCity*nStudent)+i*nStudent+j]);
                printf("\n");
            }
        }
        
        printf("\n");
        for(int l = 0; l < nRegions; l++){
            for(int i = 0; i < nCity; i++){
                printf("Reg %d - Cid %d: menor: %02d, maior: %02d, mediana: %.2f, média: %.2f e DP: %.2f \n"
                ,l,i,mMinGradesCity[l*nCity+i],mMaxGradesCity[l*nCity+i],mMedianGradesCity[l*nCity+i],mMeanGradesCity[l*nCity+i],mStdGradesCity[l*nCity+i]);
            }
            printf("\n");
        }

        printf("\n");
        for(int l = 0; l < nRegions; l++){
            
            printf("Reg %d: menor: %02d, maior: %02d, mediana: %.2f, média: %.2f e DP: %.2f \n"
            ,l,mMinGradesRegions[l],mMaxGradesRegions[l],mMedianGradesRegions[l],mMeanGradesRegions[l],mStdGradesRegions[l]);
            
        }
        printf("\n");

        printf("\nBrasil: menor: %02d, maior: %02d, mediana: %.2f, média: %.2f e DP: %.2f \n\n"
            ,mMinGradesCountry[0],mMaxGradesCountry[0],mMedianGradesCountry[0],mMeanGradesCountry[0],mStdGradesCountry[0]);

        printf("\nMelhor região: Região %d\n",bestRegion);
        printf("\nMelhor cidade: Região %d, Cidade %d\n",bestRegion,bestCity[bestRegion]); 
    

        printf("\nTempo de resposta sem considerar E/S, em segundos: %fs\n\n", masterTime);

        //printf("\nCountry:%fs, Region:%fs, City:%fs \n\n"
        //,masterTime - masterTime_region, masterTime_region - masterTime_city, masterTime_city);

    }

    write2file(masterTime,0,1);

    free(mGrades);
    free(mMaxGradesCity);
    free(mMinGradesCity);
    free(mMedianGradesCity);
    free(mMeanGradesCity);
    free(mStdGradesCity);
    free(mMaxGradesRegions);
    free(mMinGradesRegions);
    free(mMedianGradesRegions);
    free(mMeanGradesRegions);
    free(mStdGradesRegions);
    free(mMaxGradesCountry);
    free(mMinGradesCountry);
    free(mMedianGradesCountry);
    free(mMeanGradesCountry);
    free(mStdGradesCountry);
        

    return 0;
}

void findMax(unsigned int* mGrade, unsigned int* mMax, unsigned int* mInd, unsigned int sizeVec){

    unsigned int max = mGrade[0];

    unsigned int ind = 0;
    
    for(int i = 1; i < sizeVec; i++){
        if(mGrade[i] > max){
            max = mGrade[i];
            ind = i;
        }
    }

    mMax[0] = max;
    mInd[0] = ind;
}

void findMin(unsigned int* mGrade, unsigned int* mMin, unsigned int sizeVec){

    unsigned int min = mGrade[0];
    
    for(int i = 1; i < sizeVec; i++){
        if(mGrade[i] < min)
            min = mGrade[i];
    }

    mMin[0] = min;
}

void findMedian(unsigned int* mGrade, double* mMedian, unsigned int sizeVec){  

    unsigned int tmpGrades[sizeVec];

    for(int k=0; k<sizeVec; k++)
        tmpGrades[k] = mGrade[k];

    quicksort(&tmpGrades[0], 0, sizeVec-1);

    mMedian[0] = tmpGrades[sizeVec/2];
    
    if(!(sizeVec%2)){  // if it is even
        mMedian[0] += tmpGrades[(sizeVec-1)/2];
        mMedian[0] /= 2;
    }

}

void findMean(unsigned int* mGrade, double* mMean, unsigned int sizeVec){  

    double sum = 0;

    for(int i = 0; i < sizeVec; i++){
        sum += mGrade[i];
    }

    mMean[0] = sum / sizeVec;

} 

void findMeanF(double* mGrade, double* mMean, unsigned int sizeVec){  

    double sum = 0;

    for(int i = 0; i < sizeVec; i++){
        sum += mGrade[i];
    }

    mMean[0] = sum / sizeVec;

} 

void calcStd(unsigned int* mGrade, double mean, double* mStd, unsigned int sizeVec){  

    double sum = 0;

    for(int i = 0; i < sizeVec; i++){
        sum += pow(mGrade[i] - mean,2);
    }

    mStd[0] = sqrt(sum / (sizeVec-1));

} 

int partition (unsigned int *arr, int low, int high){
    //Adapted from: https://www.geeksforgeeks.org/quick-sort/

    int i, j;
    unsigned int pivot,swap;
    
    // pivot (Element to be placed at right position)
    pivot = arr[high];  
 
    i = (low - 1);  // Index of smaller element

    for (j = low; j <= high-1; j++)
    {
        // If current element is smaller than or
        // equal to pivot
        if (arr[j] <= pivot)
        {
            i++;    // increment index of smaller element
            
            // swap arr[i] and arr[j]
            swap = arr[i];
            arr[i] = arr[j];
            arr[j] = swap;
        }
    }
    
    //swap arr[i + 1] and arr[high]
    swap = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = swap;
    
    return (i + 1);
} 

void quicksort(unsigned int *arr, int low, int high){

    //Adapted from: https://www.geeksforgeeks.org/quick-sort/

    int pi;
    
    if (low < high)  {
        /* pi is partitioning index, arr[pi] is now
           at right place */
        pi = partition(arr, low, high);

        quicksort(arr, low, pi - 1);  // Before pi
        quicksort(arr, pi + 1, high); // After pi
    }
    
}




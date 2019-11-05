// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: November, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
*/
// ---------------------------------------------------------------------------------------


#include "studentspar.h"

/*
*** MAIN ***
*/

int main(int argc,char **argv){

    unsigned int nRegions,nCity,nStudent; 

    unsigned int maxValue,maxValueInd,minValue;
    double medianValue, meanValue, stdValue;

    unsigned int whoAmI;

    /*
    MPI initialization
    */
    int npes, myrank;
    unsigned int nReceive;
    double sendbuf,recvbuf;

    MPI_Comm interCommParent;
    MPI_Status status;

    MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &npes);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    MPI_Comm_get_parent(&interCommParent);

    // Get nRegions,nCity,nStudent parameters
    MPI_Bcast(&nRegions, 1, MPI_UNSIGNED, 0, interCommParent);
    MPI_Bcast(&nCity, 1, MPI_UNSIGNED, 0, interCommParent);
    MPI_Bcast(&nStudent, 1, MPI_UNSIGNED, 0, interCommParent);

    // Calc of number of data for memory allocation of matrix mGrades 
    if(npes == (nRegions*nCity)){
        nReceive = nStudent;
        whoAmI = 0;     // I am calculating for each city
    }
    else if(npes == nRegions){
        nReceive = nCity*nStudent;
        whoAmI = 1;     // I am calculating for each region
    }
    else
    {
        nReceive = nCity*nStudent*nRegions;
        whoAmI = 2;     // I am calculating for the whole country
    }

    // Memory allocation for matrix mGrades 
    unsigned int* const mGrades = (unsigned int*)malloc(nReceive * sizeof(unsigned int));
    
    MPI_Scatter(&sendbuf, nReceive, MPI_UNSIGNED, mGrades, nReceive, MPI_UNSIGNED, 0, interCommParent);

    /*printf("I am a slave with rank: %d and with %d brothers.\n",myrank,npes);
    for(int j = 0; j < nReceive; j++)
                    printf("%02d ",mGrades[j]);
    printf("\n");  */

    findMax(&mGrades[0], &maxValue, &maxValueInd, nReceive);
    findMin(&mGrades[0], &minValue, nReceive);
    findMean(&mGrades[0], &meanValue, nReceive);
    calcStd(&mGrades[0], meanValue, &stdValue, nReceive);
    findMedian(&mGrades[0], &medianValue, nReceive);

    //printf("I am a slave with rank: %02d, with %02d brothers, min:%02d, max:%02d, median:%.2f, mean:%.2f and std:%.2f.\n"
    //,myrank,npes,minValue,maxValue,medianValue,meanValue,stdValue);


    // Send data for master
    MPI_Gather(&maxValue, 1, MPI_UNSIGNED, &recvbuf, 1, MPI_UNSIGNED, 0, interCommParent);
    MPI_Gather(&minValue, 1, MPI_UNSIGNED, &recvbuf, 1, MPI_UNSIGNED, 0, interCommParent);
    MPI_Gather(&meanValue, 1, MPI_DOUBLE, &recvbuf, 1, MPI_DOUBLE, 0, interCommParent);
    MPI_Gather(&medianValue, 1, MPI_DOUBLE, &recvbuf, 1, MPI_DOUBLE, 0, interCommParent);
    MPI_Gather(&stdValue, 1, MPI_DOUBLE, &recvbuf, 1, MPI_DOUBLE, 0, interCommParent);

    // Send indices of max values
    if(whoAmI == 2){
        MPI_Gather(&maxValueInd, 1, MPI_UNSIGNED, &recvbuf, 1, MPI_UNSIGNED, 0, interCommParent);
    }

    MPI_Finalize();

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




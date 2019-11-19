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

    char *p;

    // Get nRegions,nCity,nStudent parameters
    nRegions    = (unsigned int) strtol(argv[1], &p, 10);
    nCity       = (unsigned int) strtol(argv[2], &p, 10);
    nStudent    = (unsigned int) strtol(argv[3], &p, 10);

    unsigned int nVecTotal;
    unsigned int nDataOnEachVec;

    /*
    MPI initialization
    */
    int npes, myrank;

    int displs[NCORES];
    int send_counts[NCORES],recv_counts[NCORES];

    double sendbuf,recvbuf;

    MPI_Comm interCommParent;
    MPI_Status status;

    MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &npes);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    

        
    char name[MPI_MAX_PROCESSOR_NAME];
    int len;
    MPI_Get_processor_name(name, &len);
    printf("Hello, world.  I am %02d of %02d on %s\n", myrank, npes, name); 
    //printf("I am a slave with rank: %d, %d brothers, nStudent:%d, nCity:%d and nRegions:%d. \n",myrank,npes,nStudent,nCity,nRegions);
   

    MPI_Comm_get_parent(&interCommParent);

        
    unsigned int whoAmI;
    MPI_Bcast(&whoAmI, 1, MPI_UNSIGNED, 0, interCommParent);

    //printf("I am: %d. \n",whoAmI);

    // Calc of number of data for memory allocation of matrix mGrades 
    if(whoAmI == 0){        // I am calculating for each city
        nVecTotal = nRegions*nCity;
        nDataOnEachVec = nStudent;
    }
    else if(whoAmI == 1){   // I am calculating for each region
        nVecTotal = nRegions;
        nDataOnEachVec = nStudent*nCity;  
    }
    else{                   // I am calculating for the whole country
        nVecTotal = 1;
        nDataOnEachVec = nRegions*nStudent*nCity; 
    } 
    

    
    unsigned int ratio = nVecTotal / NCORES;
    unsigned int ratioRemain = nVecTotal % NCORES;

    //printf("Ratio:%d, remain:%d.\n",ratio,ratioRemain);


    unsigned int tmp_sum = 0; 
    for(int l = 0; l < NCORES; l++){
        send_counts[l] = ratio * nDataOnEachVec;

        if (ratioRemain > 0) {
            send_counts[l] += nDataOnEachVec;
            ratioRemain--;
        }

        displs[l] = tmp_sum;
        tmp_sum += send_counts[l];
        //printf("SendC[%d]: %d Displ: %d\n",l,send_counts[l],displs[l]);
    }

    // Memory allocation for matrix mGrades 
    unsigned int* mGrades = (unsigned int*)malloc(send_counts[myrank] * sizeof(unsigned int));

    MPI_Scatterv(&sendbuf, send_counts, displs, MPI_UNSIGNED, mGrades, send_counts[myrank], MPI_UNSIGNED, 0, interCommParent);

 
    /* 
    printf("I am a slave with rank: %d and with %d brothers.\n",myrank,npes);
    for(int j = 0; j < send_counts[myrank]; j++)
        printf("%02d ",mGrades[j]);
    printf("\n");   
    */

    // Dynamically allocate memory for return values
    unsigned int* maxValue = (unsigned int*)malloc(send_counts[myrank] * sizeof(unsigned int));
    unsigned int* maxValueInd = (unsigned int*)malloc(send_counts[myrank] * sizeof(unsigned int));
    unsigned int* minValue = (unsigned int*)malloc(send_counts[myrank] * sizeof(unsigned int));

    double* medianValue = (double*)malloc(send_counts[myrank] * sizeof(double));
    double* meanValue = (double*)malloc(send_counts[myrank] * sizeof(double));
    double* stdValue = (double*)malloc(send_counts[myrank] * sizeof(double));

    // Number of city vectors that are been calculated
    unsigned int nVec = send_counts[myrank]/nDataOnEachVec;

    findMax(mGrades, maxValue, maxValueInd, nDataOnEachVec,nVec);
    findMin(mGrades, minValue, nDataOnEachVec,nVec);
    findMean(mGrades, meanValue, nDataOnEachVec,nVec);
    calcStd(mGrades, meanValue, stdValue, nDataOnEachVec,nVec);
    findMedian(mGrades, medianValue, nDataOnEachVec,nVec);

    /*     
    for(int l = 0; l < send_counts[myrank]/nDataOnEachVec; l++){
        printf("I am a slave with rank: %02d, with %02d brothers, %02d nVec, %02d city, min:%02d, max:%02d, median:%.2f, mean:%.2f and std:%.2f.\n"
        ,myrank,npes,send_counts[myrank]/nDataOnEachVec,l,minValue[l],maxValue[l],medianValue[l],meanValue[l],stdValue[l]);
    }  
    */


    // Send data for master
    MPI_Gatherv(maxValue, nVec, MPI_UNSIGNED, &recvbuf, recv_counts, displs, MPI_UNSIGNED, 0, interCommParent);
    MPI_Gatherv(minValue, nVec, MPI_UNSIGNED, &recvbuf, recv_counts, displs, MPI_UNSIGNED, 0, interCommParent);
    MPI_Gatherv(meanValue, nVec, MPI_DOUBLE, &recvbuf, recv_counts, displs, MPI_DOUBLE, 0, interCommParent);
    MPI_Gatherv(medianValue, nVec, MPI_DOUBLE, &recvbuf, recv_counts, displs, MPI_DOUBLE, 0, interCommParent);
    MPI_Gatherv(stdValue, nVec, MPI_DOUBLE, &recvbuf, recv_counts, displs, MPI_DOUBLE, 0, interCommParent);

    // Send indices of max values
    if(whoAmI == 2){
        MPI_Gatherv(maxValueInd, nVec, MPI_UNSIGNED, &recvbuf, recv_counts, displs, MPI_UNSIGNED, 0, interCommParent);
    }

    MPI_Finalize();

    return 0;
}

void findMax(unsigned int* mGrade, unsigned int* mMax, unsigned int* mInd, unsigned int sizeVec, unsigned int nVec){
    
    for(int k = 0; k < nVec; k++){ 

        unsigned int max = mGrade[k*sizeVec];
        
        unsigned int ind = 0;
        
        for(int i = 1; i < sizeVec; i++){
            if(mGrade[k*sizeVec + i] > max){
                max = mGrade[k*sizeVec + i];
                ind = k*sizeVec + i;
            }
        }
        
        mMax[k] = max;
        mInd[k] = ind;
    }
}

void findMin(unsigned int* mGrade, unsigned int* mMin, unsigned int sizeVec, unsigned int nVec){

    for(int k = 0; k < nVec; k++){
        unsigned int min = mGrade[k*sizeVec];
        
        for(int i = 1; i < sizeVec; i++){
            if(mGrade[k*sizeVec + i] < min)
                min = mGrade[k*sizeVec + i];
        }

        mMin[k] = min;
    }
}

void findMedian(unsigned int* mGrade, double* mMedian, unsigned int sizeVec, unsigned int nVec){  

    unsigned int tmpGrades[sizeVec];

    for(int k = 0; k < nVec; k++){
        
        for(int l = 0; l < sizeVec; l++)
            tmpGrades[l] = mGrade[k*sizeVec + l];

        quicksort(&tmpGrades[0], 0, sizeVec-1);

        mMedian[k] = tmpGrades[sizeVec/2];
        
        if(!(sizeVec%2)){  // if it is even
            mMedian[k] += tmpGrades[(sizeVec-1)/2];
            mMedian[k] /= 2;
        }
    }
}

void findMean(unsigned int* mGrade, double* mMean, unsigned int sizeVec, unsigned int nVec){  

    for(int k = 0; k < nVec; k++){
        double sum = 0;

        for(int i = 0; i < sizeVec; i++){
            sum += mGrade[k*sizeVec + i];
        }

        mMean[k] = sum / sizeVec;
    }
} 

void calcStd(unsigned int* mGrade, double* mean, double* mStd, unsigned int sizeVec, unsigned int nVec){  

    for(int k = 0; k < nVec; k++){
        double sum = 0;

        for(int i = 0; i < sizeVec; i++){
            sum += pow(mGrade[k*sizeVec + i] - mean[k],2);
        }

        mStd[k] = sqrt(sum / (sizeVec-1));
    }
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




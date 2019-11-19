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


    unsigned int nCityTotal = nRegions*nCity;

    // Memory allocation for matrix mGrades (nCity X nStudent X nRegions)
	unsigned int* const mGrades = (unsigned int*)malloc(nCity*nStudent*nRegions* sizeof(unsigned int));
    // Memory allocation for City metrics (nRegions X nCity)
    unsigned int* const mMaxGradesCity = (unsigned int*)malloc(nCityTotal* sizeof(unsigned int));
    unsigned int* const mMinGradesCity = (unsigned int*)malloc(nCityTotal* sizeof(unsigned int));
    double* const mMedianGradesCity = (double*)malloc(nCityTotal* sizeof(double));
    double* const mMeanGradesCity = (double*)malloc(nCityTotal* sizeof(double));
    double* const mStdGradesCity = (double*)malloc(nCityTotal* sizeof(double));
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

    unsigned int bestRegion, bestCity,bestGrade_Ind;

    
    // Initialization, should only be called once.
	srand(seed);

    // Generate random numebers 0-100 to place on matrix A
    generateRandNumbers(mGrades,nCity,nStudent,nRegions);

    
    // Show preliminary information
    for(int l = 0; l < nRegions; l++){
        printf("\nRegion: %d ------------ \n",l);
        for(int i = 0; i < nCity; i++){
            for(int j = 0; j < nStudent; j++)
                    printf("%02d ",mGrades[(l*nCity*nStudent)+i*nStudent+j]);
            printf("\n");
        }
    }
    




    clock_t wtime = clock();

    /*
    MPI initialization
    */
    int npes, myrank;
    int errcodes[nCityTotal];

    int displs[NCORES];
    int send_counts[NCORES],recv_counts[NCORES];

    double sendbuf,recvbuf;

    MPI_Comm interCommCity, interCommRegion, interCommCountry;
    MPI_Status status;
    MPI_Info info;

    MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &npes);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    // These lines are intend to spawn on different nodes
    MPI_Info_create(&info);
    MPI_Info_set( info, "file", "halley.txt");


    




    unsigned int cityRatio = nCityTotal / NCORES;
    unsigned int cityRatioRemain = nCityTotal % NCORES;

    //printf("Ratio:%d, remain:%d.\n",cityRatio,cityRatioRemain);


    unsigned int tmp_sum = 0, cityRatioRemain_tmp = cityRatioRemain; 
    for(int l = 0; l < NCORES; l++){
        send_counts[l] = cityRatio * nStudent;

        if (cityRatioRemain_tmp > 0) {
            send_counts[l] += nStudent;
            cityRatioRemain_tmp--;
        }

        displs[l] = tmp_sum;
        tmp_sum += send_counts[l];
        //printf("SendC[%d]: %d Displ: %d\n",l,send_counts[l],displs[l]);
    }

    if(cityRatio == 0){
        // Create slaves for cities calculations
        MPI_Comm_spawn("studentspar_slave.bin", argv+1, nCityTotal, info, 0, MPI_COMM_WORLD, &interCommCity, errcodes);
    }
    else{
        // Create slaves for cities calculations
        MPI_Comm_spawn("studentspar_slave.bin", argv+1, NCORES, info, 0, MPI_COMM_WORLD, &interCommCity, errcodes);
    }

    unsigned int whoAmI = 0;     // I am calculating for each city
    MPI_Bcast(&whoAmI, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);

    // Distribute data (each city) for slaves
    MPI_Scatterv(mGrades, send_counts, displs, MPI_UNSIGNED, &recvbuf, nStudent, MPI_UNSIGNED, MPI_ROOT, interCommCity);
    


    tmp_sum = 0;
    cityRatioRemain_tmp = cityRatioRemain;
    for(int l = 0; l < NCORES; l++){
        recv_counts[l] = cityRatio;

        if (cityRatioRemain_tmp > 0) {
            recv_counts[l]++;
            cityRatioRemain_tmp--;
        }

        displs[l] = tmp_sum;
        tmp_sum += recv_counts[l];
        //printf("SendC[%d]: %d Displ: %d\n",l,recv_counts[l],displs[l]);
    }
    
    MPI_Gatherv(&sendbuf, cityRatio, MPI_UNSIGNED, mMaxGradesCity, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommCity);
    MPI_Gatherv(&sendbuf, cityRatio, MPI_UNSIGNED, mMinGradesCity, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommCity);
    MPI_Gatherv(&sendbuf, cityRatio, MPI_DOUBLE, mMeanGradesCity, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCity);
    MPI_Gatherv(&sendbuf, cityRatio, MPI_DOUBLE, mMedianGradesCity, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCity);
    MPI_Gatherv(&sendbuf, cityRatio, MPI_DOUBLE, mStdGradesCity, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCity);









    printf("\n\n\n\n");








    unsigned int regionRatio = nRegions / NCORES;
    unsigned int regionRatioRemain = nRegions % NCORES;


    tmp_sum = 0; 
    unsigned int regionRatioRemain_tmp = regionRatioRemain; 
    for(int l = 0; l < NCORES; l++){
        send_counts[l] = regionRatio * (nStudent*nCity);

        if (regionRatioRemain_tmp > 0) {
            send_counts[l] += (nStudent*nCity);
            regionRatioRemain_tmp--;
        }

        displs[l] = tmp_sum;
        tmp_sum += send_counts[l];
        //printf("SendC[%d]: %d Displ: %d\n",l,send_counts[l],displs[l]);
    }

    if(regionRatio == 0){
        // Create slaves for regions calculations
        MPI_Comm_spawn("studentspar_slave.bin", argv+1, nRegions, info, 0, MPI_COMM_WORLD, &interCommRegion, errcodes);
    }
    else{
        // Create slaves for regions calculations
        MPI_Comm_spawn("studentspar_slave.bin", argv+1, NCORES, info, 0, MPI_COMM_WORLD, &interCommRegion, errcodes);
    }

    whoAmI = 1;     // I am calculating for each region
    MPI_Bcast(&whoAmI, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    // Distribute data (each region) for slaves
    MPI_Scatterv(mGrades, send_counts, displs, MPI_UNSIGNED, &recvbuf, (nStudent*nCity), MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    tmp_sum = 0;
    regionRatioRemain_tmp = regionRatioRemain;
    for(int l = 0; l < NCORES; l++){
        recv_counts[l] = regionRatio;

        if (regionRatioRemain_tmp > 0) {
            recv_counts[l]++;
            regionRatioRemain_tmp--;
        }

        displs[l] = tmp_sum;
        tmp_sum += recv_counts[l];
        //printf("SendC[%d]: %d Displ: %d\n",l,recv_counts[l],displs[l]);
    }
    
    MPI_Gatherv(&sendbuf, regionRatio, MPI_UNSIGNED, mMaxGradesRegions, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommRegion);
    MPI_Gatherv(&sendbuf, regionRatio, MPI_UNSIGNED, mMinGradesRegions, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommRegion);
    MPI_Gatherv(&sendbuf, regionRatio, MPI_DOUBLE, mMeanGradesRegions, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommRegion);
    MPI_Gatherv(&sendbuf, regionRatio, MPI_DOUBLE, mMedianGradesRegions, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommRegion);
    MPI_Gatherv(&sendbuf, regionRatio, MPI_DOUBLE, mStdGradesRegions, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommRegion);







printf("\n\n\n\n");










    // Create slaves for country calculations
    MPI_Comm_spawn("studentspar_slave.bin", argv+1, 1, info, 0, MPI_COMM_WORLD, &interCommCountry, errcodes);

    whoAmI = 2;     // I am calculating for the country
    MPI_Bcast(&whoAmI, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);

    displs[0] = 0;
    send_counts[0] = nRegions*nStudent*nCity;
    recv_counts[0] = 1;

    // Send data (all grades) for unique slave
    MPI_Scatterv(mGrades, send_counts, displs, MPI_UNSIGNED, &recvbuf, (nStudent*nCity), MPI_UNSIGNED, MPI_ROOT, interCommCountry);


    MPI_Gatherv(&sendbuf, 1, MPI_UNSIGNED, mMaxGradesCountry, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommCountry);
    MPI_Gatherv(&sendbuf, 1, MPI_UNSIGNED, mMinGradesCountry, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommCountry);
    MPI_Gatherv(&sendbuf, 1, MPI_DOUBLE, mMeanGradesCountry, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCountry);
    MPI_Gatherv(&sendbuf, 1, MPI_DOUBLE, mMedianGradesCountry, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCountry);
    MPI_Gatherv(&sendbuf, 1, MPI_DOUBLE, mStdGradesCountry, recv_counts, displs, MPI_DOUBLE, MPI_ROOT, interCommCountry);
    

    // Get indices of max values
    MPI_Gatherv(&sendbuf, 1, MPI_UNSIGNED, &bestGrade_Ind, recv_counts, displs, MPI_UNSIGNED, MPI_ROOT, interCommCountry);








    for(int l = 1; l <= nRegions; l++){
        unsigned int upperBound = l*nCity*nStudent;
        if(bestGrade_Ind < upperBound){
            bestRegion  = l - 1;
            l = nRegions; // break
        }
    }

    for(int i = 1; i <= nCity; i++){
        unsigned int upperBound = (bestRegion*nCity*nStudent)+i*nStudent;
        if(bestGrade_Ind < upperBound){
            bestCity = i - 1;
            i = nCity; // break
        }
    }

    
    double masterTime = (double)(clock() - wtime) / CLOCKS_PER_SEC;



    // Show all information
/*     printf("\n");
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
    printf("\n"); */

    printf("\nBrasil: menor: %02d, maior: %02d, mediana: %.2f, média: %.2f e DP: %.2f \n\n"
        ,mMinGradesCountry[0],mMaxGradesCountry[0],mMedianGradesCountry[0],mMeanGradesCountry[0],mStdGradesCountry[0]);

    printf("\nMelhor região: Região %d\n",bestRegion);
    printf("\nMelhor cidade: Região %d, Cidade %d\n",bestRegion,bestCity);


    printf("\nTempo de resposta sem considerar E/S, em segundos: %fs\n\n", masterTime);

        
    MPI_Finalize();

    return 0;
}




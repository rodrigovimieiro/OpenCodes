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
    int errcodes[nRegions*nCity];

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

    // Create slaves for cities calculations
    MPI_Comm_spawn("studentspar_slave.bin", MPI_ARGV_NULL, nRegions*nCity, info, 0, MPI_COMM_WORLD, &interCommCity, errcodes);

    // Create slaves for regions calculations
    MPI_Comm_spawn("studentspar_slave.bin", MPI_ARGV_NULL, nRegions, info, 0, MPI_COMM_WORLD, &interCommRegion, errcodes);

    // Create slaves for country calculations
    MPI_Comm_spawn("studentspar_slave.bin", MPI_ARGV_NULL, 1, info, 0, MPI_COMM_WORLD, &interCommCountry, errcodes);


    MPI_Bcast(&nRegions, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);
    MPI_Bcast(&nCity, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);
    MPI_Bcast(&nStudent, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);
 
    MPI_Bcast(&nRegions, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);
    MPI_Bcast(&nCity, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);
    MPI_Bcast(&nStudent, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    MPI_Bcast(&nRegions, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);
    MPI_Bcast(&nCity, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);
    MPI_Bcast(&nStudent, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry); 

    // Distribute data (each city) for slaves
    MPI_Scatter(mGrades, nStudent, MPI_UNSIGNED, &recvbuf, nStudent, MPI_UNSIGNED, MPI_ROOT, interCommCity);

    // Distribute data (each region) for slaves
    MPI_Scatter(mGrades, nStudent*nCity, MPI_UNSIGNED, &recvbuf, nStudent*nCity, MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    // Send data (all grades) for unique slave
    MPI_Scatter(mGrades, nStudent*nCity*nRegions, MPI_UNSIGNED, &recvbuf, nStudent*nCity*nRegions, MPI_UNSIGNED, MPI_ROOT, interCommCountry);


    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMaxGradesCity, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);

    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMaxGradesRegions, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMaxGradesCountry, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);

    

    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMinGradesCity, 1, MPI_UNSIGNED, MPI_ROOT, interCommCity);

    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMinGradesRegions, 1, MPI_UNSIGNED, MPI_ROOT, interCommRegion);

    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, mMinGradesCountry, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);



    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMeanGradesCity, 1, MPI_DOUBLE, MPI_ROOT, interCommCity);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMeanGradesRegions, 1, MPI_DOUBLE, MPI_ROOT, interCommRegion);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMeanGradesCountry, 1, MPI_DOUBLE, MPI_ROOT, interCommCountry);



    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMedianGradesCity, 1, MPI_DOUBLE, MPI_ROOT, interCommCity);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMedianGradesRegions, 1, MPI_DOUBLE, MPI_ROOT, interCommRegion);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mMedianGradesCountry, 1, MPI_DOUBLE, MPI_ROOT, interCommCountry);



    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mStdGradesCity, 1, MPI_DOUBLE, MPI_ROOT, interCommCity);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mStdGradesRegions, 1, MPI_DOUBLE, MPI_ROOT, interCommRegion);

    MPI_Gather(&sendbuf, 1, MPI_DOUBLE, mStdGradesCountry, 1, MPI_DOUBLE, MPI_ROOT, interCommCountry);

    
    // Get indices of max values
    MPI_Gather(&sendbuf, 1, MPI_UNSIGNED, &bestGrade_Ind, 1, MPI_UNSIGNED, MPI_ROOT, interCommCountry);

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
    printf("\nMelhor cidade: Região %d, Cidade %d\n",bestRegion,bestCity);


    printf("\nTempo de resposta sem considerar E/S, em segundos: %fs\n\n", masterTime); 

        
    MPI_Finalize();

    return 0;
}




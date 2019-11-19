// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: November, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
*/
// ---------------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <limits.h>
#include <errno.h>
#include <unistd.h>
#include <mpi.h>

#define NCORES 37 // 51   // Number of cores - 1

void findMax(unsigned int* mGrade, unsigned int* mMax, unsigned int* mInd, unsigned int sizeVec, unsigned int nVec);
void findMin(unsigned int* mGrade, unsigned int* mMin, unsigned int sizeVec, unsigned int nVec);
void findMedian(unsigned int* mGrade, double* mMedian, unsigned int sizeVec, unsigned int nVec);
void findMean(unsigned int* mGrade, double* mMean, unsigned int sizeVec, unsigned int nVec);
void calcStd(unsigned int* mGrade, double* mean, double* mStd, unsigned int sizeVec, unsigned int nVec);

// Adapted from: https://www.geeksforgeeks.org/quick-sort/
int partition (unsigned int *arr, int low, int high);
void quicksort(unsigned int *arr, int low, int high);

#include "generateRandNumbers.c"
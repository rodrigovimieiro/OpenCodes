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

void findMax(unsigned int* mGrade, unsigned int* mMax, unsigned int* mInd, unsigned int sizeVec);
void findMin(unsigned int* mGrade, unsigned int* mMin, unsigned int sizeVec);
void findMedian(unsigned int* mGrade, double* mMedian, unsigned int sizeVec);
void findMean(unsigned int* mGrade, double* mMean, unsigned int sizeVec);
void findMeanF(double* mGrade, double* mMean, unsigned int sizeVec);
void calcStd(unsigned int* mGrade, double mean, double* mStd, unsigned int sizeVec);

// Adapted from: https://www.geeksforgeeks.org/quick-sort/
int partition (unsigned int *arr, int low, int high);
void quicksort(unsigned int *arr, int low, int high);

#include "generateRandNumbers.c"
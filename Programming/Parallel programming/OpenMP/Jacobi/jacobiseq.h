// ---------------------------------------------------------------------------------------
/*
=========================================================================
Author: Rodrigo de Barros Vimieiro
Date: October, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
*/
// ---------------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <time.h>
#include <stdbool.h>
#include <limits.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define PRECISION 0.001

bool showAuxInf = true;

#include "generateRandNumbers.c"
#include "write2file.c"

int convergenceTest(float* const A,
                    unsigned int rank,
                    unsigned int nTreads);

void solveJacobi(float* const A,
                 float* const x,
                 float* const b,
                 unsigned int rank,
                 const float epsilon,
                 unsigned int *nIter,
                 unsigned int nTreads);


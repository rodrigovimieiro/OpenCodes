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
#include <time.h>
#include <stdbool.h>
#include <limits.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define PRECISION 0.001

bool showAuxInf = false;

#include "generateRandNumbers.c"
#include "write2file.c"

int convergenceTest(double* const A,
                    unsigned int rank,
                    unsigned int nTreads);

void solveJacobi(double* const A,
                 double* const x,
                 double* const b,
                 unsigned int rank,
                 const double epsilon,
                 unsigned int *nIter,
                 unsigned int nTreads);


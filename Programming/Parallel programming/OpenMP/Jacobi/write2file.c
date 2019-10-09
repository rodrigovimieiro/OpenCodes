// Write to file
void write2file(double finalTime,
                unsigned int nIter,
                unsigned int nTreads){

    char filename[30];

    struct stat st = {0};

    if (stat("output", &st) == -1) {
        mkdir("output", 0700);
    }

    snprintf(filename,14,"output/time_%d",nTreads);
    strcat(filename,".txt");
    
    // Open for append. Data is added to the end of the file.
    FILE *pFile = fopen (filename,"a");

    if (pFile==NULL) perror ("Error opening file");
    else
    {
        fprintf(pFile, "%.5f %d\n",finalTime,nIter);

        fclose (pFile);
    }

    return;

}
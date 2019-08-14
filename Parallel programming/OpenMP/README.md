[OpenMP](https://www.openmp.org/)
======


### Commands to compile on unix based systems:

C++ - > `g++ yourprogram.cpp -o yourprogram -fopenmp`

C - > `gcc yourprogram.c -o yourprogram -fopenmp`


### Run the code on linux:

`./yourprogram <yourinput.txt`

### Run the code and measure the time:

`time ./yourprogram <yourinput.txt`


### Compile with Visual Studio (VS):

 - Project propreties -> c/c++ -> Language -> OpenMP Support -> Yes(/openmp)
 - [Reference](https://stackoverflow.com/questions/4515276/openmp-is-not-creating-threads-in-visual-studio)

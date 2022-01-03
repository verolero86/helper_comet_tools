#include "stdio.h"

// Reads a CoMet Czekanowski input in binary and outputs a human readable
// histogram
//

#ifndef NUM_BINS
  #define NUM_BINS 1000
#endif

#define HIST_MIN 0
#define HIST_MAX 1

int main(){

    int bin_assigned;
    int histogram[NUM_BINS] = 0;
    typedef unsigned int UINT32;
    typedef float Float_t;

    if (sizeof(UINT32 != 4)) {
        return 1;
    }

    typedef struct {
        UINT32 vec0;
        UINT32 vec1;
        Float_t value;
    } Element;

    Element e;
    double bin_width = ((double)HIST_MAX - (double)HIST_MIN) / (double)NUM_BINS;

    printf("Creating histogram with %d bins of width %d\n",(double)NUM_BINS,bin_width);

    while(true) {

        const size_t num_read = fread(&e, sizeof(e), 1, stdin);

        if(num_read != 1) {
            break;
        }

        bin_assigned = (double)e.value/bin_width;

        histogram[bin_assigned - 1] += 1;
    
    }

    printf("Final histogram\n");
    printf("---------------\n");

    for(int i=0; i<NUM_BINS; i++) {
        printf("bin[%i]\t=\t%i\n",i,histogram[i]);
    }

    return 0;

}

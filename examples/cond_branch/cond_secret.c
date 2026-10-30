#include "../common.h"
#define POMMES_INPUT_COND_SECRET SEC SEC
#define N_SHARES 1

void cond_secret(uint32_t * in, uint32_t * out){
    uint32_t s;
    for(uint32_t i = 0; i < 1; ++i){
        s = *in;
        if(s == 0){
            *out = s;
        }
        else{
            *out = s ^ 0;
        }
    }
}

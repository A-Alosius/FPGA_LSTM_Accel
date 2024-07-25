#include "MKL25Z4.h"
#include "board.h"

#define ctrl1 (1)  // PTE1 
#define ctrl0 (0)  // PTE0

// input pins
#define in0 (7)    // PTC7
#define in1 (0)    // PTC0 
#define in2 (3)    // PTC3
#define in3 (4)    // PTC4 
#define in4 (5)    // PTC5
#define in5 (6)    // PTC6
#define in6 (10)   // PTC10 
#define in7 (11)   // PTC11
#define in8 (12)   // PTC12 
#define in9 (13)   // PTC13

#define sign (16)  // PTC16

// output pins
#define out0 (30)  // PTE30
#define out1 (29)  // PTE29 
#define out2 (23)  // PTE23
#define out3 (22)  // PTE22
#define out4 (21)  // PTE21
#define out5 (20)  // PTE20
#define out6 (5)   // PTE5 
#define out7 (4)   // PTE4
#define out8 (3)   // PTE3 
#define out9 (2)   // PTE2

#define MASK(X) (1UL<<X)

// global variables
int input, nbits;
int* output;

// function prototypes
void config();
int* num2bin(int);
int bin2num(int*);
void send_inputs(int);
void read_inference();

// function definitions
void config(){
    SIM->SCGC5|= MASK(11) | MASK(13); // clock gating for C and E...confirm from manual
    uint8_t ins [] = [in9, in8, in7, in6, in5, in4, in3, in2, in1, in0];
    uint8_t outs[] = [out9, out8, out7, out6, out5, out4, out3, out2, out1, out0];

    for (int i = 0; i < 10; i++){
        PORTC->PCR[ins[i]] &= ~0x700; //Clear mux
        PORTC->PCR[ins[i]] |= MASK(8); //setup to be GPIO
        PTC->PDDR &= ~MASK(ins[i]); // set as input

        PORTE->PCR[outs[i]] &= ~0x700; // clear mux
        PORTE->PCR[outs[i]] |= MASK(8); // setp as GPIO
        PTE->PDDR |= MASK(ins[i]); // set as output
    }
}

void send_inputs(int num){
    int
}

void read_inference(){

}

int* num2bin(int num, int nbits){
	int* bits = (int*) malloc(sizeof(int) * nbits);
	for (int i=0; i<nbits; i++){
		bits[nbits-1-i] = num%2;
		num /= 2;
		printf("%d", bits[nbits-1-i]);
	}
}

int bin2num(int *bits, int nbits){
	for (int i=0; i<nbits; i++){
		bits[nbits-1-i] = num%2;
		num /= 2;
		printf("%d", bits[nbits-1-i]);
	}
}

int main(){
    nbits = 10;
    output = (int*) malloc(sizeof(int) * nbits);
    while(1){

    }
    return 0;
}
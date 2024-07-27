#include "MKL25Z4.h"
#include "board.h"
#include <math.h>
#include <stdlib.h>
#include "keypad.c"

// special signals
#define ctrl1 (1)  // PTB1 note...may need a input control and output control to relay ctrl signal to FPGA
#define ctrl0 (0)  // PTB0
#define clk   (8)  // PTB9
#define sign  (9)  // PTB9
#define rst   (10) // PTB10

// input pins
#define in0 (7)    // PTC7
#define in1 (0)    // PTC0 
#define in2 (3)    // PTC3
#define in3 (4)    // PTC4 
#define in4 (5)    // PTC5
#define in5 (6)    // PTC6
#define in6 (8)    // PTC8 
#define in7 (9)    // PTC9
#define in8 (2)    // PTC2
#define in9 (1)    // PTC1

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

// reusables
#define MASK(X) (1UL<<X)
#define NBITS (10)

// global variables
int input, output;
int output_bits[NBITS], input_bits[NBITS];
uint8_t ins [] = {in9, in8, in7, in6, in5, in4, in3, in2, in1, in0};
uint8_t outs[] = {out9, out8, out7, out6, out5, out4, out3, out2, out1, out0};

// function prototypes
void config();
int* num2bin(int);
int  bin2num(int*);
void read_input();
void send_inputs(int);
void read_inference();

/********************  function definitions ******************/

// configure io pins
void io_config(){
    SIM->SCGC5|= MASK(9) | MASK(10) | MASK(11) | MASK(13); // clock gating for C and E...confirm from manual
    
    // input and output pins
    for (int i = 0; i < 10; i++){
        PORTC->PCR[ins[i]] &= ~0x700; //Clear mux
        PORTC->PCR[ins[i]] |= MASK(8); //setup to be GPIO
        PTC->PDDR |= MASK(ins[i]); // set as output to send inputs to FPGA

        PORTE->PCR[outs[i]] &= ~0x700; // clear mux
        PORTE->PCR[outs[i]] |= MASK(8); // setp as GPIO
        PTE->PDDR &= ~MASK(outs[i]); // set as input to receive inference from FPGA
    }
    PORTC->PCR[ins[i]] &= ~0x700; //Clear mux
    PORTC->PCR[ins[i]] |= MASK(8); //setup to be GPIO
    PTC->PDDR |= MASK(ins[i]);
    // comms pins

}


// read keypad input
void read_input(){
    input = key;
}

// read inputs, convert to bin and set appropriate states for pins
void send_inputs(){
    read_input();
    num2bin();
    for (int i = 0; i < NBITs; i++){
        if (output_bits[i])
            PTC->PSOR |= MASK(ins[i]);
        else
            PTC->PCOR |= MASK(ins[i]);
    }
}

// read result pins for prediction
void read_inference(){
    for (int i = 0; i < NBITs; i++){
        output_bits[i] = (PTE->PDIR & MASK(outs[i])) ? 1:0;
    }
    bin2num();
}

// convert input to bin and store in input_bits array
void num2bin(){
	for (int i=0; i<NBITS; i++){
		input_bits[NBITS-1-i] = input % 2;
		input = (input >> 1);
		printf("%d", input_bits[NBITS-1-i]);
	}
}

// convert bit results from FPGA to num and store in output variable
void bin2num(){
	output = 0;
    for (int i=0; i<NBITS; i++){
		output += output_bits[i]*pow(2, nbits-1-i);
	}
    printf("%d", output);
}


int main(){
    io_config();
    keypad_config();

    while(1){
        loop_cols();
        read_row();
    }
    return 0;
}
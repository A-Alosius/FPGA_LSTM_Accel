#pragma once
#include <stdio.h>
#include "MKL25Z4.h"

// keypad input
#define R1 (17) // PTA17
#define R2 (16) // PTA16
#define R3 (17) // PTC17
#define R4 (16) // PTC16
//keypad output
#define C1 (13) // PTC13
#define C2 (12) // PTC12
#define C3 (11) // PTC11
#define C4 (10) // PTC10

//Other useful functions:
void read_row(void);
void loop_cols(void);
void keypad_config(void);
void compute_key(void);

uint8_t col1, col2, col3, col4;
uint16_t key;
uint8_t keys[5];
uint8_t degree = 0;

void keypad_config(){
	// configure cols as output
	for (int i = 0; i < 4; i++){
		PORTC->PCR[10+i] &= ~0x700; //Clear mux
        PORTC->PCR[10+i] |= MASK(8); //setup to be GPIO
        PTC->PDDR |= MASK(10+i); // set as input
	}
	
	PORTC->PCR[R4] &= ~0x700; //Clear mux
    PORTC->PCR[R4] |= MASK(8); //setup to be GPIO
    PTC->PDDR &= ~MASK(R4); // set as input

	PORTC->PCR[R3] &= ~0x700; //Clear mux
    PORTC->PCR[R3] |= MASK(8); //setup to be GPIO
    PTC->PDDR &= ~MASK(R3); // set as input

	PORTA->PCR[R2] &= ~0x700; //Clear mux
    PORTA->PCR[R2] |= MASK(8); //setup to be GPIO
    PTA->PDDR &= ~MASK(R2); // set as input

	PORTA->PCR[R1] &= ~0x700; //Clear mux
    PORTA->PCR[R1] |= MASK(8); //setup to be GPIO
    PTA->PDDR &= ~MASK(R1); // set as input
}

void read_row(){
	if (!PTA->PDIR & MASK(R1) && col1){
		keys[degree] = 1;
		degree++;
	}
	else if (!PTA->PDIR & MASK(R2) && col1){
		keys[degree] = 4;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R3) && col1){
		keys[degree] = 7;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R4) && col1){
		degree--;
	}
	else if (!PTA->PDIR & MASK(R1) && col2){
		keys[degree] = 2;
		degree++;
	}
	else if (!PTA->PDIR & MASK(R2) && col2){
		keys[degree] = 5;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R3) && col2){
		keys[degree] = 8;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R4) && col2){
		keys[degree] = 0;
		degree++;
	}
	else if (!PTA->PDIR & MASK(R1) && col3){
		keys[degree] = 3;
		degree++;
	}
	else if (!PTA->PDIR & MASK(R2) && col3){
		keys[degree] = 6;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R3) && col3){
		keys[degree] = 9;
		degree++;
	}
	else if (!PTC->PDIR & MASK(R4) && col3){
		compute_key();
	}
	else if (!PTA->PDIR & MASK(R1) && col4){
		// degree--; clk signal
	}
	else if (!PTA->PDIR & MASK(R2) && col4){
		// keys[degree] = 66; ctrl 1
	}
	else if (!PTC->PDIR & MASK(R3) && col4){
		// keys[degree] = 67; ctrl 0
	}
	else if (!PTC->PDIR & MASK(R4) && col4){
		// keys[degree] = 68; sign
	}
	else keys[degree] = 'a';
}

// flaw with this approach is that you'll wait for whole main to run before checking again which could be slow for larger programs. Alternative will be timer
void loop_cols(){
	static enum states {s1, s2, s3, s4};
	static states state = s1;
	
	switch(state){
		case s1:
			PTC->PCOR |= MASK(C1);
			PTC->PSOR |= MASK(C2);
			PTC->PSOR |= MASK(C3);
			PTC->PSOR |= MASK(C4);
			col1 = 1;
			col2 = 0;
			col3 = 0;
			col3 = 0;
			state = s2;
			break;
		case s2:
			PTC->PSOR |= MASK(C1);
			PTC->PCOR |= MASK(C2);
			PTC->PSOR |= MASK(C3);
			PTC->PSOR |= MASK(C4);
			col1 = 0;
			col2 = 1;
			col3 = 0;
			col3 = 0;
			state = s3;
			break;
		case s3:
			PTC->PSOR |= MASK(C1);
			PTC->PSOR |= MASK(C2);
			PTC->PCOR |= MASK(C3);
			PTC->PSOR |= MASK(C4);
			col1 = 0;
			col2 = 0;
			col3 = 1;
			col3 = 0;
			state = s4;
			break;
		case s4:
			PTC->PSOR |= MASK(C1);
			PTC->PSOR |= MASK(C2);
			PTC->PSOR |= MASK(C3);
			PTC->PCOR |= MASK(C4);
			col1 = 0;
			col2 = 1;
			col3 = 0;
			col3 = 0;
			state = s1;
			break;
		default:
			state = s1;
			break;
	}
}

void compute_key(){
	key = 0;
	for (int i = 0; i < degree; i++){
		key += keys[i] * pow(degree-1-i);
	}
	degree = 0;
}
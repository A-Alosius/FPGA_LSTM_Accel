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
#define C3 (6) // PTC6
#define C4 (5) // PTC5

//Other useful functions:
void read_input(void);
void loop_rows(void);
void keypad_config(void);

uint8_t col1, col2, col3, col4;

void read_input(){
	if (!PTA->PDIR & MASK(R1) && col1){
		key = 1;
	}
	else if (!PTA->PDIR & MASK(R2) && col1){
		key = 4;
	}
	else if (!PTC->PDIR & MASK(R3) && col1){
		key = 7;
	}
	else if (!PTC->PDIR & MASK(R4) && col1){
		key = 42;
	}
	else if (!PTA->PDIR & MASK(R1) && col2){
		key = 2;
	}
	else if (!PTA->PDIR & MASK(R2) && col2){
		key = 5;
	}
	else if (!PTC->PDIR & MASK(R3) && col2){
		key = 8;
	}
	else if (!PTC->PDIR & MASK(R4) && col2){
		key = 0;
	}
	else if (!PTA->PDIR & MASK(R1) && col3){
		key = 3;
	}
	else if (!PTA->PDIR & MASK(R2) && col3){
		key = 6;
	}
	else if (!PTC->PDIR & MASK(R3) && col3){
		key = 9;
	}
	else if (!PTC->PDIR & MASK(R4) && col3){
		key = 35;
	}
	else if (!PTA->PDIR & MASK(R1) && col4){
		key = 65;
	}
	else if (!PTA->PDIR & MASK(R2) && col4){
		key = 66;
	}
	else if (!PTC->PDIR & MASK(R3) && col4){
		key = 67;
	}
	else if (!PTC->PDIR & MASK(R4) && col4){
		key = 68;
	}
	else key = 'a';
}

// flaw with this approach is that you'll wait for whole main to run before checking again which could be slow for larger programs. Alternative will be timer
void loop_rows(){
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
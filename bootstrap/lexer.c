#include "compiler.h"

void GetChar() {
	Look = fgetc(infile);
}

void SkipWhite() {
	while (Look == ' ' || Look == '\t' || Look == '\n' || Look == '\r') {
		GetChar();
	}
}

#include "compiler.h"

void Match(char c) {
	if (Look == c) {
		GetChar();
		SkipWhite();
	} else {
		fprintf(stderr, "Error: Expected '%c', got '%c'\n", c, Look);
		exit(1);
	}
}

void ParseNumber() {
	char num_str[16];
	int i = 0;
	if (!isdigit(Look)) {
		fprintf(stderr, "Error: Expected a number\n");
		exit(1);
	}
	while (isdigit(Look)) {
		num_str[i++] = Look;
		GetChar();
	}
	num_str[i] = '\0';
	fprintf(outfile, "\tmov rcx, %s\n", num_str);
	SkipWhite();
}

void ParseExit() {
	Match('e'); Match('x'); Match('i'); Match('t');
	Match('(');
	ParseNumber();
	Match(')');
	Match(';');
	
	EmitLn("\tcall ExitProcess");
}
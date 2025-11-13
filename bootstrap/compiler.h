#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

extern FILE *infile;
extern FILE *outfile;
extern char Look;

void GetChar();
void SkipWhite();

void EmitLn(char *s);

void Match(char c);
void ParseNumber();
void ParseExit();
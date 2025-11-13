#include "compiler.h"

FILE *infile;
FILE *outfile;
char Look;

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <sourcefile>\n", argv[0]);
        return 1;
    }
    
    infile = fopen(argv[1], "r");
    outfile = fopen("output.asm", "w");

    EmitLn("extern ExitProcess");
    EmitLn("global main");
    EmitLn("section .text");
    EmitLn("main:");

    GetChar();
    ParseExit();

    fclose(infile);
    fclose(outfile);
    
    printf("Bureaucratic compilation complete.\n");
    return 0;
}
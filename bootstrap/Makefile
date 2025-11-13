# Makefile for the NotP Seed Compiler

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -g # -Wall/-Wextra shows all warnings, -g adds debug info

# Linker and flags
LD = gcc
LDFLAGS =

# Source files
SRCS = main.c lexer.c parser.c emitter.c

# Object files (derived from source files)
OBJS = $(SRCS:.c=.o)

# Target executable name
TARGET = compiler.exe

# The default goal, executed when you just type "make"
all: $(TARGET)

# Rule to link the final executable
$(TARGET): $(OBJS)
	$(LD) $(OBJS) -o $(TARGET) $(LDFLAGS)

# Pattern rule to compile .c files into .o files
%.o: %.c compiler.h
	$(CC) $(CFLAGS) -c $< -o $@

# Target to run the whole toolchain
run: all
	@echo "--- [STAGE 1] Compiling NotP source code ---"
	./$(TARGET) exit.notp
	@echo "--- [STAGE 2] Assembling with NASM ---"
	nasm -f win64 output.asm -o output.obj
	@echo "--- [STAGE 3] Linking final executable ---"
	$(LD) output.obj -o exit.exe
	@echo "--- [STAGE 4] Running final executable (exit.exe) ---"
	./exit.exe
	@echo "Program exited with code: %ERRORLEVEL%"

# Target to clean up all generated files
clean:
	rm -f $(TARGET) $(OBJS) output.asm output.obj exit.exe

# Phony targets are not files
.PHONY: all run clean
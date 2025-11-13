@echo off
echo [STAGE 1] Building the NotP C compiler...
gcc main.c lexer.c parser.c emitter.c -o compiler.exe
if %errorlevel% neq 0 (
    echo Compiler build failed!
    exit /b 1
)
echo Compiler built successfully: compiler.exe

echo.
echo [STAGE 2] Compiling exit.notp to assembly...
.\compiler.exe exit.notp
if %errorlevel% neq 0 (
    echo NotP compilation failed!
    exit /b 1
)
echo Assembly generated: output.asm

echo.
echo [STAGE 3] Assembling output.asm to an object file...
nasm -f win64 output.asm -o output.obj
if %errorlevel% neq 0 (
    echo Assembly failed!
    exit /b 1
)
echo Object file created: output.obj

echo.
echo [STAGE 4] Linking object file to create the final executable...
gcc output.obj -o exit.exe
if %errorlevel% neq 0 (
    echo Linking failed!
    exit /b 1
)
echo Final executable created: exit.exe

echo.
echo --- Build Complete ---
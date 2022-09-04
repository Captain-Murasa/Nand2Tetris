// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
    // initialization
    @SCREEN
    D=A
    @addr
    M=D     // addr = 16384

    @KBD
    D=M
    @PRESSED
    D;JNE   // if pressed goto PRESSED

    // no key is pressed
(NOTPRESSED)
    @addr
    A=M 
    M=0    // RAM[addr]=0

    @addr
    M=M+1
    D=M     // addr++

    @KBD
    D=A-D
    @NOTPRESSED
    D;JNE   // if addr < 24576 goto PRESSED

    @END
    0;JMP   // if done, goto END

(PRESSED)
    @addr
    A=M 
    M=-1    // RAM[addr]=1111111111111111

    @addr
    M=M+1
    D=M     // addr++

    @KBD
    D=A-D
    @PRESSED
    D;JNE   // if addr < 24576 goto PRESSED 

(END)
    // infinite loop
    @LOOP
    0;JMP
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

  
(LOOP)
    @24576      
    D=M         
    @BLACK
    D;JNE       
    
    @16384
    D=A
    @addr
    M=D   
    
(WHITE)
    @addr
    A=M  
    M=0  
    
    @addr
    M=M+1      
    D=M
    @24576     
    D=A-D      
    @WHITE
    D;JGT      
    
    @LOOP
    0;JMP
    
(BLACK)
    @16384         
    D=A
    @addr
    M=D        
    
(FILL)
    @addr
    A=M        
    M=-1       
    
    @addr
    M=M+1      
    D=M
    @24576     
    D=A-D      
    @FILL
    D;JGT      
    
    @LOOP
    0;JMP

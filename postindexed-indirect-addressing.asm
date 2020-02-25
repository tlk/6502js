; This code was compiled with https://skilldrick.github.io/easy6502/
; Hexdump: a9ff8d2301a901853aa9208539a003a901187139c8d0fb4c1706
;
; Visual 6502 Simulator:
; http://www.visual6502.org/JSSim/expert.html?graphics=false&a=0&d=a9ff8d2301a901853aa9208539a003a901187139c8d0fb4c1706

setup:
    lda #$ff
    sta $0123   ; store value 0xff in address 0x0123.
                ; 0x0123 minus 3 is 0x0120.
    lda #$01
    sta $3a
    lda #$20
    sta $39     ; store value 0x0120 in address 0x39 and 0x3a.

    ldy #$03    ; load value 0x03 in register y.
    lda #$01    ; load value 0x01 in register a:
                ;   when the value from address 0x0123 (0xff)
                ;   is added it will result in a = 0x00
                ;   and processor flag Z and C are set.
    clc

loop1:
    adc ($39),y ; post-indexed indirect addressing:
                ; 1. read the value stored in memory address 0x39
                ;    and memory address 0x3a (little endian)
                ;    which in this case is 0x0120,
                ; 2. add the value of the y register to this
                ;    which gives the address 0x123,
                ; 3. read the memory value at address 0x123
                ; 4. add the value to the a register (with carry)
                ; 5. set the Z processor flag if the result value in register a is zero
                ; 6. set the C processor flag if the operation resulted in a carry

    iny         ; 1. increment y register.
                ; 2. set the Z processor flag if the value is zero.
                ; 3. clear the Z processor flag if the value is not zero.

    bne loop1   ; goto loop1 if processor flag Z is not set.

foobar:
    jmp foobar  ; infinite loop.


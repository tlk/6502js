# 6502 emulator in javascript

Origins of this code base and full credits to:
- http://www.6502asm.com (Stian Søreng)
- https://skilldrick.github.io/easy6502/ (Nick Morgan)

This fork is based on easy6502 with the following modifications:
- Program start at **$0800**
- No RNG and Keyboard input at **$fe** and **$ff**
- Flashing a ROM-file (.bin) to the virtual chip as an alternative to writing assembly code

### Interesting forks
- https://github.com/MarcusPeixe/6502js (syntax highlight, "define" command, and more)
- https://github.com/OmgItsBkid/6502js (elements moved around to give a more IDE feel)

### Crazy good video introductions to the 6502
- https://eater.net/6502

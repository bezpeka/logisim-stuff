;to use put value to increment by in address 0 and read result out of address 1
.dseg
inc: .alloc 1
res: .alloc 1
.cseg
inc:
loadb inc; loads inc value
loada res; loads previous result, is zero if just started.
add; adds inc value and previous result
store res; stores result
jumpnz inc; jump to beginning if not zero
clearpc; halt the program
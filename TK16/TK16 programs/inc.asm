;to use put vaue to inc by in adress 0 get res out of adress 1
.dseg
inc: .alloc 1
res: .alloc 1
.cseg
inc:
loadb inc; loads inc value
loada res; loads previous result is zero if just started.
add; adds inc value and previous result
store res; stores result
jump inc; jump to beginning

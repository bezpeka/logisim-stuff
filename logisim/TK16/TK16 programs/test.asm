.dseg
temp: .alloc 1 
.def cons1 1
.cseg
loop:
loada temp
iloadb cons1
add
store temp
incp
jump loop
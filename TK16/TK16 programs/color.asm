;Cycle through color values

.dseg
colorval: .alloc 1
xpos: .alloc 1
ypos: .alloc 1
temp: .alloc 1 

.def screen_base 0xC000

.cseg
	;start at x=0 y=0 color = 0
  	iloada 0
	copya
	store xpos
	store ypos
	store colorval
loop_x:
	;shift y 7 spaces to make x, y address
  	loada ypos
	iloadb 7
	lshift
	store temp
	loada temp
	loadb xpos
	add		;R now has ypos*128 + xpos
	store temp
	loada temp
	iloadb screen_base
	add    ;R is now screen pixel address
	setp	;pixel address now in register P
	loada colorval
	storep ;puts colorval into addresss pointed to by P
	;increment color
	loada colorval
	iloadb 1
	add
	store colorval
	;increment x, check if 128
	loada xpos
	iloadb 1
	add
	store xpos
	loada xpos
	iloadb 128
	sub
	jumpnz loop_x  ;X wasnt at 128
	;X went to 128, reset and increment Y
	iloada 0
	copya
	store xpos
	loada ypos
	iloadb 1
	add
	store ypos
	;check if ypos went to 128 and reset if it did
	loada ypos
	iloadb 128
	sub
	jumpnz loop_x
	;need to reset Y
	iloada 0
	copya
	store ypos
	jump loop_x


.var E 0
ldai 255
ldbi 255
add
jmpc yes
yes:
ldai 1
sta E
no:
ldai 0
sta E

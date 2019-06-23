#Simple assembler for TK16
# CAK 2014
import os
print(os.getcwd())
import re
import sys

SOURCE_FILENAME = raw_input('input file:')
t = SOURCE_FILENAME.strip( '.asm' )
OUTPUT_FILENAME = t+ ".code"

VALID_LABEL = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")

#for TK16
#key is lowercase instruction name
#value is (numeric code, True is needs argument)
INSTRUCTION_TABLE = {
    'loada':(0, True),
    'loadb':(1, True),
    'store':(2, True),
    'iloada':(3, True),
    'iloadb':(4, True),
    'setp':(5, False),
    'ploada':(6, False),
    'ploadb':(7, False),
    'skey':(8, True),
    'ldisp':(9, True),
    'ktod':(10, False),
    'storep':(11, False),
    'add':(12, False),
    'sub':(13, False),
    'mul':(14, False),
    'div':(15, False),
    'neg':(16, False),
    'and':(17, False),
    'or':(18, False),
    'not':(19, False),
    'lshift':(20, False),
    'rshift':(21, False),
    'copya':(22, False),
    'copyb':(23, False),
    'jump':(24, True),
    'jumpz':(25, True),
    'jumpnz':(26, True),
    'cleargdisp':(27,False),
    'clearpc':(28,False),
    'incp':(29,False),
    'call':(30,True),
    'return':(31,False),
    'push':(32,True),
    'pop':(33,True),
    'clearpop':(34,False),
    'clearstack':(35,False)
    }
    
    

output_file = open(OUTPUT_FILENAME, "w")

#initialize counters for data and code segments
counters = {}
counters['dseg'] = 0
counters['cseg'] = 0
labels = {}
current_segment = 'cseg' #default at start


def convert_number(instring):
    if instring.startswith(("0x", "0X")):
        return int(instring[2:], 16)
    elif instring.startswith(("x", "X")):
        return int(instring[1:], 16)
    elif instring.startswith(("b", "B")):
        return int(instring[1:], 2)
    else:
        #try good old decimal conversion
        return int(instring)
    
def assert_label(instring):
    #throw an AsserionError if the string is not a valid label or
    #instruction name
    if VALID_LABEL.match(instring) is None:
        raise AssertionError(
            "'{0}' is not a valid label/token".format(instring))

asm_file = open(SOURCE_FILENAME)
asm_lines = asm_file.readlines()

#first pass works out values for labels
linenum = 1
for line in asm_lines:
    try:
        #take out any comment
        line = line.strip()
        line = line.split(";")[0]
        tokens = line.split()
        print tokens
        #check for segment directive
        if len(tokens) > 0 and tokens[0].lower() in (".cseg", ".dseg"):
            #change of segment code/data
            current_segment = tokens[0][1:].lower()
            tokens = tokens[1:]
        #check for label declaration
        if len(tokens) > 0 and tokens[0][-1] == ":":
            #a label, put it in the table
            label_name = tokens[0][:-1]
            assert_label(label_name)
            labels[label_name] = counters[current_segment]
            tokens = tokens[1:]
        #check for a definition
        if len(tokens) > 0 and tokens[0] == ".def":
            if len(tokens) >= 3:
                (name, value) = tokens[1:]
                assert_label(name)
                labels[name] = convert_number(value)
                #remove the three tokens in the .def statement
                tokens = tokens[3:] 
            else:
                raise AssertionError("Bad .def statement")
        #check for .alloc of memory spaces
        if len(tokens) > 0 and tokens[0] == ".alloc":
            if len(tokens) >= 2:
                size = tokens[1]
                if size in labels:
                    size = labels[size]
                else:
                    size = convert_number(size)
                counters[current_segment] += size
                #remove the .alloc statement tokens
                tokens = tokens[2:]
            else:
                raise AssertionError("Bad .alloc statement")
        #check if there is a token that is a valid instruction
        if len(tokens) > 0:
            instruction = tokens[0].lower()
            if instruction in INSTRUCTION_TABLE:
                #increment program counter
                counters[current_segment] += 1
                tokens = tokens[1:]
            else:
                raise AssertionError(
                    "Unknown instruction '{0}'".format(instruction))
    except:
        #catch in error and include line number
        print "Error at .asm file line {0}".format(linenum)
        #keep passing the error along
        raise
    linenum += 1

#second pass generates code
output_code = []
code_list = []
linenum = 1
code_segment = False #need to look for .cseg
for line in asm_lines:
    try:
        #take out any comment
        line = line.strip()
        without_comments = line.split(";")[0]
        tokens = without_comments.split()
        if len(tokens) > 0 and tokens[0][-1] == ":":
            #label at start, remove from token list
            tokens = tokens[1:]
        if len(tokens) > 0 and tokens[0].lower() == ".cseg":
            #start of code segment
            code_segment = True
            tokens = tokens[1:]
        if len(tokens) > 0 and tokens[0][0] != ".":
            #should be an instruction
            instruction = tokens[0].lower()
            if instruction in INSTRUCTION_TABLE:
                (opcode, needs_argument) = INSTRUCTION_TABLE[instruction]
                code = opcode << 16
                if needs_argument:
                    if len(tokens) > 1:
                        argument = tokens[1]
                        if argument in labels:
                            argument = labels[argument]
                        else:
                            argument = convert_number(argument)
                        code += argument
                    else:
                        raise AssertionError(
                            "Argument Missing for {0}".format(instruction))
                output_code.append(code)
                code_list.append(
                    "({0})    {1}".format(hex(code),line.strip()))
            else:
                raise AssertionError(
                    "{0} is not a valid instruction".format(instruction))
        else:
            #should still add to code listing
            code_list.append(line)
    except:
        print "Error at .asm file line {0}".format(linenum)
        raise
    linenum += 1
              
print labels
print output_code
for line in code_list:
    print line

#header for logisim image
output_file.write("v2.0 raw\n")

for code in output_code:
    output_file.write("{0:06x}\n".format(code))


asm_file.close()
output_file.close()
    


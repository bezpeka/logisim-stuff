#Assembler for new Terpstra CPU
# Dec 20 2014
# CAK

import re
import sys

if len(sys.argv) == 2:
    #first argument is second in list
    SOURCE_FILENAME = sys.argv[1]
else:
    SOURCE_FILENAME = raw_input('input file:')
t = SOURCE_FILENAME.strip( '.asm' )
OUTPUT_FILENAME = t+ ".code"

VALID_LABEL = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")

#key is lowercase instruction name
#value is (numeric code, True is needs argument)
INSTRUCTION_TABLE = {
    'lda':(0, True),
    'ldb':(1, True),
    'ldai':(2, True),
    'ldbi':(3, True),
    'add':(4, False),
    'sub':(5, False),
    'mult':(6, False),
    'div':(7, False),
    'sta':(8, True),
    'stb':(9, True),
    'str':(10, True),
    'jmp':(11, True),
    'jmpc':(12, True),
    'jmpz':(13, True)
    }
    
    

output_file = open(OUTPUT_FILENAME, "w")

labels = {}
memcounter = 0


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

#first pass works out values for labels and variables
linenum = 1
for line in asm_lines:
    try:
        #take out any comment
        line = line.strip()
        line = line.split(";")[0]
        tokens = line.split()
        print tokens
        #check for label declaration
        if len(tokens) > 0 and tokens[0][-1] == ":":
            #a label, put it in the table
            label_name = tokens[0][:-1]
            assert_label(label_name)
            labels[label_name] = memcounter
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
        #check for a variable definition, dont do anything until
        #next pass
        if len(tokens) > 0 and tokens[0] == ".var":
            if len(tokens) >= 3:
                tokens = tokens[3:] 
            else:
                raise AssertionError("Bad .var statement")
        #check if there is a token that is a valid instruction
        if len(tokens) > 0:
            instruction = tokens[0].lower()
            if instruction in INSTRUCTION_TABLE:
                #increment program counter (by 2)
                memcounter += 2
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
init_values = [] #for data variables
for line in asm_lines:
    try:
        #take out any comment
        line = line.strip()
        without_comments = line.split(";")[0]
        tokens = without_comments.split()
        if len(tokens) > 0 and tokens[0][-1] == ":":
            #label at start, remove from token list
            tokens = tokens[1:]
        if len(tokens) > 0 and tokens[0][0] != ".":
            #should be an instruction
            instruction = tokens[0].lower()
            if instruction in INSTRUCTION_TABLE:
                (opcode, needs_argument) = INSTRUCTION_TABLE[instruction]
                output_code.append(opcode)
                if needs_argument:
                    if len(tokens) > 1:
                        argument = tokens[1]
                        if argument in labels:
                            argument = labels[argument]
                        else:
                            argument = convert_number(argument)
                    else:
                        raise AssertionError(
                            "Argument Missing for {0}".format(instruction))
                else:
                    argument = 0x00 #space for no argument
                output_code.append(argument)
                code_list.append("({0} {1}) {2}".format(
                            hex(opcode), hex(argument),line.strip()) )
            else:
                raise AssertionError(
                    "{0} is not a valid instruction".format(instruction))
        elif len(tokens) > 0 and tokens[0] == ".var":
            #variable definition, make room at the end of the program
            (name, init_value) = tokens[1:]
            labels[name] = memcounter  #end of program
            memcounter += 1
            init_values.append(convert_number(init_value))
        else:
            #should still add to code listing
            code_list.append(line)
    except:
        print "Error at .asm file line {0}".format(linenum)
        raise
    linenum += 1

#append variables with initial values to end of code
for val in init_values:
    output_code.append(val)
              
print labels
print output_code
for line in code_list:
    print line

#header for logisim image
output_file.write("v2.0 raw\n")

for code in output_code:
    output_file.write("{0:02x}\n".format(code))


asm_file.close()
output_file.close()
    


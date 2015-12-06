stop = false
input_file = ""
output_file = ""
ins_table = {}
ins_table["ld"]=1
ins_table["str"]=2
ins_table["add"]=3
ins_table["sub"]=4
ins_table["jmp"]=5
ins_table["jmpz"]=6
ins_table["jmpnz"]=7
ins_table["imm"]=8
mem_loc = 0
label_table = {}
var_table = {}
while not stop
print "Input file:"
input_file = gets.chomp
if input_file != "exit"
output_file = input_file.gsub(".asm",".code")
output_file = File.open(output_file, "w")
output_file.puts("v2.0 raw")
input_file = File.open(input_file, "r")
input_file.each_line do |line|
pos = line.index(":")
if pos == nil
mem_loc +=1
else
line = line.split(":")
line = line[0]
temp = String(mem_loc)
while temp.length < 4
temp = "0" + temp
end
label_table[line] = temp
puts "Label "+line+" assigned "+temp
end
end
input_file.rewind
input_file.each_line do |line|
if line.index(":") == nil
line = line.split(" ")
print "ins:" + line[0] + " "
puts "arg:" + line[1]
ins = ins_table[line[0]]
puts "ins code:" + String(ins)
ins = String(ins)
arg = String(line[1])
if label_table.has_key?(arg)
arg = label_table[arg]
end
ins = arg.prepend(ins)
puts "final ins:" + ins
output_file.puts(ins)
end
end
output_file.close
input_file.close
else
stop = true
end
end
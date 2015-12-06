class String
  def convert_base(from, to)
    self.to_i(from).to_s(to)
    # In Ruby 1.9.2+ the more strict below is possible:
    # Integer(self, from).to_s(to)
  end
end
input_file = ""
output_file = ""
ins_table = {}
n = 1
a = 0
zero=false
incn = true
mem = {}
ins_table["1"]="ld"
ins_table["2"]="str"
ins_table["3"]="add"
ins_table["4"]="sub"
ins_table["5"]="jmp"
ins_table["6"]="jmpz"
ins_table["7"]="jmpnz"
ins_table["8"]="imm"
print "Code file:"
input_file = gets.chomp
output_file = input_file.gsub(".code",".data")
output_file = File.open(output_file,"w")
while n <= File.foreach(input_file).count
line = IO.readlines(input_file)[n]
ins = ins_table[line[0]]
arg = String(line[1]) + String(line[2]) + String(line[3]) + String(line[4])
arg = arg.convert_base(16,10)
arg = Integer(arg)
if ins == "ld"
if arg < 65536
if mem[arg] != nil
a = mem[arg]
else
a = 0
end
end
elsif ins == "str"
if arg < 65536
mem[arg] = a
end
elsif ins == "add"
if mem[arg] != nil
if mem[arg] + a < 4294967296
a = mem[arg] + a
if a == 0
z=true
end
else
exit
end
end
elsif ins == "sub"
if mem[arg] != nil
if a - mem[arg] >= 0
a = mem[arg] + a
else
exit
end
end
elsif ins == "jmp"
n = arg + 1
incn = false
elsif ins == "jmpz"
if zero
n = arg + 1
incn = false
end
elsif ins == "jmpnz"
if not zero
n = arg + 1
incn = false
end
elsif ins == "imm"
a = arg
end
if incn
n += 1
else
incn = true
end
string = ""
mem.each do |key, value|
string += "#{key}=>#{value}, "  
output_file.puts string
end
end

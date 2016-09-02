puts "Assembly file:"
insSet={"LOADA"=>"0", "LOADB"=>"1", "SAVE"=>"2", "LOWBITS"=>"3", "ADD"=>"40", "SUB"=>"41", "AND"=>"42", "OR"=>"43", "XOR"=>"44", "INVA"=>"45", "INVB"=>"46", "PASSA"=>"47", "PASSB"=>"48", "LSHIFT"=>"49", "RSHIFT"=>"4a", "CLEAR"=>"4b", "INC"=>"4c", "DEC"=>"4d"}
file=gets.chomp!
outFile=file.gsub(".asm", ".code")
file=File.open(file, "r")
outFile=File.open(outFile, "w")
outFile.puts "v2.0 raw"
file.each_line do |line|
  line = line.split(" ")
    if insSet[line[0][0]].length == 1
      outFile.puts insSet[line[0]]+line[1]
    else
      outFile.puts insSet[line[0][0]]
    end
end
file.close
outFile.close
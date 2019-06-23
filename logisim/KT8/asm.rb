insSet={"LOADA"=>"0", "LOADB"=>"1", "SAVE"=>"2", "LOWBITS"=>"3", "ADD"=>"40", "SUB"=>"41", "AND"=>"42", "OR"=>"43", "XOR"=>"44", "INVA"=>"45", "INVB"=>"46", "SWAPA"=>"47", "SWAPB"=>"48", "LSHIFT"=>"49", "RSHIFT"=>"4a", "CLEAR"=>"4b", "INC"=>"4c", "DEC"=>"4d","SWAWPB"=>"4e","FJMP"=>"5", "BJMP"=>"6", "FJMPZ"=>"7", "BJMPZ"=>"8", "FJMPNZ"=>"9", "BJMPNZ"=>"a", "RESET"=>"b0", "HALT"=>"b1"}
mcounter=0
file = ""
until File.exist?(file)
  print "File:"
  file=gets.chomp!
  if file.split(".").length == 1
    file+=".asm"
  end
  unless File.exist?(file)
    puts "Invalid file!"
  end
end
outFile=file.gsub(".asm", ".code")
file=File.open(file, "r")
outFile=File.open(outFile, "w")
outFile.puts "v2.0 raw"
file.each_line do |line|
  line = line.split(" ")
  puts "line;#{line} "
  if insSet[line[0]].length == 1
    outFile.puts insSet[line[0]]+line[1]
  else
    outFile.puts insSet[line[0]]
  end
end
file.close
outFile.close
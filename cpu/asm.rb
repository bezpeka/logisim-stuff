instructionSet = { "lda" => ["0",true], "ldb" => ["1",true], "ldai" => ["2",true], "ldbi" => ["3",true], "add" => ["4",false], "sub" => ["5",false], "str" => ["6",true], "jmp" => ["7",true], "jmpc" => ["8",true], "jmpnc" => ["9",true], "jmpz" => ["a",true], "jmpnz" => ["b",true], "hlt" => ["c",false]}
inFile = gets.chomp
outFile = inFile.gsub(".asm",".code")
outFile = File.open(outFile,"w")
File.open(inFile,"r") do |f|
	outFile.puts("v2.0 raw")
	f.each_line do |line|
		line = line.split(" ")
		puts "Line:"+line.to_s
		ins = instructionSet[line[0]][0]
		requireArg = instructionSet[line[0]][1]
		puts "Ins:"+ins
		puts "arg?:"+requireArg.to_s
		if requireArg
			arg = line[1]
			puts "Arg:"+arg
			outFile.puts ins+arg
		else
		outFile.puts ins+"0"
		end
	end
end
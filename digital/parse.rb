require "nokogiri"
dig_file = File.open(ARGV[0]) { |f| Nokogiri::XML(f) }
elements=dig_file.xpath("//visualElement")
elements.each do |element|
  name=element.at_xpath("elementName").text
  pos=element.at_xpath("pos")
  puts "#{name} at #{pos["x"]},#{pos["y"]}"
end
wires=dig_file.xpath("//wire")
wires.each do |wire|
  p1=wire.at_xpath("p1")
  p2=wire.at_xpath("p2")
  puts "Wire from #{p1["x"]},#{p1["y"]} to #{p2["x"]},#{p2["y"]}"
end

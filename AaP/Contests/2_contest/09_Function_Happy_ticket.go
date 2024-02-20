func isLucky(line string) bool {
	var firstHalf = line[0] + line[1] + line[2]
	var secondHalf = line[3] + line[4] + line[5]
	return firstHalf == secondHalf
}

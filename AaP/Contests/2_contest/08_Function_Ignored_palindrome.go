import "strings"

func isPalindrome(line string) bool {
	line = strings.ToLower(line)
	var firstLowerLetter int = 'a'
	var lastLowerLetter int = 'z'
	for i := 0; i < firstLowerLetter; i++ {
		line = strings.ReplaceAll(line, (string)(i), "")
	}
	for i := lastLowerLetter + 1; i < 255; i++ {
		line = strings.ReplaceAll(line, (string)(i), "")
	}
	for i := 0; i < len(line)/2; i++ {
		if line[i] != line[len(line)-i-1] {
			return false
		}
	}
	return true
}

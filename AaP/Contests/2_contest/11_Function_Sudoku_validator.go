func isValidSudoku(bord [rows][cols]int) bool {
	rightSummary := 45
	for i := 0; i < rows; i++ {
		summary := 0
		for j := 0; j < cols; j++ {
			summary += bord[i][j]
		}
		if summary != rightSummary {
			return false
		}
	}
	for i := 0; i < cols; i++ {
		summary := 0
		for j := 0; j < rows; j++ {
			summary += bord[j][i]
		}
		if summary != rightSummary {
			return false
		}
	}
	return true
}

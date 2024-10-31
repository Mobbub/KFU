def leg_count_in_longest_sequence(legs):
    max_count = 0
    current_count = 1
    max_leg = legs[0]
    
    for i in range(1, len(legs)):
        if legs[i] == legs[i - 1]:
            current_count += 1
        else:
            if current_count > max_count:
                max_count = current_count
                max_leg = legs[i - 1]
            current_count = 1
    
    if current_count > max_count:
        max_leg = legs[-1]
    
    return max_leg
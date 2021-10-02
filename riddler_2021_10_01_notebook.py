# https://fivethirtyeight.com/features/can-you-power-through-the-workout/
# Riddler Classic

import collections

def check_movement_valid(s, proposed_addition):
    """
    Exactly two rangers should switch locations each week.
    """
    return (
        len(s[-1][0].intersection(proposed_addition[0])) == 1
        and len(s[-1][1].intersection(proposed_addition[1])) == 1
    )

def check_equal_north_south(s):
    """
    Each ranger should spend as many weeks in the north as they do in the south.
    """
    for ranger in range(1, 5):
        weeks_n = 0
        for week in s:
            if ranger in week[0]:
                weeks_n += 1
            else:
                weeks_n -= 1
        if weeks_n != 0:
            return False
    return True

def check_equal_number_of_switches(s):
    """
    All rangers should move the same number of times over the course of the schedule. 
    This includes potentially moving back to their starting assignment after the last week of the schedule.
    """    
    switches_l = []  # List of number of switches for all rangers
    for ranger in range(1, 5):
        switches_n = 0  # Number of switches for a given ranger

        # Loop sequence, because we have to check including the return
        looped_sequence = s[:]
        looped_sequence.append(looped_sequence[0])

        # Count number of switches
        for i in range(len(looped_sequence) - 1):
            if (
                ranger in looped_sequence[i][0] and ranger in looped_sequence[i + 1][1]
            ) or (
                ranger in looped_sequence[i][1] and ranger in looped_sequence[i + 1][0]
            ):
                switches_n += 1
        switches_l.append(switches_n)

        # Check switches are equal
        if min(switches_l) != max(switches_l):
            return False
    return True

def check_equal_partners(s):
    """
    Each ranger should spend the same number of weeks paired with each other ranger.
    """
    for ranger in range(1,5):

        # List of partners
        partners = []
        for week in s:
            if ranger in week[0]:
                partners.append(week[0].difference({ranger}).pop())
            else:
                partners.append(week[1].difference({ranger}).pop())
        
        # Check partners are equal
        ct=collections.Counter(partners)
        if (max(ct.values()) != min(ct.values())) or len(ct) != 3:
            return False
    return True

def check_final_return_possible(s):
    return check_movement_valid(s,s[0])


# Assume each ranger has an ID number from 1-4
# First two rangers are in north, last two are in south

# All potential week orientations
all_permutations = [[{1,2},{3,4}],
                    [{1,3},{2,4}],
                    [{1,4},{2,3}],                    
                    [{3,4},{2,1}],
                    [{2,4},{1,3}],
                    [{2,3},{4,1}]]

# This must be the starting sequence, all others are isomorphic
queue = [[[{1, 2}, {3, 4}], [{1, 3}, {2, 4}]]]

# Run from shortest sequences and get longer, until solution is found
max_length = 100000000
while len(queue) < max_length:
    s = queue[0]

    # Length has to be multiple of 6 - to speed up computation?
    # Because must be even (north/south) and multiple of 3 (equal partners)
    if len(s) % 6 == 0 and check_equal_north_south(s) and check_equal_number_of_switches(s) and check_equal_partners(s) and check_final_return_possible(s):
        print("Success: {}".format(s))
        break
    else:
        for perm in all_permutations:
            new_seq = s[:]
            if check_movement_valid(new_seq, perm):
                new_seq.append(perm)
                queue.append(new_seq)
    queue.remove(s)

"""
Success: [[{1, 2}, {3, 4}], [{1, 3}, {2, 4}], [{1, 2}, {3, 4}], [{1, 4}, {2, 3}], [{3, 4}, {1, 2}], [{1, 3}, {2, 4}], [{3, 4}, {1, 2}], [{2, 3}, {1, 4}], [{2, 4}, {1, 3}], [{1, 4}, {2, 3}], [{2, 4}, {1, 3}], [{2, 3}, {1, 4}]]
(length of 12)
"""

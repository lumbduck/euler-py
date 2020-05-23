"""
This file contains material for calculating cycles in the sequence of gaps that occur between terms given by the expansion of repeating fraction in problem 57.
"""
from itertools import accumulate, chain, cycle

from numb import num_digits

from common import elapsed, split_timer

# First few cycles keyed by the expansion iteration where they begin
# Further cycles alternate between the 2nd and 3rd, switching cycles around every 3700-4700 terms of the fraction expansion
gap_map = {
    0: (8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8),
    3229: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
    7947: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
}


def expand_terms(n=3, d=2):
    while True:
        yield n, d

        d0 = d
        d = n + d
        n = d + d0


def find_cycle(gap_list):
    """Used for determining cycles during :func detect_cycles:."""
    expected_cycle_lens = (31, 32, 33)

    # Stringent on first test
    if not any(gap_list[:i] == gap_list[i:2 * i] for i in expected_cycle_lens):
        return -1

    # Actual test
    for i in expected_cycle_lens:
        failed_test = False
        test_cycle = gap_list[:i]
        test_field = gap_list[i:]

        while i <= len(test_field):
            if not test_cycle == test_field[:i]:
                failed_test = True
                break
            else:
                test_field = test_field[i:]

        if not failed_test:
            return test_cycle


def pp(dictionary):
    """Pretty print a dictionary at one level of depth."""
    print("{")
    for k, v in dictionary.items():
        print(f"    {k}: {v},")
    print("}")


def detect_cycles():
    """
    Detect cycles and update cycle_map while iterating over :expand_terms:.

    This function appears to be redundant now, as it has determined that after the 1st cycle (which is an
    offset of another cycle), the cycles seem to alternate consistently between two versions.
    """
    # NOTE: Program will crash around 567000 iterations, as the fraction terms have over 217034 digits.

    # Indeces where current count of valid terms will be reported. Program quits on last report index.
    report_indeces = [10**k for k in range(3, 6)] + [566000]
    report = dict()
    valid_terms = 0  # As determined by the statement of problem 57

    start_index = 1
    start_n, start_d = 3, 2

    while True:
        split_timer()

        # Variables for gap testing
        new_gaps = []
        last_gap = 0
        last_failure = None

        # Test for next failure and then begin cycle testing
        for i, (n, d) in enumerate(expand_terms(start_n, start_d), start_index):
            if i == 1:
                print(f"Starting cycle detection...")
                gap_cycle = accumulate(cycle(gap_map[0]))
            elif i in gap_map:
                print(f"Updated cycle at {i}...")
                gap_cycle = accumulate(chain([i], cycle(gap_map[i])))

            if i in report_indeces:
                print(f"Valid terms after {i} iterations: {valid_terms}")
                report[i] = valid_terms
                if i == report_indeces[-1]:
                    "Ending at limit"
                    return report

            if num_digits(n) > num_digits(d):
                if last_failure:
                    # Determining next gap cycle
                    new_gaps.append(i - last_gap)

                    if len(new_gaps) > 200:
                        next_cycle = find_cycle(new_gaps)
                        if next_cycle:
                            if next_cycle == -1:
                                print(f"Cycle detection error:\n{new_gaps}")
                                return report
                            else:
                                gap_map[last_failure] = next_cycle
                                start_index = last_failure
                                print(f"New cycle: {next_cycle}")
                                break

                else:
                    next_gap_accum = next(gap_cycle)
                    if not i == next_gap_accum:
                        print(f"FAILED {i}: expected {next_gap_accum}")
                        last_failure = i
                        start_n, start_d = n, d
                    else:
                        valid_terms += 1

                last_gap = i


def alternate_cycles():
    """Test alternating cycle pattern without generating new cycles while iterating over :expand_terms:."""
    # NOTE: Program will crash around 567000 iterations, as the fractions terms have over 217034 digits.

    # Indeces where current count of valid terms will be reported. Program quits on last report index.
    report_indeces = [10**k for k in range(3, 7)] + [567000]
    valid_terms = 0  # As determined by the statement of problem 57

    # Tracking cycle swaps after the initial cycle fails
    alternating_cycle_ids = (3229, 7947)
    cycle_id_pointer = 0
    swap_points = []

    print(f"Starting cycle/expansion comparison...")
    gap_cycle = accumulate(cycle(gap_map[0]))

    while True:
        # Test for next failure and then alternate cycles
        for i, (n, d) in enumerate(expand_terms(), 1):
            if i in report_indeces:
                print(f"\tValid terms after {i} iterations: {valid_terms}")
                print(f"\tFraction scale: {num_digits(n)} digits in numerator")
                if i == report_indeces[-1]:
                    "Ending at limit"
                    return swap_points

            if num_digits(n) > num_digits(d):
                next_gap_accum = next(gap_cycle)
                valid_terms += 1
                if not i == next_gap_accum:
                    print(f"Switching cycle at {i} (cycle_id={alternating_cycle_ids[cycle_id_pointer]})")
                    gap_cycle = accumulate(chain([i], cycle(gap_map[alternating_cycle_ids[cycle_id_pointer]])))
                    cycle_id_pointer = 0 if cycle_id_pointer else 1
                    swap_points.append(i)

                    assert i == next(gap_cycle), f"FAILED {i}: Cycles out of sync."


# term_report = detect_cycles()

# print("\nAll valid terms found during cycle detection:")
# pp(term_report)
# print("\nCycles detected:")
# pp(gap_map)

swap_points = alternate_cycles()
print("\nAll cycle swap points:")
print(swap_points, "\n")

last = None
spaces = []
for i in sorted(swap_points):
    if last:
        spaces.append(i - last)
    last = i
print("\nSpacing between swap points:")
print(spaces, "\n")

elapsed()

##########################
# Final reporting of alternate_cycles() with report_indeces = [10**k for k in range(3, 6)] + [567000]
##########################
#
#         Valid terms after 567000 iterations: 85344
#         Fraction scale: 217034 digits in numerator
#
# All cycle swap points:
# [3229, 7947, 11717, 16226, 20205, 24714, 28693, 33202, 37181, 41690, 45460, 50178, 53948, 58666, 62436, 66945, 70924, 75433, 79412, 83921, 87900, 92409, 96388, 100897, 104667, 109385, 113155, 117873, 121643, 126152, 130131, 134640, 138619, 143128, 147107, 151616, 155595, 160104, 163874, 168592, 172362, 177080, 180850, 185359, 189338, 193847, 197826, 202335, 206314, 210823, 214802, 219311, 223081, 227799, 231569, 236287, 240057, 244566, 248545, 253054, 257033, 261542, 265521, 270030, 274009, 278518, 282288, 287006, 290776, 295494, 299264, 303773, 307752, 312261, 316240, 320749, 324728, 329237, 333216, 337725, 341495, 346213, 349983, 354701, 358471, 362980, 366959, 371468, 375447, 379956, 383935, 388444, 392214, 396932, 400702, 405420, 409190, 413908, 417678, 422187, 426166, 430675, 434654, 439163, 443142, 447651, 451421, 456139, 459909, 464627, 468397, 473115, 476885, 481394, 485373, 489882, 493861, 498370, 502349, 506858, 510628, 515346, 519116, 523834, 527604, 532322, 536092, 540601, 544580, 549089, 553068, 557577, 561556, 566065]
#
# Spacing between swap points:
# [4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509]


##########################
# Final reporting of detect_cycles() with report_indeces = [10**k for k in range(3, 6)] + [565000]
##########################
# All valid terms found during cycle detection:
# {
#     1000: 153,
#     10000: 1508,
#     100000: 15052,
#     565000: 85042,
# }

# Cycles detected:
# {
#     0: (8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8),
#     3229: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     7947: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     11717: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     16226: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     20205: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     24714: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     28693: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     33202: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     37181: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     41690: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     45460: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     50178: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     53948: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     58666: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     62436: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     66945: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     70924: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     75433: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     79412: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     83921: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     87900: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     92409: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     96388: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     100897: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     104667: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     109385: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     113155: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     117873: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     121643: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     126152: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     130131: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     134640: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     138619: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     143128: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     147107: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     151616: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     155595: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     160104: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     163874: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     168592: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     172362: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     177080: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     180850: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     185359: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     189338: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     193847: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     197826: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     202335: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     206314: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     210823: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     214802: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     219311: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     223081: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     227799: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     231569: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     236287: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     240057: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     244566: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     248545: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     253054: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     257033: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     261542: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     265521: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     270030: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     274009: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     278518: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     282288: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     287006: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     290776: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     295494: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     299264: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     303773: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     307752: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     312261: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     316240: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     320749: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     324728: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     329237: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     333216: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     337725: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     341495: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     346213: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     349983: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     354701: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     358471: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     362980: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     366959: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     371468: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     375447: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     379956: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     383935: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     388444: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     392214: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     396932: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     400702: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     405420: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     409190: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     413908: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     417678: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     422187: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     426166: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     430675: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     434654: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     439163: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     443142: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     447651: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     451421: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     456139: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     459909: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     464627: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     468397: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     473115: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     476885: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     481394: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     485373: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     489882: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     493861: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     498370: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     502349: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     506858: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     510628: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     515346: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     519116: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     523834: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     527604: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     532322: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     536092: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     540601: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     544580: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     549089: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     553068: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
#     557577: [3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5],
#     561556: [8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8],
# }

# Spacing between cycle generation points:
# [4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979, 4509, 3770, 4718, 3770, 4718, 3770, 4718, 3770, 4509, 3979, 4509, 3979, 4509, 3979]

# Elapsed time: 97.798241 seconds
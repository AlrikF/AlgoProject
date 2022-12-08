import sys
import time
import psutil

gap = 30


def read():  # Reading input from "input.txt" file

    file = sys.argv[1]  # Reading first argument which is the file "input.txt"
    f = open(file, "r")
    string_list = []  # list of both strings
    pos1 = []  # list of positions for first string
    pos2 = []  # list of positions for second string

    for line in f.readlines():
        line = line.strip()

        if not line.isnumeric():
            string_list.append(line)

        else:
            if len(string_list) < 2:  # if secon string is encountered already then add numbers in pos2
                pos1.append(int(line))
            else:
                pos2.append(int(line))

    f.close()
    return string_list, pos1, pos2


def string_generator(string, num):  # generates string from the pos and string

    index = 0

    while index < len(num):
        string = string[0:num[index] + 1] + string + string[num[index] + 1:]
        index += 1

    return string


def get_input():  # gets both the generated strings and adds them in a list and returns the list
    str_list, pos1, pos2 = read()
    string_list = []
    string_list.append(string_generator(str_list[0], pos1))
    string_list.append(string_generator(str_list[1], pos2))

    return string_list


def penalty_mismatch(a1, a2):  # function that holds the penalty mismatch matrix
    str = 'ACGT'
    index1 = str.find(a1)
    index2 = str.find(a2)
    penalty_metrix = [[0, 110, 48, 94],
                      [110, 0, 118, 48],
                      [48, 118, 0, 110],
                      [94, 48, 110, 0]]
    return penalty_metrix[index1][index2]


def sequence_alignment(s1, s2):  # MAIN ALGORITHM THE CALCULATES THE COST AND sequence_alignment

    s1_len = len(s1)

    s2_len = len(s2)

    OPT = [[0 for col in range(s2_len + 1)] for row in range(s1_len + 1)]  # Creating dp array

    for i in range(s1_len + 1):  # for no sequence_alignment
        OPT[i][0] = gap * i

    for j in range(s2_len + 1):  # for no sequence_alignment
        OPT[0][j] = gap * j

    # To calculate the cost of alignment

    for i in range(1, s1_len + 1):
        for j in range(1, s2_len + 1):
            if s1[i - 1] == s2[j - 1]:
                min_value = min(OPT[i - 1][j - 1],
                                OPT[i - 1][j] + gap,
                                OPT[i][j - 1] + gap)
                OPT[i][j] = min_value
            else:
                min_value = min(OPT[i - 1][j - 1] + penalty_mismatch(s1[i - 1], s2[j - 1]),
                                OPT[i - 1][j] + gap,
                                OPT[i][j - 1] + gap)
                OPT[i][j] = min_value

    # TO calculate the alignment

    i = s1_len
    j = s2_len
    seq = [[0 for col in range(s2_len + 1)] for row in range(s1_len + 1)]
    seq[i][j] = 1
    seq[0][0] = 1
    while i != 0 or j != 0:
        if OPT[i][j] == OPT[i - 1][j] + gap:
            seq[i - 1][j] = 1
            i = i - 1
        elif OPT[i][j] == OPT[i][j - 1] + gap:
            seq[i][j - 1] = 1
            j = j - 1
        else:
            seq[i - 1][j - 1] = 1
            i = i - 1
            j = j - 1

    s1_final = ''
    s2_final = ''
    i = 0
    j = 0
    while i != s1_len and j != s1_len:
        if i != s1_len and seq[i + 1][j] == 1:
            s1_final = s1_final + s1[i]
            s2_final = s2_final + '-'
            i = i + 1
        elif j != s2_len and seq[i][j + 1] == 1:
            s1_final = s1_final + '-'
            s2_final = s2_final + s2[j]
            j = j + 1
        else:
            s1_final = s1_final + s1[i]
            s2_final = s2_final + s2[j]
            i = i + 1
            j = j + 1
    # if len(s1_final) < 100:
    #     print(s1_final)
    #     print(s2_final)
    #     output = [s1_final, s2_final]
    # else:
    #     print(s1_final[0:50], s1_final[-50:])
    #     print(s2_final[0:50], s2_final[-50:])
    #     output = [s1_final[0:50] + " " + s1_final[-50:], s2_final[0:50] + " " + s2_final[-50:]]

    output = [str(OPT[-1][-1]), s1_final, s2_final]

    return OPT, output


def time_wrapper(s1, s2):  # calculating time
    start_time = time.time()
    OPT, output = sequence_alignment(s1, s2)  # Calling the algorithm
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return OPT, output, time_taken


def process_memory():  # calculating memory
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


input_string = get_input()
s1 = input_string[0]
s2 = input_string[1]

OPT, output, run_time = time_wrapper(s1, s2)

memory_consumed = process_memory()

print(OPT[len(s1)][len(s2)])
print(output[0])
print(output[1])
print(run_time)
print(memory_consumed)
print("input size:", len(s1) + len(s2))

output.append(str(run_time))
output.append(str(memory_consumed))
file = sys.argv[2]
f = open(file, 'wt')
f.write('\n'.join(output))
f.close()
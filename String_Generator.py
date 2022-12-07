import tracemalloc
from time import *
import sys

DELTA = 30
ALPHA = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]

def generate_string(s1, s1_index):
    string1 = s1
    for i in s1_index:
        string1 = string1[:i+1] + string1 + string1[i+1:]

    #assert len(string1)==2**len(s1_index)*len(s1)
    print(string1)
    return string1

def penalty_mismatch(b1, b2):
    str_index = 'ACGT'
    index_b1= str_index.find(b1)
    index_b2= str_index.find(b2)
    return ALPHA[index_b1][index_b2]
    

#generate_string("ACTG", [3,6,1]) 
#generate_string("TACG", [1,2,9])
#print(penalty_mismatch("A", "G"))
def get_input(file):
    #file = sys.argv[1]
    #f = open(file, "r")
    f = open(file, "r")
    string_list = []
    b1_index = []
    b2_index = []
    is_second = True
    for line in f.readlines():
        line = line.strip()
        if not line.isnumeric():
            string_list.append(line)
            if len(string_list) == 2:
                is_second = False
        else:
            if is_second:
                b1_index.append(int(line))
            else:
                b2_index.append(int(line))
    f.close()
    return string_list, b1_index, b2_index

def store_output(string1, string2):
    f = open("generated_string.txt","wt")
    f.write(string1)
    f.write("\n")
    f.write(string2)
    f.close()

def main():
    file = sys.argv[1]
    string_list, b1_index, b2_index = get_input(file)
    string1 = generate_string(string_list[0], b1_index)
    string2 = generate_string(string_list[1], b2_index)
    store_output(string1, string2)

main()


from time import *
import psutil
import sys
class Basic_Algorithm():
    def __init__(self):
        self.DELTA = 30
        self.ALPHA = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
        self.Maxlen=0
        self.ans=[" "]

    def generate_string(self,s1, s1_index):
        string1 = s1
        for i in s1_index:
            string1 = string1[:i + 1] + string1 + string1[i + 1:]

        return string1


    def get_input(self,file):
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


    def penalty_mismatch(self,b1, b2):
        str_index = 'ACGT'
        index_b1 = str_index.find(b1)
        index_b2 = str_index.find(b2)
        return self.ALPHA[index_b1][index_b2]


    def get_optimal(self,string1, string2,alignment_string1,alignment_string2):
        OPT = [[0 for _ in range(len(string2) + 1)] for __ in range(len(string1) + 1)]
        for i in range(len(string1) + 1):
            OPT[i][0] = self.DELTA * i
        for j in range(len(string2) + 1):
            OPT[0][j] = self.DELTA * j

        for i in range(1, len(string1) + 1):
            for j in range(1, len(string2) + 1):
                if string1[i - 1] == string2[j - 1]:
                    min_penalty = min(OPT[i - 1][j - 1], OPT[i - 1][j] + self.DELTA, OPT[i][j - 1] + self.DELTA)
                    OPT[i][j] = min_penalty
                else:
                    min_penalty = min(OPT[i - 1][j - 1] + self.penalty_mismatch(string1[i - 1], string2[j - 1]),
                                      OPT[i - 1][j] + self.DELTA, OPT[i][j - 1] + self.DELTA)
                    OPT[i][j] = min_penalty
        return self.get_string_alignment(OPT, string1, string2,alignment_string1,alignment_string2)


    def get_string_alignment(self, OPT, string1, string2, alignment_string1, alignment_string2):
        i = len(string1)
        j = len(string2)
        c=0
        while i > 0 and j > 0:
            if OPT[i][j] == OPT[i][j - 1] + self.DELTA:
                alignment_string1[c]= '-'
                alignment_string2[c]= string2[j - 1]
                j = j - 1
            elif OPT[i][j] == OPT[i - 1][j] + self.DELTA:
                alignment_string1[c]= string1[i - 1]
                alignment_string2[c]= '-'
                i = i - 1
            else:
                alignment_string1[c]= string1[i - 1]
                alignment_string2[c]= string2[j - 1]
                i = i - 1
                j = j - 1
            c+=1
        while i:
            alignment_string1[c]= string1[i - 1]
            alignment_string2[c]= '-'
            i = i - 1
            c += 1
        while j:
            alignment_string1[c]= '-'
            alignment_string2[c]= string2[j - 1]
            j = j - 1
            c += 1
        print(c)
        alignment_string1 = "".join(alignment_string1[:c])
        alignment_string2 = "".join(alignment_string2[:c])
        return alignment_string1[::-1], alignment_string2[::-1], OPT[len(string1)][len(string2)]


    def write_output(self, file, total_time, memory_consumed, alignment_string1, alignment_string2, opt_value, string1="",
                     string2=""):
        print(total_time, "Total Time")
        print(memory_consumed, "Memory Consumed")
        print("input size:", len(string1) + len(string2))
        print(string1)
        print(string2)
        print(alignment_string1)
        print(alignment_string2)
        print(opt_value, "Penalty")
        # print(peak, "p")

        f = open(file, 'wt')
        f.write(str(opt_value) + "\n" + alignment_string1 + "\n" + alignment_string2 + "\n" + str(total_time) + "\n" + str(
            memory_consumed))
        f.close()


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ba=Basic_Algorithm()
    string_list, b1_index, b2_index = ba.get_input(input_file)
    string1 = ba.generate_string(string_list[0], b1_index)
    string2 = ba.generate_string(string_list[1], b2_index)
    ba.Maxlen=len(string2)*len(string1)
    assignment_string1 = [" "] * ba.Maxlen
    assignment_string2 = [" "] * ba.Maxlen
    start = time()
    # tracemalloc.start(25) #com
    alignment_string1, alignment_string2, penalty = ba.get_optimal(string1, string2, assignment_string1, assignment_string2)
    end = time()
    total_time = (end - start) * 1000
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    # size, peak = tracemalloc.get_traced_memory() #com
    ba.write_output(output_file, total_time, memory_consumed, alignment_string1, alignment_string2, penalty, string1,
                 string2)


main()
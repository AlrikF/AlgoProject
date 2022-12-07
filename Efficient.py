import math
import sys
from time import *
import psutil

class AlgoUtils:
    # UTIL FUNCTIONS
    def generate_string(self, s1, s1_index):
        string1 = s1
        for i in s1_index:
            string1 = string1[:i + 1] + string1 + string1[i + 1:]

        return string1

    def get_input(self, file):
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

    def write_output(self, file, total_time, memory_consumed, final_dna1_align, final_dna2_align,  total_dna_align_cost, dna1="", dna2=""):

        print("Total Time                 ::",total_time )
        print("Memory Consumed            ::",memory_consumed, )
        print("Input size                 ::", len(dna1) + len(dna2))
        print("Generated DNA 1            ::", dna1)
        print("Generated DNA 2            ::",dna2)
        print("Final DNA1 string matching :: ", final_dna1_align)
        print("Final DNA2 string matching :: ", final_dna2_align)
        print("\nTotal Cost of Matching ::", total_dna_align_cost)


        f = open(file, 'wt')
        f.write(dna1 + "\n" + dna2 + "\n")
        f.write(
            str(total_dna_align_cost) + "\n" + final_dna1_align + "\n" + final_dna2_align + "\n" + str(total_time) + "\n" + str(
                memory_consumed))
        f.close()



class Efficient_Algorithm:


    def __init__(self):
        self.Alpha = { 'A':{'A':0,'C':110,'G':48,'T':94},
          'C':{'A':110,'C':0,'G':118,'T':48},
          'G':{'A':48,'C':118,'G':0,'T':110},
          'T':{'A':94,'C':48,'G':110,'T':0} }

        self.Delta = 30

        self.final_strings=[]


    #Efficient ALgo Functions
    def divide_conquer_split(self,dna1,dna2):
        if len(dna1) <= 2 or len(dna2) <= 2:
            self.final_strings.append(self.align_strings(dna1, dna2))
            return

        dna_split2=len(dna2)//2

        fdna= self.forward_down_alignment(dna1,dna2[:dna_split2])
        bdna= self.backward_up_alignment(dna1,dna2[dna_split2:])

        min_cost= math.inf
        dna_split1 = 0
        for i in range(len(dna1) + 1):
            if fdna[i][1] + bdna[i][1] < min_cost:
                min_cost = fdna[i][1] + bdna[i][1]
                dna_split1 = i

        self.divide_conquer_split(dna1[:dna_split1], dna2[:dna_split2])
        self.divide_conquer_split(dna1[dna_split1:], dna2[dna_split2:])


    def forward_down_alignment(self, dna1, dna2):
        #prev current
        dp = [[0] * 2 for _ in range(len(dna1) + 1)]

        for i in range(len(dna1) + 1):
           dp[i][0] = i * self.Delta

        for j in range(1, len(dna2) + 1):
            dp[0][1] = dp[0][0] + self.Delta
            for i in range(1, len(dna1) + 1):
                dp[i][1] = min(dp[i - 1][1] + self.Delta,  dp[i][0] + self.Delta,  dp[i - 1][0] + self.Alpha[dna1[i - 1]][dna2[j - 1]]  )

            for i in range(len(dna1) + 1):
                dp[i][0] = dp[i][1]

        return dp

    def backward_up_alignment(self, dna1, dna2):
        # prev current
        dp = [[0] * 2 for _ in range(len(dna1) + 1)]
        for i in range(len(dna1) + 1):
            dp[i][0] = (len(dna1) - i) * self.Delta

        for j in range(len(dna2) - 1, -1, -1):
            dp[len(dna1)][1] = dp[len(dna1)][0] + self.Delta
            for i in range(len(dna1) - 1, -1, -1):
                dp[i][1] = min( dp[i + 1][1] + self.Delta,  dp[i][0] + self.Delta, dp[i + 1][0] + self.Alpha[dna1[i]][dna2[j]]  )

            for i in range(len(dna1) + 1):
                dp[i][0] = dp[i][1]
        return dp

    def align_strings(self,dna1, dna2):
        dp = [[0]*(len(dna2) + 1) for _ in range(len(dna1) + 1)]
        final_dna1 = []
        final_dna2 = []
        sq1 = len(dna1)
        sq2 = len(dna2)

        for i in range(1,len(dna1) + 1):
            dp[i][0] = dp[i-1][0] + self.Delta

        for i in range(1,len(dna2) + 1):
            dp[0][i] = dp[0][i-1] + self.Delta

        for i in range(1, len(dna1) + 1):
            for j in range(1, len(dna2) + 1):
                dp[i][j] = min(dp[i - 1][j] + self.Delta, dp[i][j - 1] + self.Delta, dp[i - 1][j - 1] + self.Alpha[dna1[i - 1]][dna2[j - 1]]  )



        while sq1 > 0 and sq2 > 0:
            if dp[sq1][sq2] == dp[sq1 - 1][sq2 - 1] + self.Alpha[dna1[sq1 - 1]][dna2[sq2 - 1]]:
                final_dna1.append(dna1[sq1 - 1])
                final_dna2.append(dna2[sq2 - 1])
                sq1 -= 1
                sq2 -= 1
            elif dp[sq1][sq2] == dp[sq1 - 1][sq2] + self.Delta:
                final_dna1.append(dna1[sq1 - 1])
                final_dna2.append("_")
                sq1 -= 1
            else:
                final_dna1.append("_")
                final_dna2.append(dna2[sq2 - 1])
                sq2 -= 1

        if sq1:
            for i in range(sq1, 0, -1):
                final_dna1.append(dna1[i - 1])
                final_dna2.append("_")
        elif sq2:
            for i in range(sq2, 0, -1):
                final_dna1.append("_")
                final_dna2.append(dna2[i - 1])

        final_dna1.reverse()
        final_dna1.reverse()

        return "".join(final_dna1), "".join(final_dna2)



if __name__== "__main__":

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    au = AlgoUtils()
    ea = Efficient_Algorithm()

    string_list, b1_index, b2_index = au.get_input(input_file)
    dna1 = au.generate_string(string_list[0], b1_index)
    dna2 = au.generate_string(string_list[1], b2_index)

    start = time()

    ea.divide_conquer_split(dna1,dna2)

    final_dna1_align = "".join([x[0] for x in ea.final_strings])
    final_dna2_align = "".join([x[1] for x in ea.final_strings])

    total_dna_align_cost = 0
    for i in range(len(final_dna1_align)):
        if final_dna1_align[i] != "_" and final_dna2_align[i] != "_":
            total_dna_align_cost += ea.Alpha[final_dna1_align[i]][final_dna2_align[i]]
        else:
            total_dna_align_cost += ea.Delta

    end = time()
    total_time = (end - start) * 1000
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)

    au.write_output( output_file, total_time, memory_consumed, final_dna1_align, final_dna2_align, total_dna_align_cost,dna1,dna2 )





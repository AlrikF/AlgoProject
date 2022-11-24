def generate_string(s1, s1_index):
    string1 = s1
    for i in s1_index:
        string1 = string1[:i+1] + string1 + string1[i+1:]

    
    print(string1)
    print("TATTATACGCTATTATACGCGACGCGGACGCG")

#generate_string("ACTG", [3,6,1]) 
generate_string("TACG", [1,2,9])
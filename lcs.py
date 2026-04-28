def lcs(s1,s2):
    c=0
    k=0
    for i in range(len(s1)):
        for j in range(k,len(s2)):
            if s1[i]==s2[j]:
                c+=1
                k=j+1
    print(c)
s1="ABCDE"
s2="ACE"
lcs(s1,s2)
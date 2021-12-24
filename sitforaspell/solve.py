# Solve the NYT sit for a spell game
# https://www.nytimes.com/svc/crosswords/v2/puzzle/print/Dec1221.2.pdf

# Load data
path = ''
w = open(path + "words.txt").readlines()
w = [i.strip() for i in w]

# Filter dictionary to doubles
def double(s):
    for i in range(1,len(s)):
        if s[i] == s[i-1]:
            return True
    return False

# Check if word is valid
def check_valid(w):
    for i in range(len(w)-1):
        if w[i] not in d:
            return False
        elif w[i+1] not in d[w[i]]:
            return False
    print(w)
    return True

# Create graph 
d = {
     'B':{'H','C','D','L','O','B'}
    ,'H':{'B','C','S','M','O','H'}
    ,'M':{'H','S','O','P','I','M'}
    ,'I':{'M','O','P','T','E','I'}
    ,'E':{'I','T','N','L','O','E'}
    ,'L':{'B','D','N','E','O','L'}
    ,'C':{'B','H','S','D','O','C'}
    ,'S':{'C','H','M','P','O','S'}
    ,'P':{'M','S','O','I','T','P'}
    ,'T':{'O','I','P','N','E','T'}
    ,'N':{'D','O','T','L','E','N'}
    ,'D':{'B','C','O','N','L','D'}
    ,'O':{'B','H','M','I','E','L','C','D','S','P','T','N','O'}
    }

# Doubled words
wd = [i.strip().upper() for i in w if double(i) and i[0].islower() and len(i) >= 6]
for w in wd:
    check_valid(w)

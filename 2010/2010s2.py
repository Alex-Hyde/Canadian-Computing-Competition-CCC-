f = open("s2.6.in", "r")
lcodes = {}
k = int(f.readline().strip())
for i in range(k):
    letter, code = f.readline().strip().split()
    lcodes[code] = letter

seq = f.readline().strip()
string = ""
last_stop = 0
for i in range(len(seq)):
    section = seq[last_stop:i+1]
    if section in lcodes:
        string += lcodes[section]
        last_stop = i+1

print(string)

import sys

infile = open(sys.argv[1])

print("\\begin{table}")
print("\\begin{tabular}{l r}")

for line in infile:
    #print(line)
    vals = line.split()
    if len(vals)==3:
        #print(vals)

        dataset = vals[2]
        N = vals[0]

        print(f"{dataset} & {N} \\\\")

print("\\end{tabular}")
print("\\end{table}")

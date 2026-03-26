import random
import sys

n = int(sys.argv[1])
outfile = sys.argv[2]

with open(outfile, "w") as f:
    for _ in range(2 * n * n):
        f.write(str(random.randint(0, 1)) + "\n")
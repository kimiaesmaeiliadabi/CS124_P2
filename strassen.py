import sys
import time

# matrix helpers 

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

# split an even sized matrix into 4 quadrants
def split(M):
    n = len(M)
    mid = n // 2
    A11 = [row[:mid] for row in M[:mid]]
    A12 = [row[mid:] for row in M[:mid]]
    A21 = [row[:mid] for row in M[mid:]]
    A22 = [row[mid:] for row in M[mid:]]
    return A11, A12, A21, A22

# join 4 quadrants back into one matrix
def combine(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bot = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bot

# standard O(n^3) multiplication 
def naive(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):    
            a_ik = A[i][k]
            for j in range(n):
                C[i][j] += a_ik * B[k][j]
    return C

# Strassen's algorithm

def strassen(A, B, cutoff=32):
    n = len(A)

    if n <= cutoff:
        return naive(A, B)

    # if n is odd, pad to n+1 then trim the result
    if n % 2 == 1:
        # pad A and B to (n+1)x(n+1)
        A = [row + [0] for row in A] + [[0] * (n + 1)]
        B = [row + [0] for row in B] + [[0] * (n + 1)]
        C = strassen(A, B, cutoff)
        return [row[:n] for row in C[:n]]

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    P1 = strassen(A11,           sub(B12, B22), cutoff)
    P2 = strassen(add(A11, A12), B22,           cutoff)
    P3 = strassen(add(A21, A22), B11,           cutoff)
    P4 = strassen(A22,           sub(B21, B11), cutoff)
    P5 = strassen(add(A11, A22), add(B11, B22), cutoff)
    P6 = strassen(sub(A12, A22), add(B21, B22), cutoff)
    P7 = strassen(sub(A21, A11), add(B11, B12), cutoff)

    C11 = add(sub(add(P5, P4), P2), P6)
    C12 = add(P1, P2)
    C21 = add(P3, P4)
    C22 = add(sub(add(P1, P5), P3), P7)

    return combine(C11, C12, C21, C22)

# helpers
def read_input(filepath, n):
    with open(filepath) as f:
        nums = list(map(int, f.read().split()))
    if len(nums) != 2 * n * n:
        raise ValueError(f"Expected {2*n*n} integers, got {len(nums)}")
    idx = 0
    A = []
    for _ in range(n):
        A.append(nums[idx:idx + n]); idx += n
    B = []
    for _ in range(n):
        B.append(nums[idx:idx + n]); idx += n
    return A, B

# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 strassen.py <flag> <dimension> <inputfile>",
              file=sys.stderr)
        sys.exit(1)

    _flag      = sys.argv[1]  
    n          = int(sys.argv[2])
    inputfile  = sys.argv[3]

    CUTOFF = 32 # best crossover found experimentally

    A, B = read_input(inputfile, n)

    start = time.time()
    C = strassen(A, B, CUTOFF)
    elapsed = time.time() - start

    print(f"Time: {elapsed:.6f}s", file=sys.stderr)

    # output: diagonal entries only, one per line
    for i in range(n):
        print(C[i][i])
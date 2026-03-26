import sys
import time

# matrix operations
def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def split(M):
    n = len(M)
    mid = n // 2
    A = [row[:mid] for row in M[:mid]]
    B = [row[mid:] for row in M[:mid]]
    C = [row[:mid] for row in M[mid:]]
    D = [row[mid:] for row in M[mid:]]
    return A, B, C, D

def combine(A, B, C, D):
    n = len(A)
    new = []
    for i in range(n):
        new.append(A[i] + B[i])
    for i in range(n):
        new.append(C[i] + D[i])
    return new

# naive multiplication
def naive(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# strassen
def strassen(A, B, cutoff):
    n = len(A)

    if n <= cutoff:
        return naive(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    P1 = strassen(A11, sub(B12, B22), cutoff)
    P2 = strassen(add(A11, A12), B22, cutoff)
    P3 = strassen(add(A21, A22), B11, cutoff)
    P4 = strassen(A22, sub(B21, B11), cutoff)
    P5 = strassen(add(A11, A22), add(B11, B22), cutoff)
    P6 = strassen(sub(A12, A22), add(B21, B22), cutoff)
    P7 = strassen(sub(A21, A11), add(B11, B12), cutoff)

    C11 = add(sub(add(P5, P4), P2), P6)
    C12 = add(P1, P2)
    C21 = add(P3, P4)
    C22 = add(sub(add(P1, P5), P3), P7)

    return combine(C11, C12, C21, C22)

# input
def read_input(file, n):
    with open(file, "r") as f:
        nums = list(map(int, f.read().split()))

    if len(nums) != 2 * n * n:
        raise ValueError("Input file does not contain exactly 2*n^2 integers.")

    A = []
    B = []
    idx = 0

    for _ in range(n):
        A.append(nums[idx:idx + n])
        idx += n

    for _ in range(n):
        B.append(nums[idx:idx + n])
        idx += n

    return A, B

def next_power_of_two(n):
    p = 1
    while p < n:
        p *= 2
    return p

def pad_matrix(M, size):
    n = len(M)
    P = [[0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            P[i][j] = M[i][j]
    return P

def trim_matrix(M, size):
    return [row[:size] for row in M[:size]]

# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 strassen.py 0 dimension inputfile")
        sys.exit(1)

    _, _, n, file = sys.argv
    n = int(n)

    A, B = read_input(file, n)

    orig_n = n
    m = next_power_of_two(n)

    if m != n:
        A = pad_matrix(A, m)
        B = pad_matrix(B, m)

    cutoff = 16   

    C = strassen(A, B, cutoff)

    start = time.time()
    C = strassen(A, B, cutoff)
    end = time.time()

    print("Time:", end - start, file=sys.stderr)

    if m != orig_n:
        C = trim_matrix(C, orig_n)

    for i in range(orig_n):
        print(C[i][i])
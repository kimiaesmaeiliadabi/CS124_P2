import sys
import time


def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split(M):
    n = len(M)
    mid = n // 2
    M11 = [row[:mid] for row in M[:mid]]
    M12 = [row[mid:] for row in M[:mid]]
    M21 = [row[:mid] for row in M[mid:]]
    M22 = [row[mid:] for row in M[mid:]]
    return M11, M12, M21, M22


def combine(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bot = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bot


def naive(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for k in range(n):
            a_ik = A[i][k]
            row_bk = B[k]
            row_ci = C[i]
            for j in range(n):
                row_ci[j] += a_ik * row_bk[j]

    return C


def strassen(A, B, cutoff=64):
    n = len(A)

    if n <= cutoff:
        return naive(A, B)

    if n % 2 == 1:
        A_pad = [row + [0] for row in A] + [[0] * (n + 1)]
        B_pad = [row + [0] for row in B] + [[0] * (n + 1)]
        C_pad = strassen(A_pad, B_pad, cutoff)
        return [row[:n] for row in C_pad[:n]]

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


def read_input(filepath, n):
    with open(filepath, "r") as f:
        nums = [int(x) for x in f.read().split()]

    expected = 2 * n * n
    if len(nums) != expected:
        raise ValueError(f"Expected {expected} integers, got {len(nums)}")

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


def main():
    if len(sys.argv) != 4:
        sys.exit(1)

    flag = sys.argv[1]
    n = int(sys.argv[2])
    inputfile = sys.argv[3]

    cutoff = 64  # best experimental cutoff

    A, B = read_input(inputfile, n)

    start = time.perf_counter()
    C = strassen(A, B, cutoff)
    elapsed = time.perf_counter() - start

    print(f"Time: {elapsed:.6f}s", file=sys.stderr)

    for i in range(n):
        print(C[i][i])


if __name__ == "__main__":
    main()
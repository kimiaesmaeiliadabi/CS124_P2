import random
import math
from strassen import strassen


def zero_matrix(n):
    return [[0] * n for _ in range(n)]


def random_graph_adj(n, p):
    A = zero_matrix(n)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                A[i][j] = 1
                A[j][i] = 1
    return A


def trace(M):
    return sum(M[i][i] for i in range(len(M)))


def triangle_count(A, cutoff=32):
    A2 = strassen(A, A, cutoff)
    A3 = strassen(A2, A, cutoff)
    return trace(A3) // 6


def expected_triangles(n, p):
    return math.comb(n, 3) * (p ** 3)


if __name__ == "__main__":
    random.seed(124)
    n = 1024
    ps = [0.01, 0.02, 0.03, 0.04, 0.05]

    for p in ps:
        A = random_graph_adj(n, p)
        observed = triangle_count(A, cutoff=32)
        expected = expected_triangles(n, p)
        ratio = observed / expected
        print(f"p={p:.2f}: expected={expected:.1f}, observed={observed}, ratio={ratio:.3f}")
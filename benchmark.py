import time
import random
from strassen import naive, strassen


def random_matrix(n, vals=(0, 1)):
    return [[random.choice(vals) for _ in range(n)] for _ in range(n)]


def time_once(fn, A, B, *args):
    start = time.perf_counter()
    fn(A, B, *args) if args else fn(A, B)
    return time.perf_counter() - start


def best_of_three(fn, A, B, *args):
    return min(time_once(fn, A, B, *args) for _ in range(3))


def benchmark_cutoffs():
    random.seed(124)
    cutoffs = [8, 16, 32, 64, 128]
    sizes = [128, 256]

    print("Cutoff experiment")
    for n in sizes:
        A = random_matrix(n)
        B = random_matrix(n)
        print(f"\nn = {n}")
        for c in cutoffs:
            t = best_of_three(strassen, A, B, c)
            print(f"cutoff={c}: {t:.6f}")


def benchmark_crossover():
    random.seed(124)
    sizes = [16, 32, 64, 96, 128, 192, 256, 320, 512]

    print("\nNaive vs Strassen(cutoff=64)")
    for n in sizes:
        A = random_matrix(n)
        B = random_matrix(n)

        t_naive = best_of_three(naive, A, B)
        t_strassen = best_of_three(strassen, A, B, 64)
        print(f"n={n}: naive={t_naive:.6f}, strassen64={t_strassen:.6f}")


if __name__ == "__main__":
    benchmark_cutoffs()
    benchmark_crossover()
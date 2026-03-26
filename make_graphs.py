import matplotlib.pyplot as plt

# -----------------------------
# Graph 1: Naive vs Strassen (cutoff = 64)
# -----------------------------
n_vals = [16, 32, 64, 96, 128, 192, 256, 320, 512]
naive_times = [0.000148, 0.001085, 0.009664, 0.028018, 0.065166, 0.220916, 0.527254, 1.047381, 4.942209]
strassen_64 = [0.000145, 0.001371, 0.008158, 0.027533, 0.062749, 0.205260, 0.487722, 0.901444, 3.654454]

plt.figure(figsize=(8, 5))
plt.plot(n_vals, naive_times, marker='o', label=r'Naive $O(n^3)$')
plt.plot(n_vals, strassen_64, marker='s', linestyle='--', label='Strassen (cutoff=64)')
plt.axvline(64, linestyle=':', label=r'Observed breakeven $\approx 64$')
plt.yscale('log')
plt.xlabel(r'Matrix dimension $n$')
plt.ylabel('Time (seconds)')
plt.title('Naive vs Strassen Runtime')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_crossover.png', dpi=200)
plt.close()

# -----------------------------
# Graph 2: Effect of cutoff
# -----------------------------
cutoffs = [8, 16, 32, 64, 128]
times_128 = [0.119521, 0.078138, 0.071930, 0.068264, 0.073127]
times_256 = [0.827423, 0.574950, 0.507688, 0.484016, 0.480850]

plt.figure(figsize=(8, 5))
plt.plot(cutoffs, times_128, marker='o', label=r'$n=128$')
plt.plot(cutoffs, times_256, marker='s', linestyle='--', label=r'$n=256$')
plt.axvline(64, linestyle=':', label='Chosen cutoff = 64')
plt.xlabel(r'Cutoff $n_0$')
plt.ylabel('Time (seconds)')
plt.title('Effect of Cutoff on Strassen Runtime')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_cutoff.png', dpi=200)
plt.close()

# -----------------------------
# Graph 3: Triangle counts
# -----------------------------
p_vals = [0.01, 0.02, 0.03, 0.04, 0.05]
expected = [178.4, 1427.5, 4817.7, 11419.7, 22304.1]
observed = [158, 1374, 4919, 11310, 22342]

x = list(range(len(p_vals)))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar([i - width/2 for i in x], expected, width=width, label='Expected')
plt.bar([i + width/2 for i in x], observed, width=width, label='Observed')

for i, (e, o) in enumerate(zip(expected, observed)):
    plt.text(i, max(e, o) + 250, f'{o/e:.3f}x', ha='center')

plt.xticks(x, [rf'$p={p:.2f}$' for p in p_vals])
plt.xlabel(r'Edge probability $p$')
plt.ylabel('Number of triangles')
plt.title(r'Expected vs Observed Triangle Counts in $G(1024,p)$')
plt.legend()
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig_triangles.png', dpi=200)
plt.close()

print("Saved fig_crossover.png, fig_cutoff.png, fig_triangles.png")
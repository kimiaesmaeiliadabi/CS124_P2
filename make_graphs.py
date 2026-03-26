import matplotlib.pyplot as plt

# Replace these with your actual benchmark results
n_vals = [16, 32, 64, 96, 128, 192, 256, 320, 512]
naive_times = [0.00015, 0.00135, 0.0098, 0.033, 0.075, 0.274, 0.648, 1.25, 5.685]
strassen_32 = [0.00022, 0.0011, 0.0092, 0.033, 0.076, 0.294, 0.627, 1.21, 4.797]

cutoffs = [8, 16, 32, 64, 128]
times_128 = [0.125, 0.089, 0.076, 0.081, 0.078]
times_256 = [0.938, 0.706, 0.648, 0.627, 0.660]

p_vals = [0.01, 0.02, 0.03, 0.04, 0.05]
expected = [178.4, 1427.5, 4817.7, 11419.7, 22304.1]
observed = [185, 1414, 4844, 11568, 22808]

# Graph 1: naive vs strassen
plt.figure(figsize=(8, 5))
plt.plot(n_vals, naive_times, marker='o', label='Naive $O(n^3)$')
plt.plot(n_vals, strassen_32, marker='s', linestyle='--', label='Strassen (cutoff=32)')
plt.axvline(256, linestyle=':', label='Observed breakeven ≈ 256')
plt.yscale('log')
plt.xlabel('Matrix dimension $n$')
plt.ylabel('Time (seconds)')
plt.title('Naive vs Strassen Runtime')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_crossover.png', dpi=200)
plt.close()

# Graph 2: cutoff experiment
plt.figure(figsize=(8, 5))
plt.plot(cutoffs, times_128, marker='o', label='$n=128$')
plt.plot(cutoffs, times_256, marker='s', linestyle='--', label='$n=256$')
plt.axvline(32, linestyle=':', label='Best cutoff = 32')
plt.xlabel('Cutoff $n_0$')
plt.ylabel('Time (seconds)')
plt.title('Effect of Cutoff on Strassen Runtime')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_cutoff.png', dpi=200)
plt.close()

# Graph 3: triangle counts
x = list(range(len(p_vals)))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar([i - width/2 for i in x], expected, width=width, label='Expected')
plt.bar([i + width/2 for i in x], observed, width=width, label='Observed')

for i, (e, o) in enumerate(zip(expected, observed)):
    plt.text(i, max(e, o) + 250, f'{o/e:.3f}x', ha='center')

plt.xticks(x, [f'$p={p:.2f}$' for p in p_vals])
plt.xlabel('Edge probability $p$')
plt.ylabel('Number of triangles')
plt.title('Expected vs Observed Triangle Counts in $G(1024,p)$')
plt.legend()
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig_triangles.png', dpi=200)
plt.close()

print("Saved fig_crossover.png, fig_cutoff.png, fig_triangles.png")
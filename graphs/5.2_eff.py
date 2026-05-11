import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('benchmark_results.csv')
plt.rcParams.update({'font.size': 11})
plt.figure(figsize=(10, 6))

sizes = sorted(df['Size_Words'].unique())
processes = sorted(df['Processes'].unique())

for s in sizes:
    subset = df[df['Size_Words'] == s].sort_values('Processes')
    label = f'N = {s:,} слів'
    plt.plot(subset['Processes'], subset['Speedup'], marker='o', linewidth=2, label=label)

plt.title('Залежність прискорення від кількості процесів для різних обсягів даних', 
          fontsize=13, fontweight='bold', pad=15)

plt.xlabel('Кількість процесів, од.', fontsize=12)
plt.ylabel('Коефіцієнт прискорення, S', fontsize=12)

plt.xticks(processes) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Обсяг даних", fontsize=10, title_fontsize=11)

plt.tight_layout()

plt.savefig('figure_5_2_all_speedups.png', dpi=300)
plt.show()

print("Графік 'figure_5_2_all_speedups.png' успішно згенерований.")

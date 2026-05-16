import pandas as pd
import matplotlib.pyplot as plt
import os

output_dir = 'graphs/results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'results', 'benchmark_database_results.csv'))
df = pd.read_csv(file_path)

df['DB_Size_Files'] = df['DB_Size_Files'] + 1

plt.rcParams.update({'font.size': 11})
plt.figure(figsize=(10, 6))

sizes = sorted(df['DB_Size_Files'].unique())
processes = sorted(df['Processes'].unique())

for s in sizes:
    subset = df[df['DB_Size_Files'] == s].sort_values('Processes')
    words = subset['Total_Words'].iloc[0]
    label = f'N = {s} файлів ({words:,} слів)'.replace(',', ' ')
    plt.plot(subset['Processes'], subset['Speedup'], marker='o', linewidth=2, label=label)

plt.title('Залежність прискорення від кількості процесів', 
          fontsize=14, fontweight='bold', pad=15)

plt.xlabel('Кількість процесів, од.', fontsize=12)
plt.ylabel('Коефіцієнт прискорення, S', fontsize=12)

plt.xticks(processes) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Обсяг бази даних", fontsize=10, title_fontsize=11)

plt.tight_layout()
save_path = os.path.join(output_dir, '5_3_all_speedups.png')
plt.savefig(save_path, dpi=300)
plt.show()

print("✅ Графік прискорення '5_3_all_speedups.png' успішно згенерований.")
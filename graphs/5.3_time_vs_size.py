import pandas as pd
import matplotlib.pyplot as plt
import os

output_dir = 'graphs/results'
os.makedirs(output_dir, exist_ok=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'results', 'benchmark_database_results.csv'))
df = pd.read_csv(file_path)

df['DB_Size_Files'] = df['DB_Size_Files'] + 1

plt.rcParams.update({'font.size': 11}) 
plt.figure(figsize=(10, 6))

processes = sorted(df['Processes'].unique())

for p in processes:
    subset = df[df['Processes'] == p].sort_values('DB_Size_Files')
    label = f'Послідовно (P=1)' if p == 1 else f'Паралельно (P={p})'
    plt.plot(subset['DB_Size_Files'], subset['Avg_Time'], marker='o', label=label, linewidth=2)

plt.title('Залежність часу виконання від обсягу вхідних даних', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Обсяг бази даних (кількість документів)', fontsize=12) 
plt.ylabel('Час виконання, сек', fontsize=12) 

sizes = sorted(df['DB_Size_Files'].unique())
plt.xticks(sizes)

plt.legend(title="Конфігурація", fontsize=10) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

save_path = os.path.join(output_dir, '5_3_time_vs_size.png')
plt.savefig(save_path, dpi=300)
plt.show()

print("✅ Графік успішно згенерований.")
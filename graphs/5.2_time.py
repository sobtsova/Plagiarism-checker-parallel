import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv('benchmark_results.csv')

plt.rcParams.update({'font.size': 11}) 
plt.figure(figsize=(10, 6))
processes = sorted(df['Processes'].unique())

for p in processes:
    subset = df[df['Processes'] == p].sort_values('Size_Words')
    label = f'Послідовно (P=1)' if p == 1 else f'Паралельно (P={p})'
    plt.plot(subset['Size_Words'], subset['Avg_Time'], marker='o', label=label, linewidth=2)

plt.title('Залежність часу виконання від обсягу вхідних даних', fontsize=14, fontweight='bold')
plt.xlabel('Обсяг даних, слів', fontsize=12) 
plt.ylabel('Час виконання, сек', fontsize=12) 

plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.legend(fontsize=10) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('time_vs_size.png', dpi=300)
plt.show()

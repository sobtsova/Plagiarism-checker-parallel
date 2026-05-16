import pandas as pd
import matplotlib.pyplot as plt
import os

output_dir = 'graphs/results'
os.makedirs(output_dir, exist_ok=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'results', 'benchmark_k_results.csv'))
df = pd.read_csv(file_path)

plt.rcParams.update({'font.size': 11}) 
plt.figure(figsize=(10, 6))

plt.plot(df['k'], df['Seq_Time'], marker='o', label='Послідовно (P=1)', linewidth=2)
plt.plot(df['k'], df['Par_Time'], marker='o', label='Паралельно (P=4)', linewidth=2)

plt.title('Залежність часу виконання від довжини шингла', fontsize=14, fontweight='bold')
plt.xlabel('Довжина шингла, слів', fontsize=12) 
plt.ylabel('Час виконання, сек', fontsize=12) 

plt.xticks(df['k'])

plt.legend(fontsize=10) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
save_path = os.path.join(output_dir, '5_4_time_vs_k.png')
plt.savefig(save_path, dpi=300)
plt.show()
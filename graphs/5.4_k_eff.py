import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('shingle_k_results.csv')

plt.rcParams.update({'font.size': 11}) 
fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#1f77b4'
ax1.set_xlabel('Довжина шингла, слів', fontsize=12)
ax1.set_ylabel('Схожість текстів, %', color=color1, fontsize=12)
line1 = ax1.plot(df['k'], df['Similarity'], marker='o', color=color1, linewidth=2, label='Схожість (%)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.7)

ax2 = ax1.twinx()  
color2 = '#d62728'
ax2.set_ylabel('Коефіцієнт прискорення, S', color=color2, fontsize=12)
line2 = ax2.plot(df['k'], df['Speedup'], marker='s', color=color2, linewidth=2, label='Прискорення (S)')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Вплив довжини шингла на чутливість та прискорення алгоритму', fontsize=14, fontweight='bold')
ax1.set_xticks(df['k'])

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', fontsize=10)

fig.tight_layout()
plt.savefig('figure_5_3_k_effect.png', dpi=300)
plt.show()
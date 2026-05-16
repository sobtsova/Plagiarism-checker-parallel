import matplotlib.pyplot as plt
import os

output_dir = 'graphs/results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

documents = [25, 50, 125, 250, 500] 
time_taken = [1.165258, 2.312446, 5.837190, 11.674382, 23.443265]

plt.figure(figsize=(10, 6))
plt.plot(documents, time_taken, marker='o', color='royalblue', linewidth=2, label='Послідовний алгоритм')

plt.xlabel('Кількість документів у базі (шт.)', fontsize=12) 
plt.ylabel('Час виконання (сек.)', fontsize=12)
plt.title('Залежність часу обробки від розміру бази даних', fontsize=14)

plt.text(500, 23.5, ' (10 млн слів)', fontsize=10, verticalalignment='bottom', horizontalalignment='right')

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.ticklabel_format(style='plain', axis='x')

plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

save_path = os.path.join(output_dir, '2_4_results.png')
plt.savefig(save_path, dpi=300)

print(f"✅ Графік успішно збережено у файл: {save_path}")
plt.show()

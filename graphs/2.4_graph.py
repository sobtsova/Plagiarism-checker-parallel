import matplotlib.pyplot as plt

words = [100000, 500000, 1000000, 2500000, 5000000, 10000000]
time_taken = [0.208500, 1.078842, 2.215151, 5.651253, 11.504344, 23.305507]

plt.figure(figsize=(10, 6))

plt.plot(words, time_taken, marker='o', linestyle='-', color='royalblue', 
         linewidth=2, label='Послідовний алгоритм')

plt.xlabel('Кількість слів, шт.', fontsize=12) 
plt.ylabel('Час виконання, сек.', fontsize=12)

plt.title('Залежність часу обробки тексту від кількості даних', fontsize=14)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.ticklabel_format(style='plain', axis='x')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('performance_plot_final.png', dpi=300)
plt.show()

import matplotlib.pyplot as plt

rates = [
    (0, 10000000, 15)
]

groups = ['0 - 10000000']

costs = [15]

plt.figure(figsize=(4, 6))

bars = plt.bar(groups, costs, color="#fe7f0e")

plt.xlabel('SBU tier')
plt.ylabel('Cost per 1000 SBU (EUR)')
plt.title('Snellius costs')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, round(yval, 2), ha='center', va='bottom', fontsize=9)

plt.ylim(12, 17)
plt.savefig('plot.png', dpi=300)


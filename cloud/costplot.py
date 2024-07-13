import matplotlib.pyplot as plt

rates = [
    (0, 80000, 36.70),      
    (80000, 800000, 34.07), 
    (800000, 8000000, 31.45),
    (8000000, float('inf'), 28.83)
]

rates_snellius = [(0, 10000000, 15)]

groups = ['0 - 80k', '80k - 800k', '800k - 8M', '> 8M']

costs = [rate[2] for rate in rates]
cost_snellius = [rate[2] for rate in rates_snellius]

plt.figure(figsize=(10, 6))

bars = plt.bar(groups, costs)
bars = list(bars) + list(plt.bar('0 - 10M', cost_snellius, color="#fe7f0e"))

plt.xlabel('Pricing Tier')
plt.ylabel('Cost per 1000 core-hours/SBU (EUR)')
plt.title('HPC Cloud vs Snellius costs')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, round(yval, 2), ha='center', va='bottom', fontsize=9)



plt.ylim(12, 38)
plt.savefig('plot.pdf')


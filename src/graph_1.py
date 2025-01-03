import matplotlib.pyplot as plt

init_group_payoff = 10
z_values = [0.01, 0.1, 0.5, 1, 100]
colors_value = ["orange", "blue", "red", "green", "brown"]  # Orange, Blue, Red, Green, Brown

for z, color in zip(z_values, colors_value):
    print(f"Run z : {z}")
    payoff_differences = [i * 0.25 for i in range(-4 * init_group_payoff, 4 * init_group_payoff)]

    G_i = [init_group_payoff] * len(payoff_differences)
    G_j = [init_group_payoff + payoff_differences[i] for i in range(len(payoff_differences))]

    winning_proba = [
        1 - (G_i[i] ** (1 / z) / (G_i[i] ** (1 / z) + G_j[i] ** (1 / z)))
        for i in range(len(payoff_differences))
    ]
    print(f"""Result:
        -G_i : {G_i}
        -payoff_differences : {payoff_differences}
        -G_j : {G_j}
        -winning_proba : {winning_proba}
    """)

    plt.plot(payoff_differences, winning_proba, color=color, linestyle='--', label=f"z = {z}")

plt.xlabel("Payoff Differences")
plt.ylabel("Winning Probability")
plt.title("Winning Probability vs Payoff Differences")
plt.legend()
plt.show()

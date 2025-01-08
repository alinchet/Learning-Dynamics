import matplotlib.pyplot as plt
import numpy as np

from src.classes.population import Population
from src.settings.constants import Strategy
from src.settings.config import *

# Figure 2: Fixation probability vs b/c
def fig2_fixation_vs_bc():
    bc_values = np.linspace(1.5, 5.0, 20)
    results = []
    for bc in bc_values:
        result = simulate_fixation_probabilities(n, m, q, α, κ, z, λ, w, bc)
        results.append(result)
    plt.plot(bc_values, results, label=f'n={n}, m={m}, q={q}, α={α}')
    plt.xlabel('b/c (Benefit-to-Cost Ratio)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs b/c')
    plt.legend()
    plt.grid(True)
    plt.savefig('fig2_fixation_vs_bc.png')


# Figure 3: Fixation probability vs λ for different b/c
def fig3_fixation_vs_lambda():
    λ_values = np.linspace(0.0, 1.0, 20)
    bc_values = [10, 5, 2]
    styles = ['-', '--', ':']
    for bc, style in zip(bc_values, styles):
        results = []
        for λ in λ_values:
            result = simulate_fixation_probabilities(n, m, q, α, κ, z, λ, w, bc)
            results.append(result)
        plt.plot(λ_values, results, style, label=f'b/c={bc}')
    plt.xlabel('λ (Migration Rate)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs λ')
    plt.legend()
    plt.grid(True)
    plt.savefig('fig3_fixation_vs_lambda.png')


# Figure 5: Fixation probability vs α
def fig5_fixation_vs_alpha():
    α_values = np.linspace(0.0, 1.0, 20)
    results = []
    for α_val in α_values:
        result = simulate_fixation_probabilities(n, m, q, α_val, κ, z, λ, w, bc_default)
        results.append(result)
    plt.plot(α_values, results, label=f'b/c={bc_default}')
    plt.xlabel('α (Ingroup Interaction Frequency)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs α')
    plt.legend()
    plt.grid(True)
    plt.savefig('fig5_fixation_vs_alpha.png')


# Figure 6: Fixation probability vs b/c with fixed κ, z
def fig6_fixation_vs_bc_fixed_kappa_z():
    bc_values = np.linspace(1.5, 5.0, 20)
    results = []
    for bc in bc_values:
        result = simulate_fixation_probabilities(n, m, q, α, κ, z, λ, w, bc)
        results.append(result)
    plt.plot(bc_values, results, label=f'κ={κ}, z={z}')
    plt.xlabel('b/c (Benefit-to-Cost Ratio)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs b/c (fixed κ, z)')
    plt.legend()
    plt.grid(True)
    plt.savefig('fig6_fixation_vs_bc_fixed_kappa_z.png')


# Figure 7: Fixation probability vs λ for different b/c (same as Fig. 3)
def fig7_fixation_vs_lambda():
    fig3_fixation_vs_lambda()  # Reuse logic from Fig. 3
    plt.title('Fixation Probability vs λ (Different b/c)')


# Figure 11: Fixation probability vs z
def fig11_fixation_vs_z():
    z_values = np.linspace(0.0, 1.0, 20)
    results = []
    for z_val in z_values:
        result = simulate_fixation_probabilities(n, m, q, α, κ, z_val, λ, w, bc_default)
        results.append(result)
    plt.plot(z_values, results, label=f'b/c={bc_default}')
    plt.xlabel('z (Winning Probability Steepness)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs z')
    plt.legend()
    plt.grid(True)
    plt.savefig('fig11_fixation_vs_z.png')


# Run all simulations and save figures
def main():
    fig2_fixation_vs_bc()
    fig3_fixation_vs_lambda()
    fig5_fixation_vs_alpha()
    fig6_fixation_vs_bc_fixed_kappa_z()
    fig7_fixation_vs_lambda()
    fig11_fixation_vs_z()
    print("Simulation complete. Results saved as PNG files.")


if __name__ == "__main__":
    main()
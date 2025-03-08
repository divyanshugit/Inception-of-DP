import random
import math
import matplotlib.pyplot as plt
import numpy as np


def generate_synthetic_ages(n=1000, age_min=20, age_max=60):
    """Generate synthetic employee age data uniformly distributed between given age limits."""
    data = [random.uniform(age_min, age_max) for _ in range(n)]
    return data


def laplace_mechanism(true_value, sensitivity, epsilon):
    """Apply the Laplace Mechanism to add noise to a numerical query result."""
    scale = sensitivity / epsilon
    u = random.uniform(-0.5, 0.5)
    noise = -scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))
    return true_value + noise


def get_privacy_description(epsilon):
    """Return a description of the privacy level based on epsilon value."""
    if epsilon <= 0.1:
        return "Strong Privacy (high noise)"
    elif epsilon <= 1.0:
        return "Moderate Privacy"
    else:
        return "Weaker Privacy (low noise)"


def demonstrate_laplace_mechanism_on_ages(n=1000, epsilon=1.0, num_trials=1000):
    """Generate synthetic employee age data and apply the Laplace mechanism with visualization."""
    data = generate_synthetic_ages(n)
    true_mean_age = sum(data) / len(data)
    sensitivity = (60 - 20) / n  # Max possible age range divided by dataset size
    privacy_desc = get_privacy_description(epsilon)

    # Generate multiple noisy means
    noisy_means = [
        laplace_mechanism(true_mean_age, sensitivity, epsilon)
        for _ in range(num_trials)
    ]

    # Calculate error statistics
    errors = [abs(noisy - true_mean_age) for noisy in noisy_means]
    mean_error = np.mean(errors)
    std_error = np.std(errors)

    # Create visualization
    fig = plt.figure(figsize=(15, 6))

    # Plot 1: Distribution of noisy means
    plt.subplot(1, 2, 1)
    plt.hist(
        noisy_means, bins=50, alpha=0.7, color="blue", label="Noisy Means", density=True
    )
    plt.axvline(
        true_mean_age, color="red", linestyle="dashed", linewidth=2, label="True Mean"
    )

    # Add theoretical Laplace distribution
    x = np.linspace(min(noisy_means), max(noisy_means), 100)
    scale = sensitivity / epsilon
    laplace_pdf = [
        1 / (2 * scale) * math.exp(-abs(xi - true_mean_age) / scale) for xi in x
    ]
    plt.plot(x, laplace_pdf, "g--", label="Theoretical Laplace", alpha=0.7)

    plt.xlabel("Age")
    plt.ylabel("Density")
    plt.title(f"Distribution of Noisy Means\nε={epsilon} ({privacy_desc})")
    plt.legend()

    # Plot 2: Error distribution
    plt.subplot(1, 2, 2)
    plt.hist(
        errors,
        bins=50,
        alpha=0.7,
        color="purple",
        label="Absolute Errors",
        density=True,
    )
    plt.axvline(
        mean_error,
        color="red",
        linestyle="dashed",
        linewidth=2,
        label=f"Mean Error: {mean_error:.2f}",
    )

    # Add error statistics
    plt.text(
        0.98,
        0.95,
        f"Mean Error: {mean_error:.2f}\nStd Error: {std_error:.2f}",
        transform=plt.gca().transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.8),
    )

    plt.xlabel("Absolute Error")
    plt.ylabel("Density")
    plt.title("Error Distribution")
    plt.legend()

    plt.tight_layout()
    return fig


if __name__ == "__main__":
    print("Demonstrating Laplace Mechanism with different privacy levels:")
    print("- ε=0.1: Strong privacy (high noise)")
    print("- ε=1.0: Moderate privacy")
    print("- ε=2.0: Weaker privacy (low noise)\n")

    for eps in [0.1, 1.0, 2.0]:
        print(f"\nRunning with ε={eps} ({get_privacy_description(eps)})")
        fig = demonstrate_laplace_mechanism_on_ages(n=1000, epsilon=eps)
        plt.show()

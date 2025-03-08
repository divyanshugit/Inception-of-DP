import math
import random
import matplotlib.pyplot as plt
import numpy as np


def exponential_mechanism(choices, utilities, epsilon):
    """Apply the Exponential Mechanism to select an option based on utility scores."""
    scaled_utilities = [u / max(utilities) for u in utilities]

    exp_weights = [math.exp((epsilon * u) / 2) for u in scaled_utilities]
    total_weight = sum(exp_weights)
    probabilities = [w / total_weight for w in exp_weights]

    return random.choices(choices, probabilities)[0], probabilities


def get_privacy_description(epsilon):
    """Return a description of the privacy level based on epsilon value."""
    if epsilon <= 0.1:
        return "Strong Privacy (more uniform distribution)"
    elif epsilon <= 1.0:
        return "Moderate Privacy"
    else:
        return "Weaker Privacy (closer to original distribution)"


def demonstrate_exponential_mechanism_with_visualization(epsilon=1.0, num_trials=1000):
    """
    Demonstrate the Exponential Mechanism with visualization.

    Privacy levels:
    - ε=0.1: Strong privacy (more uniform distribution)
    - ε=1.0: Moderate privacy
    - ε=2.0: Weaker privacy (closer to original distribution)
    """
    choices = ["Free Lunch", "Gym Membership", "Extra Paid Leave"]
    votes = [120, 80, 60]  # Example vote counts

    privacy_desc = get_privacy_description(epsilon)

    # Run multiple trials
    results = []
    _, probabilities = exponential_mechanism(choices, votes, epsilon)

    for _ in range(num_trials):
        selected, _ = exponential_mechanism(choices, votes, epsilon)
        results.append(selected)

    # Create visualization
    plt.figure(figsize=(15, 6))

    # Plot 1: Theoretical probabilities
    plt.subplot(1, 2, 1)
    bars = plt.bar(choices, probabilities)
    plt.title(f"Theoretical Selection Probabilities\nε={epsilon} ({privacy_desc})")
    plt.ylabel("Probability")
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom",
        )
    plt.ylim(0, max(probabilities) * 1.2)

    # Plot 2: Empirical frequencies
    plt.subplot(1, 2, 2)
    counts = [results.count(choice) for choice in choices]
    empirical_probs = [count / num_trials for count in counts]
    bars = plt.bar(choices, empirical_probs)
    plt.title(f"Empirical Frequencies\n({num_trials} trials)")
    plt.ylabel("Frequency")
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom",
        )
    plt.ylim(0, max(empirical_probs) * 1.2)

    plt.tight_layout()
    plt.show()

    # Print original vote distribution
    total_votes = sum(votes)
    print(f"\nResults for ε={epsilon} ({privacy_desc}):")
    print("Original Vote Distribution:")
    for choice, vote in zip(choices, votes):
        print(f"{choice}: {vote} votes ({vote/total_votes:.3f})")


if __name__ == "__main__":
    print("Privacy Levels in Exponential Mechanism:")
    print("- ε=0.1: Strong privacy (more uniform distribution)")
    print("- ε=1.0: Moderate privacy")
    print("- ε=2.0: Weaker privacy (closer to original distribution)\n")

    for eps in [0.1, 1.0, 2.0]:
        demonstrate_exponential_mechanism_with_visualization(
            epsilon=eps, num_trials=1000
        )

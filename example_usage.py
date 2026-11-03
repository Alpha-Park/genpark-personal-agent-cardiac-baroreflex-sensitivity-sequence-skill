"""
Example Usage: Cardiac Baroreflex Sensitivity (BRS) Sequence Technique.
Demonstrates zero-dependency calculation of spontaneous BRS gain from Up/Up and Down/Down sequences, and cardiovagal tone scoring.
"""

from client import CardiacBaroreflexSensitivityClient


def main():
    client = CardiacBaroreflexSensitivityClient()
    print("=== Cardiac Baroreflex Sensitivity (BRS) Sequence Demo ===")

    # Test Case 1: Healthy vigorous cardiovagal baroreflex buffering
    up_slopes = [14.5, 16.2, 13.8, 15.1, 14.9]
    down_slopes = [13.2, 14.8, 15.6, 12.9, 14.1]
    res1 = client.evaluate_brs_sequences(
        up_sequences_slopes=up_slopes,
        down_sequences_slopes=down_slopes,
        mean_sbp_mmhg=118.0,
        mean_rr_ms=865.0
    )
    print("\nTest Case 1: Robust Cardiovagal BRS Buffering")
    print(f"  Up Sequences: {res1['up_sequences_count']} (Mean: {res1['up_mean_slope_ms_per_mmhg']} ms/mmHg)")
    print(f"  Down Sequences: {res1['down_sequences_count']} (Mean: {res1['down_mean_slope_ms_per_mmhg']} ms/mmHg)")
    print(f"  Overall Mean BRS: {res1['mean_brs_ms_per_mmhg']} ms/mmHg (Total {res1['total_sequences_count']} sequences)")
    print(f"  Baroreflex Score: {res1['baroreflex_autonomic_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Physiological Interpretation: {res1['physiological_interpretation']}")
    print(f"  Actionable Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Blunted baroreflex sensitivity (autonomic failure / arterial stiffening)
    res2 = client.evaluate_brs_sequences(
        up_sequences_slopes=[4.5, 5.2, 4.8],
        down_sequences_slopes=[4.1, 4.9],
        mean_sbp_mmhg=138.0,
        mean_rr_ms=720.0
    )
    print("\nTest Case 2: Depressed Baroreflex Sensitivity Pattern")
    print(f"  Mean BRS: {res2['mean_brs_ms_per_mmhg']} ms/mmHg")
    print(f"  Baroreflex Score: {res2['baroreflex_autonomic_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Actionable Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()

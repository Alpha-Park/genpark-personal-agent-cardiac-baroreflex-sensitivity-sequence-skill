"""
Cardiac Baroreflex Sensitivity (BRS) & Sequence Technique Engine.
Provides deterministic, zero-dependency modeling of spontaneous beat-to-beat systolic blood pressure (SBP)
and RR-interval ramp sequences (Up/Up, Down/Down), baroreceptor gain (ms/mmHg), and cardiovagal autonomic tone.
"""

from typing import Dict, Any, List, Optional


class CardiacBaroreflexSensitivityClient:
    """
    Deterministic client for calculating spontaneous Baroreflex Sensitivity (BRS) via the sequence method.
    Assesses carotid sinus and aortic arch baroreceptor gain, parasympathetic vagal buffering,
    cardiac autonomic balance, and vulnerability to orthostatic syncope.
    """

    def __init__(self):
        pass

    def evaluate_brs_sequences(
        self,
        up_sequences_slopes: List[float],
        down_sequences_slopes: List[float],
        mean_sbp_mmhg: float = 120.0,
        mean_rr_ms: float = 850.0
    ) -> Dict[str, Any]:
        """
        Calculates mean BRS gain from Up/Up and Down/Down sequences.
        Normative values for spontaneous resting BRS:
        - Mean BRS: 10.0 - 25.0 ms/mmHg
        - Borderline BRS: 6.0 - 9.9 ms/mmHg
        - Depressed / Pathological BRS: < 6.0 ms/mmHg (blunted cardiovagal buffering)
        """
        all_slopes = up_sequences_slopes + down_sequences_slopes
        if not all_slopes:
            return {"error": "At least one valid sequence slope must be provided"}
        if any(s <= 0 for s in all_slopes):
            return {"error": "Sequence slopes (delta RR / delta SBP) must be positive"}

        up_mean = round(sum(up_sequences_slopes) / len(up_sequences_slopes), 2) if up_sequences_slopes else None
        down_mean = round(sum(down_sequences_slopes) / len(down_sequences_slopes), 2) if down_sequences_slopes else None

        mean_brs_ms_per_mmhg = round(sum(all_slopes) / len(all_slopes), 2)
        total_sequences = len(all_slopes)

        # Baroreflex Autonomic Resilience Score (0 - 100)
        score = 80.0
        if mean_brs_ms_per_mmhg >= 14.0:
            score += 15.0
        elif mean_brs_ms_per_mmhg >= 10.0:
            score += 8.0
        elif mean_brs_ms_per_mmhg < 4.5:
            score -= 35.0  # Profound baroreflex failure
        elif mean_brs_ms_per_mmhg < 7.0:
            score -= 20.0
        elif mean_brs_ms_per_mmhg < 10.0:
            score -= 8.0

        if total_sequences >= 10:
            score += 5.0
        elif total_sequences < 4:
            score -= 10.0  # Low sequence frequency

        brs_score = round(min(100.0, max(5.0, score)), 1)

        if brs_score >= 85.0 and mean_brs_ms_per_mmhg >= 11.0:
            tier = "OPTIMAL_CARDIOVAGAL_BAROREFLEX_SENSITIVITY"
            interp = f"Robust baroreflex sensitivity ({mean_brs_ms_per_mmhg} ms/mmHg, {total_sequences} sequences); rapid vagal heart rate modulation against blood pressure swings."
            guidance = "Superior cardiovascular autonomic adaptability. Excellent defense against orthostatic hypotension and stress-induced hypertensive spikes."
        elif mean_brs_ms_per_mmhg < 6.5:
            tier = "DEPRESSED_BAROREFLEX_SENSITIVITY"
            interp = f"Severely blunted baroreceptor responsiveness ({mean_brs_ms_per_mmhg} ms/mmHg < 7.0 ms/mmHg); reflects loss of cardiovagal control and arterial compliance stiffening."
            guidance = "Attenuated vagal buffering. Practice slow resonant breathing (0.1 Hz / 6 breaths/min) to stimulate arterial baroreceptors; avoid rapid unassisted standing."
        else:
            tier = "MODERATE_BARORECEPTOR_GAIN"
            interp = f"Adequate baroreflex sensitivity ({mean_brs_ms_per_mmhg} ms/mmHg); moderate autonomic compensation."
            guidance = "Maintain cardiorespiratory fitness and adequate electrolyte hydration to preserve baroreflex gain."

        return {
            "mean_brs_ms_per_mmhg": mean_brs_ms_per_mmhg,
            "up_sequences_count": len(up_sequences_slopes),
            "up_mean_slope_ms_per_mmhg": up_mean,
            "down_sequences_count": len(down_sequences_slopes),
            "down_mean_slope_ms_per_mmhg": down_mean,
            "total_sequences_count": total_sequences,
            "mean_sbp_mmhg": mean_sbp_mmhg,
            "mean_rr_ms": mean_rr_ms,
            "baroreflex_autonomic_score": brs_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }

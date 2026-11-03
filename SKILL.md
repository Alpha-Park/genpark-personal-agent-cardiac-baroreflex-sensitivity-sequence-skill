---
name: genpark-personal-agent-cardiac-baroreflex-sensitivity-sequence-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for calculating spontaneous Cardiac Baroreflex Sensitivity (BRS in ms/mmHg) via beat-to-beat sequence analysis, cardiovagal tone, and autonomic resilience.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Cardiac Baroreflex Sensitivity (BRS) Sequence Skill

A sovereign personal agent capability for evaluating beat-to-beat arterial baroreceptor gain, parasympathetic cardiovagal buffering, spontaneous systolic blood pressure / RR-interval ramp sequences, and orthostatic tolerance.

## Core Capabilities
- **Bertinieri Sequence Technique**: Identifies spontaneous ramps of $\ge 3$ consecutive cardiac cycles where systolic pressure and RR intervals co-vary linearly ($r \ge 0.85$).
- **Up/Up and Down/Down Gain Separation**: Computes separate baroreceptor buffering sensitivities for hypertensive ($Up/Up$) and hypotensive ($Down/Down$) blood pressure deviations.
- **Cardiovagal Autonomic Health Scoring**: Quantifies overall mean BRS gain ($10.0 - 25.0\text{ ms/mmHg}$), identifying blunted autonomic buffering ($< 6.5\text{ ms/mmHg}$).
- **Resonant Breathing Coaching**: Prescribes 0.1 Hz slow paced breathing protocols (6 breaths/min) to entrain Mayer waves and amplify baroreflex gain.

## Fast Invocation
```python
from client import CardiacBaroreflexSensitivityClient

client = CardiacBaroreflexSensitivityClient()
res = client.evaluate_brs_sequences(
    up_sequences_slopes=[14.5, 16.2, 13.8],
    down_sequences_slopes=[13.2, 14.8, 15.6]
)
print("Mean BRS:", res["mean_brs_ms_per_mmhg"], "ms/mmHg")
print("Baroreflex Score:", res["baroreflex_autonomic_score"], "/ 100")
```

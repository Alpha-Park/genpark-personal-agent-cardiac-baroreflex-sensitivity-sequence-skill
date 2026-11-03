# Cardiac Baroreflex Sensitivity (BRS) Sequence Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of spontaneous Cardiac Baroreflex Sensitivity (BRS), beat-to-beat sequence analysis, cardiovagal tone, and autonomic resilience.

```mermaid
flowchart TD
    ContinuousBP["Beat-to-Beat Systolic Blood Pressure (SBP) Stream"] & ContinuousECG["Continuous ECG RR-Interval Stream"] --> SequenceDetection["Sequence Extraction: >= 3 Consecutive Beats (r >= 0.85)"]
    SequenceDetection --> UpUp["Up/Up Sequences (Delta SBP > 0, Delta RR > 0)"]
    SequenceDetection --> DownDown["Down/Down Sequences (Delta SBP < 0, Delta RR < 0)"]
    UpUp & DownDown --> LinearSlope["Regression Slopes (Delta RR / Delta SBP in ms/mmHg)"]
    LinearSlope --> BRS_Mean["Mean Baroreflex Sensitivity (BRS) & Autonomic Score"]
    BRS_Mean --> Agent["OpenClaw / Hermes Personal Agent Resonant Pacing"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Cardiovascular Autonomic Standards**: Implements validated Bertinieri sequence method equations for spontaneous arterial baroreflex gain.
- **Cardiovagal Buffering & Orthostatic Screening**: Detects early loss of parasympathetic blood pressure regulation and syncope vulnerability.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import CardiacBaroreflexSensitivityClient

client = CardiacBaroreflexSensitivityClient()
result = client.evaluate_brs_sequences(
    up_sequences_slopes=[14.5, 16.2, 13.8],
    down_sequences_slopes=[13.2, 14.8, 15.6]
)
print("Mean BRS:", result["mean_brs_ms_per_mmhg"], "ms/mmHg")
print("Baroreflex Score:", result["baroreflex_autonomic_score"])
print("Classification:", result["classification"])
```

## License
Apache-2.0

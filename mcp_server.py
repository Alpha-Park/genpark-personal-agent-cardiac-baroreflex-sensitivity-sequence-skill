"""
MCP Server for Cardiac Baroreflex Sensitivity (BRS) Sequence Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating spontaneous BRS sequence slopes, vagal buffering, and autonomic scores.
"""

import sys
import json
from typing import Dict, Any, List
from client import CardiacBaroreflexSensitivityClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_brs_sequences",
                "description": "Calculates spontaneous Cardiac Baroreflex Sensitivity (BRS in ms/mmHg) using Up/Up and Down/Down sequences, cardiovagal tone, and autonomic resilience score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "up_sequences_slopes": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of regression slopes (delta RR / delta SBP) for Up/Up sequences in ms/mmHg (e.g. [14.2, 16.5, 12.8])."
                        },
                        "down_sequences_slopes": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of regression slopes for Down/Down sequences in ms/mmHg (e.g. [13.5, 15.1, 11.9])."
                        },
                        "mean_sbp_mmhg": {
                            "type": "number",
                            "description": "Mean systolic blood pressure in mmHg (default: 120.0 mmHg).",
                            "default": 120.0
                        },
                        "mean_rr_ms": {
                            "type": "number",
                            "description": "Mean RR interval in milliseconds (default: 850.0 ms).",
                            "default": 850.0
                        }
                    },
                    "required": ["up_sequences_slopes", "down_sequences_slopes"]
                }
            }
        ]
    }


def handle_request(client: CardiacBaroreflexSensitivityClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_brs_sequences":
            up_slopes = [float(x) for x in args.get("up_sequences_slopes", [14.0, 15.0])]
            down_slopes = [float(x) for x in args.get("down_sequences_slopes", [13.0, 14.5])]
            res = client.evaluate_brs_sequences(
                up_sequences_slopes=up_slopes,
                down_sequences_slopes=down_slopes,
                mean_sbp_mmhg=float(args.get("mean_sbp_mmhg", 120.0)),
                mean_rr_ms=float(args.get("mean_rr_ms", 850.0))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {name}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": f"Invalid Request: Unsupported method {method}"
            }
        }


def main():
    client = CardiacBaroreflexSensitivityClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error or exception: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

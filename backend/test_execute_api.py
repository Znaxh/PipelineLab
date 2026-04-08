from pathlib import Path

import requests
import json

# Path to a sample PDF relative to repo root (create frontend/public/sample.pdf or edit this path)
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_SAMPLE = _REPO_ROOT / "frontend" / "public" / "sample.pdf"


def test_execute():
    url = "http://127.0.0.1:8000/api/v1/pipeline/execute"
    sample_path = _DEFAULT_SAMPLE
    payload = {
        "nodes": [
            {
                "id": "node_1",
                "type": "loader",
                "config": {"path": str(sample_path)},
            },
            {
                "id": "node_2",
                "type": "splitter",
                "config": {"windowSize": 1, "threshold": 0.5, "minChunkSize": 100}
            },
            {
                "id": "node_3",
                "type": "embedder",
                "config": {"provider": "local", "model": "all-MiniLM-L6-v2"}
            }
        ],
        "edges": [
            {"source": "node_1", "target": "node_2"},
            {"source": "node_2", "target": "node_3"}
        ]
    }
    
    print(f"Checking health at http://127.0.0.1:8000/api/v1/health...")
    try:
        h = requests.get("http://127.0.0.1:8000/api/v1/health")
        print(f"Health Status: {h.status_code}")
        print(f"Health Body: {h.json()}")
    except Exception as e:
        print(f"Health failed: {e}")

    print(f"Testing POST {url}...")
    try:
        r = requests.post(url, json=payload)
        print(f"Status Code: {r.status_code}")
        print(f"Response Body:")
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_execute()

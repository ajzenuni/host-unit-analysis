# Host Unit Analysis Script

## Overview

This Python script performs host unit analysis by querying specified endpoint, processing the data, and posting the results to another endpoint. It is designed to be run periodically using scheduling.

## Requirements

- Python 3.x
- Required Python packages (`requests`, `schedule`)

## Usage

Ensure you have Python installed on your system. Then, follow these steps to use the script:

1. Clone the repository or download the script file.
2. Install the required Python packages:
```bash
    pip install -r requirements.txt
```
3. Run the script with the following command:

Replace `managed_url`, `managed_api-token`, `saas_url`, and `saas_api-token` with the appropriate values. Here's what each argument represents:
- `managed_url`: URL for the managed endpoint.
- `managed_api-token`: API token for the managed endpoint (v2: Read Entities, v1: Access problem and event feed, metrics, and topology).
- `saas_url`: URL for the SaaS endpoint.
- `saas_api-token`: API token for the SaaS endpoint (v2: Ingest metrics).
```bash
    python host_unit_analysis.py managed_url managed_api-token saas_url saas_api-token
```


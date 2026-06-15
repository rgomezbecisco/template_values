# Template Values Scripts

Scripts to connect to a Cisco vManage instance and retrieve SDWAN device information and template values.

## Prerequisites

- Python 3.9+
- `catalystwan` and `openpyxl` Python modules installed
- Access to a Cisco vManage instance

## Setup

1. Install required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### devices.py

Retrieves device configuration data and exports it to CSV files:

```sh
python devices.py --VMANAGE_IP <vmanage_ip> --VMANAGE_USER <username> --VMANAGE_PASSWORD <password> [--VMANAGE_PORT <port>]
```

Example:

```sh
python devices.py --VMANAGE_IP 192.168.1.100 --VMANAGE_USER admin --VMANAGE_PASSWORD password123
```

This will:

- Connect to the vManage API
- Fetch device configuration data
- Save results to `devices.csv` in the current directory

### template_values_xl.py

Retrieves SDWAN templates and their device values, exporting to an Excel workbook with multiple sheets:

```sh
python template_values_xl.py --VMANAGE_IP <vmanage_ip> --VMANAGE_USER <username> --VMANAGE_PASSWORD <password> [--VMANAGE_PORT <port>]
```

Example:

```sh
python template_values_xl.py --VMANAGE_IP 192.168.1.100 --VMANAGE_USER admin --VMANAGE_PASSWORD password123
```

This will:

- Connect to the vManage API
- Fetch device info and template data
- Create a workbook with a Summary sheet and individual sheets per template
- Save to `template_values.xlsx` in the current directory

## Output

- `devices.csv`: List of edge devices (vedge) with configuration details

- `template_values.xlsx`: Excel workbook containing:
  - **Summary**: Overview of collected templates with device counts
  - **Per-template sheets**: Template values for each collected template

## Notes

- Both scripts filter edge devices (vedge) from the SDWAN network
- Credentials can be hardcoded in the script for testing, but CLI arguments are recommended for security
- `--VMANAGE_PORT` is optional and defaults to 443
- Make sure your vManage credentials are correct and the API is reachable

## Files

- [`devices.py`](devices.py): Retrieve device configuration data
- [`template_values_xl.py`](template_values_xl.py): Retrieve template values into Excel workbook

---

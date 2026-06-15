
import urllib3
import csv
from os import path
import os
from argparse import ArgumentParser
from catalystwan.session import create_manager_session
from datetime import datetime
import json
from pygments import highlight, lexers, formatters

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def tprint(message):
    """Print with timestamp prefix in format [HH:MM:SS DDMMYYYY]"""
    timestamp = datetime.now().strftime("[%H:%M:%S %d%m%Y]")
    print(f"{timestamp} {message}")


def pretty_print_dict_as_json(data):
    """Print dictionary as colored JSON format."""

    formatted_json = json.dumps(data, indent=4)
    colorful_json = highlight(
        formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
    )
     
    print(colorful_json)


def get_static_vmanage_credentials():

    # Use this variables to hardcode credentials - ONLY FOR TESTING PURPOSES
    MANAGER_IP = ""
    USERNAME = ""
    PASSWORD = ""
    PORT = ""

    parser = ArgumentParser(description="Obtain vManage credentials from CLI arguments")
    parser.add_argument("--VMANAGE_IP", required=False, default=MANAGER_IP, help="VMANAGE IP or Hostname")
    parser.add_argument("--VMANAGE_USER", required=False, default=USERNAME, help="VMANAGE Username")
    parser.add_argument("--VMANAGE_PASSWORD", required=False, default=PASSWORD, help="VMANAGE Password")
    parser.add_argument("--VMANAGE_PORT", default=PORT if PORT else 443, help="VMANAGE Port", type=int)

    args = parser.parse_args()


    return (
        args.VMANAGE_IP,
        args.VMANAGE_USER,
        args.VMANAGE_PASSWORD,
        args.VMANAGE_PORT,
    )


def get_vmanage_credentials():

    parser = ArgumentParser(description="Obtain vManage credentials from CLI arguments")
    parser.add_argument("--VMANAGE_IP", required=True, help="VMANAGE IP or Hostname")
    parser.add_argument("--VMANAGE_USER", required=True, help="VMANAGE Username")
    parser.add_argument("--VMANAGE_PASSWORD", required=True, help="VMANAGE Password")
    parser.add_argument("--VMANAGE_PORT", default="443", help="VMANAGE Port", type=int)

    args = parser.parse_args()

    return (
        args.VMANAGE_IP,
        args.VMANAGE_USER,
        args.VMANAGE_PASSWORD,
        args.VMANAGE_PORT,
    )


def get_device_health_data(session):

    endpoint = "/dataservice/health/devices?page_size=12000"

    try:
        response = session.get(endpoint)
        data = response.json()["devices"]

    except Exception as error:
        tprint(f"Failed to collect device config data: {error}")
        data = []

    return data


def get_device_config_data(session):

    endpoint = "dataservice/system/device/vedges"

    try:
        response = session.get(endpoint)
        data = response.json()["data"]

    except Exception as error:
        tprint(f"Failed to collect device config data: {error}")
        data = []

    return data


def save_data_to_csv(destination_file, data):

    if not data:
        tprint(f"No data to save for {destination_file}. Skipping CSV creation.")
        return

    headers = data[0].keys()
    data_table = [list(item.values()) for item in data]

    with open(destination_file, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(data_table)

    tprint(f"{destination_file} saved!")


def filter_device_info(health_data, config_data):

    filter_by = "device_type"
    filter_value = "vedge"

    all_edges_info = []

    for device in health_data:

        device_info = {}

        if device.get(filter_by) == filter_value and device.get("system_ip"):

            device_info["SystemIP"] = device.get("system_ip")
            device_info["Host-name"] = device.get("name")
            device_info["Reachability"] = device.get("reachability")
            device_info["Status"] = device.get("health")
            device_info["BfdSessionsUp"] = device.get("bfd_sessions_up")
            device_info["UUID"] = device.get("uuid")
            device_info["ControlConnections"] = device.get("control_connections_up")
            device_info["Version"] = device.get("software_version")
            device_info["Site-id"] = device.get("site_id")
            device_info["Site-Name"] = device.get("site_name")
            
            for n in config_data:

                if n.get("host-name") == device.get("name"):

                    device_info["TemplateName"] = n.get("template")
                    break

            all_edges_info.append(device_info)

    return all_edges_info


if __name__ == "__main__":

    
    url, username, password, port, = get_static_vmanage_credentials()
    if not all([url, username, password, port]):
        url, username, password, port, = get_vmanage_credentials()

    try:

        with create_manager_session(
            url=url,
            username=username,
            password=password,
            port=int(port),
        ) as session:

            if session:
                tprint("vManage Session created successfully!")

                config_data = get_device_config_data(session)
                health_data = get_device_health_data(session)
                all_edges_info = filter_device_info(health_data, config_data)

        tprint("Device info collected for {} devices".format(len(all_edges_info)))
        csv_file = "devices.csv"
        save_data_to_csv(csv_file, all_edges_info)

    except Exception as error:
        tprint(f"An error occurred: {error}")

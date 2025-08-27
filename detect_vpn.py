import requests
import pandas as pd

# Counters for true statuses
true_vpn_count = 0
true_hosting_status = 0
true_relay_count = 0

# Read the Excel file
xlsx_file_path = "ips.xlsx"
df = pd.read_excel(xlsx_file_path, sheet_name="Sheet1")

# Get the list of IP addresses
ip_addresses = df.iloc[:, 0].tolist()
ip_addresses_no_duplicates = list(set(ip_addresses))

# Output the number of IPs
print(f"The number of IPs in the list is: {len(ip_addresses)}")
print(f"The number of unique IPs in the list is: {len(ip_addresses_no_duplicates)}")

# Loop over unique IPs
for ip in ip_addresses_no_duplicates:
    # url = f"https://vpnapi.io/api/{ip}?key=b2bbdecaea634632b7f2504d8b45661a"
    # url = f"https://vpnapi.io/api/{ip}?key=5d087e5367ed478b862a011bbea7caf1"
    # url = f"https://vpnapi.io/api/{ip}?key=4571e8f474b94040b730b25aa1b18adf"
    # url = f"https://vpnapi.io/api/{ip}?key=158d6a312652474ba153f1cd735b270c"
    url = f"https://vpnapi.io/api/{ip}?key=7cbe42862e7744d6b2c15a37739b3352"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Check VPN, Hosting, and Relay statuses
            vpn_status = data.get("security", {}).get("vpn", False)
            hosting_status = data.get("security", {}).get("hosting", False)
            relay_status = data.get("security", {}).get("relay", False)

            # If any of the statuses are True, print the IP
            if vpn_status or hosting_status or relay_status:
                print(ip)
                if vpn_status:
                    true_vpn_count += 1
                if hosting_status:
                    true_hosting_status += 1
                if relay_status:
                    true_relay_count += 1

        else:
            print(f"Request failed for IP {ip} with status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing IP {ip}: {e}")

# Output the final counts
print(f"Total True VPN statuses: {true_vpn_count}")
print(f"Total True Hosting statuses: {true_hosting_status}")
print(f"Total True Relay statuses: {true_relay_count}")

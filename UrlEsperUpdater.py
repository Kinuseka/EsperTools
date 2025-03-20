import io
import requests
import time

block_list_hosts = ["https://github.com/hagezi/dns-blocklists/raw/refs/heads/main/share/facebook.txt", 
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/share/microsoft.txt", 
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/share/ultimate-known-issues.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/domains/native.huawei.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/domains/native.samsung.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.samsung.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/domains/native.tiktok.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/domains/native.vivo.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.huawei.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.huawei-onlydomains.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.winoffice-onlydomains.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.winoffice.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.tiktok.extended.txt",
                    "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/wildcard/native.tiktok.extended-onlydomains.txt"
                    #Add more blocklists here (only wildcards and domain, future esper versions might include regex)
                    ]
esper_url = "http://esper.com"
blocked_domains = []


def process_domains(domain_list):
    for line in domain_list:
        line = line.strip()
        if not line.startswith("#") and line:
            blocked_domains.append(line)

def process_hosts(block_list_hosts):
    for each in block_list_hosts:
        response = requests.get(each)
        fileObj = io.StringIO(response.text)
        process_domains(fileObj)

def fetch_blacklist(esper_url):
    response = requests.get(esper_url+"/blacklist.txt")
    blacklists = response.text.splitlines()
    blacklists = [line for line in blacklists if line] #Removes empty strings
    return blacklists

def update_list(esper_url):
    blacklists = fetch_blacklist(esper_url)
    errors = 0
    success = 0
    perc = 0.0
    for blocked in blocked_domains:
        if blocked in blacklists:
            print(f"[{blocked}] Ignored, already in list")
            success += 1
        else:
            try:
                response = requests.put(esper_url+f"/blacklist/{blocked}")
            except requests.exceptions.RequestException as e:
                print(f"[{blocked}] Error: {e}")
                errors += 1
            if response.status_code != 200:
                print(f"[{blocked}] Error: {response.content}")
                errors += 1
            else:
                print(f"[{blocked}] Added")
                success += 1
        perc = ((errors+success) / len(blocked_domains)) * 100
        print(f"\033[K[D:{success} F: {errors} T: {len(blocked_domains)}] {round(perc, 2)}%", end="\r")
if __name__ == "__main__":
    try:
        print("Fetching Blocklists")
        print(block_list_hosts)
        start = time.time()
        process_hosts(block_list_hosts)
        end = time.time()
        print(f"Loaded blocklists ({end-start})")
        print("Sending to Esper device")
        start = time.time()
        update_list(esper_url)
        end = time.time()
        print(f"Operation finished ({end-start})")
    except KeyboardInterrupt:
        print("Operation stopped (Keyboard interrupt)")
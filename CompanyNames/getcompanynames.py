import requests
import csv
import time

def get_first_google_result_title(domain):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": f"site:{domain}", "limit": "1"}
    
    headers = {
        "x-rapidapi-key": "f5099b8793msh9396441b8f28f11p122ca6jsn983a85f217d7",
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    try:
        result = response.json()
    except ValueError:
        return "Unable to fetch result"  # In case of JSON decoding issues 

    if result.get("results"):
        title = result["results"][0]["title"]
        return title
    else:
        return "No results found"

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()
    return domains

def append_to_csv(domain, title, csv_file_path):
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([domain, title])

domains_file_path = 'domains.txt'
output_csv_file_path = 'output.csv'

# Create the CSV file and write the header
with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Domain', 'Title'])

domains = read_domains_from_file(domains_file_path)

for domain in domains:
    start_time = time.time()  # Note the start time for rate limiting
    title = get_first_google_result_title(domain)
    append_to_csv(domain, title, output_csv_file_path)
    print(f"{domain}: {title}")
    elapsed_time = time.time() - start_time
    time_to_sleep = max(0, 0.25 - elapsed_time)  # Ensure we adhere to the rate limit
    time.sleep(time_to_sleep)

print(f"Results have been written to {output_csv_file_path}")
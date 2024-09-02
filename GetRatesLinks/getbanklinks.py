import requests
import csv
import time

def get_first_google_result_link(query):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": query, "limit": "1"}
    
    headers = {
        "x-rapidapi-key": "f5099b8793msh9396441b8f28f11p122ca6jsn983a85f217d7",
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    try:
        result = response.json()
    except ValueError:
        return query, "Unable to fetch result"  # In case of JSON decoding issues 

    if result.get("results") and "url" in result["results"][0]:
        link = result["results"][0]["url"]
        return query, link
    else:
        return query, "No results found"

def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read().splitlines()
    return queries

def append_to_csv(query, link, csv_file_path):
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([query, link])

queries_file_path = 'queries.txt'
output_csv_file_path = 'banklinks.csv'

# Create the CSV file and write the header
with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Search String', 'First Result Link'])

queries = read_queries_from_file(queries_file_path)

for query in queries:
    start_time = time.time()  # Note the start time for rate limiting
    query, link = get_first_google_result_link(query)
    append_to_csv(query, link, output_csv_file_path)
    print(f"{query}: {link}")
    elapsed_time = time.time() - start_time
    time_to_sleep = max(0, 0.25 - elapsed_time)  # Ensure we adhere to the rate limit
    time.sleep(time_to_sleep)

print(f"Results have been written to {output_csv_file_path}")
import requests
from bs4 import BeautifulSoup
import openai

# Add your API keys
RAPIDAPI_KEY = ''
RAPIDAPI_HOST = 'google-search74.p.rapidapi.com'
OPENAI_API_KEY = ''
# Function to search Google for CD offerings
def search_google(domain):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": f"site:{domain} share certificates of deposit", "limit": "3"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json().get('results', [])

# Function to scrape text content from a webpage
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

# Function to generate an overview and pros/cons using GPT-4
def generate_overview(text, bank_name):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify the GPT-4 model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Provide a brief one-paragraph overview and a list of pros and cons for the Certificate of Deposit offerings from {bank_name} based on the following information:\n\n{text}"}
        ],
        max_tokens=1000
    )
    return response['choices'][0]['message']['content'].strip()

# Function to read domains from a text file
def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Main function to process a list of bank domains and write results to a file
def main(domain_file, output_file):
    bank_domains = read_domains_from_file(domain_file)
    with open(output_file, 'w') as output:
        for domain in bank_domains:
            print(f"Processing {domain}...")
            search_results = search_google(domain)
            text_content = ''

            for result in search_results:
                url = result['url']
                print(f"Scraping {url}...")
                text_content += scrape_text_from_url(url)

            overview = generate_overview(text_content, domain)
            output.write(f"Overview for {domain}:\n{overview}\n\n")

if __name__ == "__main__":
    # Path to the file containing bank domains
    domain_file = "domains.txt"
    # Path to the output file
    output_file = "cd_overviews.txt"
    main(domain_file, output_file)

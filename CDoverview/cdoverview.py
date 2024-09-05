import requests
from bs4 import BeautifulSoup
import openai
import csv
from bs4.element import Comment
import os
import urllib.parse

# Add your API keys
RAPIDAPI_KEY = 'f5099b8793msh9396441b8f28f11p122ca6jsn983a85f217d7'
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

# Function to determine if an HTML element contains visible text
def is_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Function to scrape visible text content from a webpage
def scrape_visible_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    texts = soup.find_all(string=True)
    visible_texts = filter(is_visible, texts)
    return ' '.join(t.strip() for t in visible_texts if t.strip()), response.text

# Function to generate an overview and pros/cons using GPT-4
def generate_overview(text, bank_name):
    openai.api_key = OPENAI_API_KEY

    system_prompt = f"""
    Provide a brief one-paragraph overview, followed by a list of pros separated by pipes (`|`),
    and a list of cons separated by pipes (`|`) for the Certificate of Deposit offerings from
    {bank_name} based on the following information:\n\n{text}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "First Community Bank, established in 1983 in Alice, Texas, has grown to include branches in Kingsville, Portland, Padre Island, Premont, Rockport, and Victoria, with headquarters and a Home Loan Center in Corpus Christi. The bank provides a range of financial services, including competitive certificates of deposit (CDs). First Community Bank offers local expertise and personalized customer service to meet the financial needs of individuals and businesses in South Texas."},
        {"role": "user", "content": "Vision One Credit Union was founded in 1956 and has been dedicated to serving its members with personalized financial solutions for over six decades. As a not-for-profit financial cooperative, Vision One is committed to providing excellent service and competitive rates to help its members achieve their financial goals. With a focus on community involvement and member satisfaction, Vision One offers a wide range of products and services, including savings accounts, loans, and online banking options, all designed to meet the diverse needs of its membership base."},
        {"role": "user", "content": "California Bank & Trust (CB&T), established in 1952, has been providing financial services to individuals and businesses across California for nearly 70 years. As a division of Zions Bancorporation, N.A., CB&T manages more than $14 billion in loans and $15 billion in deposits through over 85 branches statewide. Among its diverse financial products, CB&T offers competitive certificates of deposit (CDs) with APY rates that are highly attractive in the current market."},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=4095
        )
        description = response['choices'][0]['message']['content'].strip()
        return description
    except Exception as e:
        return f"Failed to generate description for {bank_name}: {e}"

# Function to read domains from a text file
def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to split the overview into paragraph, pros, and cons
def split_overview(overview):
    parts = overview.split('\n', 1)
    paragraph = parts[0] if parts else ''

    pros = cons = ''
    if len(parts) > 1:
        pros_cons_parts = parts[1].split('Cons:', 1)
        if len(pros_cons_parts) == 2:
            pros = pros_cons_parts[0].replace('Pros:', '').strip().replace('|', ', ')
            cons = pros_cons_parts[1].strip().replace('|', ', ')
        else:
            cons = pros_cons_parts[0].strip()

    return paragraph, pros, cons

# Main function to process a list of bank domains and write results to a CSV file
def main(domain_file, output_file):
    bank_domains = read_domains_from_file(domain_file)
    output_dir = "output_html"
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Domain', 'Overview', 'Pros', 'Cons', 'URL 1', 'URL 2', 'URL 3'])

        for domain in bank_domains:
            print(f"Processing {domain}...")
            search_results = search_google(domain)
            text_content = ''
            urls = []

            for i, result in enumerate(search_results):
                url = result['url']
                print(f"Scraping {url}...")
                visible_text, html_content = scrape_visible_text(url)
                text_content += visible_text
                urls.append(url)

                # Extract domain name from URL for filename
                parsed_url = urllib.parse.urlparse(url)
                domain_name = parsed_url.netloc.replace('.', '_')

                # Write the scraped HTML to a file for auditing
                with open(os.path.join(output_dir, f"{domain_name}_{i + 1}.html"), 'w', encoding='utf-8') as file:
                    file.write(html_content)

            # Ensure we have 3 URLs even if there were fewer search results
            urls += [''] * (3 - len(urls))

            try:
                overview = generate_overview(text_content, domain)
                paragraph, pros, cons = split_overview(overview)
                writer.writerow([domain, paragraph, pros, cons, urls[0], urls[1], urls[2]])
            except Exception as e:
                print(f"Error processing {domain}: {e}")

if __name__ == "__main__":
    # Path to the file containing bank domains
    domain_file = "domains.txt"
    # Path to the output file
    output_file = "cd_overviews.csv"
    main(domain_file, output_file)

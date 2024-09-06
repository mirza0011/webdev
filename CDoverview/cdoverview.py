import requests
from bs4 import BeautifulSoup
import openai
import csv
from bs4.element import Comment
import os
import urllib.parse
from fake_useragent import UserAgent
import warnings

# Disable warnings about unverified HTTPS requests
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Add your API keys
RAPIDAPI_KEY = 'f5099b8793msh9396441b8f28f11p122ca6jsn983a85f217d7'
RAPIDAPI_HOST = 'google-search74.p.rapidapi.com'
OPENAI_API_KEY = ''

# Proxy settings
proxies = {
    "http": "http://flbVSD77PUMdUuZh:FHXcnnZPb9if3N8w@geo.iproyal.com:12321",
    "https": "http://flbVSD77PUMdUuZh:FHXcnnZPb9if3N8w@geo.iproyal.com:12321",
}

# Function to generate a fake user agent
def get_fake_user_agent():
    ua = UserAgent()
    return {'User-Agent': ua.random}

# Function to search Google for CD offerings
def search_google(domain):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": f"site:{domain} share certificates of deposit", "limit": "3"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    headers.update(get_fake_user_agent())  # Add fake user agent to headers
    response = requests.get(url, headers=headers, params=querystring, proxies=proxies, verify=False)
    return response.json().get('results', [])

# Function to determine if an HTML element contains visible text
def is_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Function to scrape visible text content from a webpage and capture the title
def scrape_visible_text(url):
    headers = get_fake_user_agent()  # Use the fake user agent
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    texts = soup.find_all(string=True)
    visible_texts = filter(is_visible, texts)
    return ' '.join(t.strip() for t in visible_texts if t.strip()), response.text

# Function to generate an overview and pros/cons using GPT-4o-mini
def generate_overview(text, bank_name):
    openai.api_key = OPENAI_API_KEY

    system_prompt = f"""
    You will be given text that describes the CD (Certificate of Deposit) offerings of {bank_name}. Please provide a one-paragraph overview of these offerings as well as the products' pros and cons. Separate the company overview and the pros and cons with a tilde (~) character. Separate the individual pros and cons with pipe characters as well.
    The information for {bank_name} is directly below and you will also find three example outputs in the first three user prompts:\n\n{text}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Landmark Credit Union offers a Certificate of Deposit (CD) program that gives account holders a way to invest their savings and see them grow steadily over time. With terms ranging from 3 months to 5 years, there's flexibility to suit varying financial goals and time frames. The minimum investment amount is just $500, and all CDs from Landmark are federally insured by the NCUA for up to $250,000 per account owner, ensuring that your funds are safe and protected. The dividend rates offered range from 0.50% APY for a 3-month term to 3.83% APY for terms ranging from 18 months to 5 years ~ Higher APY than regular savings account | Terms from 3 months to 5 years for flexibility | Federally insured up to $250,000 by NCUA | Low minimum deposit of $500 | Multiple CD terms yield higher returns ~ Penalty may apply for early withdrawal | Requires an upfront deposit of at least $500 | Locked in rate - can't take advantage if rates rise | Funds cannot be added to the CD after the initial deposit | Not suitable for short-term savings"},
        {"role": "user", "content": "Washington State Employees Credit Union (WSECU) offers Share Certificates also known as certificates that allow individuals to earn a higher Annual Percentage Yield (APY) than standard savings accounts, with their offering reaching up to 4.60% APY on a 7-month term. These certificates lock in a fixed rate for a future return and are excellent savings mechanisms for individuals seeking to save for significant expenditures or reach particular savings milestones. The value upon maturity can be determined the day the account opens, making it a reliable option for those seeking certainty in their investments. Penalties may apply for early withdrawal.~ Higher yield than most savings accounts | Certainty of return upon maturity | Variety of term lengths | Deposits insured up to $250,000 by the NCUA ~ Funds are locked until the maturity date, limiting access | Penalties may apply for early withdrawals | Cannot add funds to existing certificates, but multiple certificates can be opened | Not suitable for long-term goals as the yield may not compare well to long-term yields from the stock market."},
        {"role": "user", "content": "Connexus Credit Union offers a versatile selection of Certificate of Deposit (CD) options, designed to meet diverse financial goals. Their offerings range from regular CDs to money market CD accounts, with varying maturity terms and competitive rates. The financial institution features online availability and accessibility to make operations smoother and more convenient. ~ Competitive interest rates | Various maturity options (from 12 to 60 months) | High Yield CD accounts available | Access to accounts online | Regularly holds rewards programs | Federally insured by NCUA | No monthly service fees ~ Requires a minimum balance to open a CD account | Early withdrawal penalties | Lower APY for lower balance tiers | Lack of physical branches for face-to-face assistance | Rewards program not available for all CDs"}
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

# Function to split the overview, pros, and cons
def split_overview(overview):
    parts = overview.split('~', 2)
    paragraph = parts[0].strip() if parts else ''
    pros = parts[1].strip() if len(parts) > 1 else ''
    cons = parts[2].strip() if len(parts) > 2 else ''
    return paragraph, pros, cons

# Main function to process a list of bank domains and write results to a CSV file
def main(domain_file, output_file):
    bank_domains = read_domains_from_file(domain_file)
    output_dir = "output_html"
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Domain', 'Overview', 'Pros', 'Cons', 'URL 1', 'URL 2', 'URL 3', 'Title 1', 'Title 2', 'Title 3'])

        for domain in bank_domains:
            print(f"Processing {domain}...")
            search_results = search_google(domain)
            text_content = ''
            urls = []
            titles = []

            for result in search_results:
                url = result['url']
                title = result['title']
                print(f"Scraping {url}...")
                visible_text, html_content = scrape_visible_text(url)
                text_content += visible_text + " "
                urls.append(url)
                titles.append(title)

                # Extract domain name from URL for filename
                parsed_url = urllib.parse.urlparse(url)
                domain_name = parsed_url.netloc.replace('.', '_')

                # Write the scraped HTML to a file for auditing
                with open(os.path.join(output_dir, f"{domain_name}_{len(urls)}.html"), 'w', encoding='utf-8') as file:
                    file.write(html_content)

            # Ensure we have 3 URLs even if there were fewer search results
            urls += [''] * (3 - len(urls))
            titles += ['No title'] * (3 - len(titles))

            try:
                overview = generate_overview(text_content.strip(), domain)
                paragraph, pros, cons = split_overview(overview)
                writer.writerow([domain, paragraph, pros, cons, urls[0], urls[1], urls[2], titles[0], titles[1], titles[2]])
            except Exception as e:
                print(f"Error processing {domain}: {e}")

if __name__ == "__main__":
    # Path to the file containing bank domains
    domain_file = "domains.txt"
    # Path to the output file
    output_file = "cd_overviews.csv"
    main(domain_file, output_file)

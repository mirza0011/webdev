from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests import Session, RequestException, ConnectTimeout
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
from fake_useragent import UserAgent
import cloudscraper
import os
import json
import concurrent.futures
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import warnings
from urllib3.util.ssl_ import create_urllib3_context
import time
from PyPDF2 import PdfReader
import io
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

TIMEOUT = 180  # 3 minutes
GPT_API_URL = 'https://api.openai.com/v1/chat/completions'
GPT_API_KEY = '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'
proxies = {
    "http": "http://us-pr.oxylabs.io:1000",
    "https": "http://us-pr.oxylabs.io:10000",
}
def merge_json_files(input_folder, output_file):
    merged_data = {}

    # List all files in the given directory
    for filename in os.listdir(input_folder):
        # Construct full file path
        file_path = os.path.join(input_folder, filename)

        # Check if the path points to a file (not a directory)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                print(file)
                # Read JSON content from the file
                json_content = json.load(file)

                # Use filename (without extension) as the key
                key = os.path.splitext(filename)[0]

                # Add the JSON content to the merged data under the key
                merged_data[key] = json_content

    # Write merged data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)
        
def query_gpt(context_snippets):
    prompt = (
        "We are trying to help our customers understand the features of various bank and credit union certificates of deposit (CDs). The most critical features are: "
        "(1) The term (or duration) of the CD. This is what distinguishes one CD from another. "
        "(2) The APY (Annual Percentage Yield). "
        "(3) The deposit amount(s) required to purchase this CD. "
        "Two more highly important features are: "
        "(4) The 'as of' (or effective) DATE of the pricing. "
        "(5) The interest rate (or dividend rate) corresponding to the APY. "
        "Note that CDs may also go by the names: time deposits, fixed deposits, term deposits, deposit certificates, savings certificates, share certificates, or simply just a certificate. strictly exclude IRA or Retirement CDs."
        "You will be provided with HTML code in the system prompt that shows the various CDs that a bank offers. The term and APY, at minimum, should be featured prominently while the rest of the information may be in the footnotes. Please return this data in JSON structure. Strictly do not add anything additional, no comments, no code identifier nothing. I have given the example json in user prompt, use the exact same format for values and keys. Provide the following information in the exact format as shown below: Term: 6 Months APY: 4.25% Interest (Dividend) Rate: 4.24% Minimum Balance (Deposit): $500 \"As of\" Date (Effective Date): 5/29/2024.Respond like as an api endpoint Only JSON response is expected. Always give latest 'As of Date (Effective Date)' data. For effective date use mm/dd/yyyy format only. If Term, APY,Interest (Dividend) Rate,Minimum Balance (Deposit),As of Date (Effective Date) are not in given or not available or asking to click, negotiable etc. then mark them as 'NA' and strictly avoid special characters or symbols in any of the fields. If term have range of duration then use the date which is lower and only mention in format of day, month, year strictly do not keep any other extra words or symbols anything. Round all rates / APYs to two decimal points (example: instead of 1.736%, 1.74%). Round all minimum deposit amounts to the nearest dollars (example: instead of $500.00, $500). Strictly do not change numbers, provide them as they are given. I want every single possiblle CD product from the given content. Do not miss a single available CD in provided content and strictly do not mix up products. Please follow this json template structure: \"Product Name\": \"360 CD Account\", \"Term\": \"12 Months\", \"APY\": \"5.00%\", \"Interest (Dividend) Rate\": \"4.99%\", \"Minimum Balance (Deposit)\": \"$500\", \"As of Date (Effective Date)\": \"5/29/24\""
    )
    additional_prompt = (
        "[ { \"Product Name\": \"Share Term Certificate\", \"Term\": \"6 months\", \"APY\": \"4.50%\", \"Interest (Dividend) Rate\": \"4.50%\", \"Minimum Balance (Deposit)\": \"$250\", \"As of Date (Effective Date)\": \"6/13/2024\" }, { \"Product Name\": \"Share Term Certificate\", \"Term\": \"24 months\", \"APY\": \"4.30%\", \"Interest (Dividend) Rate\": \"4.30%\", \"Minimum Balance (Deposit)\": \"$250\", \"As of Date (Effective Date)\": \"6/13/2024\" }, { \"Product Name\": \"Share Term Certificate\", \"Term\": \"30 months\", \"APY\": \"3.00%\", \"Interest (Dividend) Rate\": \"3.00%\", \"Minimum Balance (Deposit)\": \"$250\", \"As of Date (Effective Date)\": \"6/13/2024\" } ]"
    )
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    messages = [
        {"role": "system", "content": json.dumps(context_snippets, indent=4)},
        {"role": "user", "content": prompt},
        {"role": "user", "content": additional_prompt}
    ]
    
    data = {
        'model': 'gpt-4o',
        'messages': messages
    }
    
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    
    try:
        response = http.post(GPT_API_URL, headers=headers, json=data, timeout=TIMEOUT)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"GPT-4 API request failed: {e}")
        return None

def create_scraper_with_ssl_fix():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return cloudscraper.create_scraper(ssl_context=ssl_context)

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

def extract_text_from_pdf(pdf_content):
    pdf_file = io.BytesIO(pdf_content)
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def check_url_status(url):
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }

    try:
        session = Session()
        response = session.get(url, timeout=20, headers=headers, verify=False)
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'application/pdf' in content_type:
            html_content = extract_text_from_pdf(response.content)
        else:
            html_content = response.text
        
        response_text = html_content.lower()
        print(f"{url}: {status_code}")

        # Check for Cloudflare protection
        if 'cloudflare' in response_text or 'enable javascript' in response_text or 'cookies to continue' in response_text or status_code in [403, 503] or status_code >= 400:
            print(f"Detected issue requiring Selenium for {url}...")
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--log-level=3")  # Logging level to suppress logs
            
            # Suppressing console messages
            os.environ['WDM_LOG_LEVEL'] = '0'
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                driver.get(url)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(5)
                
                status_code = 200
                html_content = driver.page_source
                response_text = html_content.lower()
                print(f"{url} (Selenium bypass): {status_code}")
            finally:
                driver.quit()

        if status_code == 403:
            return url, status_code, "Access forbidden - try adjusting headers or authentication", html_content
        elif "cloudflare" in response_text:
            return url, status_code, "Cloudflare protection detected", html_content
        elif status_code >= 400:
            return url, status_code, f"HTTP error {status_code}", html_content
        else:
            return url, status_code, "OK", html_content
    except SSLError:
        return url, None, "SSL error", None
    except ConnectTimeout:
        return url, None, "Connection timed out", None
    except RequestException as e:
        return url, None, f"Request failed: {str(e)}", None

def clean_url(url):
    return url.replace('://', '_').replace('/', '_').replace('?', '_').replace('=', '_').replace('&', '_')


def json_to_csv(json_file_path, csv_file_path):
    """
    Convert a JSON file to a CSV file.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    # Read JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Initialize a list to collect all records
    all_records = []

    # Initialize a set to collect all header fields
    all_headers = set()

    # Iterate over each key in the JSON
    for key in data:
        # Extract records for the current key
        records = data[key]

        # Add URL key as a new field in each record
        for record in records:
            record['Source URL'] = key
            all_records.append(record)
            # Update the set of all headers
            all_headers.update(record.keys())

    # Convert header set to a list
    headers = list(all_headers)

    # Check if the file exists to determine if we need to write the headers
    file_exists = os.path.isfile(csv_file_path)

    # Write data to CSV file
    with open(csv_file_path, 'a', newline='') as csv_file:  # Open in append mode
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        
        # Only write headers if the file does not already exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(all_records)

    print(f"Data has been appended to {csv_file_path} successfully.")

def main():
    input_file = 'urls.txt'
    html_directory = './html_files/'  # Directory to store HTML files
    max_workers = 1
    json_directory = './json_output'

    if not os.path.exists(html_directory):
        os.makedirs(html_directory)

    if not os.path.exists(json_directory):
        os.makedirs(json_directory)

    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Remove any surrounding whitespace or newline characters from URLs
    urls = [url.strip() for url in urls]
    all_url_info = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url_status, url): url for url in urls}
        future_to_gpt = {}

        for future in concurrent.futures.as_completed(future_to_url):
            url_info = {}
            try:
                url, status_code, status_description, html_content = future.result()
                url_info = {
                    'URL': url,
                    'Status Code': status_code,
                    'Status Description': status_description,
                }
                all_url_info.append(url_info)

                if html_content:
                    soup = BeautifulSoup(html_content, 'lxml')
                    for tag in soup.find_all(['script', 'img', 'link','head', 'style']):
                        tag.decompose()
                    parsed_html = soup.prettify()
                    file_name = os.path.join(html_directory, f"{clean_url(url)}.html")
                    with open(file_name, 'w', encoding='utf-8') as html_file:
                        html_file.write(parsed_html)

                    future_json = executor.submit(query_gpt, parsed_html)
                    future_to_gpt[future_json] = file_name

            except Exception as e:
                print(f"Error processing {url_info.get('URL', '')}: {e}")

        for future_json in concurrent.futures.as_completed(future_to_gpt):
            try:
                gpt_json = future_json.result()
                json_file_name = os.path.join(json_directory, f"{clean_url(future_to_gpt[future_json])}.json")
                if gpt_json:
                    with open(json_file_name, 'w', encoding='utf-8') as json_file:
                        json_file.write(gpt_json)
            except Exception as e:
                print(f"Error processing GPT: {e}")

    # all_json_file_name = os.path.join(json_directory, "all_urls.json")
    # with open(all_json_file_name, 'w', encoding='utf-8') as all_json_file:
    #     json.dump(all_url_info, all_json_file, indent=4)
    input_folder = 'json_output'
    output_file = 'merged.json'
    merge_json_files(input_folder, output_file)
    json_to_csv('merged.json', 'output.csv')

if __name__ == "__main__":
    main()
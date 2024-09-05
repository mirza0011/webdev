import openai
import time
import concurrent.futures

def read_company_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def generate_description(company_name, api_key):
    openai.api_key = api_key
    
    system_prompt = f"""
Write a 1 paragraph description of the following company: {company_name}. Provide an informative, engaging summary of the company's history, services, and any notable achievements. """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "First Community Bank, established in 1983 in Alice, Texas, has grown to include branches in Kingsville, Portland, Padre Island, Premont, Rockport, and Victoria, with headquarters and a Home Loan Center in Corpus Christi. The bank provides a range of financial services, including competitive certificates of deposit (CDs). First Community Bank offers local expertise and personalized customer service to meet the financial needs of individuals and businesses in South Texas."},
                {"role": "user", "content": "Vision One Credit Union was founded in 1956 and has been dedicated to serving its members with personalized financial solutions for over six decades. As a not-for-profit financial cooperative, Vision One is committed to providing excellent service and competitive rates to help its members achieve their financial goals. With a focus on community involvement and member satisfaction, Vision One offers a wide range of products and services, including savings accounts, loans, and online banking options, all designed to meet the diverse needs of its membership base."},
                {"role": "user", "content": "California Bank & Trust (CB&T), established in 1952, has been providing financial services to individuals and businesses across California for nearly 70 years. As a division of Zions Bancorporation, N.A., CB&T manages more than $14 billion in loans and $15 billion in deposits through over 85 branches statewide. Among its diverse financial products, CB&T offers competitive certificates of deposit (CDs) with APY rates that are highly attractive in the current market."}

            ],
            max_tokens=4095
        )
        description = response['choices'][0]['message']['content'].strip()
        return description
    except Exception as e:
        return f"Failed to generate description for {company_name}: {e}"

def write_descriptions_to_file(descriptions, output_file_path):
    with open(output_file_path, 'w') as file:
        for description in descriptions:
            file.write(description + "\n")

def main():
    api_key = ''  # Replace with your OpenAI API key
    input_file = 'companynames.txt'
    output_file = 'company_descriptions.txt'

    company_names = read_company_names(input_file)
    descriptions = [None] * len(company_names)  # Pre-allocate list with placeholders

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(generate_description, name, api_key): i for i, name in enumerate(company_names)}
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                description = future.result()
                descriptions[index] = description
                print(f"Processed: {company_names[index]}")
            except Exception as e:
                descriptions[index] = f"Failed to process {company_names[index]}: {e}"
                print(f"Failed to process {company_names[index]}: {e}")

    write_descriptions_to_file(descriptions, output_file)

if __name__ == "__main__":
    main()

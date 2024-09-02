import openai
import time

def read_company_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def generate_description(company_name, api_key):
    if company_name in ('#N/A', '#REF!', '#REF'):
        return "No company name"

    openai.api_key = api_key
    prompt = f"Write a 1 paragraph description of the following company: {company_name}. You will find an example in the first user prompt: 'California Bank & Trust (CB&T), established in 1952, has been providing financial services to individuals and businesses across California for nearly 70 years. As a division of Zions Bancorporation, N.A., CB&T manages more than $14 billion in loans and $15 billion in deposits through over 85 branches statewide. Among its diverse financial products, CB&T offers competitive certificates of deposit (CDs) with APY rates that are highly attractive in the current market.'"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4095,
        )
        description = response['choices'][0]['message']['content'].strip()
        return description
    except Exception as e:
        return f"Failed to generate description for {company_name}: {e}"

def write_descriptions_to_file(descriptions, output_file_path):
    with open(output_file_path, 'w') as file:
        for description in descriptions:
            file.write(description + "\n\n")

def main():
    api_key = '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'  # Replace with your OpenAI API key
    input_file = 'company_names.txt'
    output_file = 'company_descriptions.txt'

    company_names = read_company_names(input_file)
    descriptions = []

    for company_name in company_names:
        description = generate_description(company_name, api_key)
        descriptions.append(description)
        print(f"Processed: {company_name}")
        time.sleep(1)  # Be mindful of rate limits

    write_descriptions_to_file(descriptions, output_file)

if __name__ == "__main__":
    main()
import openai
import csv
import random
import concurrent.futures

def read_company_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def read_cd_data(file_path):
    cd_data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company = row['Company']
            if company not in cd_data:
                cd_data[company] = []
            cd_data[company].append(row)
    return cd_data

def generate_cd_overview(company_name, cd_details, api_key):
    if company_name in ('#N/A', '#REF!', '#REF', 'No company name'):
        return company_name, "<p class='text-danger'>No information available.</p>"

    openai.api_key = api_key
    
    cd_data_list = random.sample(cd_details, min(5, len(cd_details)))  # Select up to 5 random data points
    cd_data_text = "\n".join([f"<li><b>Term:</b> {item['Term']} | <b>APY:</b> {item['APY']} | <b>Minimum Deposit:</b> {item['Min Deposit']}</li>" for item in cd_data_list])
    
    prompt = f"""
Create a CD overview section for the company: {company_name} using the following data:
<ul>{cd_data_text}</ul>
Example templates:
<div class='container'>
<div class='row mb-4 text-center'>
<div class='col'>
<h2 class='mb-2 m-0 text-start fw-bold my-4'>{company_name} Certificate Overview</h2>
<p class='m-0 text-start'>{company_name} offers Certificates of Deposit (CDs) as a secure way to grow your savings. By committing to keep your money for a specified term, you can earn a higher interest rate compared to regular savings accounts. Here, we'll review the key features, advantages, and potential drawbacks of opening a CD at {company_name}.</p>
</div>
</div>
<div class='row justify-content-center mb-4'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Key Features</h3>
<p class='mb-2 m-0 text-start'>The minimum amount to open a {company_name} CD is $100, and terms range from 90 days to 4 years. Here are some important details to consider before opening an account.</p>
<div class='table-responsive'>
<table class='m-0 table table-bordered table-hover'>
<thead class='table-light'>
<tr><th scope='col'>Feature</th><th scope='col'>Value</th></tr>
</thead>
<tbody>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> APY Range</td><td class='text-end'>Varies by term</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Minimum Balance</td><td class='text-end'>$100</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Term Range</td><td class='text-end'>90 days–4 years</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Early Withdrawal Penalty</td><td class='text-end'>Varies by term</td></tr>
</tbody>
</table>
</div>
</div>
</div>
<div class='row justify-content-center'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Pros and Cons</h3>
<div class='col-12 ftr-ct'>
<h4 class='m-0 text-start text-success'>Pros</h4>
<ul class='list-unstyled mt-3'>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Competitive interest rates</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Flexible term options</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>FDIC insured up to applicable limits</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Option to renew upon maturity</li>
</ul>
</div>
<div class='col-12 ftr-ct'>
<h4 class='m-0 text-start text-danger'>Cons</h4>
<ul class='list-unstyled mt-3'>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Early withdrawal penalties apply</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Minimum opening deposit required</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Interest rates can vary</li>
</ul>
</div>
</div>
</div>
</div>

<div class='container'>
<div class='row mb-4 text-center'>
<div class='col'>
<h2 class='mb-2 m-0 text-start fw-bold my-4'>MSU Federal Credit Union Certificate Overview</h2>
<p class='m-0 text-start'>Start to dreamBIG and save more for your future with Certificates from MSUFCU. A Certificate account pays higher dividends than other savings accounts on funds you deposit for a fixed period, offering guaranteed returns, high return rates, and federal insurance by the NCUA. MSUFCU offers 3-Month, 6-Month, and 1-year add-on certificates as well as longer terms from 18-months to 5 years. Let's take a closer look at some of the MSUFCU Certificate pros and cons.</p>
</div>
</div>
<div class='row justify-content-center mb-4'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Key Features</h3>
<p class='mb-2 m-0 text-start'>The minimum amount to open an MSUFCU Certificate varies by term, starting as low as $50 for a 1-Year Add-On Certificate. Terms range from 3 months to 7 years. Rates for Certificates at MSUFCU are competitive with rates available elsewhere. However, there are some key details you should know before opening an account.</p>
<div class='table-responsive'>
<table class='m-0 table table-bordered table-hover'>
<thead class='table-light'>
<tr><th scope='col'>Feature</th><th scope='col'>Value</th></tr>
</thead>
<tbody>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> APY Range</td><td class='text-end'>3.25%–4.50%</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Minimum Balance</td><td class='text-end'>$50–$100,000</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Term Range</td><td class='text-end'>3 months–7 years</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Early Withdrawal Penalty</td><td class='text-end'>90–365 days dividends based on amount withdrawn</td></tr>
</tbody>
</table>
</div>
</div>
</div>
<div class='row justify-content-center'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Pros and Cons</h3>
<div class='col-12 ftr-ct'>
<h4 class='m-0 text-start text-success'>Pros</h4>
<ul class='list-unstyled mt-3'>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>High return rates</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Variety of term options</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Low minimum deposit</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-success-subtle'><i class='fe fe-check'></i></span>Federally insured by the NCUA</li>
</ul>
</div>
<div class='col-12 ftr-ct'>
<h4 class='m-0 text-start text-danger'>Cons</h4>
<ul class='list-unstyled mt-3'>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Fees for early withdrawal</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Higher deposits needed for competitive rates</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>No automatic roll-over</li>
<li class='mb-2 align-items-center d-flex'><span class='badge badge-rounded-circle fs-6 me-4 mt-1 text-bg-danger-subtle'><i class='fe fe-x'></i></span>Penalty for early withdrawals of Certificates over 5 years</li>
</ul>
</div>
</div>
</div>
</div>

<div class='container'>
<div class='row mb-4 text-center'>
<div class='col'>
<h2 class='mb-2 m-0 text-start fw-bold my-4'>Camden National Bank Certificate Overview</h2>
<p class='m-0 text-start'>Camden National Bank offers a variety of Certificate of Deposit (CD) accounts with competitive interest rates. These accounts require a minimum deposit and come with terms that provide flexibility and potential for higher returns, depending on the term length chosen. Below, we will explore some of the key features, and benefits, as well as some considerations to keep in mind when opening a CD account with Camden National Bank.</div>
</div>
<div class='row justify-content-center mb-4'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Key Features</h3>
<p class='mb-2 m-0 text-start'>The minimum amount to open a Camden National Bank CD is $1,000, and they offer special promotions and standard CD rates. Here are some details:</p>
<div class='table-responsive'>
<table class='m-0 table table-bordered table-hover'>
<thead class='table-light'>
<tr><th scope='col'>Feature</th><th scope='col'>Value</th></tr>
</thead>
<tbody>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Special CD APY</td><td class='text-end'>4.35% - 4.75%</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Minimum Balance</td><td class='text-end'>$1,000</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Term Range</v><td class='text-end'>7-9 months (for specials)</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Early Withdrawal Penalty</td><td class='text-end'>Yes</td></tr>
</tbody>
</table>
</div>
</div>
</div>
</div>

<div class='container'>
<div class='row mb-4 text-center'>
<div class='col'>
<h2 class='mb-2 m-0 text-start fw-bold my-4'>iQ Credit Union Certificate Overview</h2>
<p class='m-0 text-start'>iQ Credit Union's CDs offer a reliable option for those looking to safely grow their savings. These CDs provide competitive interest rates and a variety of term lengths to fit different investment needs. iQ Credit Union offers both regular and jumbo CDs that cater to different deposit amounts. Let's take a closer look at some of the iQ Credit Union CD pros and cons.</div>
</div>
<div class='row justify-content-center mb-4'>
<div class='col-12'>
<h3 class='mb-2 m-0 text-start fw-bold my-3'>Key Features</h3>
<p class='mb-2 m-0 text-start'>iQ Credit Union CDs require a minimum amount to open an account, with terms ranging from as short as 3 months to as long as 60 months. Interest rates are competitive, though there are some important details to consider.<div class='table-responsive'>
<table class='m-0 table table-bordered table-hover'>
<thead class='table-light'>
<tr><th scope='col'>Feature</th><th scope='col'>Value</th></tr>
</thead>
<tbody>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> APY Range</td><td class='text-end'>1.50%â€“4.00%</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Minimum Balance</td><td class='text-end'>$500</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Term Range</td><td class='text-end'>3â€“60 months</td></tr>
<tr><td><i class='text-success bi bi-check-circle me-2'></i> Early Withdrawal Penalty</td><td class='text-end'>Forfeit of some interest</td></tr>
</tbody>
</table>
</div>
</div>
</div>
</div>
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=4095,
        )
        overview = response['choices'][0]['message']['content'].strip()
        return company_name, overview
    except Exception as e:
        return company_name, f"<p>Failed to generate CD overview for {company_name}: {e}</p>"

def save_html(output_file_path, descriptions):
    with open(output_file_path, 'w') as file:
        file.write('<html><head><title>Company CD Overviews</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"></head><body>')
        for company, description in descriptions:
            file.write(f'{description}<br/>\n')
        file.write('</body></html>')

def main():
    api_key = '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'  # Replace with your OpenAI API key
    input_file = 'company_names.txt'
    cd_data_file = 'cd_data.csv'
    output_file = 'company_cd_overview.html'

    company_names = read_company_names(input_file)
    cd_data = read_cd_data(cd_data_file)
    descriptions = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_company = {
            executor.submit(generate_cd_overview, name, cd_data.get(name, []), api_key): name for name in company_names
        }
        for future in concurrent.futures.as_completed(future_to_company):
            company_name = future_to_company[future]
            try:
                company, description = future.result()
                descriptions.append((company, description))
                print(f"Processed: {company_name}")
            except Exception as e:
                print(f"Failed to process {company_name}: {e}")

    save_html(output_file, descriptions)

if __name__ == "__main__":
    main()
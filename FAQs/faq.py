import openai
import time
import concurrent.futures

def read_company_names(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

def generate_faqs(company_name, api_key):
        if company_name in ('#N/A', '#REF!', '#REF', 'No company name'):
            return company_name, """
                    <p class='text-danger'>No information available.</p>
                    """

        openai.api_key = api_key
        prompt = f"""
Create 5 Frequently Asked Questions (FAQs), with both questions and answers, for the company: {company_name}. 
Example:
<section class="py-5 cd-rates-faq">
      <div class="container">
            <div class="row justify-content-center mb-4">
                  <div class="col-12 ">
                        <h2 class="fw-bold m-0 mb-2 text-start my-4">Frequently asked questions</h2>
                  </div>
            </div>
            <div class="row justify-content-center">
                  <div class="col-12">
                        <div class="accordion" id="faqAccordion_{company_name.lower().replace(" ", "_")}">
                              <div class="accordion-item mb-4 border-0">
                                    <h3 class="accordion-header m-0" id="heading0_{company_name.lower().replace(" ", "_")}">
                                          <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse0_{company_name.lower().replace(" ", "_")}" aria-expanded="false" aria-controls="collapse0_{company_name.lower().replace(" ", "_")}">
                                                <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>Why should I open
                                                a Checking Account with First Community Bank?
                                          </button>
                                    </h3>
                                    <div id="collapse0_{company_name.lower().replace(" ", "_")}" class="accordion-collapse collapse" aria-labelledby="heading0_{company_name.lower().replace(" ", "_")}" data-bs-parent="#faqAccordion_{company_name.lower().replace(" ", "_")}">
                                          <div class="accordion-body pt-5">
                                                Opening a checking account with First Community Bank offers numerous
                                                benefits, including free ATM transactions at all FCB ATMs, Online and
                                                Mobile Banking access, and tailored accounts like Community Checking
                                                Plus which provides additional perks such as ID protection and shopping
                                                rewards.
                                          </div>
                                    </div>
                              </div>

                              <div class="accordion-item mb-4 border-0">
                                    <h3 class="accordion-header m-0" id="heading1_{company_name.lower().replace(" ", "_")}">
                                          <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1_{company_name.lower().replace(" ", "_")}" aria-expanded="false" aria-controls="collapse1_{company_name.lower().replace(" ", "_")}">
                                                <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>How can I report
                                                a lost or stolen debit card?
                                          </button>
                                    </h3>
                                    <div id="collapse1_{company_name.lower().replace(" ", "_")}" class="accordion-collapse collapse" aria-labelledby="heading1_{company_name.lower().replace(" ", "_")}" data-bs-parent="#faqAccordion_{company_name.lower().replace(" ", "_")}">
                                          <div class="accordion-body pt-5">
                                                If you have lost or misplaced your debit card, call your local bank
                                                location or their main number at (361) 888-9310. If you are calling
                                                after banking hours, please follow the instructions on the recording.
                                          </div>
                                    </div>
                              </div>

                              <div class="accordion-item mb-4 border-0">
                                    <h3 class="accordion-header m-0" id="heading2_{company_name.lower().replace(" ", "_")}">
                                          <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2_{company_name.lower().replace(" ", "_")}" aria-expanded="false" aria-controls="collapse2_{company_name.lower().replace(" ", "_")}">
                                                <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>What is the
                                                routing number for First Community Bank?
                                          </button>
                                    </h3>
                                    <div id="collapse2_{company_name.lower().replace(" ", "_")}" class="accordion-collapse collapse" aria-labelledby="heading2_{company_name.lower().replace(" ", "_")}" data-bs-parent="#faqAccordion_{company_name.lower().replace(" ", "_")}">
                                          <div class="accordion-body pt-5">
                                                The routing number for First Community Bank is 114911807.
                                          </div>
                                    </div>
                              </div>

                              <div class="accordion-item mb-4 border-0">
                                    <h3 class="accordion-header m-0 " id="heading3_{company_name.lower().replace(" ", "_")}">
                                          <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse3_{company_name.lower().replace(" ", "_")}" aria-expanded="false" aria-controls="collapse3_{company_name.lower().replace(" ", "_")}">
                                                <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>What can I do
                                                with First Community Bank's Online Banking?
                                          </button>
                                    </h3>
                                    <div id="collapse3_{company_name.lower().replace(" ", "_")}" class="accordion-collapse collapse" aria-labelledby="heading3_{company_name.lower().replace(" ", "_")}" data-bs-parent="#faqAccordion_{company_name.lower().replace(" ", "_")}">
                                          <div class="accordion-body pt-5">
                                                With First Community Bank's Online Banking, you can check current
                                                balances, transfer funds between accounts, view up to 180 days of
                                                account activity, download transaction information, and pay virtually
                                                anyone online.
                                          </div>
                                    </div>
                              </div>

                              <div class="accordion-item mb-4 border-0">
                                    <h3 class="accordion-header m-0" id="heading4_{company_name.lower().replace(" ", "_")}">
                                          <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse4_{company_name.lower().replace(" ", "_")}" aria-expanded="false" aria-controls="collapse4_{company_name.lower().replace(" ", "_")}">
                                                <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>What should I do
                                                if I receive a suspicious email or phone call?
                                          </button>
                                    </h3>
                                    <div id="collapse4_{company_name.lower().replace(" ", "_")}" class="accordion-collapse collapse" aria-labelledby="heading4_{company_name.lower().replace(" ", "_")}" data-bs-parent="#faqAccordion_{company_name.lower().replace(" ", "_")}">
                                          <div class="accordion-body pt-5">
                                                If you receive a suspicious email or phone call, do not give out any
                                                personal information. Report the email to spam@fcbot.com and call us at
                                                (361) 888-9310 to verify if the communication was legitimate.
                                          </div>
                                    </div>
                              </div>
                        </div>
                  </div>
            </div>
      </div>
</section>

Please ensure the output is in HTML format.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2048,
            )
            faqs = response['choices'][0]['message']['content'].strip()
            return company_name, faqs
        except Exception as e:
            return company_name, f"<p>Failed to generate FAQs for {company_name}: {e}</p>"

def save_html(output_file_path, descriptions):
        with open(output_file_path, 'w') as file:
            file.write('<html><head><title>Company FAQs</title></head><body>')
            for company, description in descriptions:
                file.write(f'<h2>{company}</h2>{description}<br/>\n')
            file.write('</body></html>')

def main():
        api_key = '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'  # Replace with your OpenAI API key
        input_file = 'company_names.txt'
        output_file = 'company_faqs.html'

        company_names = read_company_names(input_file)
        descriptions = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_company = {executor.submit(generate_faqs, name, api_key): name for name in company_names}
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
import random
import re

def read_answers(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    qa_pairs = content.split("\n\n")  # Assuming double newline separates Q&A pairs
    qa_dict = {}

    for pair in qa_pairs:
        if pair.strip():
            q, a = pair.split("A: ", 1)
            question = re.sub(r'^\d+\.\s+', '', q.replace("Q: ", "").strip())  # Removing question number
            answer = a.strip()
            qa_dict[question] = answer
    
    return qa_dict

def read_company_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_faq_html(question, answer, index, company_id):
    return f"""
<div class="accordion-item mb-4 border-0">
    <h3 class="accordion-header m-0" id="heading{index}_{company_id}">
        <button class="accordion-button bg-light fw-bold px-4 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}_{company_id}" aria-expanded="false" aria-controls="collapse{index}_{company_id}">
            <i class="bi bi-plus-circle-fill me-4 icon-toggle"></i>{question}
        </button>
    </h3>
    <div id="collapse{index}_{company_id}" class="accordion-collapse collapse" aria-labelledby="heading{index}_{company_id}" data-bs-parent="#faqAccordion_{company_id}">
        <div class="accordion-body pt-5">
            {answer}
        </div>
    </div>
</div>
"""

def generate_faq_html(faqs, num_questions=5, company_id=""):
    faq_items = list(faqs.items())
    selected_faqs = random.sample(faq_items, num_questions)  # Convert dict items to a list here
    faq_html = ""

    for i, (question, answer) in enumerate(selected_faqs):
        faq_html += get_faq_html(question, answer, i, company_id)

    return faq_html

def save_html(output_file_path, content):
    with open(output_file_path, 'w') as file:
        file.write(content)

def main():
    answers_file = 'answers.txt'
    company_names_file = 'company_names.txt'
    output_file = 'company_faqsNew.html'

    # Read questions and answers from answers.txt
    answers = read_answers(answers_file)

    # Read company names
    company_names = read_company_names(company_names_file)

    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FAQs</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            .icon-toggle { margin-right: .5rem; }
            .accordion-button:not(.collapsed) .icon-toggle { transform: rotate(45deg); }
        </style>
    </head>
    <body>
        {company_faqs}
    </body>
    </html>
    """

    company_faqs_html = ""

    # Generate FAQs for each company
    for company in company_names:
        company_id = company.lower().replace(" ", "_")
        faqs_html = generate_faq_html(answers, num_questions=5, company_id=company_id)
        company_faqs_html += f"""
        <section class="py-5 cd-rates-faq">
            <div class="container">
                <div class="row justify-content-center mb-4">
                    <div class="col-12">
                        <h2 class="fw-bold m-0 mb-2 text-start my-4">Frequently asked questions - {company}</h2>
                    </div>
                </div>
                <div class="row justify-content-center">
                    <div class="col-12">
                        <div class="accordion" id="faqAccordion_{company_id}">
                            {faqs_html}
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    final_html = html_template.replace("{company_faqs}", company_faqs_html)
    save_html(output_file, final_html)

if __name__ == "__main__":
    main()
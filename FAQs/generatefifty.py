import openai

def generate_questions(api_key):
    openai.api_key = api_key
    prompt = "Generate a list of 50 conceptual questions about Certificates of Deposit (CDs)."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    questions = response['choices'][0]['message']['content']
    return questions

def main():
    api_key = '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'  # Replace with your OpenAI API key
    questions = generate_questions(api_key)
    print(questions)

if __name__ == "__main__":
    main()
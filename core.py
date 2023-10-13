import json
from difflib import get_close_matches


def load_data(file_path) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)

    return data


def save_data(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def find_best_matches(user_question: str, questions: list[str]):
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)

    return matches[0] if matches else None


def get_answer_for_question(question, data: dict):
    for q in data['questions']:
        if q['question'] == question:
            return q['answer']


def chat_bot():
    data: dict = load_data('data.json')

    while True:
        user_input = input('You: ')

        if user_input == 'exit':
            break

        best_match = find_best_matches(user_input, [q['question'] for q in data['questions']])

        if best_match:
            answer = get_answer_for_question(best_match, data)
            print(f'Bot: {answer}')

        else:
            print("I don't know the answer. Can you teach me?")
            new_answer = input("Type the answer or press 'enter' to skip it: ")

            if new_answer.lower() != '':
                data['questions'].append({'question': user_input, 'answer': new_answer})
                save_data('data.json', data)
                print('Thank you I learned a new response!')


if __name__ == '__main__':
    chat_bot()

from .utils.questions import get_questions, print_question_with_prompt
from cyclopts import App
from rich.prompt import Prompt

app = App()


@app.default
def main(amount):
    try:
        questions = get_questions(amount=amount)
        score = 0
        for index, question in enumerate(questions):
            score += print_question_with_prompt(index, question)

        print(f"You answered {score} out of {len(questions)} correctly.")
    except Exception as e:
        print(f"Error: ${e}")


if __name__ == "__main__":
    app()

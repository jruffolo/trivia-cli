from typing import Literal, Annotated
from .utils.questions import get_questions, print_question_with_prompt
from cyclopts import App, Parameter, validators
from rich.prompt import Prompt

app = App()


@app.default
def main(
    *,
    amount: Annotated[
        int,
        Parameter(alias="-a", validator=validators.Number(gte=0, lte=50)),
    ] = 10,
    category: Annotated[
        Literal[*list(range(9, 33))] | None, Parameter(alias="-c")
    ] = None,
    difficulty: Annotated[
        Literal["easy", "medium", "hard"] | None, Parameter(alias="-d")
    ] = None,
    type: Annotated[
        Literal["multiple", "boolean"] | None, Parameter(alias="-t")
    ] = None,
    session: bool = False,
):
    """
    `trivia` is a full-featured CLI implementation of the Open Trivia DB API.

    To play, simply type `trivia` in your terminal window.

    Additionally, you may pass parameters to refine the questions you want to play.

    Parameters
    ----------
    amount:
        Choose number of questions (min = 1, max = 50)
    category:
        Select question category (e.g. Sports, History, etc)
    difficulty:
        Select difficulty level (easy, medium, hard)
    type:
        Select question type (multiple choice, true/false)
    session:
        Use a session key (avoid duplicate questions)
    """
    try:
        questions = get_questions(
            amount=amount, category=category, difficulty=difficulty, type=type
        )
        score = 0
        for index, question in enumerate(questions):
            score += print_question_with_prompt(index, question)

        print(f"You answered {score} out of {len(questions)} correctly.")
        return 0
    except Exception as e:
        print(f"Error: ${e}")
        return 1


if __name__ == "__main__":
    app()

import json
import random
from html import unescape
from operator import itemgetter

import requests
from rich import print
from rich.prompt import Prompt

QUESTION_URL = "https://opentdb.com/api.php?"


def get_questions(**kwargs):
    """
    Takes **kwargs (which will be handled as actual typed keyword options at CLI command level) and returns a list of Questions from API
    """
    # Make API Call
    try:
        response = requests.get(build_url(QUESTION_URL, kwargs))

        # Raise error if HTTP Response is not OK
        if response.status_code != 200:
            raise Exception(f"HTTP Request Not OK: Status Code {response.status_code}")

        # Load response as JSON
        data = json.loads(response.text)

        # Handle Open Trivia DB API Response Codes (i.e. no results, invalid parameter, rate limit)
        check_api_response(data["response_code"])

        # Unencode all strings within the list of Questions
        unencode(data)

        # Return the List of Question objects
        return data["results"]
    except Exception as e:
        print(f"Error: {e}")


def print_question_with_prompt(index, q) -> int:
    question, correct_answer, incorrect_answers, category, difficulty, type = (
        itemgetter(
            "question",
            "correct_answer",
            "incorrect_answers",
            "category",
            "difficulty",
            "type",
        )(q)
    )

    # Randomize question order
    questions = random.sample(
        [correct_answer] + incorrect_answers, k=len(incorrect_answers) + 1
    )
    prompt_choices = []
    answer_key = {}

    # Print index and question info
    print(
        f"[bold yellow]Question {index + 1} | {category} | {difficulty}[/bold yellow]"
    )

    if type == "multiple":
        prompt_choices = ["A", "B", "C", "D"]
        answer_key = dict(zip(prompt_choices, questions))
        print(question)
        for label, answer in answer_key.items():
            print(f"{label}: {answer}")
    elif type == "boolean":
        prompt_choices = ["True", "False"]
        answer_key = {
            "True": "True",
            "False": "False",
        }
        print(f"True or False: {question}")

    response = Prompt.ask("Your Answer", choices=prompt_choices, case_sensitive=False)

    if answer_key[response] == correct_answer:
        print("\n[bold green]Correct![/bold green]\n")
        return 1

    print(
        f"\n[bold red]Incorrect![/bold red] The correct answer was {correct_answer}\n"
    )
    return 0


# Build URL from BASE_URL
def build_url(base_url: str, params: dict[str, str | int]) -> str:
    """
    Returns a valid API Request String built from a dictionary of parameters
    """
    url = base_url
    for key, val in params.items():
        if val:
            url += f"{key}={val}&"
    return url


def check_api_response(response_code: int):
    match response_code:
        case 0:
            pass
        case 1:
            raise Exception("Open Trivia DB Code 1: No Results")
        case 2:
            raise Exception("Open Trivia DB Code 2: Invalid Parameter")
        case 3:
            raise Exception("Open Trivia DB Code 3: Token Not Found")
        case 4:
            raise Exception("Open Trivia DB Code 4: Token Empty")
        case 5:
            raise Exception("Open Trivia DB Code 5: Rate Limit")
        case _:
            pass


def unencode(iterable):
    if type(iterable) == dict:
        for key, val in iterable.items():
            if type(val) == str:
                iterable[key] = unescape(val)
            else:
                unencode(iterable[key])
    elif type(iterable) == list:
        for idx, item in enumerate(iterable):
            if type(item) == str:
                iterable[idx] = unescape(item)
            else:
                unencode(item)

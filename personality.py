# import scoring functions
from scoring import init_scores, calculate_personality
from typing import Dict  # import Dict type for type hints

# list of personality questions with options and mapping as well
QUESTIONS = [
    {
        "question": "When you face a complex problem, what do you do?",
        "options": {
            "A": "I analyze it",
            "B": "I find a creative solution",
            "C": "I ask others for help",
            "D": "I take responsibility for leading the solution"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "In a group project, what is your typical role?",
        "options": {
            "A": "Analyst",
            "B": "Idea generator",
            "C": "Coordinator",
            "D": "Leader"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "When you need to make an important decision, what is your priority?",
        "options": {
            "A": "Data-driven analysis",
            "B": "Innovation and new solutions",
            "C": "Consulting with others",
            "D": "Leadership and management approach"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "When you have a technical problem, what is your usual approach?",
        "options": {
            "A": "I analyze the problem thoroughly",
            "B": "I propose a creative solution",
            "C": "I consult with friends or colleagues",
            "D": "I try to take charge of managing the project"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "Which activity is most motivating for you?",
        "options": {
            "A": "Solving logical problems",
            "B": "Creating something new",
            "C": "Helping others",
            "D": "Leading a team"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "When facing new challenges, what do you usually do?",
        "options": {
            "A": "I analyze the situation",
            "B": "I act creatively",
            "C": "I seek advice",
            "D": "I make decisions"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "How do you prefer to drive projects forward?",
        "options": {
            "A": "With logic and careful planning",
            "B": "With innovation",
            "C": "With group collaboration",
            "D": "With leadership and task delegation"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "In teamwork, what do you focus on most?",
        "options": {
            "A": "Precision and analysis",
            "B": "Ideas and creativity",
            "C": "Communication and coordination",
            "D": "Organization and direction"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "When you need to solve a problem, what is your strategy?",
        "options": {
            "A": "Carefully analyze the problem",
            "B": "Find an innovative solution",
            "C": "Get help from others",
            "D": "Lead the team to solve it"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    },
    {
        "question": "What matters most to you in a work environment?",
        "options": {
            "A": "Accuracy and logic",
            "B": "Creativity and innovation",
            "C": "Relationships and harmony",
            "D": "Decision-making power and leadership"
        },
        "mapping": {"A": "analytical", "B": "creative", "C": "social", "D": "leadership"}
    }
]
# a function to ask the questions


def ask_questions() -> str:
    scores = init_scores()  # create score dictionary

    print("\n Answer the questions. (A/ B/ C/ D)\n")

    # loop through all questions from question dictionary
    for index, q in enumerate(QUESTIONS, 1):
        print(f"{index}. {q['question']}")  # print question

        # print all answer options
        for key, value in q["options"].items():
            print(f" {key}) {value}")

        answer = ""  # save user answer
        # keep asking until valid answer is given
        while answer not in ["A", "B", "C", "D"]:
            answer = input("Your answer : ").strip()

        ptype = q["mapping"][answer]  # get personality type from answer
        scores[ptype] += 1  # increase score for that type

    final_type = calculate_personality(scores)  # find highest personality
    return final_type, scores  # return result and scores


def ask_user_skills() -> Dict[str, int]:
    print("Please rate your skills from 0 to 10. \n")
    skills = {}  # dictionary to save skills

    # list of skill names
    for skill in ["analytical", "logic", "creativity", "communication", "leadership"]:
        value = -1  # start with invalid number

        # keep asking until number is between 0 and 10
        while value < 0 or value > 10:
            try:
                value = int(input(f"{skill}: "))  # get user input
            except:
                continue  # if error, ask again

        skills[skill] = value  # save skill value

    return skills  # return skills dictionary

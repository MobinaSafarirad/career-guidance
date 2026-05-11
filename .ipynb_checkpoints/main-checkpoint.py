from personality import ask_questions, ask_user_skills
from scoring import personality_to_skills, merge_skills
from ML_model import train_model, load_model, predict_job
import os


def main():
    if not os.path.exists("model.pkl"):
        print("Training model...")
        train_model()

    model = load_model()

    personality, scores = ask_questions()

    personality_skills = personality_to_skills(scores)

    user_skills = ask_user_skills()

    final_skills = merge_skills(personality_skills, user_skills)

    print(f"\nYour personality type: {personality}")
    print(f"Your final skills: {final_skills}")

    job = predict_job(model, final_skills)

    print(f"\nYour suggested job: {job}")

if __name__ == "__main__":
    main()
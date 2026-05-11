# This file runs the project in console if you want to run the console version
# import functions to ask personality questions and user skill input
from personality import ask_questions, ask_user_skills
# import functions to convert and merge skill scores
from scoring import personality_to_skills, merge_skills
# import machine learning related functions
from ML_model import train_model, load_model, predict_job, select_best_job
import os  # used to check if model file exists


def main():
    # check if trained model file exists
    if not os.path.exists("model.pkl"):
        print("Training model...")  # notify user that training is starting
        train_model()  # train model and save it

    model = load_model()  # load trained model from file

    # run personality test and get personality type and raw scores
    personality, scores = ask_questions()

    # convert personality scores into skill-based scores
    personality_skills = personality_to_skills(scores)

    user_skills = ask_user_skills()  # get skill ratings directly from user input

    # merge personality-based skills with user-entered skills
    final_skills = merge_skills(personality_skills, user_skills)

    # predict job title using trained ML model
    job_title = predict_job(model, final_skills)

    # choose best job based on predicted title and personality type
    best_job = select_best_job(job_title, personality)
    if best_job:  # if a suitable job is found
        # print suggested job title
        print(f"\nYour suggested job: {best_job['title']}")
        # print final merged skills
        print(f"Your final skills: {final_skills}")
        # print market score of job
        print(f"Job market score: {best_job['market_score']}")
        print("\nCareer advancement roadmap: ")  # print roadmap
        for step in best_job["roadmap"]:  # loop through roadmap steps
            print(" -", step)  # print each roadmap step
    else:
        print("No job found.")  # print message if no job found


# run main function only if this file is executed directly
if __name__ == "__main__":
    main()

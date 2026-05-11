import json  # import json module to read json files
import csv   # import csv module to write csv files
import random  # import random module to add random noise


SAMPLE_PER_JOB = 30  # how many samples we create for each job
NOISE_RANGE = 1  # the range of random noise added to skills

# open jobs.json file and load data
with open("data\\jobs.json", "r", encoding="UTF-8") as f:
    jobs = json.load(f)

rows = []  # a list to save all sample rows

# loop through each job in the jobs list
for job in jobs:
    job_name = job["title"]  # get job title
    base_skills = job["skills"]  # get base skills for this job

    # create samples for each job
    for _ in range(SAMPLE_PER_JOB):
        sample = {}  # create a new sample dictionary for dataset
        # loop through each skill and its values
        for skill, value in base_skills.items():
            # add random noise
            noise = random.randint(-NOISE_RANGE, NOISE_RANGE)
            new_value = value + noise  # new skill value with noise

            # limit the skill value between 0 and 10
            new_value = max(0, min(10, new_value))
            sample[skill] = new_value  # add skill to sample dictionary

        sample["job"] = job_name  # add job name to sample
        rows.append(sample)  # add sample to rows list

# define fields for CSV
field_names = ["analytical", "logic",
               "creativity", "communication", "leadership", "job"]

# write all samples to the CSV file
with open("training_data.csv", "w", newline="", encoding="UTF-8") as f:
    writer = csv.DictWriter(f, fieldnames=field_names)  # create csv writer
    writer.writeheader()  # write header row
    writer.writerows(rows)  # write all data rows

print("Dataset were successfuly built.")  # print success message

# Career Guidance System

A Python program that recommends jobs based on your **personality type** and **self‑rated skills**.  
Answers 10 questions, slides a few bars, and instantly gets a career roadmap + market score.


## Features

- 10‑question personality test (analytical, creative, social, leadership)
- Skill self‑assessment (0–10) for 5 areas: analytical, logic, creativity, communication, leadership
- Machine learning model (regression model) predicts the most suitable job
- Shows a career roadmap from junior to executive level
- Displays a market demand score (0–100) for each job
- Clean, offline GUI built with Tkinter
- Model persists – trains once, reuses later


## Requirements

- Python 3.7+
- scikit‑learn
- pandas
- joblib


## Installation

**Using Virtual Environment (Recommended)**

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

When you're done, deactivate the virtual environment:
```bash
deactivate
```

**Without Virtual Environment**

If you prefer not to use a virtual environment, you can install dependencies directly:
```bash
pip install -r requirements.txt
```

> On first run, the model trains itself (~2 seconds). Next launches are instant.


## Usage

```bash
python main.py
```

1. Click **Start**
2. Answer 10 personality questions (choose one option per question)
3. Rate your skills from 0 to 10 using the sliders
4. Click **Show the results**
5. Read your recommended job, market score, and career roadmap


## Example

Suppose a user gets:

- Personality: **analytical**
- Self‑rated skills: analytical = 9, logic = 8, creativity = 4, communication = 5, leadership = 3

The system might output:

```
Recommended job: Data Analyst
Job market score: 85
Your career roadmap:
 - Junior Data Analyst
 - Data Analyst
 - Senior Data Analyst
 - Data Scientist
 - Data Analytics Manager
```


# How It Works

1. **Personality test** → each answer maps to one of 4 types (analytical, creative, social, leadership).  
2. **Skill sliders** → user sets 5 numeric values (0–10).  
3. **Merge** → personality type gives baseline skill weights, combined with user sliders.  
4. **Prediction** → a pre‑trained Logistic Regression model takes the merged skills and outputs a job title.
5. **Job selection** → the app picks the best‑matching job from a built‑in database (title, roadmap, market score) based on the predicted title + personality alignment.  
6. **Display** → shows the result in a clean GUI window.

The database of jobs is stored in `jobs_data.py`. The model is trained once when `model.pkl` does not exist.



## Project Structure

```
career-guidance/
├── data/
    ├── building_AutoData.py
    ├── training_data.csv
    ├── jobs.json        # job list (titles, skills, roadmaps)
├── main.py              # main flow
├── GUI.py               # graphic user interface
├── scoring.py           # personality → skills, merging logic
├── personality.py       # questions + answer mappings
├── ML_model.py          # train, predict, select best job
├── Console_Run.py       # This file runs the project in console
├── model.pkl            # saved model (auto‑generated)
├── requirements.txt     # dependencies
└── README.md
```



## Customization

- **Add or edit jobs** – modify `jobs_data.py`. Each job needs:
  ```python
  {
    "title": "Job Name",
    "skills": {"analytical": 0-10, "logic": 0-10, ...},
    "personality": "analytical/creative/social/leadership",
    "market_score": 0-100,
    "roadmap": ["step1", "step2", ...]
  }
  ```
- **Change questions** – edit `personality.py` (keep mapping keys: `A`, `B`, `C`, `D`)
- **Update skill categories** – change `skills_list` in both `main.py` and `scoring.py`

After any change to jobs or questions, **delete `model.pkl`** and restart – the model will retrain automatically.



## License

This project is proprietary.

Copyright © 2026 Mobina Safarirad.
All Rights Reserved.


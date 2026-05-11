import pandas as pd  # import pandas for data handling
# split data into train and test sets
from sklearn.model_selection import train_test_split
# import Logistic Regression model for training model
from sklearn.linear_model import LogisticRegression
# import function to calculate accuracy
from sklearn.metrics import accuracy_score
import joblib  # used to save and load the trained model
import json  # used to read json files


def train_model():
    # read training dataset from CSV file
    data = pd.read_csv("data\\training_data.csv")

    # separate input features (skills) from target label (job)
    X = data.drop("job", axis=1)  # all skill columns unless "job"
    y = data["job"]  # job column (target)

    # split dataset into training set (80%) and test set (20%)
    X_tarin, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # create Logistic Regression model
    # max_iter=1000 means allow more iterations to make sure it will return the right job
    model = LogisticRegression(max_iter=1000)

    # train (fit) the model using training data
    model.fit(X_tarin, y_train)

    # predict jobs for test data
    y_pred = model.predict(X_test)

    # calculate accuracy between real values and predicted values
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy: ", round(acc, 2))  # print accuracy with 2 decimal places

    # save trained model into a file called model.pkl
    joblib.dump(model, "model.pkl")

    print("Model saved successfully.")  # confirmation message

    return model  # return trained model


def load_model():
    # load trained model from model.pkl file
    return joblib.load("model.pkl")


def predict_job(model, skills_dict):
    # convert input skills dictionary into a DataFrame
    # model expects data in table format
    input_df = pd.DataFrame([skills_dict])

    # predict job using trained model
    prediction = model.predict(input_df)

    # return predicted job (first result)
    return prediction[0]


def load_jobs():
    # open jobs.json file and load job data
    with open("data\\jobs.json", "r", encoding="UTF-8") as f:
        return json.load(f)


def select_best_job(predicted_job, personality):
    # load all jobs from json file
    jobs = load_jobs()

    # filter jobs that match the given personality type
    filtered_jobs = [job for job in jobs if job["personality"] == personality]

    # if no job matches personality, return None
    if not filtered_jobs:
        return None

    # select job with highest market_score
    best_job = max(filtered_jobs, key=lambda x: x["market_score"])

    return best_job  # return best matching job


# if this file is run directly, train the model
if __name__ == "__main__":
    train_model()

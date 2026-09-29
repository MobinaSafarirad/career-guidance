from tkinter import *  # import all tkinter components for GUI
from tkinter import messagebox  # import messagebox for pop-up alerts
# import scoring logic
from scoring import init_scores, calculate_personality, personality_to_skills, merge_skills
from personality import QUESTIONS  # import personality questions
# import ML functions
from ML_model import train_model, load_model, predict_job, select_best_job
import os  # used to check if model file exists or not

# ---------------- Main Window Settings ----------------
root = Tk()  # create main window
root.title("Jon recommender")  # set window title
root.geometry("700x500")  # set window size
root.configure(bg="#081b2e")  # set background color
root.resizable(False, False)  # disable resizing

# if model file does not exist, train it first
if not os.path.exists("model.pkl"):
    train_model()

# load trained model
model = load_model()

# ---------------- Rounded Background Frame ----------------
canvas = Canvas(root, width=650, height=450,
                bg="#081b2e", highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor="center")  # center canvas

# function to draw rounded rectangle


def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):

    # define corner points for rounded shape
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]

    # draw smooth polygon (rounded rectangle)
    return canvas.create_polygon(points, smooth=True, **kwargs)


# draw main rounded rectangle background
round_rectangle(10, 10, 640, 440, radius=40,
                fill="#3358be", outline="#3b82f6", width=2)

# main frame inside rounded background
main_frame = Frame(root, bg="#3b82f6")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

# ---------------- Variables ----------------
current_question = 0  # track current question index
scores = init_scores()  # personality scores
selected_option = StringVar()  # save selected radio button value

# list of skill names
skills_list = ["analytical", "logic",
               "creativity", "communication", "leadership"]
skill_vars = []  # save skill slider variables

# ---------------- Frames ----------------
welcome_frame = Frame(main_frame, bg="#3b82f6")  # first page
question_frame = Frame(main_frame, bg="#3b82f6")  # question page
skill_frame = Frame(main_frame, bg="#3b82f6")  # skill input page
result_frame = Frame(main_frame, bg="#3b82f6")  # result page

welcome_frame.pack(fill="both", expand=True)  # show welcome page first

# ---------------- Welcome Page ----------------
Label(welcome_frame,
      text="Welcome to the career guidance system.",
      font=("Calibri", 20, "bold"),
      bg="#3b82f6", fg="white",
      wraplength=500).pack(pady=(100, 2))  # main title

Label(welcome_frame,
      text="If you haven't yet chosen a job that matches your abilities, this system is designed for you",
      font=("Calibri", 12),
      bg="#3b82f6", fg="white",
      wraplength=400).pack(pady=1)  # subtitle


# start button
Button(welcome_frame, text="Start",
       bg="white", fg="#3b82f6",
       command=lambda: start_test()).pack(pady=90)

Label(welcome_frame,
      text="Version 1.0 — This system is designed for gradual development and continuous improvement",
      font=("Calibri", 10),
      bg="#3b82f6", fg="#d1d5db",
      wraplength=500).place(relx=0.5, rely=0.95, anchor="center")

# container for question content
content_frame = Frame(question_frame, bg="#3b82f6")
content_frame.pack(expand=True)

# ---------------- Question Section ----------------
question_label = Label(content_frame,
                       font=("Calibri", 14),
                       bg="#3b82f6", fg="white",
                       wraplength=500,
                       justify="left", anchor="w")
question_label.pack(pady=10)  # question text label

# create 4 radio buttons for options
radio_buttons = []
for i in range(4):
    rb = Radiobutton(content_frame,
                     variable=selected_option,
                     font=("Calibri", 12),
                     bg="#3b82f6", fg="white",
                     selectcolor="#2563eb",
                     anchor="w", justify="left")
    rb.pack(fill="x", padx=40)
    radio_buttons.append(rb)

# navigation buttons frame
button_frame = Frame(content_frame, bg="#3b82f6")
button_frame.pack(pady=15)

# next and previous buttons
Button(button_frame, text="Next", bg="white", fg="#3b82f6",
       command=lambda: next_question()).grid(row=0, column=1, padx=10)

Button(button_frame, text="Previous", bg="white", fg="#3b82f6",
       command=lambda: previous_question()).grid(row=0, column=0, padx=10)


# ---------------- Functions ----------------

# start personality test
def start_test():
    welcome_frame.pack_forget()  # hide welcome page
    question_frame.pack(fill="both", expand=True)  # show question page
    load_question()  # load first question

# load current question data


def load_question():
    global current_question
    q = QUESTIONS[current_question]  # get question data
    question_label.config(text=f"Q {current_question+1}: {q['question']}")
    selected_option.set("")  # reset selection

    # update radio buttons text and values
    for i, (key, text) in enumerate(q["options"].items()):
        radio_buttons[i].config(text=text, value=key)

# go to next question


def next_question():
    global current_question, scores

    # if no option selected show error
    if selected_option.get() == "":
        messagebox.showerror("Warning", "Choose an option.")
        return

    q = QUESTIONS[current_question]
    ptype = q["mapping"][selected_option.get()]  # get personality type
    scores[ptype] += 1  # increase score

    # move to next question or go to skill page
    if current_question < len(QUESTIONS)-1:
        current_question += 1
        load_question()
    else:
        question_frame.pack_forget()
        show_skills()

# go to previous question


def previous_question():
    global current_question
    if current_question > 0:
        current_question -= 1
        load_question()

# ---------------- Skill Input Page ----------------


def show_skills():
    skill_frame.pack(fill="both", expand=True)

    # create scrollable canvas
    canvas_skill = Canvas(skill_frame, bg="#3b82f6", highlightthickness=0)
    scrollbar = Scrollbar(skill_frame, orient="vertical",
                          command=canvas_skill.yview)
    scrollable_frame = Frame(canvas_skill, bg="#3b82f6")

    # update scroll region when frame size changes
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_skill.configure(
            scrollregion=canvas_skill.bbox("all")
        )
    )

    canvas_skill.create_window((100, 0), window=scrollable_frame, anchor="nw")
    canvas_skill.configure(yscrollcommand=scrollbar.set)

    canvas_skill.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="left", fill="y")

    # enable mouse scroll
    def _on_mousewheel(event):
        canvas_skill.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas_skill.bind_all("<MouseWheel>", _on_mousewheel)

    # page title
    Label(scrollable_frame,
          text="Please rate your skills from 0 to 10.",
          font=("Calibri", 16, "bold"),
          bg="#3b82f6", fg="white").pack(pady=10)

    skill_vars.clear()

    # create sliders for each skill
    for skill in skills_list:
        var = IntVar()
        skill_vars.append(var)

        Label(scrollable_frame,
              text=skill,
              font=("Calibri", 12),
              bg="#1b6bec", fg="white").pack(pady=5)

        Scale(scrollable_frame,
              from_=0, to=10,
              orient=HORIZONTAL,
              variable=var,
              length=350,
              bg="#3b82f6",
              fg="white",
              troughcolor="#2563eb",
              highlightthickness=0).pack(pady=5)

    # result button
    Button(scrollable_frame,
           text="Show the results",
           bg="white", fg="#3b82f6",
           command=final_result).pack(pady=20)

# ---------------- Result Page ----------------


def show_result_page(best_job, final_skills):
    result_frame.pack(fill="both", expand=True)

    # remove previous widgets if exist
    for widget in result_frame.winfo_children():
        widget.destroy()

    # if no job found
    if not best_job:
        Label(result_frame,
              text="No job found.",
              font=("Calibri", 14),
              bg="#3b82f6", fg="white").pack(pady=20)
        return

    # show job title
    Label(result_frame,
          text=f"Recommended job: {best_job['title']}",
          font=("Calibri", 18, "bold"),
          bg="#3b82f6", fg="white").pack(pady=15)

    # show market score
    Label(result_frame,
          text="Job market score: {best_job['market_score']}",
          font=("Calibri", 12),
          bg="#3b82f6", fg="white").pack(pady=5)

    # roadmap title
    Label(result_frame,
          text="Your career roadmap: ",
          font=("Calibri", 16, "bold"),
          bg="#3b82f6", fg="white").pack(pady=10)

    # show roadmap steps
    for step in best_job["roadmap"]:
        Label(result_frame,
              text=" - " + step,
              font=("Calibri", 14),
              bg="#3b82f6", fg="white").pack(anchor="w", padx=40)

# restart program (go back to welcome page)


def restart_program():
    result_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

# final calculation and ML prediction


def final_result():
    # get user skill values
    user_skills = {skill: var.get()
                   for skill, var in zip(skills_list, skill_vars)}

    # convert personality scores to skill scores
    personality_skills = personality_to_skills(scores)

    # merge personality skills and user skills
    final_skills = merge_skills(personality_skills, user_skills)

    # predict job using ML model
    job_title = predict_job(model, final_skills)

    # select best job based on personality and market score
    best_job = select_best_job(job_title, calculate_personality(scores))

    skill_frame.pack_forget()
    show_result_page(best_job, final_skills)

# root.mainloop()

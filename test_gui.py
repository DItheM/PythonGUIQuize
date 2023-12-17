import random
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("500x500")
root.title("Quiz Maker Application")

questions = [
    "What is the capital of France?",
    "Python is a high-level programming language. (True/False)",
    "Which planet is known as the 'Red Planet'?",
    "What is the powerhouse of the cell?",
    "Which famous scientist developed the theory of relativity?",
    "Which country is known as the 'Land of the Rising Sun'?",
    "Which ocean is the largest and deepest?",
    "Who painted the Mona Lisa?",
    "Which gas do plants absorb during photosynthesis?",
    "Which is the longest river in the world?",
]

options = [
    ["Paris", "London", "Berlin", "Madrid"],
    ["True", "False"],
    ["Mars", "Jupiter", "Venus", "Saturn"],
    ["Mitochondria", "Nucleus", "Ribosome", "Chloroplast"],
    ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Stephen Hawking"],
    ["Japan", "China", "South Korea", "Vietnam"],
    ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
    ["Leonardo da Vinci", "Michelangelo", "Pablo Picasso", "Vincent van Gogh"],
    ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
    ["Nile", "Amazon", "Mississippi", "Yangtze"],
]

correct_answers = ["Paris", "True", "Mars", "Mitochondria", "Albert Einstein",
                   "Japan", "Pacific Ocean", "Leonardo da Vinci", "Carbon Dioxide", "Nile"]

current_question = 0
score = 0
timer = 10  # Time for each question in seconds
first_name = ""
lasy_name = ""
student_id = ""
after_id = None
end_quiz_window = None

name_label = tk.Label(root, text="Enter First Name:")
name_entry = tk.Entry(root)

surname_label = tk.Label(root, text="Enter Last Name:")
surname_entry = tk.Entry(root)

id_label = tk.Label(root, text="Enter 6-digit Student ID:")
id_entry = tk.Entry(root)

question_label = tk.Label(root, text="")
option_buttons = []
timer_label = tk.Label(root, text="")
score_label = tk.Label(root, text="")

def display_question():
    global current_question, score, timer
    if current_question < len(questions):
        timer = 10  # Reset timer for each new question
        question_label.config(text=questions[current_question])
        score_label.config(text=f"Score: {score}")  # Update score display
        for button in option_buttons:
            button.destroy()
        option_buttons.clear()
        for option in options[current_question]:
            button = tk.Button(root, text=option, command=lambda o=option, q=current_question: check_answer(o, q))
            option_buttons.append(button)
            button.pack()
        countdown(timer)         

def check_answer(selected_option, question_number):
    global score
    if selected_option == correct_answers[question_number]:
        score += 1
    global current_question
    current_question += 1
    if after_id:
        root.after_cancel(after_id)  # Cancel the after event
    if current_question < len(questions):
        display_question()
    else:
        current_question = len(questions) - 1
        end_quiz()

def countdown(seconds):
    global current_question, timer,after_id
    if seconds >= 0:
        timer_label.config(text=f"Time left: {seconds} seconds")
        after_id = root.after(1000, countdown, seconds - 1)
    else:
        if current_question < len(questions) - 1:  # Check if there are more questions
            current_question += 1
            display_question()
        else:
            end_quiz()

def save_results(student_id, score):
    filename = f"results.txt"
    with open(filename, "a") as file:
        file.write(f"Student ID: {student_id}, Score: {score}\n")

def end_quiz():
    global current_question, option_buttons, quit_button, end_quiz_window, student_id
    timer_label.config(text="Quiz ended")
    percentage = (score / len(questions)) * 100
    result = f"Score: {score}/{len(questions)} ({percentage:.2f}%)"
    if current_question == len(questions) - 1:
        end_report()
    else:
        current_question = len(questions) - 1
        if after_id:
            root.after_cancel(after_id) 
        quit_button.destroy()
        question_label.destroy()
        for button in option_buttons:
            button.destroy()
        option_buttons.clear()

        end_quiz_window = tk.Toplevel(root)
        end_quiz_window.title("Quiz Result")
        
        result_label = tk.Label(end_quiz_window, text=result)
        result_label.pack()

        retake_same_user_button = tk.Button(
            end_quiz_window, text="Retake (Same User)", command=retake_same_user
        )
        retake_same_user_button.pack()

        retake_different_user_button = tk.Button(
            end_quiz_window, text="Retake (Different User)", command=retake_different_user
        )
        retake_different_user_button.pack()

        quit_button = tk.Button(end_quiz_window, text="Quit", command=root.destroy)
        quit_button.pack()
    save_results(student_id, score)

def retake_same_user():
    global current_question, score, end_quiz_window, question_label, timer_label, score_label, quit_button 
    end_quiz_window.destroy()
    score_label.destroy()
    timer_label.destroy()
    question_label = tk.Label(root, text="")
    timer_label = tk.Label(root, text="")
    score_label = tk.Label(root, text="")
    quit_button = tk.Button(root, text="Quit Quiz", command=confirm_quit)
    question_label.pack()
    score_label.pack()
    timer_label.pack()
    quit_button.pack(side=tk.BOTTOM, pady=20)
    reset_quiz()
    shuffle()
    display_question()

def retake_different_user():
    global current_question, score, end_quiz_window
    end_quiz_window.destroy()
    reset_quiz()
    shuffle()
    set_entries()

def reset_quiz():
    global current_question, score
    current_question = 0
    score = 0
    # Reset any other necessary variables or GUI elements
    
def handle_response(response, same_user_func, different_user_func):
    if response == "Retake (Same User)":
        same_user_func()
    elif response == "Retake (Different User)":
        different_user_func()
    else:
        root.destroy()

def shuffle():
    global questions, options, correct_answers

    # Combine questions, options, and correct answers for shuffling
    combined_data = list(zip(questions, options, correct_answers))
    
    # Shuffle the combined data
    random.shuffle(combined_data)

    # Unpack shuffled data into separate lists
    questions, options, correct_answers = zip(*combined_data)


def end_report():
    global current_question, option_buttons, quit_button, end_quiz_window
    timer_label.config(text="Quiz ended")
    percentage = (score / len(questions)) * 100
    result = f"Score: {score}/{len(questions)} ({percentage:.2f}%)"

    if percentage >= 50:
        result += "\nPassed!"
    else:
        result += "\nFailed!"
    correct_answers_info = "\n\nCorrect Answers:\n"
    for i, (question, answer) in enumerate(zip(questions, correct_answers), start=1):
        correct_answers_info += f"Question {i}: {question}\nAnswer: {answer}\n\n"

    if after_id:
        root.after_cancel(after_id) 
    quit_button.destroy()
    question_label.destroy()
    for button in option_buttons:
        button.destroy()
    option_buttons.clear()
    
    end_quiz_window = tk.Toplevel(root)
    end_quiz_window.title("Quiz Result")
    
    result_label = tk.Label(end_quiz_window, text=result + correct_answers_info)
    result_label.pack()

    retake_same_user_button = tk.Button(
        end_quiz_window, text="Retake (Same User)", command=retake_same_user
    )
    retake_same_user_button.pack()

    retake_different_user_button = tk.Button(
        end_quiz_window, text="Retake (Different User)", command=retake_different_user
    )
    retake_different_user_button.pack()

    quit_button = tk.Button(end_quiz_window, text="Quit", command=root.destroy)
    quit_button.pack()

def confirm_quit():
    if messagebox.askokcancel("Quit", "Are you sure you want to end the quiz?"):
        end_quiz()

def set_entries():
    global name_label, name_entry, surname_label, surname_entry, id_label, id_entry, start_button, quit_button, question_label, timer_label, score_label
    name_label = tk.Label(root, text="Enter First Name:")
    name_entry = tk.Entry(root)

    surname_label = tk.Label(root, text="Enter Last Name:")
    surname_entry = tk.Entry(root)

    id_label = tk.Label(root, text="Enter 6-digit Student ID:")
    id_entry = tk.Entry(root)

    name_label.pack()
    name_entry.pack()
    surname_label.pack()
    surname_entry.pack()
    id_label.pack()
    id_entry.pack()
    start_button = tk.Button(root, text="Start Quiz", command=start_quiz)
    start_button.pack()

    score_label.destroy()
    timer_label.destroy()

    question_label = tk.Label(root, text="")
    timer_label = tk.Label(root, text="")
    score_label = tk.Label(root, text="")
    quit_button = tk.Button(root, text="Quit Quiz", command=confirm_quit)

def start_quiz():
    global current_question, score, questions, options, correct_answers, first_name, last_name, student_id
    current_question = 0
    score = 0
    first_name = name_entry.get()
    last_name = surname_entry.get()
    student_id = id_entry.get()
    if not (first_name and last_name and student_id):
        messagebox.showerror("Error", "Please enter values for First Name, Last Name, and Student ID.")
    elif len(student_id) != 6 or not student_id.isdigit():
        messagebox.showerror("Error", "Student ID should be a 6-digit number.")
    else:
        name_entry.destroy()
        surname_entry.destroy()
        id_entry.destroy()
        name_label.destroy()
        surname_label.destroy()
        id_label.destroy()
        start_button.destroy()
        question_label.pack()
        timer_label.pack()
        score_label.pack()
        quit_button.pack(side=tk.BOTTOM, pady=20)

        shuffle()
        display_question()


name_label.pack()
name_entry.pack()
surname_label.pack()
surname_entry.pack()
id_label.pack()
id_entry.pack()
start_button = tk.Button(root, text="Start Quiz", command=start_quiz)
start_button.pack()

# Create a quit button to allow ending the quiz prematurely
quit_button = tk.Button(root, text="Quit Quiz", command=confirm_quit)


question_label.pack()
score_label.pack()
timer_label.pack()

root.mainloop()
import tkinter as tk
from tkinter import messagebox
import random

# --- Game Logic Functions ---

def play(user_choice):
    global user_score, comp_score
    
    # Computer Selection
    options = ['Rock', 'Paper', 'Scissors']
    comp_choice = random.choice(options)
    
    # Game Logic
    result = ""
    if user_choice == comp_choice:
        result = "It's a Tie!"
        result_color = "gray"
    elif (user_choice == 'Rock' and comp_choice == 'Scissors') or \
         (user_choice == 'Scissors' and comp_choice == 'Paper') or \
         (user_choice == 'Paper' and comp_choice == 'Rock'):
        result = "You Win!"
        result_color = "green"
        user_score += 1
    else:
        result = "You Lose!"
        result_color = "red"
        comp_score += 1

    # Update the UI Labels
    label_user_choice.config(text=f"You chose: {user_choice}")
    label_comp_choice.config(text=f"Computer chose: {comp_choice}")
    label_result.config(text=result, fg=result_color)
    label_score.config(text=f"Score -> You: {user_score}  |  Computer: {comp_score}")

def reset_game():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    label_user_choice.config(text="You chose: ...")
    label_comp_choice.config(text="Computer chose: ...")
    label_result.config(text="Make your move!", fg="black")
    label_score.config(text=f"Score -> You: {user_score}  |  Computer: {comp_score}")

# --- GUI Setup ---

# Initialize main window
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x450")
root.config(bg="#f0f0f0") # Light gray background

# Initialize Scores
user_score = 0
comp_score = 0

# Title
title_label = tk.Label(root, text="Rock Paper Scissors", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Display Choices
label_user_choice = tk.Label(root, text="You chose: ...", font=("Helvetica", 12), bg="#f0f0f0")
label_user_choice.pack()

label_comp_choice = tk.Label(root, text="Computer chose: ...", font=("Helvetica", 12), bg="#f0f0f0")
label_comp_choice.pack()

# Display Result
label_result = tk.Label(root, text="Make your move!", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="blue")
label_result.pack(pady=20)

# Button Frame (to hold the 3 buttons side by side)
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

# Buttons
# We use lambda to pass arguments to the function when clicked
btn_rock = tk.Button(button_frame, text="Rock", font=("Helvetica", 12),
                      width=8, bg="lightblue",
                     command=lambda: play('Rock'))
btn_rock.grid(row=0, column=0, padx=10)

btn_paper = tk.Button(button_frame, text="Paper", font=("Helvetica", 12), width=8, bg="lightgreen",
                      command=lambda: play('Paper'))
btn_paper.grid(row=0, column=1, padx=10)

btn_scissors = tk.Button(button_frame, text="Scissors", font=("Helvetica", 12), width=8, bg="lightpink",
                         command=lambda: play('Scissors'))
btn_scissors.grid(row=0, column=2, padx=10)

# Score Board
label_score = tk.Label(root, text=f"Score -> You: {user_score}  |  Computer: {comp_score}", 
                       font=("Helvetica", 12, "bold"), bg="#f0f0f0")
label_score.pack(pady=20)

# Reset Button
btn_reset = tk.Button(root, text="Reset Score", font=("Helvetica", 10), bg="orange", command=reset_game)
btn_reset.pack(pady=5)

# Run the application
root.mainloop()
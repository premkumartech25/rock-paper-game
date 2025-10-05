import tkinter as tk
from tkinter import messagebox
import random
from playsound import playsound
import threading  # to play sound without freezing UI

# Global variables
user_score = 0
computer_score = 0
ties = 0
game_running = False

# Play sound safely (threaded so GUI doesn’t lag)
def play_sound(filename):
    threading.Thread(target=lambda: playsound(filename), daemon=True).start()

def start_game():
    global game_running, user_score, computer_score, ties
    game_running = True
    user_score = computer_score = ties = 0
    update_score()
    user_choice_label.config(image="", text="You")
    computer_choice_label.config(image="", text="Computer")
    result_label.config(text="Game Started! Choose Rock, Paper, or Scissors.", fg="black")
    play_sound("click.wav")

def stop_game():
    global game_running
    game_running = False
    play_sound("click.wav")
    messagebox.showinfo("Game Over", f"Final Score:\nYou: {user_score}\nComputer: {computer_score}\nTies: {ties}")

def restart_game():
    global user_score, computer_score, ties
    user_score = computer_score = ties = 0
    update_score()
    user_choice_label.config(image="", text="You")
    computer_choice_label.config(image="", text="Computer")
    result_label.config(text="Game Restarted! Choose Rock, Paper, or Scissors.", fg="purple")
    play_sound("click.wav")

def play(user_choice):
    global user_score, computer_score, ties, game_running

    if not game_running:
        result_label.config(text="Click 'Start' to play!", fg="orange")
        play_sound("click.wav")
        return

    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)

    # Update user/computer choice images
    user_choice_label.config(image=images[user_choice], text="")
    computer_choice_label.config(image=images[computer_choice], text="")

    # Decide winner
    if user_choice == computer_choice:
        ties += 1
        result_label.config(text="It's a tie!", fg="blue")
        play_sound("tie.wav")
    elif (
        (user_choice == "rock" and computer_choice == "scissors") or
        (user_choice == "scissors" and computer_choice == "paper") or
        (user_choice == "paper" and computer_choice == "rock")
    ):
        user_score += 1
        result_label.config(text="You win! 🎉", fg="green")
        play_sound("win.wav")
    else:
        computer_score += 1
        result_label.config(text="Computer wins! 😢", fg="red")
        play_sound("lose.wav")

    update_score()

def update_score():
    score_label.config(text=f"You: {user_score}   Computer: {computer_score}   Ties: {ties}")

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("600x480")
root.config(bg="#f0f0f0")

# Load images (make sure rock.png, paper.png, scissors.png exist)
images = {
    "rock": tk.PhotoImage(file="rock.png"),
    "paper": tk.PhotoImage(file="paper.png"),
    "scissors": tk.PhotoImage(file="scissors.png")
}

# Title
title_label = tk.Label(root, text="Rock Paper Scissors Game", font=("Arial", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Score
score_label = tk.Label(root, text="You: 0   Computer: 0   Ties: 0", font=("Arial", 14), bg="#f0f0f0")
score_label.pack(pady=5)

# Choices frame
choices_frame = tk.Frame(root, bg="#f0f0f0")
choices_frame.pack(pady=20)

user_choice_label = tk.Label(choices_frame, text="You", font=("Arial", 12), bg="#f0f0f0")
user_choice_label.grid(row=0, column=0, padx=30)

vs_label = tk.Label(choices_frame, text="VS", font=("Arial", 14, "bold"), bg="#f0f0f0")
vs_label.grid(row=0, column=1, padx=20)

computer_choice_label = tk.Label(choices_frame, text="Computer", font=("Arial", 12), bg="#f0f0f0")
computer_choice_label.grid(row=0, column=2, padx=30)

# Result label
result_label = tk.Label(root, text="Click Start to begin!", font=("Arial", 14, "bold"), bg="#f0f0f0")
result_label.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=15)

rock_button = tk.Button(button_frame, text="Rock", image=images["rock"], compound="top", command=lambda: play("rock"))
rock_button.grid(row=0, column=0, padx=15)

paper_button = tk.Button(button_frame, text="Paper", image=images["paper"], compound="top", command=lambda: play("paper"))
paper_button.grid(row=0, column=1, padx=15)

scissors_button = tk.Button(button_frame, text="Scissors", image=images["scissors"], compound="top", command=lambda: play("scissors"))
scissors_button.grid(row=0, column=2, padx=15)

# Start / Stop / Restart buttons
control_frame = tk.Frame(root, bg="#f0f0f0")
control_frame.pack(pady=15)

start_button = tk.Button(control_frame, text="Start", width=12, bg="green", fg="white", command=start_game)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(control_frame, text="Stop", width=12, bg="red", fg="white", command=stop_game)
stop_button.grid(row=0, column=1, padx=10)

restart_button = tk.Button(control_frame, text="Restart", width=12, bg="blue", fg="white", command=restart_game)
restart_button.grid(row=0, column=2, padx=10)

# Run app
root.mainloop()

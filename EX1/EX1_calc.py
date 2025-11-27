import tkinter as tk
from tkinter import messagebox
import random

class arithmeticquiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("400x300")

        self.difficulty = None
        self.score = 0
        self.question_num = 0
        self.correct_answer = None
        self.first_try = True

        self.create_menu_frame()

    def clear_window(self):
        #remove widgets from window
        for w in self.root.winfo_children():
            w.destroy()

    def create_menu_frame(self):
        #difficulty menu
        self.clear_window()
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(expand=True)

        tk.Label(self.menu_frame, text="DIFFICULTY LEVEL", font=("Arial", 15)).pack(pady=15)

        tk.Button(self.menu_frame, text="Easy", command=lambda: self.start_quiz("easy")).pack(pady=5)
        tk.Button(self.menu_frame, text="Moderate", command=lambda: self.start_quiz("moderate")).pack(pady=5)
        tk.Button(self.menu_frame, text="Advanced", command=lambda: self.start_quiz("advanced")).pack(pady=5)

    def start_quiz(self, level):
        #start the quiz
        self.difficulty = level
        self.score = 0
        self.question_num = 0
        self.next_question()

    def randomint(self):
        #return random number based on
        if self.difficulty == "easy":
            return random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideoperation(self):
        #use either + or - for every question
        return random.choice(['+', '-'])

    def next_question(self):
        #generate/display the next q, show results if the player finished all 10
        if self.question_num >= 10:
            self.displayresults()
            return

        self.clear_window()
        self.question_num += 1
        self.first_try = True

        num1 = self.randomint()
        num2 = self.randomint()
        op = self.decideoperation()

        if op == '+':
            self.correct_answer = num1 + num2
        else:
            self.correct_answer = num1 - num2

        question_text = f"{num1} {op} {num2} = ?"

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text=f"Question {self.question_num}/10", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.frame, text=question_text, font=("Arial", 18)).pack(pady=10)

        self.entry = tk.Entry(self.frame, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.focus()

        tk.Button(self.frame, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        #check the user's answer and score accordingly
        try:
            user_ans = int(self.entry.get())
        except:
            messagebox.showerror("Error", "Please enter a number!")
            return

        if user_ans == self.correct_answer:
            #first try 10 points, second try 5
            if self.first_try:
                self.score += 10
            else:
                self.score += 5

            messagebox.showinfo("Correct", "Nice job!")
            self.next_question()

        else:
            if self.first_try:
                self.first_try = False
                messagebox.showwarning("Wrong", "Try again!")
                self.entry.delete(0, tk.END)
            else:
                #if the player gets 2 wrong attempts they move on to the next
                messagebox.showwarning("Incorrect", f"Incorrect! The correct answer was {self.correct_answer}.")
                self.next_question()

    def displayresults(self):
        #display final score/grade
        self.clear_window()
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        else:
            grade = "D"

        tk.Label(self.root, text="RESULTS", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text=f"Score: {self.score}/100", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.root, text=f"Grade: {grade}", font=("Arial", 14)).pack(pady=5)

        tk.Button(self.root, text="Play Again", command=self.create_menu_frame).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = arithmeticquiz(root)
    root.mainloop()

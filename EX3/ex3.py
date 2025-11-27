import tkinter as tk
from tkinter import simpledialog, messagebox
import os

FILE_PATH = "EX3/studentMarks.txt"


#load and save functions
def load_students():
    """Return list of lists: [code, name, c1, c2, c3, exam]"""
    if not os.path.exists(FILE_PATH):
        messagebox.showerror("Error", "studentMarks.txt not found!")
        return []

    with open(FILE_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    students = []
    for line in lines[1:]:
        if line == "":
            continue
        parts = line.split(",")
        code = int(parts[0])
        name = parts[1]
        c1 = int(parts[2])
        c2 = int(parts[3])
        c3 = int(parts[4])
        exam = int(parts[5])
        students.append([code, name, c1, c2, c3, exam])

    return students


def save_students(students):
    """Save list back to file."""
    with open(FILE_PATH, "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(f"{s[0]},{s[1]},{s[2]},{s[3]},{s[4]},{s[5]}\n")

def show_output(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")


#calculations
def get_overall(c1, c2, c3, exam):
    return ((c1 + c2 + c3 + exam) / 160) * 100


def get_grade(overall):
    if overall >= 70:
        return "A"
    elif overall >= 60:
        return "B"
    elif overall >= 50:
        return "C"
        result
    elif overall >= 40:
        return "D"
    else:
        return "F"


#button functions
def view_all():
    students = load_students()
    if not students:
        return

    text = ""
    total = 0

    for s in students:
        overall = get_overall(s[2], s[3], s[4], s[5])
        grade = get_grade(overall)

        text += (
            f"Name: {s[1]}\n"
            f"Code: {s[0]}\n"
            f"Coursework Total: {s[2]+s[3]+s[4]}\n"
            f"Exam: {s[5]}\n"
            f"Overall: {overall:.1f}%\n"
            f"Grade: {grade}\n"
            "-------------------------\n"
        )
        total += overall

    avg = total / len(students)
    text += f"\nTotal Students: {len(students)}\nAverage: {avg:.1f}%"

    show_output(text)


def view_one():
    students = load_students()
    target = simpledialog.askstring("Find", "Enter name or code:")
    if not target:
        return

    for s in students:
        if s[1].lower() == target.lower() or str(s[0]) == target:
            overall = get_overall(s[2], s[3], s[4], s[5])
            grade = get_grade(overall)
            text = (
                f"Name: {s[1]}\n"
                f"Code: {s[0]}\n"
                f"Coursework Total: {s[2]+s[3]+s[4]}\n"
                f"Exam: {s[5]}\n"
                f"Overall: {overall:.1f}%\n"
                f"Grade: {grade}"
            )
            show_output(text)
            return

    messagebox.showerror("Error", "Not found.")


def highest():
    students = load_students()
    best = max(students, key=lambda s: get_overall(s[2], s[3], s[4], s[5]))
    overall = get_overall(best[2], best[3], best[4], best[5])
    show_output(f"Highest Scorer:\n{best[1]} ({overall:.1f}%)")


def lowest():
    students = load_students()
    worst = min(students, key=lambda s: get_overall(s[2], s[3], s[4], s[5]))
    overall = get_overall(worst[2], worst[3], worst[4], worst[5])
    show_output(f"Lowest Scorer:\n{worst[1]} ({overall:.1f}%)")


def add_student():
    students = load_students()
    code = simpledialog.askinteger("Add", "Student code:")
    name = simpledialog.askstring("Add", "Name:")
    c1 = simpledialog.askinteger("Add", "Coursework 1:")
    c2 = simpledialog.askinteger("Add", "Coursework 2:")
    c3 = simpledialog.askinteger("Add", "Coursework 3:")
    exam = simpledialog.askinteger("Add", "Exam:")

    if None in (code, name, c1, c2, c3, exam):
        return

    students.append([code, name, c1, c2, c3, exam])
    save_students(students)
    messagebox.showinfo("Done", "Student added.")


def delete_student():
    students = load_students()
    target = simpledialog.askstring("Delete", "Enter name or code:")
    new_list = []

    found = False
    for s in students:
        if s[1].lower() == target.lower() or str(s[0]) == target:
            found = True
        else:
            new_list.append(s)

    if not found:
        messagebox.showerror("Error", "Student not found.")
        return

    save_students(new_list)
    messagebox.showinfo("Done", "Student deleted.")


def update_student():
    students = load_students()
    target = simpledialog.askstring("Update", "Enter name or code:")

    for s in students:
        if s[1].lower() == target.lower() or str(s[0]) == target:
            new_name = simpledialog.askstring("Update", "New name:", initialvalue=s[1])
            new_exam = simpledialog.askinteger("Update", "New exam:", initialvalue=s[5])

            s[1] = new_name
            s[5] = new_exam

            save_students(students)
            messagebox.showinfo("Done", "Updated.")
            return

    messagebox.showerror("Error", "Student not found.")


#tkinter window
root = tk.Tk()
root.title("Student Manager (Simple)")
root.geometry("600x500")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

buttons = [
    ("View All", view_all),
    ("View One", view_one),
    ("Highest", highest),
    ("Lowest", lowest),
    ("Add", add_student),
    ("Delete", delete_student),
    ("Update", update_student)
]

for text, cmd in buttons:
    tk.Button(btn_frame, text=text, width=20, command=cmd).pack(pady=3)

output_box = tk.Text(root, height=18, width=70, state="disabled")
output_box.pack(pady=10)

root.mainloop()

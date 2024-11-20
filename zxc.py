import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox

def solve_linear_system(A, b):
    try:
        solution = np.linalg.solve(A, b)
        return "Unique Solution", solution
    except np.linalg.LinAlgError:
        rank_A = np.linalg.matrix_rank(A)
        augmented_matrix = np.hstack((A, b.reshape(-1, 1)))
        rank_augmented = np.linalg.matrix_rank(augmented_matrix)
        
        if rank_A == rank_augmented:
            return "Infinitely Many Solutions", None
        else:
            return "No Solution", None

def plot_solution(A, b, solution, solution_type):
    fig, ax = plt.subplots()
    x = np.linspace(-10, 10, 400)

    for i in range(len(A)):
        y = (b[i] - A[i][0] * x) / A[i][1]                            
        ax.plot(x, y, label=f"Equation {i + 1}")

    if solution is not None:
        ax.plot(solution[0], solution[1], 'ro', label="Solution")

    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Linear System of Equations - {solution_type}")
    plt.grid(True)
    plt.show()

def calculate():
    try:
        n = int(entry_num_eq.get())
        A = []
        b = []
        for i in range(n):
            coefficients = list(map(float, entries_A[i].get().split()))
            if len(coefficients) != n:
                raise ValueError("Number of coefficients must be equal to the number of equations")
            A.append(coefficients)
            b_value = float(entries_b[i].get())
            b.append(b_value)
        A = np.array(A)
        b = np.array(b)
        solution_type, solution = solve_linear_system(A, b)
        plot_solution(A, b, solution, solution_type) 
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

root = Tk()
root.title("Linear System Solver")

Label(root, text="Enter the number of equations:").grid(row=0, column=0)
entry_num_eq = Entry(root)
entry_num_eq.grid(row=0, column=1)

entries_A = []
entries_b = []

def create_entries():
    for entry in entries_A + entries_b:
        entry.destroy()
    entries_A.clear()
    entries_b.clear()
    try:
        n = int(entry_num_eq.get())
        for i in range(n):
            Label(root, text=f"Enter coefficients for equation {i + 1}:").grid(row=i + 1, column=0)
            entry_A = Entry(root)
            entry_A.grid(row=i + 1, column=1)
            entries_A.append(entry_A)
            Label(root, text=f"Enter constant for equation {i + 1}:").grid(row=i + 1, column=2)
            entry_b = Entry(root)
            entry_b.grid(row=i + 1, column=3)
            entries_b.append(entry_b)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number")

Button(root, text="Set Equations", command=create_entries).grid(row=0, column=2)
Button(root, text="Calculate", command=calculate).grid(row=0, column=3)

root.mainloop()

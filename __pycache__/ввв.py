import tkinter as tk
from tkinter import messagebox

def evaluate_expression():
    try:
        expr = entry.get()
        result = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неверное выражение: {e}")

def solve_equation():
    try:
        equation = entry.get().replace("=", "-")
        equation = equation.replace("x", "*x") if "x" in equation and "*" not in equation else equation
        def f(x):
            return eval(equation)
        
        a, b = -1000, 1000
        while b - a > 1e-6:
            mid = (a + b) / 2
            if f(mid) * f(a) <= 0:
                b = mid
            else:
                a = mid
        x = round((a + b) / 2, 6)
        
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(x))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неверное уравнение: {e}")

def clear_entry():
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x250")

entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

btn_calc = tk.Button(frame, text="Вычислить", command=evaluate_expression, width=10)
btn_calc.grid(row=0, column=0, padx=5, pady=5)

btn_solve = tk.Button(frame, text="Решить уравнение", command=solve_equation, width=15)
btn_solve.grid(row=0, column=1, padx=5, pady=5)

btn_clear = tk.Button(root, text="Очистить", command=clear_entry, width=10)
btn_clear.pack(pady=5)

root.mainloop()

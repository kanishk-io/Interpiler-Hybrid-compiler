import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import io
from interpreter_engine import parser, ASTBuilder, interpret_terminal

def run_interpreter(code):
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        # Show compiler & interpreter status in the status box
        status_box.config(state="normal")
        status_box.delete("1.0", tk.END)
        status_box.insert(tk.END, "Compiler is working ......\n")
        status_box.insert(tk.END, "Interpreter is running .....\n")
        status_box.config(state="disabled")

        tree = parser.parse(code)
        tree = ASTBuilder().transform(tree)
        interpret_terminal(tree)

        output = mystdout.getvalue()
        sys.stdout = old_stdout
        return output, None
    except Exception as e:
        sys.stdout = old_stdout
        return "", str(e)

def run_code():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo("Info", "Please enter some code.")
        return

    output, error = run_interpreter(code)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    if error:
        messagebox.showerror("Error", f"Error during execution:\n{error}")
        status_box.config(state="normal")
        status_box.insert(tk.END, "Execution failed.\n")
        status_box.config(state="disabled")
    else:
        output_box.insert(tk.END, output)
        status_box.config(state="normal")
        status_box.insert(tk.END, "Execution finished.\n")
        status_box.config(state="disabled")

def quit_app():
    root.destroy()

# GUI layout
root = tk.Tk()
root.title("Interpiler GUI")
root.geometry("850x500")
root.resizable(False, False)

code_input = scrolledtext.ScrolledText(root, font=("Courier", 12))
code_input.place(x=10, y=10, width=600, height=480)

status_label = tk.Label(root, text="Status", font=("Arial", 10, "bold"))
status_label.place(x=630, y=10)

status_box = tk.Text(root, height=5, font=("Arial", 10), state="disabled", bg="#f0f0f0")
status_box.place(x=630, y=30, width=200, height=100)

output_label = tk.Label(root, text="Final Output", font=("Arial", 10, "bold"))
output_label.place(x=630, y=140)

output_box = tk.Text(root, height=10, font=("Courier", 11), state="disabled", bg="white")
output_box.place(x=630, y=160, width=200, height=220)

run_button = tk.Button(root, text="Run Code", command=run_code,
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=2)
run_button.place(x=630, y=400, width=90, height=40)

quit_button = tk.Button(root, text="Quit", command=quit_app,
                        bg="#f44336", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=2)
quit_button.place(x=740, y=400, width=90, height=40)

root.mainloop()

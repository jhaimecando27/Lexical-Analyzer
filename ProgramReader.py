# Importing required modules
import tkinter as tk
import time
from LexicalAnalyser import lexical_analysis


# AnalyzerGui class
class AnalyzerGui:
    def __init__(self):
        # Initializing the main window
        self.root = tk.Tk()
        self.root.title("Automata Theory Analyser")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="lightblue")
        self.tokens = []

        # Frame Sections
        # For the Code Input
        self.inputFrame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.inputFrame.place(relx=0.005, rely=0.01, relwidth=0.678, relheight=0.7)

        # For the Error/s Display
        self.errorFrame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.errorFrame.place(relx=0.005, rely=0.725, relwidth=0.678, relheight=0.255)

        # For Tokenization Table
        self.tableFrame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.tableFrame.place(relx=0.692, rely=0.01, relwidth=0.3, relheight=0.97)

        # Widgets
        self.lexBtn = tk.Button(
            self.inputFrame,
            text="Lexicon",
            font=("Arial", 12),
            activebackground="lightblue",
            command=self.lexeme_check,
        )
        self.lexBtn.place(x=10, y=14)

        self.errorLbl = tk.Label(
            self.errorFrame, text="Error/s", font=("Arial", 14, "bold")
        )
        self.errorLbl.pack(anchor="w")

        self.errorTxt = tk.Text(
            self.errorFrame,
            font=("Arial", 12),
            bd=2,
            relief="solid",
            state="disabled",
        )
        self.errorTxt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.lexicLbl = tk.Label(
            self.tableFrame, text="Lexeme", font=("Arial", 14, "bold")
        )
        self.lexicLbl.grid(row=0, column=0, padx=(5, 0))

        self.tokenLbl = tk.Label(
            self.tableFrame, text="Token", font=("Arial", 14, "bold")
        )
        self.tokenLbl.grid(row=0, column=1, padx=(10, 0))

        self.lexicTxt = tk.Text(
            self.tableFrame, font=("Arial", 14), bd=2, relief="solid", state="disabled"
        )
        self.lexicTxt.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="nsew")

        self.tokenTxt = tk.Text(
            self.tableFrame, font=("Arial", 14), bd=2, relief="solid", state="disabled"
        )
        self.tokenTxt.grid(row=1, column=1, padx=5, pady=(5, 5), sticky="nsew")

        self.tableFrame.columnconfigure(0, weight=1)
        self.tableFrame.columnconfigure(1, weight=1)
        self.tableFrame.rowconfigure(1, weight=1)

        self.progTxt = tk.Text(self.inputFrame, wrap="none")
        self.progTxt.place(x=10, y=65, relwidth=0.975, relheight=0.825)

        self.root.mainloop()

    def lexeme_check(self):
        self.lexicTxt.configure(state="normal")
        self.tokenTxt.configure(state="normal")
        self.errorTxt.configure(state="normal")

        # Clear ouput boxes
        self.lexicTxt.delete('1.0', tk.END)
        self.tokenTxt.delete('1.0', tk.END)
        self.errorTxt.delete('1.0', tk.END)

        prog = self.progTxt.get("1.0", "end-1c")
        lines = prog.splitlines(True)

        errors = []

        line_num = 1

        for line in lines:
            # TEST
            start = time.time()
            print(line)
            self.tokens = lexical_analysis(line + "\n")
            # TEST
            end = time.time()
            print(str(end - start) + "s")

            for lexeme, token in self.tokens:
                self.insert_centered(self.lexicTxt, f"{lexeme}\n")
                self.insert_centered(self.tokenTxt, f"{token}\n")

                if lexeme == "unknown":
                    errors.append(
                        "line "
                        + str(line_num)
                        + ": '"
                        + line.replace("\n", "")
                        + "'"
                        + "\n\tLexical Error: Unknown"
                    )

            line_num += 1

        for error in errors:
            self.errorTxt.insert(tk.END, f"{error}\n")

        self.lexicTxt.configure(state="disabled")
        self.tokenTxt.configure(state="disabled")
        self.errorTxt.configure(state="disabled")

    def insert_centered(self, text_widget, content):
        text_widget.insert(tk.END, content, "centered")
        text_widget.tag_configure("centered", justify="center")
        text_widget.tag_add("centered", "1.0", "end")


# Main function
if __name__ == "__main__":
    AnalyzerGui()

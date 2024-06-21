import tkinter as tk
from tkinter import ttk
import math
from tkinter.font import Font

EXCHANGE_RATES = {"INR": 1, "EUR": 0.011, "USD": 0.012, "GBP": 0.0095}

class LoanCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Calculator")

        style = ttk.Style()
        style.theme_use('clam')

        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Define fonts
        self.normal_font = Font(family="Arial", size=10)
        self.bold_font = Font(family="Arial", size=10, weight="bold")

        self.entries = {}
        fields = [
            ("Principal Amount (INR):", "principal"),
            ("Annual Interest Rate (%):", "interest"),
            ("Loan Tenure (years):", "tenure"),
            ("Foreclosure (years):", "foreclosure")
        ]

        for i, (label, field) in enumerate(fields):
            ttk.Label(self.main_frame, text=label, font=self.normal_font).grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            entry = ttk.Entry(self.main_frame, width=30, font=self.normal_font)
            entry.grid(row=i, column=1, sticky='w', padx=(0, 20), pady=5)
            self.entries[field] = entry

        self.entries['foreclosure'].insert(0, "7")
        self.entries['principal'].insert(0, "3000000")
        self.entries['tenure'].insert(0, "14")

        self.currency_var = tk.StringVar(value="INR")
        ttk.Label(self.main_frame, text="Display Currency:", font=self.normal_font).grid(row=4, column=0, sticky='e', padx=(0, 10), pady=10)
        currency_frame = ttk.Frame(self.main_frame)
        currency_frame.grid(row=4, column=1, sticky='w', pady=10)
        for i, currency in enumerate(EXCHANGE_RATES.keys()):
            ttk.Radiobutton(currency_frame, text=currency, variable=self.currency_var, value=currency, style='TRadiobutton').grid(row=0, column=i, padx=(0, 10))

        ttk.Button(self.main_frame, text="Calculate", command=self.calculate_and_display, style='TButton').grid(row=5, column=0, columnspan=2, pady=20)

        self.output_text = tk.Text(self.main_frame, height=9, width=60, wrap=tk.WORD, font=self.normal_font)
        self.output_text.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.schedule_tree = ttk.Treeview(self.main_frame, columns=('Month', 'Principal', 'Interest', 'Payment', 'Balance'), show='headings', height=5)
        for col in self.schedule_tree['columns']:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=100, anchor='center')
        self.schedule_tree.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

        self.theme_var = tk.StringVar(value="Light")
        ttk.Checkbutton(self.main_frame, text="Dark Mode", variable=self.theme_var, onvalue="Dark", offvalue="Light", command=self.toggle_theme, style='TCheckbutton').grid(row=8, column=0, columnspan=2, pady=10)

        style.configure("Dark.Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E", font=self.normal_font)
        style.configure("Light.Treeview", background="white", foreground="black", fieldbackground="white", font=self.normal_font)
        style.configure('TRadiobutton', font=self.normal_font)
        style.configure('TButton', font=self.normal_font)
        style.configure('TCheckbutton', font=self.normal_font)

    def calculate_and_display(self):
        try:
            principal = float(self.entries['principal'].get())
            rate = float(self.entries['interest'].get()) / 100 / 12
            tenure = int(self.entries['tenure'].get()) * 12
            foreclosure = int(self.entries['foreclosure'].get() or "7") * 12
            currency = self.currency_var.get()

            monthly_payment = principal * (rate * (1 + rate) ** tenure) / ((1 + rate) ** tenure - 1)
            total_amount = monthly_payment * tenure
            
            schedule = []
            balance = principal
            total_interest = 0
            for month in range(1, tenure + 1):
                interest = balance * rate
                principal_paid = monthly_payment - interest
                balance -= principal_paid
                total_interest += interest
                schedule.append((month, principal_paid, interest, monthly_payment, balance))

            remaining_at_fc = next(payment[4] for payment in schedule if payment[0] == foreclosure)
            extra = remaining_at_fc / foreclosure

            def format_currency(amount):
                return f"{currency} {math.ceil(amount * EXCHANGE_RATES[currency]):,}"

            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Total Amount: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(total_amount)}\n", "normal")
            self.output_text.insert(tk.END, "Monthly Payment: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(monthly_payment)}\n", "normal")
            self.output_text.insert(tk.END, f"\nForeclosure ({foreclosure//12} years) amount: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(remaining_at_fc)}\n", "normal")
            self.output_text.insert(tk.END, "Monthly extra needed: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(extra)}\n", "normal")
            self.output_text.insert(tk.END, "New EMI: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(monthly_payment + extra)}\n", "normal")
            self.output_text.insert(tk.END, "\nTotal Interest: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(total_interest)}\n", "normal")
            self.output_text.insert(tk.END, "Interest Amount Paid Per Year: ", "bold")
            self.output_text.insert(tk.END, f"{format_currency(total_interest / (tenure / 12))}\n", "normal")

            self.output_text.tag_configure("bold", font=self.bold_font)
            self.output_text.tag_configure("normal", font=self.normal_font)

            self.schedule_tree.delete(*self.schedule_tree.get_children())
            for payment in schedule:
                self.schedule_tree.insert('', 'end', values=[payment[0]] + [format_currency(amount) for amount in payment[1:]])

        except ValueError:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Please enter valid numeric values for all fields.")

    def toggle_theme(self):
        is_dark = self.theme_var.get() == "Dark"
        bg_color = "#1E1E1E" if is_dark else "white"
        fg_color = "white" if is_dark else "black"
        entry_bg = "#2E2E2E" if is_dark else "white"
        self.root.configure(bg=bg_color)
        style = ttk.Style()
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=self.normal_font)
        style.configure("TButton", background=entry_bg, foreground=fg_color, font=self.normal_font)
        style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color, font=self.normal_font)
        style.configure("TRadiobutton", background=bg_color, foreground=fg_color, font=self.normal_font)
        style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=self.normal_font)
        style.configure("TFrame", background=bg_color)
        self.output_text.configure(bg=entry_bg, fg=fg_color)
        self.schedule_tree.configure(style=f"{'Dark' if is_dark else 'Light'}.Treeview")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculator(root)
    root.mainloop()
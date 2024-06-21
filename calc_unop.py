#Relatively un-optimised version of the app

import tkinter as tk
from tkinter import ttk
import math

# Exchange rates as of April 2024 (approximate)
EXCHANGE_RATES = {
    "INR": 1,
    "EUR": 0.011,
    "USD": 0.012,
    "GBP": 0.0095
}

def calculate_amortization(principal, annual_rate, tenure):
    monthly_rate = (annual_rate / 100) / 12
    total_payments = tenure * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / ((1 + monthly_rate) ** total_payments - 1)
    
    #amortization schedule
    amortization_schedule = []
    remaining_balance = principal
    yearly_interest = {year: 0 for year in range(1, tenure + 1)}

    for payment_number in range(1, total_payments + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        year = (payment_number - 1) // 12 + 1
        yearly_interest[year] += interest_payment
        
        amortization_schedule.append({
            "Payment Number": payment_number,
            "Principal Payment": round(principal_payment, 2),
            "Interest Payment": round(interest_payment, 2),
            "Total Payment": round(monthly_payment, 2),
            "Remaining Balance": round(remaining_balance, 2)
        })
    
    return monthly_payment, amortization_schedule, yearly_interest


def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    return amount * EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]

def calculate_and_display():
    principal_amount = float(principal_entry.get())
    annual_interest_rate = float(interest_entry.get())
    loan_tenure = int(tenure_entry.get())
    foreclosure = int(foreclosure_entry.get()) if foreclosure_entry.get() else 7  # Default to 7 if empty
    selected_currency = currency_var.get()

    monthly_payment, schedule, yearly_interest = calculate_amortization(principal_amount, annual_interest_rate, loan_tenure)
    total_amount = monthly_payment * loan_tenure * 12
    remaining_at_fc = schedule[(foreclosure * 12) - 1]["Remaining Balance"]
    extra = remaining_at_fc / (foreclosure * 12)

    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"\nTotal Amount to be paid: {selected_currency} {math.ceil(convert_currency(total_amount, 'INR', selected_currency))}\n")
    output_text.insert(tk.END, f"Monthly Payment: {selected_currency} {math.ceil(convert_currency(monthly_payment, 'INR', selected_currency))}\n")
    output_text.insert(tk.END, f"\nFor a foreclosure in {foreclosure} years, amount left after initial repayment: {selected_currency} {math.ceil(convert_currency(remaining_at_fc, 'INR', selected_currency))}\n")
    output_text.insert(tk.END, f"In which case, a monthly extra of {selected_currency} {math.ceil(convert_currency(extra, 'INR', selected_currency))} needs to be saved\n")
    output_text.insert(tk.END, f"New EMI: {selected_currency} {math.ceil(convert_currency(monthly_payment + extra, 'INR', selected_currency))}\n")
    output_text.insert(tk.END, "\nYearly Interest Paid:\n")
    for year, interest in yearly_interest.items():
        if year <= foreclosure+1:
            output_text.insert(tk.END, f"Year {year}: {selected_currency} {math.ceil(convert_currency(interest, 'INR', selected_currency))}\n")

    schedule_tree.delete(*schedule_tree.get_children())
    schedule_tree.insert('', 'end', values=('Payment Number', 'Principal Payment', 'Interest Payment', 'Total Payment', 'Remaining Balance'))
    for payment in schedule:
        schedule_tree.insert('', 'end', values=(
            payment["Payment Number"],
            f'{selected_currency} {math.ceil(convert_currency(payment["Principal Payment"], "INR", selected_currency))}',
            f'{selected_currency} {math.ceil(convert_currency(payment["Interest Payment"], "INR", selected_currency))}',
            f'{selected_currency} {math.ceil(convert_currency(payment["Total Payment"], "INR", selected_currency))}',
            f'{selected_currency} {math.ceil(convert_currency(payment["Remaining Balance"], "INR", selected_currency))}'
        ))

def toggle_theme():
    if theme_var.get() == "Dark":
        root.configure(bg="black")
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TButton", background="gray", foreground="white")
        style.configure("TEntry", fieldbackground="gray", foreground="white")
        style.configure("TRadiobutton", background="black", foreground="white")
        output_text.configure(bg="gray", fg="white")
        schedule_tree.configure(style="Dark.Treeview")
    else:
        root.configure(bg="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TButton", background="lightgray", foreground="black")
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TRadiobutton", background="white", foreground="black")
        output_text.configure(bg="white", fg="black")
        schedule_tree.configure(style="Light.Treeview")

root = tk.Tk()
root.title("Loan Interest Calculator")

style = ttk.Style()
style.theme_use('clam')

# Main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

principal_label = ttk.Label(main_frame, text="Principal Amount (INR):")
principal_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
principal_entry = ttk.Entry(main_frame)
principal_entry.grid(row=0, column=1, padx=5, pady=5)

interest_label = ttk.Label(main_frame, text="Annual Interest Rate (%):")
interest_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
interest_entry = ttk.Entry(main_frame)
interest_entry.grid(row=1, column=1, padx=5, pady=5)

tenure_label = ttk.Label(main_frame, text="Loan Tenure (years):")
tenure_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
tenure_entry = ttk.Entry(main_frame)
tenure_entry.grid(row=2, column=1, padx=5, pady=5)

foreclosure_label = ttk.Label(main_frame, text="Foreclosure (years):")
foreclosure_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
foreclosure_entry = ttk.Entry(main_frame)
foreclosure_entry.grid(row=3, column=1, padx=5, pady=5)
foreclosure_entry.insert(0, "7")  # Default value

# Currency selection
currency_label = ttk.Label(main_frame, text="Display Currency:")
currency_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
currency_var = tk.StringVar(value="INR")
currency_frame = ttk.Frame(main_frame)
currency_frame.grid(row=4, column=1, padx=5, pady=5, sticky='w')
currencies = ["INR", "EUR", "USD", "GBP"]
for i, currency in enumerate(currencies):
    ttk.Radiobutton(currency_frame, text=currency, variable=currency_var, value=currency).grid(row=0, column=i, padx=5)

calculate_button = ttk.Button(main_frame, text="Calculate", command=calculate_and_display)
calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

output_text = tk.Text(main_frame, height=9, width=80)
output_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

schedule_tree = ttk.Treeview(main_frame, columns=('Payment Number', 'Principal Payment', 'Interest Payment', 'Total Payment', 'Remaining Balance'), show='headings', height=7)
schedule_tree.grid(row=7, column=0, columnspan=2, padx=1, pady=1)

# Configure table columns
schedule_tree.heading('Payment Number', text='Payment No.')
schedule_tree.column('Payment Number', width=80)
schedule_tree.heading('Principal Payment', text='Principal Payment')
schedule_tree.column('Principal Payment', width=120)
schedule_tree.heading('Interest Payment', text='Interest Payment')
schedule_tree.column('Interest Payment', width=120)
schedule_tree.heading('Total Payment', text='Total Payment')
schedule_tree.column('Total Payment', width=120)
schedule_tree.heading('Remaining Balance', text='Remaining Balance')
schedule_tree.column('Remaining Balance', width=120)

# Theme toggle
theme_var = tk.StringVar(value="Light")
theme_check = ttk.Checkbutton(main_frame, text="Dark Mode", variable=theme_var, onvalue="Dark", offvalue="Light", command=toggle_theme)
theme_check.grid(row=8, column=0, columnspan=2, pady=10)

# Configure dark mode styles
style.configure("Dark.Treeview", background="gray", foreground="white", fieldbackground="gray")
style.configure("Light.Treeview", background="white", foreground="black", fieldbackground="white")

root.mainloop()
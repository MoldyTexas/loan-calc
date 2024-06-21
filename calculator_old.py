import tkinter as tk
from tkinter import ttk
import math

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


def calculate_and_display():
    principal_amount = float(principal_entry.get())
    annual_interest_rate = float(interest_entry.get())
    loan_tenure = int(tenure_entry.get())
    foreclosure = int(foreclosure_entry.get())

    monthly_payment, schedule, yearly_interest = calculate_amortization(principal_amount, annual_interest_rate, loan_tenure)
    total_amount = monthly_payment * loan_tenure * 12
    remaining_at_fc = schedule[(foreclosure * 12) - 1]["Remaining Balance"]
    extra = remaining_at_fc / (foreclosure * 12)

    output_text.delete('1.0', tk.END) 
    output_text.insert(tk.END, f"\nToyal Amount to be paid: INR {math.ceil(total_amount)}\n")
    output_text.insert(tk.END, f"Monthly Payment: EUR {math.ceil(monthly_payment / 90)} or INR {math.ceil(monthly_payment)}\n")
    output_text.insert(tk.END, f"\nFor a foreclosure in {foreclosure} years, amount left after initial repayment: INR {math.ceil(remaining_at_fc)}\n")
    output_text.insert(tk.END, f"In which case, a monthly extra of EUR {math.ceil(extra / 90)} needs to be saved\n")
    output_text.insert(tk.END, f"New EMI: EUR {math.ceil(monthly_payment / 90) + math.ceil(extra / 90)} or INR {math.ceil(monthly_payment) + math.ceil(extra)}\n")
    output_text.insert(tk.END, "\nYearly Interest Paid:\n")
    for year, interest in yearly_interest.items():
        if year <= foreclosure+1:
            output_text.insert(tk.END, f"Year {year}: INR {math.ceil(interest)}\n")

    schedule_label = ttk.Label(root, text="Repayment Schedule:", font=('Arial', 11, 'bold'))
    schedule_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    schedule_tree.delete(*schedule_tree.get_children())
    schedule_tree.insert('', 'end', values=('Payment Number', 'Principal Payment', 'Interest Payment', 'Total Payment', 'Remaining Balance'))
    for payment in schedule:
        schedule_tree.insert('', 'end', values=(payment["Payment Number"], f'INR {payment["Principal Payment"]}', f'INR {payment["Interest Payment"]}', f'INR {payment["Total Payment"]}', f'INR {payment["Remaining Balance"]}'))


root = tk.Tk()
root.title("Loan Interest Calculator")

principal_label = ttk.Label(root, text="Principal Amount:")
principal_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
principal_entry = ttk.Entry(root)
principal_entry.grid(row=0, column=1, padx=5, pady=5)

interest_label = ttk.Label(root, text="Annual Interest Rate (%):")
interest_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
interest_entry = ttk.Entry(root)
interest_entry.grid(row=1, column=1, padx=5, pady=5)

tenure_label = ttk.Label(root, text="Loan Tenure (years):")
tenure_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
tenure_entry = ttk.Entry(root)
tenure_entry.grid(row=2, column=1, padx=5, pady=5)

foreclosure_label = ttk.Label(root, text="Foreclosure (years):")
foreclosure_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
foreclosure_entry = ttk.Entry(root)
foreclosure_entry.grid(row=3, column=1, padx=5, pady=5)

calculate_button = ttk.Button(root, text="Calculate", command=calculate_and_display)
calculate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# text area for output
output_text = tk.Text(root, height=9, width=80)
output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

schedule_tree = ttk.Treeview(root, columns=('Payment Number', 'Principal Payment', 'Interest Payment', 'Total Payment', 'Remaining Balance'), show='headings', height=7)
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

root.mainloop()
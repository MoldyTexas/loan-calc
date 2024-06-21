import math


val=22.5
annual_interest_rate = 11.15  
loan_tenure = 14 
foreclosure=7

principal_amount = val*100000
def calculate_amortization(principal, annual_rate, tenure):
   
    monthly_rate = (annual_rate / 100) / 12
    total_payments = tenure * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / ((1 + monthly_rate) ** total_payments - 1)
    
    # Generate the amortization schedule
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

monthly_payment, schedule, yearly_interest= calculate_amortization(principal_amount, annual_interest_rate, loan_tenure)
total_amount= monthly_payment*loan_tenure*12
remaining_at_fc=schedule[83]["Remaining Balance"]
extra=remaining_at_fc/(foreclosure*12)

print(f"\nToyal Amount to be paid: INR {math.ceil(total_amount)}")
print(f"Monthly Payment: EUR {math.ceil(monthly_payment/90)} or INR {math.ceil(monthly_payment)}")
print(f"\nFor a foreclosure in {foreclosure} years, amount left after initial repayment: INR {math.ceil(remaining_at_fc)}")
print(f"In which case, a monthly extra of EUR {math.ceil(extra/90)} needs to be saved")
print(f"New EMI: EUR {math.ceil(monthly_payment/90)+math.ceil(extra/90)}")
print("\nYearly Interest Paid:")
for year, interest in yearly_interest.items():
    if year<=8:
        print(f"Year {year}: INR {math.ceil(interest)}")




print("\nAmortization Schedule:")
print("{:<15} {:<20} {:<20} {:<15} {:<20}".format("Payment Number", "Principal Payment", "Interest Payment", "Total Payment", "Remaining Balance"))
for payment in schedule:
    print("{:<15} INR {:<19} INR {:<19} INR {:<14} INR {:<19}".format(payment["Payment Number"], payment["Principal Payment"], payment["Interest Payment"], payment["Total Payment"], payment["Remaining Balance"]))

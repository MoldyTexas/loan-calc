# Loan Calculator

Loan Calculator app; can calculate loan details, including monthly payments, total amount, foreclosure amounts, including an amortization schedule.

## Features

- Calculate monthly loan payments
- Display total loan amount and total interest
- Show foreclosure amount at a specified year
- Calculate extra monthly payment needed for early loan closure
- Provide an amortization schedule
- Support for multiple currencies (INR, EUR, USD, GBP)
- Dark mode option for comfortable viewing (cuz why not)

## Requirements

- Python 3.x

## Installation

Just clone this repository (main branch) or download the source code.

## Usage

1. Run the program by executing the Python script (or running directly from IDE):

   ```
   python loan_calculator.py
   ```

2. The Loan Calculator GUI will appear.

3. Enter the loan details:
   - Principal Amount (in INR)
   - Annual Interest Rate (in %)
   - Loan Tenure (in years)
   - Foreclosure (in years, 7yrs by default)

4. Select the desired display currency (INR, EUR, USD, or GBP).

5. Click the "Calculate" button to see the results.

6. The following results will be displayed:
   - Total Amount
   - Monthly Payment
   - Foreclosure amount
   - Extra monthly savings needed for foreclosure and subsequently new EMI
   - Total Interest and average interest paid per year (The latter for the purposes of tax benefits, albeit only for the first 8 years)

7. The amortization schedule will be displayed in the table below, showing details for each year of the loan.


## Customization

Exchange rates can be updated by modifying the `EXCHANGE_RATES` dictionary. Add or remove currencies and update the exchange rates as needed.

## License

This Loan Calculator is open-source software licensed under Modi Ji

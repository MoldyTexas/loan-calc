# Loan Calculator

This Loan Calculator is a Python application with a graphical user interface (GUI) built using Tkinter. It allows users to calculate loan details, including monthly payments, total amount, foreclosure amounts, and provides an amortization schedule.

## Features

- Calculate monthly loan payments
- Display total loan amount and total interest
- Show foreclosure amount at a specified year
- Calculate extra monthly payment needed for early loan closure
- Provide an amortization schedule
- Support for multiple currencies (INR, EUR, USD, GBP)
- Dark mode option for comfortable viewing

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository or download the source code.
2. Ensure you have Python 3.x installed on your system.
3. No additional libraries are required as the program uses only built-in Python modules.

## Usage

1. Run the program by executing the Python script:

   ```
   python loan_calculator.py
   ```

2. The Loan Calculator GUI will appear.

3. Enter the loan details:
   - Principal Amount (in INR)
   - Annual Interest Rate (in %)
   - Loan Tenure (in years)
   - Foreclosure (in years, optional)

4. Select the desired display currency (INR, EUR, USD, or GBP).

5. Click the "Calculate" button to see the results.

6. The results will be displayed in the text area, including:
   - Total Amount
   - Monthly Payment
   - Foreclosure amount (if applicable)
   - Monthly extra needed for foreclosure
   - New EMI (if paying extra for foreclosure)
   - Total Interest

7. An amortization schedule will be displayed in the table below, showing details for each year of the loan.

8. Toggle between light and dark modes using the "Dark Mode" checkbox for comfortable viewing in different lighting conditions.

## Customization

You can easily customize the currency options by modifying the `EXCHANGE_RATES` dictionary in the source code. Add or remove currencies and update the exchange rates as needed.

## Contributing

Contributions to improve the Loan Calculator are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This Loan Calculator is open-source software licensed under the MIT license.

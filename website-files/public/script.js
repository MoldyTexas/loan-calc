document.getElementById('calculate').addEventListener('click', calculateAndDisplay);
document.getElementById('back-button').addEventListener('click', showMainPage);
document.getElementById('currency').addEventListener('change', updateCurrency);

const EXCHANGE_RATES = { "INR": 1, "EUR": 0.011, "USD": 0.012, "GBP": 0.0095 };
let calculationResults = {};

document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add('dark-mode');
    showMainPage();
});

function showMainPage() {
    document.getElementById('main-page').style.display = 'block';
    document.getElementById('results-page').style.display = 'none';
    history.pushState({}, '', '');  // Clear the history state
}

function showResultsPage() {
    document.getElementById('main-page').style.display = 'none';
    document.getElementById('results-page').style.display = 'block';
}

function calculateAndDisplay() {
    const principal = parseFloat(document.getElementById('principal').value);
    const rate = parseFloat(document.getElementById('interest').value) / 100 / 12;
    const tenure = parseInt(document.getElementById('tenure').value) * 12;
    const foreclosure = parseInt(document.getElementById('foreclosure').value) * 12;

    if (isNaN(principal) || isNaN(rate) || isNaN(tenure) || isNaN(foreclosure)) {
        alert("Please enter valid numeric values for all fields.");
        return;
    }

    const monthlyPayment = principal * (rate * (1 + rate) ** tenure) / ((1 + rate) ** tenure - 1);
    const totalAmount = monthlyPayment * tenure;
    const schedule = [];
    let balance = principal;
    let totalInterest = 0;

    for (let month = 1; month <= tenure; month++) {
        const interest = balance * rate;
        const principalPaid = monthlyPayment - interest;
        balance -= principalPaid;
        totalInterest += interest;
        schedule.push([month, principalPaid, interest, monthlyPayment, balance]);
    }

    const remainingAtFc = schedule.find(payment => payment[0] === foreclosure)[4];
    const extra = remainingAtFc / foreclosure;

    calculationResults = {
        totalAmount,
        monthlyPayment,
        remainingAtFc,
        extra,
        totalInterest,
        schedule,
        tenure,
        foreclosure
    };

    updateCurrency();
    showResultsPage();
    history.pushState({}, '', '');  // Clear the history state
}

function updateCurrency() {
    const currency = document.getElementById('currency').value;
    const formatCurrency = amount => `${currency} ${Math.ceil(amount * EXCHANGE_RATES[currency]).toLocaleString()}`;

    const resultsHTML = `
        <p><strong>Total Amount:</strong> ${formatCurrency(calculationResults.totalAmount)}</p>
        <p><strong>Monthly Payment:</strong> ${formatCurrency(calculationResults.monthlyPayment)}</p>
        <p><strong>Foreclosure (${calculationResults.foreclosure / 12} years) amount:</strong> ${formatCurrency(calculationResults.remainingAtFc)}</p>
        <p><strong>Monthly extra needed:</strong> ${formatCurrency(calculationResults.extra)}</p>
        <p><strong>New EMI:</strong> ${formatCurrency(calculationResults.monthlyPayment + calculationResults.extra)}</p>
        <p><strong>Total Interest:</strong> ${formatCurrency(calculationResults.totalInterest)}</p>
        <p><strong>Interest Amount Paid Per Year:</strong> ${formatCurrency(calculationResults.totalInterest / (calculationResults.tenure / 12))}</p>
    `;

    const scheduleHTML = calculationResults.schedule.map(payment => `
        <tr>
            <td>${payment[0]}</td>
            <td>${formatCurrency(payment[1])}</td>
            <td>${formatCurrency(payment[2])}</td>
            <td>${formatCurrency(payment[3])}</td>
            <td>${formatCurrency(payment[4])}</td>
        </tr>
    `).join('');

    document.getElementById('results').innerHTML = resultsHTML;
    document.getElementById('schedule').querySelector('tbody').innerHTML = scheduleHTML;
}
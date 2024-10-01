import argparse

import matplotlib.pyplot as plt


def simulate_mortgage_or_invest(initial_loan, interest_rate, monthly_payment,
                                minimum_amortization, investment_return,
                                years):

    # Convert interest rate and investment return percentages to decimals
    interest_rate /= 100
    investment_return /= 100

    if monthly_payment <= minimum_amortization + (initial_loan *
                                                  (interest_rate / 12)):
        print(
            f"Monthly payment must be greater than {minimum_amortization + (initial_loan * (interest_rate / 12)):.2f}, the minimum amortization and interest on the mortgage."
        )
        exit(1)

    # Simulation parameters
    months = years * 12  # Conversion to months

    # Function to simulate Scenario 1
    def scenario_1():
        loan_balance = initial_loan
        invested_amount = 0
        loan_balances = []
        investment_balances = []

        for month in range(months):
            # Payment for interest and amortization
            monthly_interest = loan_balance * (interest_rate / 12)
            amortization = monthly_payment - monthly_interest
            loan_balance -= amortization

            if loan_balance < 0:
                loan_balance = 0

            # Once the loan is paid off, the family starts investing the full amount each month
            if loan_balance == 0:
                invested_amount = invested_amount * (
                    1 + investment_return / 12) + monthly_payment
            else:
                invested_amount = invested_amount * (1 +
                                                     investment_return / 12)

            loan_balances.append(loan_balance)
            investment_balances.append(invested_amount)

        return loan_balances, investment_balances

    # Function to simulate Scenario 2
    def scenario_2():
        loan_balance = initial_loan
        invested_amount = 0
        loan_balances = []
        investment_balances = []

        for month in range(months):
            # Payment for interest and minimum amortization
            monthly_interest = loan_balance * (interest_rate / 12)
            amortization = min(minimum_amortization, loan_balance)
            loan_balance -= amortization

            if loan_balance < 0:
                loan_balance = 0

            # Invest the difference between the monthly payment and (interest + amortization)
            investment = monthly_payment - monthly_interest - amortization
            invested_amount = invested_amount * (
                1 + investment_return / 12) + investment

            loan_balances.append(loan_balance)
            investment_balances.append(invested_amount)

        return loan_balances, investment_balances

    # Simulate both scenarios
    loan_scenario_1, investment_scenario_1 = scenario_1()
    loan_scenario_2, investment_scenario_2 = scenario_2()

    # Get final investment amounts for each scenario
    final_investment_scenario_1 = investment_scenario_1[-1]
    final_investment_scenario_2 = investment_scenario_2[-1]

    # Plot the graph
    plt.figure(figsize=(12, 6))

    # Scenario 1
    plt.subplot(1, 2, 1)
    plt.plot(loan_scenario_1, label='Loan Balance')
    plt.plot(investment_scenario_1, label='Investments')
    plt.title(
        f'Scenario 1: Pay off first, invest later\nFinal Investment: {final_investment_scenario_1:,.2f} SEK'
    )
    plt.xlabel('Months')
    plt.ylabel('Amount (SEK)')
    plt.legend()
    plt.grid()

    # Scenario 2
    plt.subplot(1, 2, 2)
    plt.plot(loan_scenario_2, label='Loan Balance')
    plt.plot(investment_scenario_2, label='Investments')
    plt.title(
        f'Scenario 2: Pay interest + minimum amortization, invest the rest\nFinal Investment: {final_investment_scenario_2:,.2f} SEK'
    )
    plt.xlabel('Months')
    plt.ylabel('Amount (SEK)')
    plt.legend()
    plt.grid()

    # Save the graph to file
    plt.tight_layout()
    plt.savefig('result.png')

    # Calculate the number of months before the loan is paid off in Scenario 1
    months_to_payoff_scenario_1 = next(
        (i for i, balance in enumerate(loan_scenario_1) if balance == 0),
        months)

    # Calculate the number of months before the loan is paid off in Scenario 2
    months_to_payoff_scenario_2 = next(
        (i for i, balance in enumerate(loan_scenario_2) if balance == 0),
        months)

    # Print the results
    print(f"Simulation Parameters:")
    print(f"Initial Loan Amount: {initial_loan:,.2f} SEK")
    print(f"Annual Interest Rate: {interest_rate * 100:.2f}%")
    print(f"Monthly Payment: {monthly_payment:,.2f} SEK")
    print(f"Minimum Monthly Amortization: {minimum_amortization:,.2f} SEK")
    print(f"Annual Investment Return: {investment_return * 100:.2f}%")
    print(f"Years: {years}")

    print("\nResults:")
    print(f"Scenario 1: Pay off first, invest later")
    print(
        f"In this scenario, the family pays off the loan first, using the full {monthly_payment:,.2f} and then invests the amount each month."
    )
    print(f"Months to pay off loan: {months_to_payoff_scenario_1}")
    print(f"Final Investment Amount: {final_investment_scenario_1:,.2f} SEK")

    print(
        f"\nScenario 2: Pay interest + minimum amortization, invest the rest")
    print(
        f"In this scenario, the family pays the interest and minimum amortization on the loan first, and then invests the remaining amount each month."
    )
    print(f"Months to pay off loan: {months_to_payoff_scenario_2}")
    print(f"First amortization payment: {minimum_amortization:,.2f} SEK")
    print(
        f"Last amortization payment: {loan_scenario_2[months_to_payoff_scenario_2-1]:,.2f} SEK"
    )
    print(
        f"First investment amount: {monthly_payment - minimum_amortization:,.2f} SEK"
    )
    print(
        f"Monthly investment amount before loan is paid off: {monthly_payment - minimum_amortization:,.2f} SEK"
    )
    print(f"Last investment amount: {investment_scenario_2[-1]:,.2f} SEK")
    print(f"Final Investment Amount: {final_investment_scenario_2:,.2f} SEK")


# Example usage
# simulate_mortgage_or_invest(initial_loan=1_000_000,
#                             interest_rate=0.06,
#                             monthly_payment=10_000,
#                             minimum_amortization=2_000,
#                             investment_return=0.06,
#                             years=30)

if __name__ == '__main__':

    def get_args():
        parser = argparse.ArgumentParser(
            description='Simulate mortgage or invest scenarios.')
        parser.add_argument('--initial_loan',
                            type=float,
                            help='Initial loan amount')
        parser.add_argument('--interest_rate',
                            type=float,
                            help='Annual interest rate')
        parser.add_argument('--monthly_payment',
                            type=float,
                            help='Monthly payment amount')
        parser.add_argument('--minimum_amortization',
                            type=float,
                            help='Minimum monthly amortization')
        parser.add_argument('--investment_return',
                            type=float,
                            help='Annual investment return rate')
        parser.add_argument('--years',
                            type=int,
                            help='Number of years for the simulation')
        return parser.parse_args()

    def prompt_for_missing_args(args):
        if args.initial_loan is None:
            args.initial_loan = float(input('Enter initial loan amount: '))
        if args.interest_rate is None:
            args.interest_rate = float(input('Enter annual interest rate: '))
        if args.monthly_payment is None:
            args.monthly_payment = float(
                input('Enter monthly payment amount: '))
        if args.minimum_amortization is None:
            args.minimum_amortization = float(
                input('Enter minimum monthly amortization: '))
        if args.investment_return is None:
            args.investment_return = float(
                input('Enter annual investment return rate: '))
        if args.years is None:
            args.years = int(
                input('Enter number of years for the simulation: '))

    if __name__ == '__main__':
        args = get_args()
        prompt_for_missing_args(args)
        simulate_mortgage_or_invest(
            initial_loan=args.initial_loan,
            interest_rate=args.interest_rate,
            monthly_payment=args.monthly_payment,
            minimum_amortization=args.minimum_amortization,
            investment_return=args.investment_return,
            years=args.years)

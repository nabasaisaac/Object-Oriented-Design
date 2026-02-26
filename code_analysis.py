# Personal Budget Tracker - SYE3209 Software Construction Project
# A simple command-line app to help Mukono students track weekly spending

# Group Members:
# NABASA ISAAC          M23B23/043
# LAKICA LETICIA        M23B23/023
# ATWIJUKIRE APOPHIA    M23B23/051


# Configuration Constants
# These values can be changed easily without modifying logic

MIN_TRANSACTIONS = 5        
LINE_WIDTH = 50
WARNING_WIDTH = 60


def get_budget():
    
    # Step 1: Get the student's weekly/monthly budget
    # We keep asking until they give a valid positive number
    
    while True:
        try:
            budget = float(input("Enter your total budget for the period (e.g. 50000 UGX): "))

            if budget < 0:
                print("Budget cannot be negative. Please enter a valid amount.")
                continue

            if budget == 0:
                print("Budget cannot be zero. Please enter a positive amount.")
                continue

            return budget  # good input → return value

        except ValueError:
            print("Invalid input. Please enter a number (e.g. 75000).")


def enter_expenses(budget: float):
    
    # Prepare two important variables:
    #   - transactions → list that keeps every expense (description + amount)
    #   - total_spent  → running sum of all money spent

    transactions = []
    total_spent = 0.0

    
    # Step 2 & 3: Let user enter expenses until they say they're done
    # We check after each expense whether they've gone over budget
    
    print("Enter your expenses one by one.")
    print("When finished, type 'done' instead of a description.\n")

    while True:
        description = input("Expense description (or 'done' to finish): ").strip()

        # User wants to stop entering expenses
        if description.lower() == 'done':
            break

        # Prevent empty descriptions
        if not description:
            print("Description cannot be empty. Try again.")
            continue

        # Get the amount with error checking
        while True:
            try:
                amount = float(input(f"Amount for '{description}' (UGX): "))

                if amount <= 0:
                    print("Amount must be positive. Try again.")
                    continue

                break  # valid amount

            except ValueError:
                print("Invalid amount. Please enter a number.")

        # Save this expense
        transactions.append((description, amount))
        total_spent += amount

        # Quick check: are we still under budget?
        remaining = budget - total_spent

        if remaining >= 0:
            # Still okay → show friendly update
            print(f"Added. Current spending: {total_spent:,.0f} UGX | Remaining: {remaining:,.0f} UGX")
        else:
            # Oh no! Over budget → big warning
            overspent = -remaining
            print("!" * WARNING_WIDTH)
            print("   WARNING: BUDGET EXCEEDED!")
            print(f"   You have overspent by {overspent:,.0f} UGX")
            print(f"   Total spent now: {total_spent:,.0f} UGX (budget was {budget:,.0f} UGX)")
            print("!" * WARNING_WIDTH)

        print()

    return transactions, total_spent


def print_summary(budget: float, transactions: list, total_spent: float):
    
    # Step 4: Show the final report
    # Includes budget, total spent, balance/deficit and full list of expenses
    
    print("\n" + "=" * LINE_WIDTH)
    print("          FINANCIAL SUMMARY")
    print("=" * LINE_WIDTH)

    print(f"Initial budget:          {budget:>12,.0f} UGX")
    print(f"Total expenses:          {total_spent:>12,.0f} UGX")

    balance = budget - total_spent

    if balance >= 0:
        print(f"Remaining balance:       {balance:>12,.0f} UGX")
        print("\nWell done! You're within budget. 🎉")
    else:
        print(f"Deficit (overspent):     {abs(balance):>12,.0f} UGX")
        print("\nCaution: You have gone over budget! 😬")

    # Show all recorded expenses in a neat list
    print("\nTransaction log:")
    print("-" * LINE_WIDTH)

    if not transactions:
        print("No expenses were recorded.")
    else:
        for i, (desc, amt) in enumerate(transactions, 1):
            print(f"{i:2d}. {desc:<35} {amt:>10,.0f} UGX")

    print("-" * LINE_WIDTH)
    print("Thank you for using Mukono Student Budget Tracker!")
    print("Stay financially wise in university life! 💸")


def main():
    
    # Show welcome message
    # Makes the program feel friendly and student-oriented
    
    print("=======================================")
    print("   Welcome to Mukono Student Budget Tracker")
    print("   Keep track of your spending this week!")
    print("=======================================\n")

    budget = get_budget()

    print(f"\nBudget set to {budget:,.0f} UGX. Start entering your expenses.\n")

    transactions, total_spent = enter_expenses(budget)

    print_summary(budget, transactions, total_spent)


# Standard Python way to run the program only if this file is executed directly
if __name__ == "__main__":
    main()
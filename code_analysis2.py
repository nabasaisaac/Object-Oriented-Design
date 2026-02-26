# Personal Budget Tracker - SYE3209 Software Construction Project
# A simple command-line app to help Mukono students track spending
# Now fully OOP with encapsulation, inheritance and composition

# Group Members:
# NABASA ISAAC          M23B23/043
# LAKICA LETICIA        M23B23/023
# ATWIJUKIRE APOPHIA    M23B23/051

# Configuration Constants
LINE_WIDTH = 50
WARNING_WIDTH = 60

# Minimum reasonable budget per period 

MIN_BUDGETS = {
    "daily": 1000.0,
    "weekly": 10000.0,
    "monthly": 100000.0,
    "yearly": 1000000.0   
}


class FinancialRecord:
    """Base class demonstrating INHERITANCE.
    All financial items share amount validation and storage."""

    def __init__(self, amount: float):
        self.amount = amount   # uses setter for validation (encapsulation)

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        if value <= 0:
            raise ValueError("Amount must be positive.")
        self._amount = float(value)


class Transaction(FinancialRecord):
    """Represents one expense.
    Inherits from FinancialRecord (inheritance) and adds description.
    Full encapsulation with private attributes + getters/setters."""

    def __init__(self, description: str, amount: float):
        super().__init__(amount)                    # inheritance + validation from base
        self.description = description              # uses setter

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not value or not value.strip():
            raise ValueError("Description cannot be empty.")
        self._description = value.strip()

    def __str__(self):
        return f"{self.description:<35} {self.amount:>10,.0f} UGX"


class Budget:
    """Represents the chosen budget (amount + period).
    Encapsulation: private attributes, validation on creation."""

    def __init__(self, amount: float, period: str):
        self._period = self._validate_period(period)
        self._amount = self._validate_amount(amount, self._period)

    @staticmethod
    def _validate_period(period: str) -> str:
        period = period.lower().strip()
        if period not in MIN_BUDGETS:
            raise ValueError("Period must be daily, weekly, monthly or yearly.")
        return period

    @staticmethod
    def _validate_amount(amount: float, period: str) -> float:
        min_amount = MIN_BUDGETS[period]
        if amount < min_amount:
            raise ValueError(
                f"Budget for {period} cannot be below {min_amount:,.0f} UGX "
                f"(minimum reasonable amount)"
            )
        if amount <= 0:
            raise ValueError("Budget must be positive.")
        return amount

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def period(self) -> str:
        return self._period.capitalize()

    def __str__(self):
        return f"{self.amount:,.0f} UGX ({self.period} period)"


class BudgetTracker:
    """Main class of the application.
    Uses COMPOSITION: contains one Budget object + list of Transaction objects.
    All logic is inside methods (no global functions)."""

    def __init__(self):
        self._budget: Budget | None = None
        self._transactions: list[Transaction] = []

    @property
    def budget(self) -> Budget:
        """Encapsulation: controlled access to budget."""
        if self._budget is None:
            raise ValueError("Budget has not been set yet.")
        return self._budget

    def set_budget(self):
        """Ask user to choose period then enter amount (with minimum check)."""
        print("Choose budget period:")
        periods = ["daily", "weekly", "monthly", "yearly"]
        for i, p in enumerate(periods, 1):
            print(f"  {i}. {p.capitalize()}")

        while True:
            try:
                choice = int(input("\nEnter choice (1-4): "))
                if 1 <= choice <= 4:
                    period = periods[choice - 1]
                    break
                print("Please choose 1-4.")
            except ValueError:
                print("Please enter a number.")

        while True:
            try:
                prompt = f"Enter your total {period} budget (UGX, minimum {MIN_BUDGETS[period]:,.0f}): "
                amount = float(input(prompt))
                self._budget = Budget(amount, period)
                print(f"\n✅ Budget set: {self.budget}")
                return
            except ValueError as e:
                print(f"❌ {e}")

    def add_transaction(self, description: str, amount: float) -> Transaction:
        """Create and store a Transaction (composition)."""
        transaction = Transaction(description, amount)
        self._transactions.append(transaction)
        return transaction

    def get_total_spent(self) -> float:
        """Sum using composition (transactions list)."""
        return sum(t.amount for t in self._transactions)

    def enter_expenses(self):
        """Main loop for entering expenses + automatic editing menu after 'done'."""
        if self._budget is None:
            print("Please set budget first!")
            return

        print(f"\nEnter expenses for this {self.budget.period} period.")
        print("Type 'done' when finished.\n")

        while True:
            desc = input("Expense description (or 'done' to finish): ").strip()
            if desc.lower() == "done":
                break
            if not desc:
                print("Description cannot be empty.")
                continue

            while True:
                try:
                    amt = float(input(f"Amount for '{desc}' (UGX): "))
                    if amt <= 0:
                        print("Amount must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")


            self.add_transaction(desc, amt)

            total = self.get_total_spent()
            remaining = self.budget.amount - total

            if remaining >= 0:
                print(f"✅ Added. Spent: {total:,.0f} | Remaining: {remaining:,.0f} UGX")
            else:
                overspent = -remaining
                print("⛔" * WARNING_WIDTH)
                print("   ⚠️  WARNING: BUDGET EXCEEDED!")
                print(f"   You have overspent by {overspent:,.0f} UGX")
                print(f"   Total spent: {total:,.0f} UGX (budget was {self.budget.amount:,.0f} UGX)")
                print("⛔" * WARNING_WIDTH)
            print()

        # After user types 'done' → allow editing (as requested)
        if self._transactions:
            self._manage_transactions()

    def _manage_transactions(self):
        """Menu to edit, delete or add more transactions (editable feature)."""
        while True:
            print("\n" + "=" * LINE_WIDTH)
            print("   MANAGE YOUR TRANSACTIONS")
            print("=" * LINE_WIDTH)
            self._list_transactions()

            print("\nOptions:")
            print("1. Edit a transaction (fix mistakes)")
            print("2. Delete a transaction")
            print("3. Add another expense")
            print("4. Finish and see summary")

            choice = input("Enter 1-4: ").strip()

            if choice == "1":
                self._edit_transaction()
            elif choice == "2":
                self._delete_transaction()
            elif choice == "3":
                self._add_another_expense()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")

    def _list_transactions(self):
        if not self._transactions:
            print("   No transactions yet.")
            return
        for i, t in enumerate(self._transactions, 1):
            print(f"   {i:2d}. {t}")

    def _edit_transaction(self):
        """Allow user to edit description or amount of any transaction."""
        if not self._transactions:
            print("No transactions to edit.")
            return

        try:
            num = int(input(f"Which transaction to edit (1-{len(self._transactions)})? "))
            if 1 <= num <= len(self._transactions):
                trans = self._transactions[num - 1]
                print(f"Current → {trans}")

                new_desc = input("New description (press Enter to keep): ").strip()
                if new_desc:
                    trans.description = new_desc

                new_amt_str = input("New amount (press Enter to keep): ").strip()
                if new_amt_str:
                    try:
                        trans.amount = float(new_amt_str)
                        print("✅ Transaction updated!")
                    except ValueError:
                        print("Invalid amount – keeping old value.")
                else:
                    print("✅ Transaction updated!")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    def _delete_transaction(self):
        if not self._transactions:
            print("Nothing to delete.")
            return
        try:
            num = int(input(f"Which transaction to delete (1-{len(self._transactions)})? "))
            if 1 <= num <= len(self._transactions):
                deleted = self._transactions.pop(num - 1)
                print(f"🗑️  Deleted: {deleted}")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    def _add_another_expense(self):
        desc = input("New expense description: ").strip()
        if not desc:
            print("Cancelled.")
            return
        while True:
            try:
                amt = float(input(f"Amount for '{desc}' (UGX): "))
                if amt <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid number.")
        self.add_transaction(desc, amt)
        print("✅ Added!")

    def print_summary(self):
        """Final report (same style as original but improved)."""
        if self._budget is None:
            print("No budget was set.")
            return

        total_spent = self.get_total_spent()
        balance = self.budget.amount - total_spent

        print("\n" + "=" * LINE_WIDTH)
        print("          FINANCIAL SUMMARY")
        print("=" * LINE_WIDTH)

        print(f"Budget period:           {self.budget.period}")
        print(f"Initial budget:          {self.budget.amount:>12,.0f} UGX")
        print(f"Total expenses:          {total_spent:>12,.0f} UGX")

        if balance >= 0:
            print(f"Remaining balance:       {balance:>12,.0f} UGX")
            print("\n🎉 Well done! You stayed within budget.")
        else:
            print(f"Deficit (overspent):     {abs(balance):>12,.0f} UGX")
            print("\n⚠️  Caution: You have gone over budget!")

        print("\nTransaction log:")
        print("-" * LINE_WIDTH)
        if not self._transactions:
            print("No expenses were recorded.")
        else:
            for i, t in enumerate(self._transactions, 1):
                print(f"{i:2d}. {t}")
        print("-" * LINE_WIDTH)
        print("Thank you for using Mukono Student Budget Tracker!")
        print("Stay financially wise in university life! 💸")


def main():
    print("===============================================================")
    print("  💹 Welcome to Mukono Student Budget Tracker 💹")
    print("   Now supports yearly, monthly, weekly & daily budgets!")
    print("===============================================================\n")

    tracker = BudgetTracker()          # composition starts here

    tracker.set_budget()
    tracker.enter_expenses()           # includes editing capability
    tracker.print_summary()


if __name__ == "__main__":
    main()
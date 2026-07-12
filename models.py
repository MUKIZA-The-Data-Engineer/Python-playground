from dataclasses import dataclass
from typing import List

@dataclass
class TaxBracket:

    """
    Represents a single Tax brackets
    """

    lower: float
    upper: float
    rate: float

    def taxable_amount(self, salary: float) -> float:
        """Calculates how much of the salary falls into this bracket."""
        if salary <= self.lower:
             return 0.0
        return min(salary, self.upper) - self.lower

class TaxRegime:
    """Holds a collection of tax brackets and applies them progressively"""

    def __init__(self, brackets: list[TaxBracket]):

        self.brackets = sorted(brackets, key=lambda b: b.lower)

    def calculate_tax(self, gross_salary: float) -> float:
        """calculates total tax by iterating through all brackets."""
        if gross_salary < 0:
            raise ValueError("Salary cannot be negative")

        total_tax = 0.0
        for bracket in self.brackets:
            amount = bracket.taxable_amount(gross_salary)
            if amount > 0:
                total_tax += amount * bracket.rate
        return total_tax
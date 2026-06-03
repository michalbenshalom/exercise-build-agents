class Calculator:
    """Generic Calculator"""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a, b):
        return a ** b

    def modulo(self, a, b):   
        if b == 0:
            raise ValueError("Cannot modulo by zero")
        return a % b

    def average(self, *numbers):
        """Return the arithmetic mean of the provided numbers."""
        if not numbers:
            raise ValueError("At least one number is required")
        return sum(numbers) / len(numbers)


# Example usage:
if __name__ == "__main__":  
    calc = Calculator()
    print(calc.add(5, 3))        # Output: 8
    print(calc.subtract(5, 3))   # Output: 2
    print(calc.multiply(5, 3))   # Output: 15
    print(calc.divide(5, 3))     # Output: 1.6666666666666667
    print(calc.power(5, 3))      # Output: 125
    print(calc.modulo(5, 3))     # Output: 2
    print(calc.average(5, 3, 1))  # Output: 3.0

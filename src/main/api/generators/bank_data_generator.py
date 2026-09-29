import random


class BankDataGenerator:
    @staticmethod
    def generate_amount(
            minimum: float,
            maximum: float
    ) -> float:
        return round(
            random.uniform(minimum, maximum),
            2
        )

    @staticmethod
    def generate_integer(
            minimum: int,
            maximum: int
    ) -> int:
        return random.randint(minimum, maximum)



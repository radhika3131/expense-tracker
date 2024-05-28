# models.py
from datetime import datetime

class Expense:
    def __init__(self, date, amount, description, frequency, base=0):
        self.date = datetime.fromisoformat(date)
        self.amount = amount
        self.description = description
        self.frequency = frequency
        self.base = base

    def to_dict(self):
        return {
            'attributes': {
                'Date': self.date.isoformat(),
                'Amount': self.amount,
                'Description': self.description,
                'Frequency': self.frequency,
                'Base': self.base
            }
        }

    @staticmethod
    def from_dict(data):
        attributes = data['attributes']
        return Expense(
            date=attributes['Date'],
            amount=attributes['Amount'],
            description=attributes['Description'],
            frequency=attributes['Frequency'],
            base=attributes.get('Base', 0)
        )

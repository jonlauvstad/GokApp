import holidays

weekdays = [
    {"int": 0, "string": "mandag"},
    {"int": 1, "string": "tirsdag"},
    {"int": 2, "string": "onsdag"},
    {"int": 3, "string": "torsdag"},
    {"int": 4, "string": "fredag"},
    {"int": 5, "string": "lørdag"},
    {"int": 6, "string": "søndag"},
]

no_holidays = holidays.country_holidays("NO", years=(2024, 2025, 2026, 2027, 2028))
bank_holidays = list(no_holidays.keys())        # USE bank_holidays !!!
# print(bank_holidays)
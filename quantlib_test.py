import QuantLib as ql

today = ql.Date(7, 6, 2025)
ql.Settings.instance().evaluationDate = today
print(f"QuantLib successfully installed. Today is set to {today}.")

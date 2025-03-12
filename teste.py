from datetime import datetime

data = "2025-03-11 12:30:23"
data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
print(data.strftime("%d/%m/%Y %H:%M:%S"))
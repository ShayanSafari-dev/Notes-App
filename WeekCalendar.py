from datetime import datetime, timedelta

today = datetime.now()

days = []
dates = []
months = []

for i in range(7):
    current = today + timedelta(days=i)

    dates.append(current.strftime("%a"))
    days.append(int(current.strftime("%d"))) #int removes the zeros in a signle digit number: 06 => 6 or 09 => 9
    months.append(current.strftime("%b"))

# Month: "%b" | Day: "%a" | Date(only day): "%d"

#print(f'Days: {days}\n Dates: {dates}\n{months}')
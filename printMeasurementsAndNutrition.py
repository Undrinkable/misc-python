import datetime
import myfitnesspal
from datetime import datetime, timedelta, date
import sys

def main():
	start = getStartDate()
	end = getEndDate()

	if start > end:
		temp = end
		end = start
		start = temp
		print("Start date was after end date. Arguments were reversed.")

	client = getClient()

	weights = client.get_measurements('Weight', start, end)
	bodyfats = client.get_measurements('Body Fat %', start, end)

	printHeader()
	for date in daterange(start,end):
		print(str(date) + "\t" + bodyMeasurementsStringForDate(date, weights, bodyfats) + "\t" + nutritionStringForDate(date))

def getStartDate():
	if len(sys.argv) < 2:
		argError()
	return dateFromArg(1)

def getEndDate():
	if len(sys.argv) < 3:
		return date.today() + timedelta(days = 1)
	return dateFromArg(2)

def getClient():
	return myfitnesspal.Client('undrinkable')

def printHeader():
	print("date\tweight\tbodyfat\tnetcarbs\tfat\tprotein")		

def bodyMeasurementsStringForDate(date, weights, bodyfats):
	weight = 0
	if date in weights:
		weight = weights[date]
	bodyfat = 0
	if date in bodyfats:
		bodyfat = bodyfats[date]
	return str(weight) + "\t" + str(bodyfat)

def nutritionStringForDate(date):
	client = getClient()
	day = client.get_date(date)
	calories = 0
	if "calories" in day.totals:
		calories = day.totals["calories"]
	net_carbs = 0
	if "carbohydrates" in day.totals:
		if "fiber" in day.totals:
			net_carbs = day.totals["carbohydrates"] - day.totals["fiber"]
	protein = 0
	if "protein" in day.totals:
		protein = day.totals["protein"]
	fat = 0
	if "fat" in day.totals:
		fat = day.totals["fat"]
	return str(calories) + "\t" + str(net_carbs) + "\t" + str(fat) + "\t" + str(protein)

def dateFromArg(arg):
	argComponents = sys.argv[arg].split("/")
	if (len(argComponents) != 3):
		invalidDateArgError(sys.argv[arg])

	return date(int(argComponents[2]), int(argComponents[0]), int(argComponents[1]))

def invalidDateArgError(arg):
	print("Date argument is invalid: " + arg + ". Must be format mm/dd/yyyy")
	exit()

def argError():
	print("Invalid arguments given. Must supply start date (inclusive) as first argument and end date (exclusive) as second argument, with format mm/dd/yyyy")
	exit()
	
def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

if __name__ == '__main__':
	main()

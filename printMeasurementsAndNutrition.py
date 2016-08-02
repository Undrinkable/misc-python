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

	allData = []
	for date in daterange(start,end):
		dayData = { "date": date, "body": bodyMeasurementsForDate(date, weights, bodyfats), "nutrition": nutritionForDate(date) }
		allData.append(dayData)
	
	printData(allData)
    printNutritionAnalysis(allData)
    printWeightLossAnalysis(allData)
  
def printData(allData):
    printHeader()
    for day in allData:
        print('\t'.join([day["date"], day["body"], day["nutrition"]]))
	print("")
	
def printNutritionAnalysis(data):
    sum = 0
    for day in data:
        sum += day["nutrition"][0]
    
    print("---Nutrition---")
    print("Average daily calories: " + str(sum/len(data)))
    print("")
  
def printWeightLossAnalysis(data):
    weeklyLosses = []
    i = 0
    while i < len(data):
        if (i is not 0):
            weeklyLosses.append(data[i]["body"][0]-data[i-1]["body"][0])
    averageWeeklyLoss = sum(weeklyLosses)/len(weeklyLosses)
    
    sw = data[0][1]
    cw = data[-1][1]
    
    print("---Body---")
    print("Day " + str(len(data)) +" (wk " + str(len(weeklyLosses)) + "): " + str(cw-sw)
    print("Current weekly loss: " + str(averageWeeklyLoss))
    print("Projected weight in 1 week: " + str(cw+averageWeeklyLoss)
    print("Projected weight in 1 month: " + str(cw+averageWeeklyLoss*4)
    print("Projected weight in 3 months: " + str(cw+averageWeeklyLoss*12)
    print("Projected weight in 6 months: " + str(cw+averageWeeklyLoss*24)
    print("")

def getStartDate():
	if len(sys.argv) < 3:
		argError()
	return dateFromArg(2)

def getEndDate():
	if len(sys.argv) < 4:
		return date.today() + timedelta(days = 1)
	return dateFromArg(3)

def getClient():
	return myfitnesspal.Client(sys.argv[1])

def printHeader():
    print("---Data---")
	print('\t'.join(["date","weight","bodyfat","calories","netcarbs","fat","protein"])

def bodyMeasurementsForDate(date, weights, bodyfats):
	weight = 0
	if date in weights:
		weight = weights[date]
	bodyfat = 0
	if date in bodyfats:
		bodyfat = bodyfats[date]
	return weight, bodyfat

def nutritionForDate(date):
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
	return calories, net_carbs, fat, protein

def dateFromArg(arg):
	argComponents = sys.argv[arg].split("/")
	if (len(argComponents) != 3):
		invalidDateArgError(sys.argv[arg])

	return date(int(argComponents[2]), int(argComponents[0]), int(argComponents[1]))

def invalidDateArgError(arg):
	print("Date argument is invalid: " + arg + ". Must be format mm/dd/yyyy")
	exit()

def argError():
	print("Invalid arguments given. Must supply MFP username, start date (inclusive), and end date (exclusive). Dates should have format mm/dd/yyyy")
	exit()
	
def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

if __name__ == '__main__':
	main()

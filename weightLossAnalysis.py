from __future__ import print_function
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
	
	print("Opening connection...")
	client = getClient()
	
	print("Retrieving weight data...")
	weights = client.get_measurements('Weight', start, end)
	
	print("Performing analysis...")
	printWeightLossAnalysis(weights)
    
def printWeightLossAnalysis(data):
    weights = list(reversed(data.values()))
    
    weeklyLosses = []
    i = 0
    while i < len(weights)-7:
        i += 7
        weeklyLosses.append(weights[i]-weights[i-7])
    averageWeeklyLoss = sum(weeklyLosses)/len(weeklyLosses)
    sw = weights[0]
    cw = weights[-1]
    
    print("")
    print("---Body---")
    print("SW: " + str(sw) + " CW: " + str(cw))
    print("Day " + str(len(data)) +" (wk " + str(len(weeklyLosses)) + "): " + str(cw-sw))
    print("Average weekly loss: " + str(averageWeeklyLoss))
    print("Projected weight in 1 week: " + str(cw+averageWeeklyLoss))
    print("Projected weight in 1 month: " + str(cw+averageWeeklyLoss*4))
    print("Projected weight in 3 months: " + str(cw+averageWeeklyLoss*12))
    print("Projected weight in 6 months: " + str(cw+averageWeeklyLoss*24))
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

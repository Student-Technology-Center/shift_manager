import os
import pandas as pd
from datetime import datetime, time

def scrape_schedule(f):
    xl = pd.ExcelFile(f)

    if len(xl.sheet_names) > 1:
        print("More than one sheet name, using first sheet {}".format(xl.sheet_names[0]))

    sh = xl.parse(xl.sheet_names[0])
    
    start = 0
    end = 0
    time = { }
    return_list = []
    start_t = datetime.strptime('08:00', '%H:%M').time()

    #Figure out where the information is stored row wise
    for i in sh:
    	for c, j in enumerate(sh[i]):
    		if j == start_t and start == 0:
    			start = c
    		if j == start_t and c != start:
    			end = c

    sh = sh[start:end + 1]

    #Set up a dict to hash index -> datetime
    for c in range(0, (end - start) + 1):
    	time_s = str(c + 8)

    	if len(time_s) < 2:
    		time_s = "0" + time_s

    	time_s += ":00"
    	time[c] = datetime.strptime(time_s, '%H:%M').time()

    for i in sh:
        for c, j in enumerate(sh[i]):
            if type(j) != float and j != 'x' and type(j) != int:
                return_list.append((j, time[c]))

    return []

    new_list = [x for x in return_list if type(x[0]) == str]

    return [x for x in new_list if (x[0].lower() != 'noon')]

def main():
    scrape_schedule("schedule.xlsm")

if __name__ == '__main__':
    main()

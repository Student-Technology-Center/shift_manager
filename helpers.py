from django.contrib.auth import get_user_model

import os
import pandas as pd
from datetime import datetime, time, timedelta

from login.models import UserOptions
from utils.message import send_stc_email

from . models import Shift

USER_MODEL = get_user_model()

def scrape_schedule(f):
    for i in Shift.objects.all():
        i.delete()

    xl = pd.ExcelFile(f)

    if len(xl.sheet_names) > 1:
        print("More than one sheet name, using first sheet {}".format(xl.sheet_names[0]))

    sh = xl.parse(xl.sheet_names[0])
    
    start = 0
    end = 0
    time = { }
    return_list = []
    col_c = 0
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
            #Ensure it's data we want, the sheet returns weird stuff.
            if type(j) != float and j != 'x' and type(j) != int:
                return_list.append((j, time[c], get_day_by_column(col_c)))
        col_c += 1

    new_list = [x for x in return_list if type(x[0]) == str]

    return [x for x in new_list if (x[0].lower() != 'noon')]

def create_shifts(shifts, file_m):
    #Gets a set of datetime objects daily between two dates.
    delta = file_m.last_date - file_m.first_date
    dates = [file_m.first_date + timedelta(days=date) for date in range(delta.days + 1)]

    #Create all the date objects.
    for day in dates:
        for shift in shifts:
            dow     = shift[2]
            time    = shift[1]
            name    = shift[0]

            if get_day_by_value(day.weekday()).lower() == dow.lower():
                shift_item = Shift.objects.create(
                    day_of_week=dow,
                    date=day,
                    start=time,
                    sheet_user=name.lower()
                )

    claim_shifts()

def claim_shifts(request=None):
    shifts = Shift.objects.all()
    for shift in shifts:

        #Get the name as it appears on the excel sheet.
        sheet_name = shift.sheet_user

        try:
            matching_user = UserOptions.objects.get(shift_name=sheet_name.lower()).user
            shift.user = matching_user
            shift.save()
        except UserOptions.DoesNotExist:
            pass

#yep
def get_day_by_column(c):
    if c >= 1 and c < 4:
        return 'sunday'
    elif c >= 5 and c <= 11:
        return 'monday'
    elif c > 12 and c <= 18:
        return 'tuesday'
    elif c >= 20 and c <= 25:
        return 'wednesday'
    elif c >= 28 and c <= 33:
        return 'thursday'
    elif c >= 33 and c <= 39:
        return 'friday'
    elif c >= 41 and c <= 46:
        return 'saturday'

def get_day_by_value(c):
    if c == 0:
        return 'monday'
    if c == 1:
        return 'tuesday'
    if c == 2:
        return 'wednesday'
    if c == 3:
        return 'thursday'
    if c == 4:
        return 'friday'
    if c == 5:
        return 'saturday'
    if c == 6:
        return 'sunday'

from __future__ import print_function
import datetime

def update_current_route(current_route, line):
    sl_ind = line.find("= For route Silver Line ")
    route_ind = line.find("= For route ")
    if "= For all routes combined" in line:
        current_route = "all"
    elif sl_ind != -1:
        current_route = line[sl_ind + 12:line.find(" ", sl_ind + 24)]
    elif route_ind != -1:
        current_route = line[route_ind + 12:line.find(" ", route_ind + 12)]
    else:
        current_route = current_route
    return current_route

def update_current_pred_category(current_pred_category, line):
    if "For predictions of 0-5 minutes" in line:
        current_pred_category = "0-5 min"
    elif "For predictions of 0-10 minutes" in line:
        current_pred_category = "0-10 min"
    else:
        current_pred_category = current_pred_category
    return current_pred_category

def get_pred_stat(current_pred_category, line):
    one_min_ind = line.find("percent +/- 0-1 minutes: ")
    two_min_ind = line.find("percent +/- 0-2 minutes: ")
    if current_pred_category == "0-5 min" and one_min_ind != -1:
        stat = "+/- 1 min," + line[one_min_ind + 25:line.find(" ", one_min_ind + 25)]
    elif current_pred_category == "0-10 min" and two_min_ind != -1:
        stat = "+/- 2 min," + line[two_min_ind + 25:line.find(" ", two_min_ind + 25)]
    else:
        stat = "n/a"
    return stat

routes_to_include = ['all', '1', 'Silver Line SL1', '350', '131']

start_date = datetime.datetime(2017, 6, 19, 0, 0)
one_day = datetime.timedelta(days=1)
end_date = datetime.datetime(2017, 9, 18, 0, 0)

date = start_date
with open('output.csv', 'w') as outfile:
    print("date_type,date,route,category,threshold,percentage", file=outfile)
    while date <= end_date:
        date_str = date.strftime('%Y-%m-%d')
        date_type = "Weekday" if date.isoweekday() in range(1, 6) else "Weekend"
        filename = 'data/pa-mbta-rpt-' + date_str + '.txt'
        try:
            with open(filename, 'r') as f:
                current_route = "unknown"
                current_pred_category = "unknown"
                for line in f:
                    current_route = update_current_route(current_route, line)
                    current_pred_category = update_current_pred_category(current_pred_category, line)
                    current_pred_stat = get_pred_stat(current_pred_category, line)
                    if current_pred_stat != "n/a" and current_route in routes_to_include:
                        print(date_type + "," + date_str + "," + current_route + "," + current_pred_category + "," + current_pred_stat, file=outfile)
        except IOError:
            print("No file found at " + filename)
        date += one_day

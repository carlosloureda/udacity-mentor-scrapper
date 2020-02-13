import json


def get_previous_day(day, info_dict):
    while str(day) not in info_dict and day > 0:
        day -= 1
    return day


def get_next_day(day, info_dict):
    while str(day) not in info_dict and day < 121:
        day += 1
    return day


json_file = open('./api/recommended_dates.json')
data = json.load(json_file)
# print(data)
if "2" in data:
    print(data["2"])
date = 10
print(get_previous_day(date, data))
print(get_next_day(date, data))

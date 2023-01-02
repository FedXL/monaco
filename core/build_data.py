import datetime
from collections import OrderedDict
from dataclasses import dataclass
from os import path
from core.config import files, START,END,RACERS




@dataclass
class DATA:
    racers_info: dict       # INC: (Racer name , command)
    racers_initials: dict   # Racer name: INC
    time_start: dict        # INC: time_start
    time_end: dict          # INC: time_end
    time_lap: dict          # INC: time_lap
    score: dict             # INC: places


#----------------------READ FILES---------------------------------------------------------------------------------------

def read_folder(folder, file):
    parent_dir = path.abspath("../")
    with open(path.join(parent_dir, folder, file), "r") as record:
        text = record.readlines()
        lines = [line[:-1] for line in text if len(line) > 1]
    return lines


def choice_how_to_parce(file, text):
    assert file in files
    if file == RACERS:
        return racers_parcer(text)
    else:
        return timer_parcer(text)


def racers_parcer(text):
    initials_nameteam = {}
    name_initials = {}
    for line in text:
        line_clean = line.split("_")
        initials_nameteam[line_clean[0]] = (line_clean[1], line_clean[2])
        name_initials[line_clean[1]] = line_clean[0]
    return initials_nameteam, name_initials


def timer_parcer(lines):
    time = {}
    for line in lines:
        time[line[:3]] = line[3:].split("_")
    return time



#------------------------------------BUILDING DATA----------------------------------------------------------------------


def make_time_lap(data: DATA):
    keys = data.time_start.keys()
    inc_time = OrderedDict()
    for key in keys:
        time_start = [float(num) for num in data.time_start[key][1].replace(" ", "").split(":")]
        time_end = [float(num) for num in data.time_end[key][1].replace(" ", "").split(":")]
        tm1 = datetime.timedelta(hours=time_start[0], minutes=time_start[1], seconds=time_start[2])
        tm2 = datetime.timedelta(hours=time_end[0], minutes=time_end[1], seconds=time_end[2])
        inc_time[key] = tm2 - tm1
    result = sort_time_lap(inc_time)
    return result


def sort_time_lap(time_lap: OrderedDict):
    values = time_lap.values()
    new = {value: key for key, value in time_lap.items()}
    sorted_values = sorted(values)
    sorted_keys = [new[key] for key in sorted_values]
    result = OrderedDict({key: time_lap[key] for key in sorted_keys})
    result = make_dnf_in_rating(result)
    return result


def make_dnf_in_rating(result: OrderedDict):
    dnf_list = []
    for racer, time in result.items():
        if time.total_seconds() <= 0:
            dnf_list.append(racer)
    dnf_list = [racer for racer, time in result.items() if time.total_seconds() <= 0]
    for racer in dnf_list:
        result[racer] = "DNF"
        result.move_to_end(racer)
    return result


def make_score(time_lap):
    INC = list(time_lap.keys())
    score = {INC[place]: place +1 for place in range(len(INC))}
    return score




def build_data(folder, files):
    data = []
    for file in files:
        text = read_folder(folder, file)
        data.append(choice_how_to_parce(file, text))
    Data = DATA(racers_info=data[0][0],
                racers_initials=data[0][1],
                time_start=data[1],
                time_end=data[2],
                time_lap=OrderedDict(),
                score={})
    Data.time_lap = make_time_lap(Data)
    Data.score = make_score(Data.time_lap)
    return Data





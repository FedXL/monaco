from build_data import build_data
from core.config import  files
from core.build_data import DATA, build_data
from fuzzywuzzy import fuzz


def build_person_report(name):
    BigData = build_data("storage", files)

    for key in list(BigData.racers_initials.keys()):
        ratio = fuzz.ratio(key.lower(), name.lower())
        if ratio >=75:
            racer_key_name = key
            break
    INC = BigData.racers_initials[racer_key_name]
    place = BigData.score[INC]
    lap_time = BigData.time_lap[INC]
    command = BigData.racers_info[INC][1]
    print(place,racer_key_name,lap_time,command)

def build_total_report():
    BigData = build_data("storage", files)
    score = BigData.score
    fifteen = 0
    for INC,value in score.items():
        if fifteen == 15:
            print("-"*50)
        place = value
        racer_name = BigData.racers_info[INC][0]
        lap_time = BigData.time_lap[INC]
        command = BigData.racers_info[INC][1]
        print(place,racer_name,lap_time,command,sep=" | ")
        fifteen +=1








build_person_report("Kimi Raikkenen")
build_total_report()








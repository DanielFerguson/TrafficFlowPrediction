import sys
import csv

# Author: Daniel Ferguson
# Version: 1.0.0
# Date Created: 06/09/2019
# Last Updated: 12/09/2019

# Tested Python Version: 3.7.2
# Tested OS Version: Windows 10, Bash

# * Purpose
# To parse the data from the given excel spreadsheets of traffic data per SCAT location

# * Using the program
# `python data-parser.py`

# File nameing convention
# [SCAT ID]_[HF VicRoads Internal]_[VR Internal Stat]_[VR Internal Loc]_[NB_TYPE_SURVEY]_[DATE].csv

# Define Columns
# SCAT_NUM = 0
# VR_LOC = 1
# DATE = 2
# FIRST_TIME = 3

# Future
# Days
# MONDAY    = 2,9,16,23,30
# TUESDAY   = 3,10,17,24,31
# WEDNESDAY = 4,11,18,25
# THURSDAY  = 5,12,19,26
# FRIDAY    = 6,13,20,27
# SATURDAY  = 7,14,21,28
# SUNDAY    = 1,8,15,22,29

# Day Types
# Weekdays  = 2,3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30,31
# Weekends  = 1,7,8,14,15,21,22,28,29


times = [
    "0:00",
    "0:15",
    "0:30",
    "0:45",
    "1:00",
    "1:15",
    "1:30",
    "1:45",
    "2:00",
    "2:15",
    "2:30",
    "2:45",
    "3:00",
    "3:15",
    "3:30",
    "3:45",
    "4:00",
    "4:15",
    "4:30",
    "4:45",
    "5:00",
    "5:15",
    "5:30",
    "5:45",
    "6:00",
    "6:15",
    "6:30",
    "6:45",
    "7:00",
    "7:15",
    "7:30",
    "7:45",
    "8:00",
    "8:15",
    "8:30",
    "8:45",
    "9:00",
    "9:15",
    "9:30",
    "9:45",
    "10:00",
    "10:15",
    "10:30",
    "10:45",
    "11:00",
    "11:15",
    "11:30",
    "11:45",
    "12:00",
    "12:15",
    "12:30",
    "12:45",
    "13:00",
    "13:15",
    "13:30",
    "13:45",
    "14:00",
    "14:15",
    "14:30",
    "14:45",
    "15:00",
    "15:15",
    "15:30",
    "15:45",
    "16:00",
    "16:15",
    "16:30",
    "16:45",
    "17:00",
    "17:15",
    "17:30",
    "17:45",
    "18:00",
    "18:15",
    "18:30",
    "18:45",
    "19:00",
    "19:15",
    "19:30",
    "19:45",
    "20:00",
    "20:15",
    "20:30",
    "20:45",
    "21:00",
    "21:15",
    "21:30",
    "21:45",
    "22:00",
    "22:15",
    "22:30",
    "22:45",
    "23:00",
    "23:15",
    "23:30",
    "23:45"
]

file_name = './raw_data.csv'


def write_file(data):
    with open('data/' + 'something' + '_data.csv', mode='w') as open_file:
        file_writer = csv.writer(
            open_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in data:
            file_writer.writerow(row)


# SCAT, VR Internal, VR Internal Loc, Date, Single Time, Vehicle Amount
with open(file_name, "r") as file_data:
    csv_reader = csv.reader(file_data)

    last_scat = None
    last_vr = None

    for row in csv_reader:
        # Get the current details
        scat_id = row[0]
        vr_loc = row[1]
        date = row[2]

        if (scat_id == last_scat or last_scat == None and vr_loc == last_vr or last_vr == None):
            with open('data/' + scat_id + '_' + vr_loc + '_data.csv', mode='a', newline='') as f:
                f_writer = csv.writer(
                    f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

                f_writer.writerow(row)
        else:
            with open('data/' + scat_id + '_' + vr_loc + '_data.csv', mode='w', newline='') as f:
                f_writer = csv.writer(
                    f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

                f_writer.writerow(row)

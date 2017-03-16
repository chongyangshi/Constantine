#!/usr/bin/env python

# Automatically make Constantine posters in term time.
# Helper script useful for cron jobs.

import utils

import datetime
import subprocess
import sys

MAIN_TIMEOUT = 15

if (not 3 <= len(sys.argv) <= 4) or (sys.argv[1] in ['-h', '--help']):
    print("Usage: python auto_poster.py /path/to/Constantine /path/to/output.pdf [YYYY-MM-DD]")
    print("Helper script useful for cron jobs. Pass in the directory of Constantine's main.py for working directory purposes.")
    print("If no date is passed in as last parameter, today's date will be used to judge whether it's term time or not.")
    sys.exit(1)

constantine_directory = sys.argv[1]
output_file = sys.argv[2]
if len(sys.argv) == 4:
    set_date = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d")
else:
    set_date = datetime.datetime.today()

settings = utils.read_config()

next_monday = set_date + datetime.timedelta(days=(7 - set_date.weekday()))
term_start = datetime.datetime.strptime(utils.get_closest_date_time(next_monday, settings['term_start_dates']), "%Y-%m-%d")
date_param = datetime.datetime.strftime(set_date, "%Y-%m-%d")
week_number = int((next_monday - term_start).days / 7 + 1)

if (1 <= week_number <= 10):
    print("Running Constantine for Week " + str(week_number) + ".")
    p = subprocess.Popen(['python', 'main.py', output_file, date_param], stdout=subprocess.PIPE, cwd=constantine_directory)
    output = p.communicate(timeout=MAIN_TIMEOUT)
    print("Finished with code " + str(p.returncode))
    sys.exit(p.returncode) # Exit with the same code for monitoring purposes.
else:
    print("Not term time, not updating the PDF.")
    sys.exit(0)

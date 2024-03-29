import random
################################
# Global variables

# [Plot Info]
#
# Line's width
widthLine = 9

# [Simulation Info]
#
# Lenght of simulation
numberDays = 14

# [Work Info]
#
# You could start working since this hour
startHour = 7.0 
# You could work until this hour
endHour = 24.0 
# Hours that you have to rest during your shift
restHours = 0.5 
# Hours that you work
workHoursWeek = 40
# Days that you work in week (5 or 6)
workDayWeek = 5
#0 Monday, 1 Tuesday, ..., 6 Sunday, -1 Randomly
jobIndecesRestDays = [5, 6]
# Hours that must pass to start new shift
gapBetweenShifts = 11.0

jobDifferenceMinimumShift = 0.5

# [Personal Info]
#
# I assume this for your standard wake up time
defaultWakeUpHours = 9.0 
# I assume this for morning routine (breakfast, shower, ...)
morningRoutineHours = 1.5 
# I assume this to arrive and prepare for work
movementWork = 0.5 
# Max hours to study
maxHoursStudy = 6.0

# Do you go to the gym?
gymInsert = True

# How many days of rest do you want between two work out?
gapDaysBetweenGym = 1
# How many hours do you want to train?
gymHoursForDay = 1.5
# I assume this to arrive and prepare for gym
movementGym = 0.5
# Openings and Closure of Gym
openingHourGym = 7
closureHourGym = 22 

startLunch = 13 
durationLunch = 1.0
startDinner = 21 
durationDinner = 1.0

# I assume this for routine of work (shower, washer, ...)
afterWorkRoutineHours = 1 

# I assume this how the deadline hours.  
endHourToStudy = 22

# I assume this for your standard falling asleep time
defaultAsleepHours = 23

####################################

# [Code Info]

debug = False
debugDeep = False
plot = True
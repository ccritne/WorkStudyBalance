import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from costants import *

def getDifferenceFromWorkSchedule(First, Second):
    
    if First["turnOFF"] > 24:
        return Second["turnIN"] + 24 - First["turnOFF"]

    return (24-First["turnOFF"]) + Second["turnIN"]


def roundHours(shift):

    integer = int(shift)
    decimal = shift - integer

    if decimal < 0.25 :
        return float(integer)
    
    if decimal >= 0.25 or decimal < 0.75:
        return float(integer + 0.5)

    return float(integer + 1)

workHoursDay = float(workHoursWeek/workDayWeek)

print(jobIndecesRestDays)

for i in range(len(jobIndecesRestDays)):
    if jobIndecesRestDays[i] == -1:
        randomNumber = -1
        while True:
            randomNumber = random.randrange(7)
            if randomNumber not in jobIndecesRestDays:
                break    
        jobIndecesRestDays[i] = randomNumber

print(jobIndecesRestDays)

pivot = startHour

data = []

shift = {
    "turnIN":0,
    "turnOFF":0,
    "rest":False
}

for x in range(numberDays):
    data.append(shift)

allShifts = []

while(pivot < endHour - workHoursDay + jobDifferenceMinimumShift):  
    shift["turnIN"] = pivot
    shift["turnOFF"] = roundHours(pivot+workHoursDay)
    shift["rest"] = False
    allShifts.append(shift.copy())
    pivot = pivot + jobDifferenceMinimumShift

for x in allShifts:
    print(x["turnIN"], x["turnOFF"])

shifts = [['F' for x in range(48)] for y in range(numberDays)]


letters = {}

letters['Z'] = {
    "color": 'black',
    "label": "Sleeping"
    }

letters['R'] = {
    "color": 'green',
    "label": "Routine"
    }

letters['W'] = {
    "color": 'red',
    "label": "Working"
    }

letters['M'] = {
    "color": 'orange',
    "label": "Moving"
    }

letters['S'] = {
    "color": 'blue',
    "label": "Studying"
    }

letters['F'] = {
    "color": 'purple',
    "label": "Free"
    }

letters['E'] = {
    "color": 'yellow',
    "label": "Eating"
    }

letters['G'] = {
    "color": 'cyan',
    "label": "Gym"
    }

indexDay = 0

workoutIndexDay = 0

if debug and debugDeep:
    for x in shifts:
            print('[',end='')
            for j in x:
                print(j, end='')
            print(']\n',end='')
    print()

totalHoursStudio = 0

for i in range(numberDays):
    
    scheduleWork = {
            "turnIN": 0,
            "turnOFF": 0,
            "rest": True
    } 
    
    wakeUP = defaultWakeUpHours
    asleepHours = defaultAsleepHours

    if i%7 in jobIndecesRestDays:
        if i > 0 and data[i-1]["turnOFF"] + afterWorkRoutineHours + movementWork > 24 and data[i-1]["rest"] == False:
            for j in range(int((data[i-1]["turnOFF"]-24)*2 + afterWorkRoutineHours*2 + movementWork*2), int(wakeUP*2)):
                shifts[i][j] = 'Z'
        else:
            for j in range(int(wakeUP*2)):
                shifts[i][j] = 'Z'
        
        for j in range(int(wakeUP*2), int(wakeUP*2 + morningRoutineHours*2)):
            shifts[i][j] = 'R'
        
        if asleepHours < 24:
            for j in range(int(asleepHours*2), 48):
                shifts[i][j] = 'Z'
    else:
        while True:
            random.shuffle(allShifts)

            if i == 0 or (i>0 and (data[i-1]["rest"] or getDifferenceFromWorkSchedule(data[i-1], allShifts[0]) >= gapBetweenShifts)):
                break
        
        scheduleWork = {
            "turnIN": allShifts[0]["turnIN"],
            "turnOFF": allShifts[0]["turnOFF"],
            "rest": False
        } 

        if scheduleWork["turnIN"] < defaultWakeUpHours + morningRoutineHours + movementWork:
            wakeUP = scheduleWork["turnIN"] - morningRoutineHours - movementWork
        
        for j in range(int(wakeUP*2), int(wakeUP*2 + morningRoutineHours*2)):
            shifts[i][j] = 'R'
        for j in range(int(scheduleWork["turnIN"]*2 - movementWork*2), int(scheduleWork["turnIN"]*2)):
            shifts[i][j] = 'M'

        if i > 0 and data[i-1]["turnOFF"] + afterWorkRoutineHours + movementWork > 24:
            for j in range(int((data[i-1]["turnOFF"] - 24)*2 + afterWorkRoutineHours*2 + movementWork*2), int(wakeUP*2)):
                shifts[i][j] = 'Z'
        else:
            for j in range(int(wakeUP*2)):
                shifts[i][j] = 'Z'
        
        if workHoursDay <= 6 :
            for j in range(int(scheduleWork["turnIN"]*2), int(min(48, scheduleWork["turnOFF"]*2))):
                shifts[i][j] = 'W'
        else:
            for j in range(int(scheduleWork["turnIN"]*2), int(min(48, scheduleWork["turnOFF"]*2))):
                if j != scheduleWork["turnIN"]*2 + 8:
                    shifts[i][j] = 'W'
        
        if i < numberDays - 1:
            if scheduleWork["turnOFF"] > 24:
                ### FIXARE IL FATTO CHE DEVO TENERE LA LINEA 'shifts[i] = ['F']*48' PER NON FAR SOVRASCIVERE. PUNTATORI DE MERDA
                for j in range(int((scheduleWork["turnOFF"]-24)*2)):
                    shifts[i+1][j] = 'W'
                for j in range(int((scheduleWork["turnOFF"]-24)*2), int((scheduleWork["turnOFF"]-24)*2 + movementWork*2)):
                    shifts[i+1][j] = 'M'
                for j in range(int((scheduleWork["turnOFF"]-24)*2 + movementWork*2), int((scheduleWork["turnOFF"]-24)*2 + movementWork*2 + afterWorkRoutineHours*2)):
                    shifts[i+1][j] = 'R'
            else:
                if scheduleWork["turnOFF"] + movementWork > 24:
                    j = int(scheduleWork["turnOFF"]*2)
                    iteraction = 0
                    while j < 48:
                        shifts[i][j] = 'M'
                        iteraction = iteraction + 1
                        j = j + 1
                    
                    for j in range(int(movementWork*2 - iteraction)):
                        shifts[i+1][j] = 'M'
                    
                    for j in range(int((scheduleWork["turnOFF"] - 24)*2 + movementWork*2), int((scheduleWork["turnOFF"] - 24)*2 + movementWork*2 + afterWorkRoutineHours*2)):
                        shifts[i+1][j] = 'R'
                else:
                    if scheduleWork["turnOFF"] + movementWork + afterWorkRoutineHours > 24:
                        for j in range(int(scheduleWork["turnOFF"]*2), int(scheduleWork["turnOFF"]*2 + movementWork*2)):
                            shifts[i][j] = 'M'

                        j = int(scheduleWork["turnOFF"]*2 + movementWork*2)
                        iteraction = 0

                        while j < 48:
                            shifts[i][j] = 'R'
                            iteraction = iteraction + 1
                            j = j + 1

                        for j in range(int(afterWorkRoutineHours*2 - iteraction)):
                            shifts[i+1][j] = 'R'
                    else:
                        for j in range(int(scheduleWork["turnOFF"]*2), int(scheduleWork["turnOFF"]*2 + movementWork*2)):
                            shifts[i][j] = 'M' 
                        for j in range(int(scheduleWork["turnOFF"]*2 + movementWork*2), int(scheduleWork["turnOFF"]*2 + movementWork*2 + afterWorkRoutineHours*2)):
                            shifts[i][j] = 'R'
            
        if scheduleWork["turnOFF"] >= defaultAsleepHours - movementWork - afterWorkRoutineHours:
            asleepHours = scheduleWork["turnOFF"] + movementWork + afterWorkRoutineHours
        
        if asleepHours < 24:
            for j in range(int(asleepHours*2), 48):
                shifts[i][j] = 'Z'
        
        

    # Lunch
    countLunch = 0

    for j in range(int(startLunch*2), int(startLunch*2 + durationLunch*2)):
            if shifts[i][j] == 'F':
                countLunch = countLunch + 1
            else:
                break
    
    if countLunch == int(durationLunch*2):
        for j in range(int(startLunch*2), int(startLunch*2 + durationLunch*2)):
            shifts[i][j] = 'E'

    # Dinner
    countDinner = 0
    for j in range(int(startDinner*2), int(startDinner*2 + durationDinner*2)):
            if shifts[i][j] == 'F':
                countDinner = countDinner + 1
            else:
                break
    
    if countDinner == int(durationDinner*2):
        for j in range(int(startDinner*2), int(startDinner*2 + durationDinner*2)):
            shifts[i][j] = 'E'

    # Gym (Usually after morning routine or in the first adjacent free slots)
    workoutCond = 'No'
    if gymInsert and i == workoutIndexDay:
        workoutCond = 'Yes'
        countGym = 0
        maxFree = 0
        indexStartMax = openingHourGym*2 - movementGym*2
        slotsNeed = int(movementGym*2)*2 + int(gymHoursForDay*2)

        workoutIndexDay = workoutIndexDay + 1 + gapDaysBetweenGym

        for j in range(int(openingHourGym*2 - movementGym*2), int(closureHourGym*2 + movementGym*2)):
            if shifts[i][j] == 'F':
                countGym = countGym + 1
            else:
                # I update the search while  
                if maxFree < slotsNeed:
                    maxFree = max(maxFree, countGym)
                    countGym = 0
                else:
                    indexStart = j - (maxFree + 1)
                    for l in range(indexStart, indexStart + int(movementGym*2)):
                        shifts[i][l] = 'M'
                    for l in range(indexStart + int(movementGym*2), indexStart + int(movementGym*2) + int(gymHoursForDay*2)):
                        shifts[i][l] = 'G'
                    for l in range(indexStart + int(movementGym*2) + int(gymHoursForDay*2), indexStart + int(movementGym*2) + int(gymHoursForDay*2) + int(movementGym*2)):
                        shifts[i][l] = 'M'
                    break            

    # Study
    countForBreak = 0
    countLimit = 0
    for j in range(48):
        if countLimit == maxHoursStudy*2 or j == endHourToStudy*2:
            break

        if countForBreak == 4:
            countForBreak = 0
            continue

        if shifts[i][j] == 'F' and \
            j > 0 and j < 47 and \
            shifts[i][j-1] != 'W' and shifts [i][j+1] != 'W':
            
            shifts[i][j] = 'S'
            countLimit = countLimit + 1
            countForBreak = countForBreak + 1
            totalHoursStudio = totalHoursStudio + 0.5
        else:
            countForBreak = 0

    data[i]["turnIN"] = scheduleWork["turnIN"]
    data[i]["turnOFF"] = scheduleWork["turnOFF"]
    data[i]["rest"] = scheduleWork["rest"]
    
    indexDay = indexDay + 1
    if debug:
        print(i,'\t', end='')
        for j in range(48):
            print(shifts[i][j], end='')
        if scheduleWork["rest"]:
            print('\t R\t'+workoutCond+'\n',end='')
        else:
            print('\t',str(scheduleWork["turnIN"])+'-'+str(scheduleWork["turnOFF"])+'\n',end='')
        if debugDeep:

            print('\n-', end="")
            print(*[x%10 for x in range(48)], sep='',end='')
            print('-\n', end="")
            for x in shifts:
                print('[',end='')
                for j in x:
                    print(j, end='')
                print(']\n',end='')
            print()
    

    scheduleWork["turnIN"] = 0
    scheduleWork["turnOFF"] = 0
    scheduleWork["rest"] = True

    shift = {
        "turnIN":0,
        "turnOFF":0,
        "rest":False
    }

    lastLetter = shifts[i][0]
    startShift = 0

    if plot:
        for j in range(48):
            if shifts[i][j] != lastLetter:
                shift["turnIN"] = startShift
                shift["turnOFF"] = float(j/2)
                startShift = shift["turnOFF"]
                
                plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = letters[lastLetter]["color"], label = letters[lastLetter]["label"], linewidth=widthLine)
                
                lastLetter = shifts[i][j]

        plt.vlines(x = i, ymin = startShift, ymax = 24, colors = letters[lastLetter]["color"], label = letters[lastLetter]["label"], linewidth=widthLine)
    

if plot:      
    plt.xlim(xmin=-1, xmax=numberDays+1)
    plt.ylim(ymin=-1, ymax=25)

    black_patch = mpatches.Patch(color='black', label='Sleeping')
    green_patch = mpatches.Patch(color='green', label='Routine')
    red_patch = mpatches.Patch(color='red', label='Working')
    orange_patch = mpatches.Patch(color='orange', label='Moving')
    blue_patch = mpatches.Patch(color='blue', label='Studying')
    purple_patch = mpatches.Patch(color='purple', label='Free')
    yellow_patch = mpatches.Patch(color='yellow', label='Eating')
    cyan_patch = mpatches.Patch(color='cyan', label='Gym')


    plt.text(numberDays/2, 24.5, 'Total study hours = ' + str(totalHoursStudio), horizontalalignment='center', verticalalignment='bottom')
    plt.text( 0.1, -0.5, 'Work hours per week = ' + str(workHoursWeek), horizontalalignment='left', verticalalignment='top')
    plt.legend(handles=[black_patch, green_patch, blue_patch, red_patch, purple_patch, yellow_patch, orange_patch, cyan_patch], loc='upper center', bbox_to_anchor=(0.5, 1.05), fancybox=False, shadow=False, ncol=8)
    plt.subplots_adjust(left=0.05, top = 0.95, right=0.95, bottom=0.1)
    plt.xlabel('Index')
    plt.ylabel('Hours')

    plt.show()
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

restWorkDayIndex = random.randrange(7)

shifts = [['F' for x in range(48)] for y in range(numberDays)]

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

    if i != restWorkDayIndex:
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
    else:
        restWorkDayIndex = restWorkDayIndex + 7
        
        if i > 0 and data[i-1]["turnOFF"] + afterWorkRoutineHours + movementWork > 24:
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

    # Lunch
    if shifts[i][int(startLunch*2)] == 'F' and shifts[i][int(startLunch*2) + 1] == 'F':
        shifts[i][int(startLunch*2)] = 'L'
        shifts[i][int(startLunch*2) + 1] = 'L'

    # Dinner
    if shifts[i][int(startDinner*2)] == 'F' and shifts[i][int(startDinner*2) + 1] == 'F':
        shifts[i][int(startDinner*2)] = 'D'
        shifts[i][int(startDinner*2) + 1] = 'D'

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
        if countLimit == maxHoursStudy*2:
            break

        if countForBreak == 4:
            countForBreak = 0
            continue

        if shifts[i][j] == 'F' and \
            countLimit < maxHoursStudy*2 and \
            j < endHourToStudy*2 and \
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
            print('\t',str(scheduleWork["turnIN"])+'-'+str(scheduleWork["turnOFF"])+'\t'+str(restWorkDayIndex)+'\t'+workoutCond+'\n',end='')
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


    for j in range(48):
        if shifts[i][j] != lastLetter:
            shift["turnIN"] = startShift
            shift["turnOFF"] = float(j/2)
            startShift = shift["turnOFF"]
            
            match lastLetter:
                case 'Z':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'black', label = 'Sleeping', linewidth=widthLine)
                case 'R':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'green', label = 'Routine', linewidth=widthLine)
                case 'W':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'red', label = 'Working', linewidth=widthLine)
                case 'M':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'orange', label = 'Moving', linewidth=widthLine)
                case 'S':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'blue', label = 'Studying', linewidth=widthLine)
                case 'F':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'purple', label = 'Free', linewidth=widthLine)
                case 'D':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'yellow', label = 'Eating', linewidth=widthLine)
                case 'L':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'yellow', label = 'Eating', linewidth=widthLine)
                case 'G':
                    plt.vlines(x = i, ymin = shift["turnIN"], ymax = shift["turnOFF"], colors = 'cyan', label = 'Gym', linewidth=widthLine)
            
            lastLetter = shifts[i][j]

    match lastLetter:
        case 'Z':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'black', label = 'Sleeping', linewidth=widthLine)
        case 'R':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'green', label = 'Routine', linewidth=widthLine)
        case 'W':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'red', label = 'Working', linewidth=widthLine)
        case 'M':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'orange', label = 'Moving', linewidth=widthLine)
        case 'S':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'blue', label = 'Studying', linewidth=widthLine)
        case 'F':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'purple', label = 'Free', linewidth=widthLine)
        case 'D':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'yellow', label = 'Eating', linewidth=widthLine)
        case 'L':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'yellow', label = 'Eating', linewidth=widthLine)
        case 'G':
            plt.vlines(x = i, ymin = startShift, ymax = 24, colors = 'cyan', label = 'Gym', linewidth=widthLine)
            


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
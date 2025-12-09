import time

def day7(content:str):
    lines = content.splitlines()
    
    i = 0
    while lines[0][i] != 'S':
        i += 1
    
    j = 1
    nbLines = len(lines)
    beams:list[int] = []
    nextBeams:list[int] = [i]
    lookUpTable:list[bool] = [False] * len(lines[0])
    lookUpTable[i] = True
    
    counter = 0
    
    while (j < nbLines):
        beams = nextBeams
        nextBeams = []
        for iBeam in beams:
            if lines[j][iBeam] == ".":
                nextBeams.append(iBeam)
            elif lines[j][iBeam] == "^":
                counter += 1
                iLeftBeam = iBeam - 1
                iRightBeam = iBeam + 1
                lookUpTable[iBeam] = False
                if not(lookUpTable[iLeftBeam]):
                    lookUpTable[iLeftBeam] = True
                    nextBeams.append(iLeftBeam)
                if not(lookUpTable[iRightBeam]):
                    lookUpTable[iRightBeam] = True
                    nextBeams.append(iRightBeam)
                
        j += 1
    
    return counter

def day7_2_1(content:str):
    lines = content.splitlines()
    
    i = 0
    while lines[0][i] != 'S':
        i += 1
    
    j = 1
    nbLines = len(lines)
    beams:list[int] = []
    nextBeams:list[int] = [i]
    # the amount of timelines/possibilities per column
    lookUpTable:list[int] = [0] * len(lines[0])
    lookUpTable[i] = 1
    
    while (j < nbLines):
        beams = nextBeams
        nextBeams = []
        for iBeam in beams:
            if lines[j][iBeam] == ".":
                nextBeams.append(iBeam)
            elif lines[j][iBeam] == "^":
                iLeftBeam = iBeam - 1
                iRightBeam = iBeam + 1
            # if not(lookUpTable[iLeftBeam]):
                lookUpTable[iLeftBeam] += lookUpTable[iBeam]
                nextBeams.append(iLeftBeam)
            # if not(lookUpTable[iRightBeam]):
                lookUpTable[iRightBeam] += lookUpTable[iBeam]
                nextBeams.append(iRightBeam)
                lookUpTable[iBeam] = 0
                
        j += 1
    
    return len(nextBeams)

def day7_2_2(content:str):
    lines = content.splitlines()
    
    i = 0
    while lines[0][i] != 'S':
        i += 1
    
    j = 1
    nbLines = len(lines)
    beams:list[int]
    nextBeams:list[int] = [i]
    # the amount of timelines/possibilities per column
    lookUpTable:list[(int, int, int)] = [(0,0,0)] * len(lines[0])
    lookUpTable[i] = (0, 1, 0)
    
    while (j < nbLines):
        beams = nextBeams
        nextBeams = []
        for iBeam in beams:
            if lines[j][iBeam] == ".":
                left, middle, right = lookUpTable[iBeam]
                lookUpTable[iBeam] = (0, left + middle + right, 0)
                nextBeams.append(iBeam)
            elif lines[j][iBeam] == "^":
                iLeftBeam = iBeam - 1
                iRightBeam = iBeam + 1
                
                leftCell = lookUpTable[iLeftBeam]
                if leftCell[0] == 0 and leftCell[1] == 0:
                    nextBeams.append(iLeftBeam)
                lookUpTable[iLeftBeam] = (leftCell[0], leftCell[1], lookUpTable[iBeam][1])
                
                rightCell = lookUpTable[iRightBeam]
                if rightCell[1] == 0 and rightCell[2] == 0:
                    nextBeams.append(iRightBeam)
                lookUpTable[iRightBeam] = (lookUpTable[iBeam][1], rightCell[1], rightCell[2])
                lookUpTable[iBeam] = (0, 0, 0)
            
        j += 1
    
    total = 0
    for beam in nextBeams:
        total += lookUpTable[beam][1] # add the center
    
    return total

filepath = "day7/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)

# start = time.time()
result = day7_2_2(content)
# end = time.time()
# print("duration: ", end - start)
print(result)


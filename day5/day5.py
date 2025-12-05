
# 760 = wrong
# 767 = wrong
# 775 = right
def binarySearch(sortedList:list[(int, int)], nb:int) -> bool:
    start = 0
    end = len(sortedList) - 1
    
    while (start < end):
        middle = (end + start) // 2
        (rangeStart, rangeEnd) = sortedList[middle]
        if nb < rangeStart:
            end = middle - 1
        elif nb > rangeEnd:
            start = middle + 1
        else:
            return True

    return sortedList[start][0] <= nb <= sortedList[start][1]\
        or sortedList[end][0] <= nb <= sortedList[end][1]

def greedy(rangeList:list[(int, int)], nb:int):
    for (start, end) in rangeList:
        if (start <= nb <= end):
            return True
        
    return False

# 49604820785631
# DOESNT WORK
def mergeRanges2(sortedRanges:list[(int, int)]) -> list[(int, int)]:
    mergedRanges:list[(int, int)] = []
    i = 0
    j = 1
    while (i + j < len(sortedRanges)):
        (start1, end1) = sortedRanges[i]
        (start2, end2) = sortedRanges[i+j]
        assert(start1 <= start2)
        if (end1 < start2):
            mergedRanges.append((start1, end1))
            i += j
            j = 1
        else:
            sortedRanges[i] = (start1, max(end1, end2))
            j += 1
    
    if j == 1:
        mergedRanges.append(sortedRanges[i])
    else:
        mergedRanges.append((sortedRanges[i][0], sortedRanges[-1][1]))

    return mergedRanges

def mergeRanges(sortedRanges:list[(int, int)]) -> list[(int, int)]:
    mergedRanges:list[(int, int)] = []
    
    mergedRanges.append(sortedRanges[0])
    
    for i in range(1, len(sortedRanges)):
        if mergedRanges[-1][1] >= sortedRanges[i][0]:
            mergedRanges[-1] = (mergedRanges[-1][0], max(mergedRanges[-1][1], sortedRanges[i][1]))
        else:
            mergedRanges.append(sortedRanges[i])
    
    return mergedRanges


def day5(content:str):
    lines = content.splitlines()

    validRanges:list[(int, int)] = []
    
    i = 0
    
    # O(n)
    while (len(lines[i]) != 0):       
        splitCurrentLine = lines[i].split('-')
        start = int(splitCurrentLine[0])
        end = int(splitCurrentLine[1])
        validRanges.append((start, end))
        i += 1
    i += 1
    
    # O(n*log(n))
    validRanges.sort(key=lambda e: e[0])
    originalRanges = validRanges
    validRanges = mergeRanges(validRanges)
    
    # for k in range(len(validRanges) - 1):
    #     assert(validRanges[k][1] < validRanges[k+1][0])
        
    # for k in range(len(validRanges)):
    #     assert(validRanges[k][0] <= validRanges[k][1])

    # print(f"ranges: {validRanges}")
    
    total = 0
    while (i < len(lines)):
        nb = int(lines[i])
        
        # unit test
        # assert(greedy(originalRanges, nb) == binarySearch(validRanges, nb))
        
        if binarySearch(validRanges, nb):
            total += 1
            # print(f"{nb} : valid")
        # else:
            # print(f"{nb} : invalid")
        
        i += 1
    
    return total

def day5_2(content:str):
    lines = content.splitlines()
    validRanges:list[(int, int)] = []
    i = 0
    # O(n)
    while (len(lines[i]) != 0):       
        splitCurrentLine = lines[i].split('-')
        start = int(splitCurrentLine[0])
        end = int(splitCurrentLine[1])
        validRanges.append((start, end))
        i += 1
    i += 1
    
    validRanges.sort(key=lambda e: e[0])
    validRanges = mergeRanges(validRanges)
    
    total = 0
    for j in range(len(validRanges)):
        total += validRanges[j][1] - validRanges[j][0] + 1
    return total


filepath = "day5/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)

result = day5_2(content) 
print(result)

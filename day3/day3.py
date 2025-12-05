def day3(content:str):
    lines = content.splitlines()

    total = 0
    
    for line in lines:
        leftIndex = 0
        rightIndex = 1
        
        left:int = int(line[0])
        right:int = int(line[1])
        
        for currentIndex in range(1, len(line)-1):
            current = int(line[currentIndex])
            if left < current:
                leftIndex = currentIndex
                rightIndex = currentIndex + 1
                left = int(line[leftIndex])
                right = int(line[rightIndex])
            elif right < current:
                rightIndex = currentIndex
                right = int(line[rightIndex])
        
        if right < int(line[-1]):
            rightIndex = len(line) - 1
            right = int(line[rightIndex])
    
        currentMax = 10 * int(left) + int(right)
        print(line, " => ", currentMax) 
        total += currentMax
    
    return total


def day3_2(content:str):
    lines = content.splitlines()

    total = 0
    
    for line in lines:
        turnedOn:list[int] = [0] * 12
        
        lineLength = len(line)
        assert(lineLength >= 12)
        for currentIndex in range(0, lineLength):
            current = int(line[currentIndex])
            
            turnedOnIndex = max(currentIndex - (lineLength - 12), 0)
            while turnedOnIndex < 12 and current <= turnedOn[turnedOnIndex]:
                turnedOnIndex += 1
                
            if turnedOnIndex == 12:
                continue
                
            turnedOn[turnedOnIndex] = current
            j = currentIndex
            
            while turnedOnIndex < 11:
                turnedOnIndex += 1
                turnedOn[turnedOnIndex] = 0

        currentMax = turnedOn[0]
        for i in range(1, 12):
            currentMax *= 10
            currentMax += turnedOn[i]
        
        print(line, " => ", currentMax)
        total += currentMax
    
    return total




filepath = "day3/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)
    
print(day3_2(content))


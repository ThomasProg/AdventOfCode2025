import time

def day4(content:str):
    lines = content.splitlines()

    total = 0
    
    sides = [(-1, -1), (0, -1), (1, -1),
             (-1, 0), (1, 0),
             (-1, 1), (0, 1), (1, 1),]
    for j in range(len(lines)):
        line = lines[j]
        for i in range(len(line)):
            if line[i] == '.':
                # print('.', end="")
                continue
            
            nbAdjacentNeighbors = 0
            for sideIndex in range(8):
                offset = sides[sideIndex]
                iNeighbor = i + offset[0]
                jNeighbor = j + offset[1]
    
                nbAdjacentNeighbors += int(iNeighbor >= 0 and iNeighbor < len(line)\
                    and jNeighbor >= 0 and jNeighbor < len(lines)\
                    and lines[jNeighbor][iNeighbor] == '@')
        
            if nbAdjacentNeighbors < 4:
                total += 1
                # print(nbAdjacentNeighbors, end="")
            # else:
                # print('@', end="")
        # print()
        
    return total


def day4_2(content:str):
    lines = content.splitlines()

    total = 0
    
    sides = [(-1, -1), (0, -1), (1, -1),
             (-1, 0), (1, 0),
             (-1, 1), (0, 1), (1, 1),]
    
    toProcess = []
    width = len(lines[0])
    height = len(lines)
    intArray:list[int] = [-1] * width * height
    
    start = time.time()
    
    for j in range(len(lines)):
        line = lines[j]
        for i in range(len(line)):
            if line[i] == '.':
                continue
            
            nbAdjacentNeighbors = 0
            for sideIndex in range(8):
                offset = sides[sideIndex]
                iNeighbor = i + offset[0]
                jNeighbor = j + offset[1]
    
                nbAdjacentNeighbors += int(iNeighbor >= 0 and iNeighbor < len(line)\
                    and jNeighbor >= 0 and jNeighbor < len(lines)\
                    and lines[jNeighbor][iNeighbor] == '@')
        
            intArray[j * width + i] = nbAdjacentNeighbors
            if (nbAdjacentNeighbors < 4):
                toProcess.append((i, j))

        print()
        
    # for j in range(height):
    #     for i in range(width):
    #         print(intArray[j * width + i], end="\t")
    #     print()
    # print()
    
    while len(toProcess) != 0:       
        (i, j) = toProcess.pop(0)
        total += 1
        
        # print("Removing ", i, "/", j)
        # for jx in range(height):
        #     for ix in range(width):
        #         element = intArray[jx * width + ix]
        #         print(element, end="\t")
        #         # if element < 4:
        #         #     print('.', end=" ")
        #         # else:
        #         #     print('@', end=" ")
        #     print()
        # print()
            
        # await asyncio.sleep(3)
        
        for sideIndex in range(8):
            offset = sides[sideIndex]
            iNeighbor = i + offset[0]
            jNeighbor = j + offset[1]
            
            if iNeighbor < 0 or iNeighbor >= width\
                or jNeighbor < 0 or jNeighbor >= height:
                continue
            
            intArray[jNeighbor * width + iNeighbor] -= 1
            if intArray[jNeighbor * width + iNeighbor] == 3:
                toProcess.append((iNeighbor, jNeighbor))
        
    # for j in range(height):
    #     for i in range(width):
    #         element = intArray[j * width + i]
    #         if element < 4:
    #             print('.', end=" ")
    #         else:
    #             print('@', end=" ")
    #     print()
    # print()
        
    return total

filepath = "day4/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)

start = time.time()
result = day4_2(content) 
end = time.time()
print("duration: ", end - start)

print(result)

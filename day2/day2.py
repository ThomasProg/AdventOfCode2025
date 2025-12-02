
# 6 => 10
# 54 => 100
# 54 * 100 + 54 => 5454
def ceilIntegerBase10(integer:int) -> int:
    ret = 1
    while ret < integer:
        ret *= 10
    return ret

# 26255179562
def day2(strInput:str):
    result = 0
    
    ids = []
    
    pairList = strInput.split(',')
    for pair in pairList:
        range = pair.split('-')
        start = int(range[0])
        end = int(range[1])
        ids.append((start, end))
        
    ids.sort(key=lambda a: a[0])
        
    idsIndex = 0
    current = 1
    
    mult = ceilIntegerBase10(current) * 10
    duplicatedCurrent = start
    while duplicatedCurrent <= ids[-1][1]:
        # 1 * 1 * 10 + 1 = 10 + 1 = 11
        # 15 * 10**2 + 15 = 15 * 100 + 15 = 1515
        duplicatedCurrent = current * mult + current
        
        while idsIndex < len(ids) and duplicatedCurrent > ids[idsIndex][1]:
            idsIndex += 1
        
        if idsIndex == len(ids):
            break
        
        if ids[idsIndex][0] <= duplicatedCurrent <= ids[idsIndex][1]:
            result += duplicatedCurrent
        current += 1
        if current == mult:
            mult *= 10



    print(result)

            
        
        
        
        
        
        
# with duplicates:
# 1111
# 11 - 11
# 1 - 1 - 1 - 1
# -> 31896413455
# without:
# -> 31680313976

def day2_2(strInput:str):
    result = 0
    
    ids = []
    
    pairList = strInput.split(',')
    for pair in pairList:
        startAndEnd = pair.split('-')
        start = int(startAndEnd[0])
        end = int(startAndEnd[1])
        ids.append((start, end))
        
    ids.sort(key=lambda a: a[0])
        
    found:set = set()
        
    i = 1
    while (10**i <= ids[-1][1]):
        idsIndex = 0
        current = 1
        
        mult = ceilIntegerBase10(current) * 10
        duplicatedCurrent = start
        while duplicatedCurrent <= ids[-1][1]:
            # 1 * 1 * 10 + 1 = 10 + 1 = 11
            # 15 * 10**2 + 15 = 15 * 100 + 15 = 1515
            
            duplicatedCurrent = current
            for j in range(i):
                duplicatedCurrent *= mult
                duplicatedCurrent += current
            
            while idsIndex < len(ids) and duplicatedCurrent > ids[idsIndex][1]:
                idsIndex += 1
            
            if idsIndex == len(ids):
                break
            
            if ids[idsIndex][0] <= duplicatedCurrent <= ids[idsIndex][1] and duplicatedCurrent not in found:
                found.add(duplicatedCurrent)
                result += duplicatedCurrent
            current += 1
            if current == mult:
                mult *= 10
        
        i += 1

    print(result)

        



filepath = "day2/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)
    
day2_2(content)
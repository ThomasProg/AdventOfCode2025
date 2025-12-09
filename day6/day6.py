
def day6(content:str):
    lines = content.splitlines()
    
    operationLine:str = lines[-1]
    operationStrs = operationLine.split()
    nbColumns = len(operationStrs) 
    nbNumberLines = len(lines) - 1

    intList:list[int] = [0] * (nbNumberLines * nbColumns)
    for j in range(len(lines) - 1):
        line = lines[j]
        numberStrs = line.split()
        for i in range(nbColumns):
            intList[i * nbNumberLines + j] = int(numberStrs[i])

    total = 0
    for i in range(nbColumns):
        operationStr = operationStrs[i]
        match operationStr:
            case "+":
                productResult = 0
                for j in range(nbNumberLines):
                    productResult += intList[i * nbNumberLines + j]
                total += productResult
            case "*":
                productResult = 1
                for j in range(nbNumberLines):
                    productResult *= intList[i * nbNumberLines + j]
                total += productResult

    return total

def day6_2(content:str):
    lines = content.splitlines()
    
    operationLine:str = lines[-1]

    total = 0
    
    i = len(operationLine) - 1
    while (i >= 0):
        start = i
        while (operationLine[i] == ' '):
            i -= 1
        end = i
        match (operationLine[i]):
            case "+":
                expressionTotal = 0
                for c in range(end, start + 1):
                    nbStr = ""
                    for j in range(0, len(lines) - 1):
                        nbStr += lines[j][c]
                    expressionTotal += int(nbStr)
                total += expressionTotal
            case "*":
                expressionTotal = 1
                for c in range(end, start + 1):
                    nbStr = ""
                    for j in range(0, len(lines) - 1):
                        nbStr += lines[j][c]
                    expressionTotal *= int(nbStr)
                total += expressionTotal

        i -= 2

    return total


filepath = "day6/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)

result = day6_2(content) 
print(result)

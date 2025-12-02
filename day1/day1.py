import math

def day1_1(content:str):
    nb = 50
    zeroCounter = 0
    lines = content.splitlines()
    for line in lines:
        multiplier = 1 if line[0] == 'R' else -1
        nbRotations = int(line[1: len(line)])

        nb += multiplier * nbRotations
        nb %= 100
        
        if nb == 0:
            zeroCounter += 1
    
    print(zeroCounter)

def day1_2(content:str):
    nb = 50
    zeroCounter = 0
    lines = content.splitlines()
    for line in lines:
        multiplier = 1 if line[0] == 'R' else -1
        nbRotations = int(line[1: len(line)])
        
        if nbRotations == 0:
            continue

        prev = nb
        added = multiplier * nbRotations
        
        nb += added
        
        div = nb // 100
        
        zeroCounterAdded = int(math.copysign(nb // 100, 1))
        
        if nb == 0:
            zeroCounterAdded += 1
        
        if prev == 0 and div < 0:
            zeroCounterAdded -= 1
        
        zeroCounter += zeroCounterAdded
        
        print(f"{prev} + ({added}) = {nb} => {nb % 100} / {zeroCounterAdded}")
        nb %= 100
    
    print("Result: ", zeroCounter)

def day1_2_2(content:str):
    nb = 50
    zeroCounter = 0
    lines = content.splitlines()
    for line in lines:
        multiplier = 1 if line[0] == 'R' else -1
        nbRotations = int(line[1: len(line)])
        
        prev = nb
        
        nb += multiplier * nbRotations
        
        if nb < 0:
            while nb < 0:
                nb += 100
                zeroCounter += 1
                
            if nb == 0 and prev != 0:
                zeroCounter += 1
           
        if nb >= 100:
            while nb >= 100:
                nb -= 100
                zeroCounter += 1
        
        print(f"{prev} + ({multiplier * nbRotations}) => {nb} / {zeroCounter}")
        
    print("Result: ", zeroCounter)

def day1_2_3(content:str):
    nb = 50
    zeroCounter = 0
    lines = content.splitlines()
    for line in lines:
        multiplier = 1 if line[0] == 'R' else -1
        nbRotations = int(line[1: len(line)])
        
        added = multiplier * nbRotations
        prev = nb
        
        if added > 0:
            for i in range(added):
                nb += 1
                if nb == 100:
                    nb = 0
                if nb == 0:
                    zeroCounter += 1

        if added < 0:
            for i in range(-added):
                nb -= 1
                if nb == -1:
                    nb = 99
                if nb == 0:
                    zeroCounter += 1
                    
        print(f"{prev} + {added} => {prev+added} => {nb}")
        
    print("Result: ", zeroCounter)



filepath = "input.txt"
try:
    with open(filepath) as file:
        day1_2_3(file.read())
except Exception as e:
    print("couldnt open file: ", e)
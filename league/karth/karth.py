import itertools
                #cost, haste,  mythic, legen., unique, bonus per legendary
items = {
    'ionian':   ( 950,  20,     False,  False,  True,   0),
    'kindlegem':( 800,  10,     False,  False,  False,  0),
    'warhammer':(1100,  15,     False,  False,  False,  0),
    'chempunk': (2800,  25,     False,  True,   True,   0),
    'Axiom Arc':(3000,  25,     False,  True,   True,   0),
    'chemtech': (2300,  20,     False,  True,   True,   0),
    'knights':  (2300,  20,     False,  True,   True,   0),
    'zekes':    (2400,  20,     False,  True,   True,   0),
    'Anathemas':(2500,  20,     False,  True,   True,   0),
    'cosmic':   (3000,  30,     False,  True,   True,   0),
    'black' :   (3100,  30,     False,  True,   True,   0),
    'Harvester':(3200,  25,     True,  False,   True,   5),
    'gore':     (3300,  20,     True,   False,  True,   7)
}

def isPurchasable(x, gold):
    totalCost = 0
    for e in x:
        totalCost += items[e][0]
    if totalCost <= gold:
        return True
    return False

def isLegal(x):
    tempList = []
    mythic = False
    for e in x:
        if items[e][2]:
            if mythic == False:
                mythic = True
            else:
                return False
        if items[e][4]:
            tempList.append(e)
    if len(set(tempList)) == len(tempList):
        return True
    return False

def haste(x):
    totalHaste = 0
    mythicBonus = 0
    for e in x:
        if items[e][2]:
            mythicBonus = items[e][5]
    for e in x:
        totalHaste += items[e][1]
        if items[e][3]:
            totalHaste += mythicBonus
    return totalHaste

def main():
    allPossible = []
    for i in range(1,7):
        allPossible += list(itertools.combinations(items, i))
    print(len(allPossible))
    bestSet = {}
    for gold in range(800,30000,50):
        #pick a unique combo
        bestSet[gold] = ([],0)
        for x in allPossible:
            if isLegal(x) and isPurchasable(x, gold):
                calcHaste = haste(x)
                if calcHaste > bestSet[gold][1]:
                    bestSet[gold] = (x, calcHaste)
    print('\n\n\n\n\n')
    for item in bestSet.items():
      print(item)
main()














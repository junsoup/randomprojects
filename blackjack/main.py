"""
This whole thing doesn't work since it is missing hit/stand value of player
rewrite to sample n from deck to simulate hand being drawn given expected value of draw into basic strategy

"""

from sty import fg, rs
import copy

#index      [0  1  2  3  4  5  6  7  8  9  10 11 12]
#           [A  2  3  4  5  6  7  8  9  10 J  Q  K ]
# deck      = [16,16,16,16,16,16,16,16,16,16,16,16,16]
deck      = [2] * 13
cardValue = [11,2, 3, 4, 5, 6, 7, 8, 9, 10,10,10,10]
trueValue = [11,2, 3, 4, 5, 6, 7, 8, 9, 10,10,10,10]
runningCount = 0

def printDeck():
    print('Deck: ',end='')
    for cards, value in zip(deck, ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J',  'Q',  'K']):
        normalized = round(cards*16*(255/256))
        print(value+":"+fg(255-normalized,normalized, 12)+str(cards)+fg.rs, end=' ')
    print('')

def removeCards(cards = None):
    if cards == None:
        cards = ''.join(input().upper()).split()
    if cards == '':
        return
    for card in cards:
        if card == 'A':
            deck[0] -= 1
            
        elif card == 'J':
            deck[10] -= 1
        elif card == 'Q':
            deck[11] -= 1
        elif card == 'K':
            deck[12] -= 1
        else:
            deck[int(card)]-= 1

def expectedValue():
    sum = 0
    for card, value in zip(deck, cardValue):
        sum += card*value
    return sum/13

def trueCount():
    for card, value in zip(deck, cardValue):
        sum += card*value

def calculateOdds(playerHand = [], dealerHand = [], deck = deck, playerStands = False):
    playerHandValue = getHandValue(playerHand)
    dealerHandValue = getHandValue(dealerHand)
    
    # Player bust!
    if playerHandValue[0] > 21:
        # print("Player bust")
        # return (0, 1, 0)
        return (0, 0, 1)
    # Dealer bust!
    if dealerHandValue[0] > 21:
        # print("Dealer bust")
        return (0, 1, 0)

    if dealerIsDone(dealerHandValue):
        # Player blackjack!
        if playerHandValue[0] == 21 and len(playerHand) == 2 and dealerHandValue < 21:
            # print("Player blackjack")
            # return (1.5, 0, 0)
            return (0, 0, 1)
        # Player and Dealer blackjack. Tie!
        if playerHandValue[0] == 21 and dealerHandValue[0] == 21:
            # print("Tie")
            return (0, 0, 1)
        if playerHandValue[0] > dealerHandValue[0]:
            # print("Player win")
            # return (1, 0, 0)
            return (0, 0, 1)
        if playerHandValue[0] == dealerHandValue[0]:
            # print("Tie")
            return (0, 0, 1)
        return (0, 0, 1)    

    results = [0, 0, 0]
    
    for i in range(2):
        if len(playerHand) >= 4 or len(dealerHand) >= 4:
            break
        # If the player cannot hit (chose to stand), skip hit case
        if i == 0:
            if playerStands:
                continue
            if playerHandValue[0] >= 17 and not playerHandValue[1]:
                continue
            if playerHandValue[0] > 13 and not playerHandValue[1] and dealerHandValue[0] <= 6:
                continue

        for j in range(0, 13):
            if deck[j] > 0:
                lookCard = j+1
                if j == 0:
                    lookCard = 11
                elif j >= 10:
                    lookCard = 10
                playerHandCopy = copy.deepcopy(playerHand)
                dealerHandCopy = copy.deepcopy(dealerHand)
                deckCopy = copy.deepcopy(deck)
                deckCopy[j] -= 1
                runResult = None
                if i == 0:
                    playerHand.append(lookCard)
                    runResult = calculateOdds(playerHandCopy, dealerHandCopy, deckCopy, False)
                else:
                    dealerHand.append(lookCard)
                    runResult = calculateOdds(playerHandCopy, dealerHandCopy, deckCopy, True)

                results[0] += runResult[0]
                results[1] += runResult[1]
                results[2] += runResult[2]
    
    return tuple(results)

def dealerIsDone(value):
    if value[0] > 17:
        return True
    if value[0] == 17 and not value[1]:
        return True
    return False

def getHandValue(hand):
    handValue = sum(hand)
    soft = hand.count(11)
    while(handValue > 21):
        if soft > 0:
            handValue -= 10
            soft -= 1
        else:
            break
    return (handValue, True if soft > 0 else False)

def printResults(results):
    # total = sum(results)
    total = results[1]+results[2]
    playerWin = round(results[0]*10000)/100 / total
    dealerWin = round(results[1]*10000) / 100 / total
    draw = round(results[2]*10000) / 100 / total

    # print("Stats: Player win:", playerWin, "%\tDealer Win:", dealerWin, "%\tDraw:",draw,"%\n")
    print("Stats: Dealer Bust:", dealerWin, "%\n")

def main():
    print("\n\nEnter initally used cards")
    removeCards()
    
    while(True):
        printDeck()
        print("Loading", end='\r')
        result = calculateOdds()
        print("       ", end='\r')
        printResults(result)
        playerHand = []
        dealerHand = []
        cards = ''.join(input().upper()).split()
        playerHand.append(cards[1:len(cards)-1])
        dealerHand.append(cards[-1])
        while(cards != 'X'):
            playerHand.append(cards[0])
            removeCards(cards)
            # print("Loading", end='\r')
            # result = calculateOdds(playerHand, dealerHand)
            # print("       ", end='\r')
            # printResults(result)
            cards = ''.join(input().upper())

main()
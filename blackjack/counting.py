"""
This whole thing doesn't work since it is missing hit/stand value of player
rewrite to sample n from deck to simulate hand being drawn given expected value of draw into basic strategy

"""

from sty import fg, rs

deck      = [16] * 13
cardValue = [11,2, 3, 4, 5, 6, 7, 8, 9, 10,10,10,10]
runningCount = 0

def printDeck():
    print('Deck: ',end='')
    for cards, value in zip(deck, ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J',  'Q',  'K']):
        normalized = round(cards*16*(255/256))
        print(value+":"+fg(255-normalized,normalized, 12)+str(cards)+fg.rs, end=' ')
    print('')

def removeCards(cards = None):
    global runningCount
    if cards == None:
        cards = ''.join(input().upper()).split()
    if cards == '':
        return
    for card in cards:
        match card:
            case 'A':
                deck[0] -= 1
                runningCount -= 1
            case '2':
                deck[1] -= 1
                runningCount += 1
            case '3':
                deck[2] -= 1
                runningCount += 1
            case '4':
                deck[3] -= 1
                runningCount += 1
            case '5':
                deck[4] -= 1
                runningCount += 1
            case '6':
                deck[5] -= 1
                runningCount += 1
            case '7':
                deck[6] -= 1
            case '8':
                deck[7] -= 1
            case '9':
                deck[8] -= 1
            case '10':
                deck[9] -= 1
                runningCount -= 1
            case 'J':
                deck[10] -= 1
                runningCount -= 1
            case 'Q':
                deck[11] -= 1
                runningCount -= 1
            case 'K':
                deck[12] -= 1
                runningCount -= 1

def expectedValue(hand = []):
    handVal = getHandValue(hand)

    total = 0
    bust = 0
    if not handVal[1]:
        bust += sum(deck[21-handVal[0]:])
    ten = deck[10]+deck[11]+deck[12]
    ace = deck[0]
    
    smallAce = False
    if handVal[0] + 11 > 21:
        smallAce = True
    for card, value in zip(deck, cardValue):
        if value == 11 and smallAce:
            total += card
        else:
            total += card*value
    
    total = round(total/sum(deck)*100)/100
    bust = round(bust/sum(deck)*10000)/100
    ten = round(ten/sum(deck)*10000)/100
    ace = round(ace/sum(deck)*10000)/100

    return f"\tNext\tBust\t10\tA\n\t{total+handVal[0]}\t{bust}%\t{ten}%\t{ace}%"

def trueCount():
    total = 0
    for card in deck:
        total += card
    return round(runningCount / (total/52) * 100) / 100

def getHandValue(hand):
    handValue = 0
    for card in hand:
        # print(caaaard)
        if card.isdigit():
            handValue += int(card)
        else:
            if card == 'A':
                handValue += 11
                continue
            handValue += 10
    
    soft = hand.count('A')
    while(handValue > 21):
        if soft > 0:
            handValue -= 10
            soft -= 1
        else:
            break
    return (handValue, True if soft > 0 else False)

# def normalizeHand(hand):
#     for i in len(hand):
#         card = hand[i]
#         match card:
#             case "A":
#                 hand[i] = 11
#             case "J":
#                 hand[i] = 10
#             case "Q":
#                 hand[i] = 


def main():
    print("\n\nEnter initally used cards")
    removeCards()
    
    while(True):
        printDeck()
        print(expectedValue(), "\tTrue Count: ", trueCount())

        playerHand = []
        dealerHand = []
        
        cards = ''.join(input().upper()).split()
        
        playerHand.append(cards[0])
        playerHand.append(cards[1])
        dealerHand.append(cards[2])
        
        while(cards[-1] != 'X'):
            removeCards(cards)
            print(expectedValue(playerHand), " , True Count: ", trueCount())

            cards = ''.join(input().upper()).split()
            for card in cards:
                if card != 'X':
                    playerHand.append(card)
                else:
                    print("Rest of dealers hand:")
                    removeCards()
main()
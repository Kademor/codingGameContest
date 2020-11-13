import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# game loop
class Brew:
    def __init__(self, inventoryChanges, id, prices):
        self.inventoryChanges = inventoryChanges
        self.id = id
        self.prices = prices


class Cast:
    def __init__(self, inventoryChanges, id):
        self.inventoryChanges = inventoryChanges
        self.id = id
        self.usedSpell = False


class InventoryChanges:
    def __init__(self, delta_0, delta_1, delta_2, delta_3):
        self.delta_0 = delta_0
        self.delta_1 = delta_1
        self.delta_2 = delta_2
        self.delta_3 = delta_3
        self.tabIngredients = [delta_0, delta_1, delta_2, delta_3]


class ActionForTurn:
    def __init__(self, action, id):
        self.action = action
        self.id = id


def castIsAvailable(paramActionId, inv_tab):
    returnValue = False
    neededSpell = checkForAvailableInv(paramActionId - (78 + witchPositionAdd), inv_tab)
    for spell in casts:
        print("checking spell " + str(spell.id) + " is available  " + str(spell.usedSpell), file=sys.stderr, flush=True)
        if spell.id == paramActionId and not spell.usedSpell:
            returnValue = True

    if casts[neededSpell - (78 + witchPositionAdd)].usedSpell:
        print("went in return value condition", file=sys.stderr, flush=True)
        returnValue = False

    return [returnValue, neededSpell]


def checkForAvailableInv(itemNeeded, invTab):
    print("item needed : " + str(itemNeeded), file=sys.stderr, flush=True)
    if (itemNeeded + 78 + witchPositionAdd) == (78 + witchPositionAdd):
        return itemNeeded + 78 + witchPositionAdd
    else:
        if 0 >= invTab[itemNeeded - 1]:
            return checkForAvailableInv(itemNeeded - 1, invTab)
        else:
            return itemNeeded + 78 + witchPositionAdd



def invalidateCastAfterTurn(castID):
    for i in range(4):
        # print(" current id " + str(casts[i].id) + "current cast it " + str(castID) + "equivalence " + str(str(casts[i].id) == str(castID)), file=sys.stderr, flush=True)
        if str(casts[i].id) == str(castID):
            casts[i].usedSpell = True


def resetCasts():
    for i in range(4):
        casts[i].usedSpell = False


def findBestBrew():
    if 2 > castedBrews:
        return brews[0]
    else:
        return findFastestBrew()


def findFastestBrew():
    lowestPrice = 1000
    currentSelectedBrew = brews[0]
    for singleBrew in brews:
        if lowestPrice > singleBrew.prices:
            lowestPrice = singleBrew.prices
            currentSelectedBrew = singleBrew
    return currentSelectedBrew

def findBrewList():
    brewListIds = ""
    for brew in brews:
        brewListIds  = brewListIds + str(brew.id) + ", "
    print(brewListIds, file=sys.stderr, flush=True)


casts = []
brews = []
castedBrews = 0
while True:
    action_count = int(input())  # the number of spells and recipes in play
    brews.clear()
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"
        # Setup spell list and brew list
        # brews.clear()
        currentInventoryChanges = InventoryChanges(delta_0, delta_1, delta_2, delta_3)
        if action_type == "BREW":
            brews.append(Brew(currentInventoryChanges, action_id, price))
        if action_type == "CAST" and len(casts) <= 3:
            casts.append(Cast(currentInventoryChanges, action_id))


    actionForTurn = ActionForTurn("REST", 0)
    witchPositionAdd = 0 if int(casts[0].id) == 78 else 4
    # print(actionForTurn.id, file=sys.stderr, flush=True)
    # print("test " + ' '.join(map(str, brews)), file=sys.stderr, flush=True)
    for i in range(2):
        findBrewList()
        selectedBrew = findBestBrew()
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        tab_inv = [inv_0, inv_1, inv_2, inv_3]
        if i == 0:
            print("inventory before can craft :  " + ''.join(str(e) for e in tab_inv), file=sys.stderr, flush=True)
            highest_price = 0
            canCraft = True

            # if inv_0 + inv_1 + inv_2 + inv_3 >= 8:
            #     casts[0].usedSpell = True
            # if not casts[0].usedSpell:
            #     actionForTurn.action = "CAST "
            #     actionForTurn.id = 78 + witchPositionAdd
            #     canCraft = False
            # else:
                # step 2 : transform while usefull until we cant anymore
            for ingredient in range(4):
                if (tab_inv[ingredient] + selectedBrew.inventoryChanges.tabIngredients[ingredient]) <= -1:
                    castAnswer = castIsAvailable(78 + witchPositionAdd + ingredient, tab_inv)
                    print("cast response " + str(castAnswer), file=sys.stderr, flush=True)
                    if castAnswer[0]:
                        actionForTurn.action = "CAST "
                        actionForTurn.id = str(castAnswer[1])
                    else:
                        actionForTurn.action = "REST"

            for ingredient in range(4):
                if canCraft:
                    canCraft = (int(tab_inv[ingredient]) + int(
                        selectedBrew.inventoryChanges.tabIngredients[ingredient])) >= 0

            if canCraft:
                actionForTurn.action = "BREW "
                actionForTurn.id = selectedBrew.id
    # Write an action using print
    print("Debug messages...", file=sys.stderr, flush=True)
    if actionForTurn.action == "REST":
        actionForTurn.id = 0
    printID = str(actionForTurn.id) if actionForTurn.id != 0 else ""

    print(actionForTurn.action + str(printID) + " targetting " + str(selectedBrew.id))

    if actionForTurn.action == "CAST ":
        invalidateCastAfterTurn(actionForTurn.id)
    elif actionForTurn.action == "REST":
        resetCasts()
    elif actionForTurn.action == "BREW ":
        castedBrews = castedBrews + 1
    # print("Spell List 78 :" + str(casts[0].usedSpell), file=sys.stderr, flush=True)
    # print("Spell List 79 :" + str(casts[1].usedSpell), file=sys.stderr, flush=True)
    # print("Spell List 80 :" + str(casts[2].usedSpell), file=sys.stderr, flush=True)
    # print("Spell List 81 :" + str(casts[3].usedSpell), file=sys.stderr, flush=True)

    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT

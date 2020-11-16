import sys
import math


class StandardAction:
    def __init__(self, action, id, inventoryChanges):
        self.action = action
        self.id = id
        self.inventoryChanges = inventoryChanges


class Brew(StandardAction):
    def __init__(self, action, id, inventoryChanges, prices):
        super().__init__(action, id, inventoryChanges)
        self.prices = prices


class Cast(StandardAction):
    def __init__(self, action, id, inventoryChanges, castable):
        super().__init__(action, id, inventoryChanges)
        self.castable = castable


class TomePage(StandardAction):
    def __init__(self, action, id, inventoryChanges, taxCount, tomeIndex, repeatable):
        super().__init__(action, id, inventoryChanges)
        self.taxCount = taxCount
        self.tomeIndex = tomeIndex
        self.repeatable = repeatable


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
    neededSpell = checkForAvailableInv(paramActionId - (78 + witchPositionAdd), inv_tab)
    return [casts[(neededSpell - (78 + witchPositionAdd))].castable, neededSpell]


def checkForAvailableInv(itemNeeded, invTab):
    if (itemNeeded + 78 + witchPositionAdd) == (78 + witchPositionAdd):
        return itemNeeded + 78 + witchPositionAdd
    else:
        if 0 >= invTab[itemNeeded - 1]:
            return checkForAvailableInv(itemNeeded - 1, invTab)
        else:
            return itemNeeded + 78 + witchPositionAdd


def findBestSpell(potion, inventory):
    # Make a new tab that gets what we miss for the recepie
    potionNeeds = []
    bestUsefullness = -20
    bestSpell = 0
    for i in range(4):
        potionNeeds.append(potion[i] + inventory[i])

    print("Potion needs " + str(potionNeeds), file=sys.stderr, flush=True)
    # Now that we know what we miss from the recepie, we can check what spell is best to cast
    for spell in casts:
        currentUsefulness = returnUsefullness(potionNeeds, spell.inventoryChanges.tabIngredients)
        if currentUsefulness > bestUsefullness:
            # Check what we have to do to craft it
            bestUsefullness = currentUsefulness
            bestSpell = spell
    # Now that we have the best cast for the recepie, we have to check if we have the ingredients, if we dont, we gotta cast
    # the best spells until we have them
    bestSpell = needsForCraft(inventory, bestSpell)
    if not bestSpell.castable:
        return ActionForTurn("REST", -1)
    else:
        return ActionForTurn("CAST ", str(bestSpell.id))


# Recursive check to find what spells needs
def needsForCraft(invTab, bestSpell):
    faultyIngredient = findFaultyIngredient(invTab, bestSpell)
    print("Went into needs for craft " + str(bestSpell.id), file=sys.stderr, flush=True)
    whiteListedSpells = casts.copy()
    while (findFaultyIngredient(invTab, bestSpell)[0] != -1):
        print("Best spell " + str(bestSpell.id), file=sys.stderr, flush=True)
        faultyIngredient = findFaultyIngredient(invTab, bestSpell)
        # Make an empty tab for faulty engredient
        emptyTab = [0, 0, 0, 0]
        emptyTab[faultyIngredient[0]] = faultyIngredient[1]
        bestUsefulness = -20
        foundBestSpell = whiteListedSpells[0]
        for spell in whiteListedSpells:
            currentUsefullness = returnUsefullness(emptyTab, spell.inventoryChanges.tabIngredients)
            if currentUsefullness > bestUsefulness:
                bestUsefulness = currentUsefullness
                foundBestSpell = spell

        count = 0
        countInv = 0
        for i in range(4):
            count = count + foundBestSpell.inventoryChanges.tabIngredients[i]
            countInv =  countInv + invTab[i]

        if not(countInv + count >= 10):
            bestSpell = foundBestSpell
        # whiteListedSpells.remove(foundBestSpell)
        print("Found best spell " + str(foundBestSpell.id), file=sys.stderr, flush=True)
        whiteListedSpells.remove(foundBestSpell)
    return bestSpell


def findFaultyIngredient(invTab, bestSpell):
    # print("Went here with spell " + str(bestSpell.id), file=sys.stderr, flush=True)
    ingredient = -1
    amountMissing = 0
    for i in range(3, -1, -1):
        if -1 >= (invTab[i] + bestSpell.inventoryChanges.tabIngredients[i]):
            if ingredient == -1:
                ingredient = i
                amountMissing = invTab[i] + bestSpell.inventoryChanges.tabIngredients[i]
                # print("Faulty ingredient is " + str(i), file=sys.stderr, flush=True)
                # print("amount missing is " + str(invTab[i] + bestSpell.inventoryChanges.tabIngredients[i] ), file=sys.stderr, flush=True)
    return [ingredient, amountMissing]


def findBestBrew():
    return findHighestBrew()
    # if 2 > castedBrews:
    #     return brews[0]
    # else:
    #     return findFastestBrew(


def findFastestBrew():
    lowestPrice = 1000
    currentSelectedBrew = brews[0]
    for singleBrew in brews:
        if lowestPrice > singleBrew.prices:
            lowestPrice = singleBrew.prices
            currentSelectedBrew = singleBrew
    return currentSelectedBrew

def findHighestBrew():
    highestPrice = 0
    currentSelectedBrew = brews[0]
    for singleBrew in brews:
        if singleBrew.prices > highestPrice:
            highestPrice = singleBrew.prices
            currentSelectedBrew = singleBrew
    return currentSelectedBrew


def findSpellForPotion(potion):
    savedPotionId = 0
    bestUsefullness = -20
    currentBestLearned = True
    spellPosition = 0
    # Find best usefulnness in already learned spells
    for spell in casts:
        currentUsefullness = returnUsefullness(potion.inventoryChanges.tabIngredients,
                                               spell.inventoryChanges.tabIngredients)
        if currentUsefullness > bestUsefullness:
            bestUsefullness = currentUsefullness
    # Check tome spells
    for spell in tome:
        currentUsefullness = returnUsefullness(potion.inventoryChanges.tabIngredients,
                                               spell.inventoryChanges.tabIngredients)
        if currentUsefullness > bestUsefullness:
            bestUsefullness = currentUsefullness
            savedPotionId = spell.id
            currentBestLearned = False
        spellPosition = spellPosition + 1

    return [currentBestLearned, savedPotionId, spellPosition]


def returnUsefullness(potion, spell):
    usefullness = 0
    # print(spell, file=sys.stderr, flush=True)
    for i in range(4):
        if i == 0 and 0 > potion[i]:
            usefullness = usefullness + (((potion[i] + spell[i]) * 0.2) if potion[i] != 0 else 0)
        if i == 1 and 0 > potion[i]:
            usefullness = usefullness + (((potion[i] + spell[i]) * 1) if potion[i] != 0 else 0)
        if i == 2 and 0 > potion[i]:
            usefullness = usefullness + (((potion[i] + spell[i]) * 1.5) if potion[i] != 0 else 0)
        if i == 3 and 0 > potion[i]:
            usefullness = usefullness + (((potion[i] + spell[i]) * 2) if potion[i] != 0 else 0)
    # print("Calculated usefullness for spell " + str(spell) + " is " + str(usefullness), file=sys.stderr, flush=True)
    return usefullness


def findBrewList():
    brewListIds = ""
    for brew in brews:
        brewListIds = brewListIds + str(brew.id) + ", "
    print(brewListIds, file=sys.stderr, flush=True)


casts = []
brews = []
tome = []
castedBrews = 0
currentTurn = 0
while True:
    action_count = int(input())  # the number of spells and recipes in play
    brews.clear()
    casts.clear()
    tome.clear()
    for i in range(action_count):
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
        currentInventoryChanges = InventoryChanges(delta_0, delta_1, delta_2, delta_3)
        if action_type == "BREW":
            brews.append(Brew(action_type, action_id, currentInventoryChanges, price))
        if action_type == "CAST":
            casts.append(Cast(action_type, action_id, currentInventoryChanges, castable))
        if action_type == "LEARN":
            tome.append(TomePage(action_type, action_id, currentInventoryChanges, tax_count, tome_index, repeatable))

    actionForTurn = ActionForTurn("REST", -1)
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
            # tomeCheck = findSpellForPotion(selectedBrew)
            # if not tomeCheck[0]:
            #     if tomeCheck[2] > tab_inv[0]:
            #         if casts[0].castable:
            #             actionForTurn.action = "CAST "
            #             actionForTurn.id = "78"
            #         else:
            #             actionForTurn.action = "REST"
            #             actionForTurn.id = "0"
            #     else:
            #         actionForTurn.action = "LEARN "
            #         actionForTurn.id = str(tomeCheck[1])
            if 10 > len(casts):
                actionForTurn.action = "LEARN "
                actionForTurn.id = tome[0].id
            elif 1 >= inv_0 and casts[0].castable:
                actionForTurn.action = "CAST "
                actionForTurn.id = str(78 + witchPositionAdd)
            else:
                actionForTurn = findBestSpell(selectedBrew.inventoryChanges.tabIngredients, tab_inv)

            # START section to check if we can craft the potion
            canCraft = False
            for brew in brews:
                testingBrews = True
                for ingredient in range(4):
                    if testingBrews:
                        testingBrews = (int(tab_inv[ingredient]) + int(
                            brew.inventoryChanges.tabIngredients[ingredient])) >= 0
                if testingBrews:
                    selectedBrew = brew
                    canCraft = True

            if canCraft:
                actionForTurn.action = "BREW "
                actionForTurn.id = selectedBrew.id
            # END section to check if we can craft the potion
    # Write an action using print
    print("Debug messages...", file=sys.stderr, flush=True)
    if actionForTurn.action == "REST":
        actionForTurn.id = -1
    printID = str(actionForTurn.id) if actionForTurn.id != -1  else ""

    print(actionForTurn.action + str(printID) + " Going for you potion " + str(selectedBrew.id))

    castedBrews = castedBrews + 1

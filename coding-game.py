import sys


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

# Recursive check to find what spells needs
def needsForCraft(invTab):
    whiteListedSpells = casts.copy()
    needsMoreSpace = True
    needsMoreIngredients = True
    spellIsExhausted = True
    foundBestSpell = casts[0]
    # Spell enter debug
    while (needsMoreIngredients or needsMoreSpace or spellIsExhausted):
        foundBestSpell = casts[0]
        # Make an empty tab for faulty ingredient
        # Combine Inventory and potion to get what we are missing
        combinedPotionAndInv = []
        for i in range(4):
            combinedPotionAndInv.append(invTab[i] + selectedBrew.inventoryChanges.tabIngredients[i])

        bestUsefulness = -20
        for spell in whiteListedSpells:
            currentUsefullness = returnUsefullness(spell.id, combinedPotionAndInv,
                                                   spell.inventoryChanges.tabIngredients, invTab)
            if currentUsefullness > bestUsefulness:
                bestUsefulness = currentUsefullness
                foundBestSpell = spell

        # Check if we can fill the items in the inventory
        needsMoreIngredients = False
        needsMoreSpace = False
        count = 0
        countInv = 0
        for i in range(4):
            count = count + foundBestSpell.inventoryChanges.tabIngredients[i]
            countInv = countInv + invTab[i]
            # Check if we have the ingredients for the spell
            itemCheck = invTab[i] + foundBestSpell.inventoryChanges.tabIngredients[i]
            if -1 >= itemCheck:
                needsMoreIngredients = True

        if countInv + count >= 10:
            needsMoreSpace = True

        spellIsExhausted = not foundBestSpell.castable
        #Check if the spell is exhausted
        print("Needs more space" + str(needsMoreSpace), file=sys.stderr, flush=True)
        print("Need more ingredients " + str(needsMoreIngredients), file=sys.stderr, flush=True)
        whiteListedSpells.remove(foundBestSpell)
        if len(whiteListedSpells) == 0:
            foundBestSpell.action = "REST"
            foundBestSpell.id = "-1"
            needsMoreSpace = False
            needsMoreIngredients = False
            spellIsExhausted = False
    return foundBestSpell


def findBestBrew():
    # return brews[0]
    print("Casted brews = " + str(castedBrews > 2), file=sys.stderr, flush=True)
    # if not castedBrews >= 3:
    #     return brews[0]
    # else:
    return findFastestBrew()
    # return findHighestBrew()
    # return findFastestBrew()
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


def returnUsefullness(id, potion, spell, inventory):
    usefullness = 0
    for i in range(4):
        usefullness = usefullness + (((potion[i] + spell[i])) if potion[i] != 0 else 0)
    print("Id : " + str(id) + " spell " + str(spell) + " is " + str(usefullness), file=sys.stderr, flush=True)
    return usefullness


selectedBrew = ""
casts = []
brews = []
tome = []
castedBrews = 0
currentTurn = 0
justCastedBrew = False
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
            casts.append(Cast(action_type + " ", action_id, currentInventoryChanges, castable))
        if action_type == "LEARN":
            tome.append(TomePage(action_type, action_id, currentInventoryChanges, tax_count, tome_index, repeatable))

    actionForTurn = ActionForTurn("REST", -1)
    witchPositionAdd = 0 if int(casts[0].id) == 78 else 4
    for i in range(2):
        selectedBrew = findBestBrew()
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        tab_inv = [inv_0, inv_1, inv_2, inv_3]

        if i == 0:
            if 18 > len(casts):
                actionForTurn.action = "LEARN "
                actionForTurn.id = tome[0].id
            elif justCastedBrew:
                actionForTurn.action = "REST"
                actionForTurn.id = -1
                justCastedBrew = False
            else:
                actionForTurn = needsForCraft(tab_inv)
            # canCraft = True
            # for ingredient in range(4):
            #     if canCraft:
            #         canCraft = (int(tab_inv[ingredient]) + int(
            #             selectedBrew.inventoryChanges.tabIngredients[ingredient])) >= 0
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
    if actionForTurn.action == "REST" or int(actionForTurn.id) == -1:
        actionForTurn.action = "REST"
        actionForTurn.id = -1

    printID = str(actionForTurn.id) if int(actionForTurn.id) != -1 else ""
    if actionForTurn.action == "BREW ":
        castedBrews = castedBrews + 1
        justCastedBrew = True

    print(actionForTurn.action + str(printID) + " Going for you potion " + str(selectedBrew.id))

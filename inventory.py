# inventory.py
held_item = 'gun'  # The item currently used by the player
inventory = ["gun","flyer"]

def add_item_to_inventory(item):
    if item not in inventory:
        inventory[item] = 1
    else:
        inventory[item] += 1

def decrease_inventory_item(item):
    if item in inventory and inventory[item] > 0:
        inventory[item] -= 1
        # If the item count hits 0, remove it from the dictionary
        if inventory[item] <= 0:
            del inventory[item]


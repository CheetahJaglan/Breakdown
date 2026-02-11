    
from setup import *

# A global list to keep track of each inventory slot.
inventory_slots = []

def add_ui():
    Entity(
        parent=camera.ui,
        model='quad',
        color=color.rgb32(200, 200, 200),
        scale=(0.04, 0.003)
    )
    Entity(
        parent=camera.ui,
        model='quad',
        color=color.rgb32(200, 200, 200),
        scale=(0.003, 0.04)
    )
    slot_count = 8  # Number of slots you want to display.
    x_start = -0.65
    x_spacing = 0.09  # Adjust spacing as needed.

    for i in range(slot_count):
        x_pos = x_start + i * x_spacing + 0.4

        # Slot background entity.
        slot_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba32(200, 200, 200, 200),
            scale=(0.07, 0.07),
            position=(x_pos, -0.43),
            z=-1
        )

        # Icon entity (will show the item's texture).
        icon = Entity(
            parent=slot_bg,
            model='quad',
            scale=(0.8, 0.8),
            color=color.rgba32(200, 200, 200, 0),
            position=(0, 0, -0.01),  # Centered in the slot.
            texture=None  # Will be set when updating.
        )

        # Count text entity positioned below the icon.
        count_text = Text(
            parent=slot_bg,
            text='',
            position=(0.1, -0.4, -0.01),  # Adjust the y-value to move the text lower.
            origin=(0.5, 1),              # Centered horizontally.
            scale=10,
            color=color.white
        )

        inventory_slots.append({
            'slot_bg': slot_bg,
            'icon': icon,
            'count_text': count_text,
            'item_type': None  # Tracks which item is assigned to this slot.
        })

def update_inventory_ui(item_held):
    """
    Updates each inventory slot with the corresponding item icon and count.
    If there are fewer items than slots, remaining slots will be cleared.
    Also highlights the slot corresponding to the selected block (block_to_place).
    """
    items_list = player.inventory 
    for i, slot in enumerate(inventory_slots):
        if i < len(items_list):
            item_type = items_list[i]
            slot['icon'].color = color.rgba32(255, 255, 255, 255)
            slot['icon'].texture = f'textures/inv/{item_type}_inv.png'
            slot['item_type'] = item_type
        else:
            # Clear any unused slots.
            slot['icon'].texture = None
            slot['count_text'].text = ''
            slot['item_type'] = None
            slot['icon'].color = color.rgba32(255, 255, 255, 0)

        # Highlight the slot if its item_type matches the currently selected block.
        if slot['item_type'] == item_held:
            slot['slot_bg'].color = color.white
        else:
            slot['slot_bg'].color = color.rgba32(200, 200, 200, 200)

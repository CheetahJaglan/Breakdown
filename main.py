from setup import *
from ui import *





def update():
    if held_keys['left mouse']:
        if held_item == 'gun':
            shoot()


def input(key):

    global held_item
    # Cycle items
    if key in ('scroll down', 'scroll up'):
            


        idx = inventory.index(held_item)
        if key == 'scroll down':
            next_idx = (idx + 1) % len(inventory)
        else:
            next_idx = (idx - 1) % len(inventory)
            held_item = inventory[next_idx]
        update_inventory_ui(item_held=held_item)


def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)


sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

add_ui()
update_inventory_ui(held_item)
app.run()


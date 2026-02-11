
from ui import *


def update():
    if held_keys['left mouse']:
        if player.held_item == 'gun':
            shoot()
    if held_keys['space'] and player.held_item == 'flyer':
            # self.gravity = 0
            player.fly()
            


def input(key):

    global player
    # Cycle items
    if key in ('scroll down', 'scroll up'):
            


        idx = player.inventory.index(player.held_item)
        if key == 'scroll down':
            next_idx = (idx + 1) % len(player.inventory)
            if player.held_item == 'gun':
                player.gun.visible = True
            else:
                player.gun.visible = False
        else:
            next_idx = (idx - 1) % len(player.inventory)
            player.held_item = player.inventory[next_idx]
            if player.held_item == 'gun':
                player.gun.visible = True
            else:
                player.gun.visible = False
        update_inventory_ui(item_held=player.held_item)


def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled

        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)


sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

add_ui()
update_inventory_ui(player.held_item)
app.run()


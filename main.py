
from ui import *


def update():
    if held_keys['left mouse']:
        if player.held_item == 'gun' or player.held_item == 'supergun':
            shoot()
    if held_keys['space'] and player.held_item == 'flyer':
            # self.gravity = 0
            player.fly()
    
    if random.randint(0, 500) == 1 and enemies:
        enemy_groans[random.randint(0,len(enemy_groans)-1)].play()
    score_popup.text= f'Score : {score}'

    


def e5seccheck():
    if player.position.y < -50:
        player.position = Vec3(0,350,-10)
    invoke(e5seccheck, delay=10)

e5seccheck() # start the loop



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
            if player.held_item == 'gun' or player.held_item == 'supergun':
                player.gun.visible = True
                player.gun.color = color.red if player.held_item == 'supergun' else color.white
            else:
                player.gun.visible = False
        update_inventory_ui(item_held=player.held_item)




sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

add_ui()
update_inventory_ui(player.held_item)
app.run()


from player import *

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=256, texture='grass', texture_scale=(4,4))
player = Player()
editor_camera = EditorCamera(enabled=False, ignore_paused=True)


wave = 1

shootables_parent = Entity()
mouse.traverse_target = shootables_parent


for i in range(64):
    Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-32,32),
        z=random.uniform(-32,32) + 20,
        collider='box',
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1))
        )
    

def shoot():
    target = mouse.hovered_entity

    if player.held_item == 'gun':
        if not player.gun.on_cooldown:
            player.gun.on_cooldown = True
            player.gun.muzzle_flash.enabled = True

            ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
                  volume=0.5, wave='noise',
                  pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)

            invoke(player.gun.muzzle_flash.disable, delay=.05)
            invoke(setattr, player.gun, 'on_cooldown', False, delay=.15)

            # 👉 Damage check (distance-limited)
            if target and hasattr(target, 'hp') and target.hp > 0:
                dist = distance_xz(player.position, target.position)
                if dist <= 15:   # only damage if close enough
                    target.blink(color.red)
                    target.hp -= 10

    elif player.held_item == 'supergun':
        if not player.gun.on_cooldown:
            player.gun.on_cooldown = True
            player.gun.muzzle_flash.enabled = True

            ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
                  volume=1, wave='noise',
                  pitch=random.uniform(-8,-7), pitch_change=-12, speed=3.0)

            invoke(player.gun.muzzle_flash.disable, delay=.05)
            invoke(setattr, player.gun, 'on_cooldown', False, delay=.15)

            # 👉 Damage check (distance-limited)
            if target and hasattr(target, 'hp') and target.hp > 0:
                dist = distance_xz(player.position, target.position)
                if dist <= 15:
                    target.blink(color.red)
                    target.hp -= 100

            

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model=load_model('assets/models/enemy.obj') ,scale=(1), origin_y=-0.05, color=color.light_gray, collider='box',texture='assets/models/enemy.png', **kwargs)
        self.health_bar = Entity(parent=self, y=3.25, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):

        dist = distance_xz(player.position, self.position)
        if dist > 80:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        global wave
        self._hp = value
        if value <= 0:
            destroy(self)
            if self in enemies:
                enemies.remove(self)
                if len(enemies) == 0:
                    wave += 1
                    [spawn_enemy(x=1*i,z=1) for i in range(wave * 1)]

                    if wave % 5 == 0:
                        spawn_boss()
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
class Boss(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model=load_model('assets/models/enemy.obj') ,scale=(5), origin_y=-0.05,x=20, color=color.light_gray, collider='box',texture='assets/models/boss.png', **kwargs)
        
        self.health_bar = Entity(parent=self, y=3.25, model='cube', color=color.blue, world_scale=(1.5,.1,.1))
        self.max_hp = 1000
        self.hp = self.max_hp

    def update(self):

        dist = distance_xz(player.position, self.position)
        if dist > 80:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        global wave
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
enemies = []
# Enemy()
def spawn_enemy(**kwargs):
    e = Enemy(**kwargs) 
    enemies.append(e)
def spawn_boss():
    ursfx([(0.0, 1.0), (0.24, 1.0), (0.41, 0.97), (0.79, 0.76), (1.34, 0.0)], volume=1.0, wave='noise', pitch=-28, pitch_change=10, speed=0.5)
    Boss()

[spawn_enemy(x=1*i) for i in range(wave * 1)]



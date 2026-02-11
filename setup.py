from player import *

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
player = Player()
editor_camera = EditorCamera(enabled=False, ignore_paused=True)




shootables_parent = Entity()
mouse.traverse_target = shootables_parent


for i in range(16):
    Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-8,8),
        z=random.uniform(-8,8) + 8,
        collider='box',
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1))
        )
    

def shoot():
    if (not player.gun.on_cooldown):


        # print('shoot')
        player.gun.on_cooldown = True
        player.gun.muzzle_flash.enabled=True
        
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(player.gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, player.gun, 'on_cooldown', False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp') and mouse.hovered_entity.hp > 0:
            mouse.hovered_entity.blink(color.red)
            mouse.hovered_entity.hp -= 10

            


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model=load_model('textures/enemy.obj') ,scale=(1), origin_y=-0.05, color=color.light_gray, collider='box',texture='textures/enemy.png', **kwargs)
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
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


# Enemy()
enemies = [Enemy(x=x*10) for x in range(4)]



from libraries import *
class Player(Entity):
    def __init__(self, height=2, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 8
        self.height = height
        self.camera_pivot = Entity(parent=self, y=self.height)
        self.model = 'assets/models/enemy.obj'
        self.z = -10
        self.y = 350
        self.color = color.black
        self.origin_y = -.5
        self.collider = 'box'
        self.inventory = ['gun', 'flyer','supergun']
        self.held_item = 'gun'

        camera.parent = self.camera_pivot
        camera.position = Vec3.zero
        camera.rotation = Vec3.zero
        camera.fov = 125
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 0.5
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]


        for key, value in kwargs.items():
            setattr(self, key ,value)



        self.gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.white, on_cooldown=False)
        self.gun.muzzle_flash = Entity(parent=self.gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)


    def on_window_ready(self):
        camera.rotation = Vec3.zero


    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space' and self.held_item != 'flyer':
            self.jump()
        if key == 'space' and self.held_item == 'flyer':
            ursfx([(0.0, 1.0), (0.06, 0.66), (0.25, 0.5), (0.37, 0.42), (1.0, 0.0)], volume=0.67, wave='noise', pitch_change=12, speed=0.8)

    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True

    def fly(self):
        self.y += held_keys['space'] * time.dt * self.speed * 2
        
    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True
        # restore parent and position/rotation from before disablem in case you moved the camera in the meantime.
        if hasattr(self, 'camera_pivot') and hasattr(self, '_original_camera_transform'):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False
        self._original_camera_transform = camera.transform  # store original position and rotation
        camera.world_parent = scene
        
    def add_item_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory[item] = 1
        else:
            self.inventory[item] += 1

    def decrease_inventory_item(self,item):
        if item in self.inventory and self.inventory[item] > 0:
            self.inventory[item] -= 1
        # If the item count hits 0, remove it from the dictionary
            if self.inventory[item] <= 0:
                del self.inventory[item]



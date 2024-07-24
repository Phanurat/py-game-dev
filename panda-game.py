from panda3d.core import Point3, Vec3, loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor

# Configuration
loadPrcFileData('', 'win-size 800 600')  # Set window size

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Add the main character
        self.character = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.character.setScale(0.005, 0.005, 0.005)
        self.character.reparentTo(self.render)

        # Position the camera
        self.disableMouse()
        self.camera.setPos(0, -30, 6)
        self.camera.lookAt(self.character)

        # Add task to update the character's position
        self.taskMgr.add(self.update_character, "update_character")

        # Add keyboard controls
        self.accept("arrow_left", self.set_key, ["left", True])
        self.accept("arrow_right", self.set_key, ["right", True])
        self.accept("arrow_up", self.set_key, ["up", True])
        self.accept("arrow_down", self.set_key, ["down", True])
        self.accept("arrow_left-up", self.set_key, ["left", False])
        self.accept("arrow_right-up", self.set_key, ["right", False])
        self.accept("arrow_up-up", self.set_key, ["up", False])
        self.accept("arrow_down-up", self.set_key, ["down", False])

        self.key_map = {"left": False, "right": False, "up": False, "down": False}

    def set_key(self, key, value):
        self.key_map[key] = value

    def update_character(self, task):
        dt = globalClock.getDt()
        pos = self.character.getPos()

        if self.key_map["left"]:
            pos.x -= 10 * dt
        if self.key_map["right"]:
            pos.x += 10 * dt
        if self.key_map["up"]:
            pos.y += 10 * dt
        if self.key_map["down"]:
            pos.y -= 10 * dt

        self.character.setPos(pos)
        return Task.cont

app = MyApp()
app.run()

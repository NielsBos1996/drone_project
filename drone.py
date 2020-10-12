class Drone:
    def __init__(self, x, y, z, c):
        self.x = x
        self.y = y
        self.z = z
        self.v = 0
        self.phi = 0
        self.theta = 0
        self.color = ""
        self.target_x = None
        self.target_y = None
        self.target_z = None
        self.final_x =  None
        self.final_y =  None
        self.final_z =  None

    def update(self, x, y, z, v, phi, theta):
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.phi = phi
        self.theta = theta

    def set_target(self, x, y, z):
        self.target_x = x
        self.target_y = y
        self.target_Z = z

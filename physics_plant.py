"""
Add basic physics engine:
-add euler integration for vel, accel, and height

ASSUMPTIONS:
-constant mass
-constant thrust
-no thrust cut-off
-no drag
"""

# Imports
import constants as c   # Imported from constants.py


rocket_state = {            # rocket's starting parameters 
  "height": 0,              # m, rocket is at the ground
  "mass": c.INITIAL_MASS,   # kg, rocket's starting mass
  "velocity": 0,            # m/s, rocket is at rest
  "acceleration": 0,        # m/s^2, rocket isn't accelerating yet
  "sim_time": 0             # s, timer hasn't started yet
}

state_list = []             # will be used to store a "snapshot" of the rocket's state
                            # at each interval "dt"

# Functions
def forceCalculation():                                                 # place holder function until variable force 
                                                                        # is introducted in a later commit

  return c.AVG_THRUST + (c.INITIAL_MASS * c.GRAVITY)                    # net_force = thrust + weight, no drag yet

def accelCalculation(force):
  return force / c.INITIAL_MASS                                         # net_accel = force / mass

def velCalculation(velocity, acceleration):
  return velocity + (acceleration * c.DT)                               # final_vel = vel + (accel * dt)

def heightCalculation(height, velocity, acceleration):
  return height + velocity * c.DT + (1/2) * acceleration * (c.DT ** 2)  # h = v*dt + (1/2)*a*dt^2


def step(state):
  
  # Declaring variables
  height = state["height"]              # Retrieves height, mass, etc. from the rocket's state dictionary
  mass = state["mass"]                  # mass and acceleration until later commit
  velocity = state["velocity"]
  time = state["sim_time"]

  net_force = forceCalculation()
  net_acceleration = accelCalculation(net_force)
  final_velocity = velCalculation(velocity, net_acceleration)
  final_height = heightCalculation(height, final_velocity, net_acceleration)
  
  state_list.append(state.copy())                     # adds the rocket's previous state to the "state_list" list
  
  state["height"] = final_height                      # Updates rocket's state dictionary 
  state["velocity"] = final_velocity
  state["acceleration"] = net_acceleration
  state["sim_time"] = time + c.DT                     # increments time by dt (0.01 s)

step(rocket_state)                                    # 
                                                      # will be utilized in the next 

while rocket_state["sim_time"] <= 10:                 # keeps the rocket flying until time has reached 10 seconds
  step(rocket_state)                    

print(f"Final height: {rocket_state["height"]:.3f} m")  # small confirmation print-out, will be vastly expanded in a later commit

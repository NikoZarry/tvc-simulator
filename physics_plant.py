"""
Add basic rocket physics loop:
-add variable mass, force, and acceleration
-add thrust cut off once propellant is depleted

ASSUMPTIONS:
-constant thrust
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
def massCalculation(mass):                    # Decreases mass due to propellant being expelled
    return mass - (c.BURN_RATE * c.DT)        # mass - (rate propellant gets expelled per increment time)

def forceCalculation(mass, time):               # Calculates net forces affecting the rocket
  if time <= c.BURN_TIME:                       
    return c.AVG_THRUST + (mass * c.GRAVITY)    # Whilst there's propellant to burn, force is equal to
  else:                                         # Thrust + (Force due to gravity)
    return mass * c.GRAVITY                     # When propellant is out, only force is gravity (drag will be added in a later commit)

def accelCalculation(mass, force):                                      # Calculates acceleration due to net forces (F=ma)
  return force / mass                                                   # a = F/m

def velCalculation(velocity, acceleration):          # Calculates velocity due to acceleration
  return velocity + (acceleration * c.DT)            # final_vel = vel + (accel * dt)

def heightCalculation(height, velocity, acceleration):                   # Calculates height due to velocity
  return height + velocity * c.DT + (1/2) * acceleration * (c.DT ** 2)   # h = v*dt + (1/2)*a*dt^2

def step(state):                        # "step" function that runs every time step (0.01 s)
  
  # Declaring variables
  height = state["height"]              # Retrieves starting height, mass, etc. from the rocket's state dictionary
  mass = state["mass"]                   
  velocity = state["velocity"]
  time = state["sim_time"]

  if time <= c.BURN_TIME:                               # If there's still propellant burning, update mass
    state["mass"] = massCalculation(state["mass"])      # If propllenat is out, mass stays constant
    mass = state["mass"]

  net_force = forceCalculation(mass, time)
  net_acceleration = accelCalculation(mass, net_force)
  final_velocity = velCalculation(velocity, net_acceleration)
  final_height = heightCalculation(height, final_velocity, net_acceleration)
  
  state_list.append(state.copy())                     # adds a copy of the rocket's previous state to the "state_list" list
  
  state["height"] = final_height                      # Updates rocket's state dictionary 
  state["velocity"] = final_velocity
  state["acceleration"] = net_acceleration
  state["sim_time"] = time + c.DT                     # increments time by dt (0.01 s)

step(rocket_state)                                    # Runs a quick step in order to make the rocket's height non-zero
                                                      # Since the condition below runs whilst the rocket is airborne
while rocket_state["height"] >= 0:                    # Keeps incrementing time until the rocket reaches the ground
  step(rocket_state)                    


# PRINT OUT
print(f"\nFinal height: {rocket_state["height"]:.3f} m")  
print(f"\nFinal vertical veloctiy : {rocket_state["velocity"]:.3f} m/s")
print(f"\nFinal vertical acceleration: {rocket_state["acceleration"]:.3f} m/s^2")
print(f"\nFinal rocket mass: {rocket_state["mass"]:.3f} kg")
print(f"\nTheoretical final rocket mass: {c.FINAL_MASS:.3f} kg")
print(f"\nFinal sim_time: {rocket_state["sim_time"]:.3f} s")
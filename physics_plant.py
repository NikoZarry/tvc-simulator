"""
Phase 2:
Add rotational mechanics
- add beginning parameters
"""

# Imports
import constants as c   # Imported from constants.py
import math


rocket_state = {              # rocket's starting parameters 
  "height": 0,                # m, how far the rocket has ascended
  "mass": c.INITIAL_MASS,     # kg, how much mass the rocket contains
  "velocity": 0,              # m/s, how quickly the rocket is ascending
  "acceleration": 0,          # m/s^2, how quickly the rocket's velocity is changing
  "sim_time": 0,              # s, total elapsed time from start of rocket's ascent
  "pitch": 0,                 # degrees, how far the rocket's body axis has rotated off the vertical
  "angular_velocity": 0,      # degrees/s, how fast a rocket's body axis is rotating off the vertical
  "angular_acceleration": 0,  # degrees/s^2, how fast a rocket's angular velocity is changing

}

state_list = []                      # will be used to store a "snapshot" of the rocket's state
                                     # at each interval "dt"

step_count = 0                                      # tracks total number of step() calls
steps_per_second = round(c.PRINT_INTERVAL / c.DT)   # e.g. 100 when dt = 0.01

# Functions
def massCalculation(mass):                    # Decreases mass due to propellant being expelled
    return mass - (c.BURN_RATE * c.DT)        # mass - (rate propellant gets expelled per increment time)

def dragCalculation(velocity):    # Calculates air drag acting on the rocket
  drag = 0.5 * c.AIR_DENSITY * (velocity ** 2) * c.DRAG_COEFFICIENT * c.CROSS_SECTION_AREA
  if velocity >= 0:    # If the rocket moving upward, drag is pushing down
    return -drag
  else:                # If the rocket is falling downward, drag is pushing up
    return drag
  
def forceCalculation(mass, drag, time):                # Calculates net forces affecting the rocket
  if time <= c.BURN_TIME:      
    translational_thrust = c.AVG_THRUST * math.cos(math.radians(c.DELTA))   # Thrust applied to moving the rocket upward           
    return translational_thrust + (mass * c.GRAVITY) + drag    # Whilst there's propellant to burn, force is equal to
  else:                                                        # Thrust + (Force due to gravity)
    return (mass * c.GRAVITY) + drag                           # When propellant is out, only forces acting are gravity and drag

def torqueCalculation(time):                               # Calculates net torque acting on the rocket's center of mass
  if time <= c.BURN_TIME:
    return c.AVG_THRUST * c.LEG_DISTANCE * math.sin(math.radians(c.DELTA))    # torque = Tdsin(delta)
  else:
    return 0                                               # If burnout has passed, return zero torque

def accelCalculation(mass, force):          # Calculates acceleration due to net forces (F=ma)
  return force / mass                       # a = F/m

def angAccelCalculation(torque):         # Calculates angular acceleration due to net torque (torque=I*alpha)
  return torque / c.MOMENT_OF_INERTIA    # alpha = torque / I

def velCalculation(velocity, acceleration):          # Calculates velocity due to acceleration
  return velocity + (acceleration * c.DT)            # final_vel = vel + (accel * dt)

def angVelCalculation(ang_velocity, ang_acceleration):   # Calculates angular velocity due to angular acceleration
  return ang_velocity + (ang_acceleration * c.DT)        # final_angvel = angvel + (angaccel * dt)

def heightCalculation(height, velocity, acceleration):                   # Calculates height due to velocity
  return height + velocity * c.DT + (1/2) * acceleration * (c.DT ** 2)   # h = v*dt + (1/2)*a*dt^2

def pitchCalculation(pitch, angular_velocity, angular_acceleration):                    # Calculates pitch angle due to angular velocity
  return pitch + angular_velocity * c.DT + (1/2) * angular_acceleration * (c.DT ** 2)   # pitch = omega*dt + (1/2)*alpha*dt^2

def step(state):                        # "step" function that runs every time step (0.01 s)
  
  # Declaring variables
  height = state["height"]              # Retrieves starting translational and rotational values from the rocket's state dictionary
  pitch = state["pitch"]
  mass = state["mass"]                   
  velocity = state["velocity"]
  angular_velocity = state["angular_velocity"]
  time = state["sim_time"]

  if time <= c.BURN_TIME:                               # If there's still propellant burning, update mass
    state["mass"] = massCalculation(state["mass"])      # If propllenat is out, mass stays constant
    mass = state["mass"]

  air_drag = dragCalculation(velocity)
  net_force = forceCalculation(mass, air_drag, time)
  net_torque = torqueCalculation(time)
  net_acceleration = accelCalculation(mass, net_force)
  net_angular_acceleration = angAccelCalculation(net_torque)
  final_velocity = velCalculation(velocity, net_acceleration)
  final_angular_velocity = angVelCalculation(angular_velocity, net_angular_acceleration)
  final_height = heightCalculation(height, final_velocity, net_acceleration)
  final_pitch = pitchCalculation(pitch, final_angular_velocity, net_angular_acceleration)

  state["height"] = final_height                    # Updates rocket's state dictionary 
  state["pitch"] = final_pitch
  state["velocity"] = final_velocity
  state["angular_velocity"] = final_angular_velocity
  state["acceleration"] = net_acceleration          
  state["angular_acceleration"] = net_angular_acceleration
  state["sim_time"] = time + c.DT                   # increments time by dt (0.01 s)
  
  global step_count
  step_count += 1

  state_list.append(state.copy())                   # adds a copy of the rocket's previous state to the "state_list" list


def print_out():                                    # Prints out a line displaying relevant translational and rotational values
  height = rocket_state["height"]
  pitch = math.degrees(rocket_state["pitch"])
  velocity = rocket_state["velocity"]
  angular_vel = math.degrees(rocket_state["angular_velocity"])
  accel = rocket_state["acceleration"]
  angular_accel = math.degrees(rocket_state["angular_acceleration"])
  time = rocket_state["sim_time"]

  print(f"time elapsed = {time:>4.1f} s", end="  |  ")
  print(f"height = {height:>8.3f} m", end="  |  ")
  print(f"velocity = {velocity:>10.3f} m/s", end="  |  ")
  print(f"acceleration = {accel:>12.3f} m/s^2")
  print(f"", end="\t\t\t")
  print(f"  pitch = {pitch:>9.3f} °", end="  |  ")
  print(f"ang velocity = {angular_vel:>3.3f} °/s", end="  |  ")
  print(f"ang acceleration = {angular_accel:>8.3f} °/s^2")
  print("")

print("--------------------------------------- POWERED FLIGHT (BURN PHASE) ---------------------------------------")

step(rocket_state)                        # Runs a quick step in order to make the rocket's height non-zero
                                          # Since the condition below runs whilst the rocket is airborne

while rocket_state["height"] >= 0:        # Keeps incrementing time until the rocket reaches the ground

  step(rocket_state)
  
  if step_count % steps_per_second == 0:
    print_out()

  if round(rocket_state["sim_time"], 2) == c.BURN_TIME:
    print("--------------------------------- BURN OUT (PROPELLANT HAS BEEN DEPLETED) ---------------------------------")

  if state_list[-2]["velocity"] > 0 and state_list[-1]["velocity"] < 0: 
    print("------------------------------------------ DESCENT (VELOCITY < 0) ------------------------------------------")


# Interpolated final state
def interpolation(x0, x1, alpha):              # Blends between two values using alpha as the fraction between them
  return x0 + alpha * (x1 - x0)                # x = x0 + alpha * (x1 - x0), general linear interpolation


def final_state():                                                                    # Corrects the overshot landing state using linear interpolation

  state0 = state_list[-2]                                                             # Last logged state still at or above ground (before the crossing)
  state1 = state_list[-1]                                                             # First logged state that overshot below ground (after the crossing)

  alpha = (0 - state0["height"]) / (state1["height"] - state0["height"])              # Fraction of the timestep where height actually crossed 0
  rocket_state["height"] = 0                                                          # True landing height, exactly ground level

  final_time = interpolation(state0["sim_time"], state1["sim_time"], alpha)           # Interpolated sim_time at the true moment of landing
  rocket_state["sim_time"] = final_time

  final_velocity = interpolation(state0["velocity"], state1["velocity"], alpha)       # Interpolated velocity at the true moment of landing
  rocket_state["velocity"] = final_velocity
  
  final_accel = interpolation(state0["acceleration"], state1["acceleration"], alpha)  # Interpolated acceleration at the true moment of landing
  rocket_state["acceleration"] = final_accel

  final_pitch = interpolation(state0["pitch"], state1["pitch"], alpha)                # Interpolated pitch at the true moment of landing
  rocket_state["pitch"] = final_pitch

  final_angVel = interpolation(state0["angular_velocity"], state1["angular_velocity"], alpha)            # Interpolated angular velocity at the true moment of landing
  rocket_state["angular_velocity"] = final_angVel

  final_angAccel = interpolation(state0["angular_acceleration"], state1["angular_acceleration"], alpha)  # Interpolated angular accel at the true moment of landing
  rocket_state["angular_acceleration"] = final_angAccel

  print("------------------------------------------- LANDING (HEIGHT = 0) -------------------------------------------")
  print(f"time elapsed = {rocket_state["sim_time"]:>4.1f} s", end="  |  ")
  print(f"height = {rocket_state["height"]:>8.3f} m", end="  |  ")
  print(f"velocity = {rocket_state["velocity"]:>10.3f} m/s", end="  |  ")
  print(f"acceleration = {rocket_state["acceleration"]:>12.3f} m/s^2")
  print(f"", end="\t\t\t")
  print(f"  pitch = {math.degrees(rocket_state["pitch"]):>9.3f} °", end="  |  ")
  print(f"ang velocity = {math.degrees(rocket_state["angular_velocity"]):>3.3f} °/s", end="  |  ")
  print(f"ang acceleration = {math.degrees(rocket_state["angular_acceleration"]):>8.3f} °/s^2")
  print("------------------------------------------------------------------------------------------------------------")


apogee_state = max(state_list, key = lambda entry: entry["height"])                             # Rocket state where max height was achieved
maxv_state = max(state_list, key = lambda entry: entry["velocity"])                             # Rocket state where max velocity was achieved
maxa_state = max(state_list, key = lambda entry: abs(entry["acceleration"]))                    # Rocket state where max acceleration was achieved
burnout_list = [entry for entry in state_list if round(entry["sim_time"], 2) == c.BURN_TIME]    # A list of rocket states where elapsed time is = burnout time (just one state)
burnout_state = burnout_list[0]                                                                 # Rocket state where the propellant was completely depleted

final_state()       # Runs the interpolation, replaces rocket_state's overshot values with the true landing state

# PRINT OUT
print("\n\n\n------------------- FINAL PRINT OUT -------------------")
print(f"Apogee Height: {apogee_state["height"]:.3f} m, reached at {apogee_state["sim_time"]:.2f} s")  
print(f"\nMax Velocity: {maxv_state["velocity"]:.3f} m/s, reached at {maxv_state["sim_time"]:.2f} s")
print(f"\nMax Acceleration: {maxa_state["acceleration"]:.3f} m/s^2, reached at {maxa_state["sim_time"]:.2f} s")
print(f"\nBurnout Height: {burnout_state["height"]:.3f} m, Burnout Velocity: {burnout_state["velocity"]:.3f} m/s, reached at {burnout_state["sim_time"]:.2f} s")

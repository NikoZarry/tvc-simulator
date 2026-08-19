"""
Phase 3: PID Implementation
- transfer physics loop onto 'main.py'
"""

# Imports
import math

import constants as c  # Imported from constants.py

rocket_state = {              # rocket's starting parameters
  "height": 0,                # m, how far the rocket has ascended
  "mass": c.INITIAL_MASS,     # kg, how much mass the rocket contains
  "velocity": 0,              # m/s, how quickly the rocket is ascending
  "acceleration": 0,          # m/s^2, how quickly the rocket's velocity is changing
  "sim_time": 0,              # s, total elapsed time from start of rocket's ascent
  "pitch": c.STARTING_PITCH,  # radians, how far the rocket's body axis has rotated off the vertical. Positive = left rotation, Negative = right rotation
  "angular_velocity": 0,      # radians/s, how fast a rocket's body axis is rotating off the vertical
  "angular_acceleration": 0,  # radians/s^2, how fast a rocket's angular velocity is changing
}

state_list = []       # will be used to store a "snapshot" of the rocket's state
                      # at each interval "dt"

step_count = 0                                      # tracks total number of step() calls
print_interval = 0.1
steps_per_second = round(print_interval / c.DT)   # e.g. 100 when dt = 0.01

# Functions
def massCalculation(mass):                    # Decreases mass due to propellant being expelled
  return mass - (c.BURN_RATE * c.DT)          # mass - (rate propellant gets expelled per increment time)

def dragCalculation(velocity):    # Calculates air drag acting on the rocket
  drag = 0.5 * c.AIR_DENSITY * (velocity ** 2) * c.DRAG_COEFFICIENT * c.CROSS_SECTION_AREA
  if velocity >= 0:               # If the rocket moving upward, drag is pushing down
    return -drag
  else:                           # If the rocket is falling downward, drag is pushing up
    return drag

def forceCalculation(mass, drag, delta, time):                # Calculates net forces affecting the rocket
  if time <= c.BURN_TIME:
    translational_thrust = c.AVG_THRUST * math.cos(delta)                   # Thrust applied to moving the rocket upward
    return translational_thrust + (mass * c.GRAVITY) + drag                 # Whilst there's propellant to burn, force is equal to
  else:                                                                     # Thrust + (Force due to gravity)
    return (mass * c.GRAVITY) + drag                                        # When propellant is out, only forces acting are gravity and drag

def torqueCalculation(delta, time):                               # Calculates net torque acting on the rocket's center of mass
  if time <= c.BURN_TIME:
    return c.AVG_THRUST * c.LEG_DISTANCE * math.sin(delta)      # torque = Tdsin(delta)
  else:
    return 0                                               # If burnout has passed, return zero torque

def accelCalculation(mass, force):          # Calculates acceleration due to net forces (F=ma)
  return force / mass                       # a = F/m

def angAccelCalculation(torque):            # Calculates angular acceleration due to net torque (torque=I*alpha)
  return torque / c.MOMENT_OF_INERTIA       # alpha = torque / I

def velCalculation(velocity, acceleration):          # Calculates velocity due to acceleration
  return velocity + (acceleration * c.DT)            # final_vel = vel + (accel * dt)

def angVelCalculation(ang_velocity, ang_acceleration):   # Calculates angular velocity due to angular acceleration
  return ang_velocity + (ang_acceleration * c.DT)        # final_angvel = angvel + (angaccel * dt)

def heightCalculation(height, velocity):                   # Calculates height due to velocity
  return height + velocity * c.DT                          # h = v_new*dt 

def pitchCalculation(pitch, angular_velocity):                    # Calculates pitch angle due to angular velocity
  return pitch + angular_velocity * c.DT                          # pitch = omega_new*dt 

def step(state, delta, wind_gust=0):                        # "step" function that runs every time step (0.01 s)

  # Declaring variables
  height = state["height"]              # Retrieves starting translational and rotational values from the rocket's state dictionary
  pitch = state["pitch"]
  mass = state["mass"]
  velocity = state["velocity"]
  angular_velocity = state["angular_velocity"]
  time = state["sim_time"]

  if time <= c.BURN_TIME:                               # If there's still propellant burning, update mass
    state["mass"] = massCalculation(state["mass"])      # mass only updates whilst propellant is burning
    mass = state["mass"]

  air_drag = dragCalculation(velocity)
  net_force = forceCalculation(mass, air_drag, delta, time)
  net_torque = torqueCalculation(delta, time) + wind_gust
  net_acceleration = accelCalculation(mass, net_force)
  net_angular_acceleration = angAccelCalculation(net_torque)
  final_velocity = velCalculation(velocity, net_acceleration)
  final_angular_velocity = angVelCalculation(angular_velocity, net_angular_acceleration)
  final_height = heightCalculation(height, final_velocity)
  final_pitch = pitchCalculation(pitch, final_angular_velocity)

  state["height"] = final_height                    # Updates rocket's state dictionary
  state["pitch"] = final_pitch
  state["velocity"] = final_velocity
  state["angular_velocity"] = final_angular_velocity
  state["acceleration"] = net_acceleration
  state["angular_acceleration"] = net_angular_acceleration
  state["sim_time"] = time + c.DT                   # increments time by dt (0.01 s)

  global step_count
  step_count += 1

  state_list.append(state.copy())                   # adds a copy of the rocket's current state to the "state_list" list

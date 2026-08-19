"""
Phase 4: Telemetry logs, static charts, live animations
- export state_list onto a CSV file in order to be used for data analysis
"""

# Imports
import math

import constants as c
import controller as co
import physics_plant as ph

rocket_state = ph.rocket_state
state_list = ph.state_list
step = ph.step
print_interval = ph.print_interval
steps_per_second = ph.steps_per_second
delta = co.PID_controller(rocket_state["pitch"], rocket_state["angular_velocity"])

# Functions
def print_out():       # Prints out a line displaying relevant translational and rotational values
  height = rocket_state["height"]
  pitch = math.degrees(rocket_state["pitch"])
  velocity = rocket_state["velocity"]
  angular_vel = math.degrees(rocket_state["angular_velocity"])
  accel = rocket_state["acceleration"]
  angular_accel = math.degrees(rocket_state["angular_acceleration"])
  time = rocket_state["sim_time"]

  print(f"time elapsed = {time:>4.1f} s", end="  |  ")
  print(f"height = {height:>8.3f} m", end="  |  ")
  print(f"velocity = {velocity:>12.3f} m/s", end="  |  ")
  print(f"acceleration = {accel:>12.3f} m/s^2")
  print(end="\t\t\t")
  print(f"  pitch = {pitch:>10.3f}°", end="  |  ")
  print(f"ang velocity = {angular_vel:>8.3f} °/s", end="  |  ")
  print(f"ang acceleration = {angular_accel:>8.3f} °/s^2")
  print()


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

  final_delta = interpolation(state0["delta"], state1["delta"], alpha)              # Interpolated delta at the true moment of landing
  rocket_state["delta"] = final_delta

  print("----------------------------------------------- LANDING (HEIGHT = 0) -----------------------------------------------")
  print(f"time elapsed = {rocket_state["sim_time"]:>4.1f} s", end="  |  ")
  print(f"height = {rocket_state["height"]:>8.3f} m", end="  |  ")
  print(f"velocity = {rocket_state["velocity"]:>12.3f} m/s", end="  |  ")
  print(f"acceleration = {rocket_state["acceleration"]:>12.3f} m/s^2")
  print(end="\t\t\t")
  print(f"  pitch = {math.degrees(rocket_state["pitch"]):>10.3f}°", end="  |  ")
  print(f"ang velocity = {math.degrees(rocket_state["angular_velocity"]):>8.3f} °/s", end="  |  ")
  print(f"ang acceleration = {math.degrees(rocket_state["angular_acceleration"]):>8.3f} °/s^2")
  print("--------------------------------------------------------------------------------------------------------------------")


# Code Body
print("----------------------------------------------- STARTING PARAMETERS -----------------------------------------------\n")
print("Simulation Parameters:")
print(f"dt: {c.DT} s", end="   ")
print(f"Wind Gust Torque: {c.GUST_TORQUE:.2f} N*m, during time interval: ({c.GUST_TIME:.2f}, {c.GUST_TIME+c.GUST_DURATION:.2f}) s")
print("\nDimensions:")
print(f"Mass: {c.INITIAL_MASS:.2f} kg", end="   ")
print(f"Length: {c.LENGTH:.2f} m", end="   ")
print(f"Body Diameter: {c.DIAMETER * 1000:.2f} mm")
print("\nRocket Parameters:")
print(f"Propellant Mass: {c.PROP_MASS} kg", end="   ")
print(f"Burn Time: {c.BURN_TIME} s", end="   ")
print(f"Average Thrust: {c.AVG_THRUST} N")
print("\nPID Parameters:")
print(f"Proportional Gain: {c.KP:.2f}", end="   ")
print(f"Integral Gain: {c.KI:.2f} Hz", end="   ")
print(f"Derivative Gain: {c.KD:.2f} s", end="   ")
print(f"Max Gimbal Angle: ±{math.degrees(c.MAX_GIMBAL_ANGLE):.2f}° (+ points left, - points right)")
print("\nInitial Rocket State:")
print_out()
print("------------------------------------------- POWERED FLIGHT (BURN PHASE) -------------------------------------------\n")


step(rocket_state, delta)                 # Runs a quick step in order to make the rocket's height non-zero
                                          # Since the condition below runs whilst the rocket is airborne

while rocket_state["height"] >= 0:        # Keeps incrementing time until the rocket reaches the ground

  # Print less frequently once coasting starts (no more active correction, dynamics are slow),
  # versus the fast, actively-controlled burn phase where finer resolution actually matters.
  if rocket_state["sim_time"] >= c.BURN_TIME:
    print_interval = 0.5
    steps_per_second = round(print_interval / c.DT)

  delta = co.PID_controller(rocket_state["pitch"], rocket_state["angular_velocity"])

  # Apply the scripted wind gust torque only while sim_time falls inside its window.
  # Print the phase marker exactly once, right at the tick where the window opens or closes, not on every tick inside it.
  if round(rocket_state["sim_time"], 2) >= c.GUST_TIME and round(rocket_state["sim_time"], 2) <= c.GUST_TIME + c.GUST_DURATION:
    if round(rocket_state["sim_time"], 2) == c.GUST_TIME:
      print("--------------------------------------------- WIND GUST (ADDED TORQUE) ---------------------------------------------\n")
    step(rocket_state, delta, c.GUST_TORQUE)
    if round(rocket_state["sim_time"], 2) == c.GUST_TIME + c.GUST_DURATION:
      print("-------------------------------------- WIND GUST OVER (NO MORE ADDED TORQUE) --------------------------------------\n")
  else: 
    step(rocket_state, delta)

  if ph.step_count % steps_per_second == 0:
    print_out()

  if round(rocket_state["sim_time"], 2) == c.BURN_TIME:
    print("------------------------------------- BURN OUT (PROPELLANT HAS BEEN DEPLETED) -------------------------------------\n")

  if state_list[-2]["velocity"] > 0 and state_list[-1]["velocity"] < 0:
    print("---------------------------------------------- DESCENT (VELOCITY < 0) ----------------------------------------------\n")


for i, delta_val in zip(range(len(state_list)), co.delta_list):       # goes through each dictionary in state_list, and
  state_list[i]["delta"] = delta_val                                  # adds a key 'delta' and puts the respective delta value at that moment

apogee_state = max(state_list, key = lambda entry: entry["height"])                             # Rocket state where max height was achieved
maxp_state = max(state_list, key = lambda entry: abs(entry["pitch"]))                           # Rocket state where max pitch was achieved
maxd_state = max(state_list, key = lambda entry: abs(entry["delta"]))                           # Delta value with the largest magnitude, either direction
maxv_state = max(state_list, key = lambda entry: entry["velocity"])                             # Rocket state where max velocity was achieved
maxav_state = max(state_list, key = lambda entry: entry["angular_velocity"])                    # Rocket state where max angular velocity was achieved
maxa_state = max(state_list, key = lambda entry: abs(entry["acceleration"]))                    # Rocket state where max acceleration was achieved
maxaa_state = max(state_list, key = lambda entry: abs(entry["angular_acceleration"]))           # Rocket state where max angular acceleration was achieved
burnout_list = [entry for entry in state_list if round(entry["sim_time"], 2) == c.BURN_TIME]    # A list of rocket states where elapsed time is = burnout time (just one state)
burnout_state = burnout_list[0]                                                                 # Rocket state where the propellant was completely depleted

final_state()                           # Runs the interpolation, replaces rocket_state's overshot values with the true landing state
state_list[-1] = rocket_state.copy()    # Replaces state_list's last dictionary with the final interpolated rocket state

# PRINT OUT
print("\n\n\n---------------------------- FINAL PRINT OUT ----------------------------\n")
print(f"Rocket's Final Mass: {rocket_state["mass"]:.2f} kg")
print(f"\nApogee Height: {apogee_state["height"]:.3f} m, reached at {apogee_state["sim_time"]:.2f} s")
print(f"\nMax Ascent Velocity: {maxv_state["velocity"]:.3f} m/s, reached at {maxv_state["sim_time"]:.2f} s")
print(f"\nMax Acceleration: {maxa_state["acceleration"]:.3f} m/s^2, reached at {maxa_state["sim_time"]:.2f} s")
print(f"\nMax Pitch: {math.degrees(maxp_state["pitch"]):.3f}°, reached at {maxp_state["sim_time"]:.2f} s")
print(f"\nMax Delta: {math.degrees(maxd_state["delta"]):.3f}°, reached at {maxd_state["sim_time"]:.2f} s")
print(f"\nMax Angular Velocity: {math.degrees(maxav_state["angular_velocity"]):.3f} °/s, reached at {maxav_state["sim_time"]:.2f} s")
print(f"\nMax Angular Acceleration: {math.degrees(maxaa_state["angular_acceleration"]):.3f} °/s^2, reached at {maxaa_state["sim_time"]:.2f} s")
print(f"\nBurnout Height: {burnout_state["height"]:.3f} m, Burnout Velocity: {burnout_state["velocity"]:.3f} m/s, reached at {burnout_state["sim_time"]:.2f} s\n")

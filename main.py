
"""
Phase 3: PID Implementation
- transfer physics loop from 'physics.py' onto main
"""

# Imports
import physics_plant as ph
import constants as c
import math

rocket_state = ph.rocket_state
state_list = ph.state_list
step = ph.step
steps_per_second = ph.steps_per_second

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
  print(f"velocity = {velocity:>12.3f} m/s", end="  |  ")
  print(f"acceleration = {accel:>12.3f} m/s^2")
  print(f"", end="\t\t\t")
  print(f"  pitch = {pitch:>10.3f}°", end="  |  ")
  print(f"ang velocity = {angular_vel:>3.3f} °/s", end="  |  ")
  print(f"ang acceleration = {angular_accel:>8.3f} °/s^2")
  print("")

print("------------------------------------------- POWERED FLIGHT (BURN PHASE) -------------------------------------------\n")

step(rocket_state)                        # Runs a quick step in order to make the rocket's height non-zero
                                          # Since the condition below runs whilst the rocket is airborne

while rocket_state["height"] >= 0:        # Keeps incrementing time until the rocket reaches the ground

  step(rocket_state)

  if ph.step_count % steps_per_second == 0:
    print_out()

  if round(rocket_state["sim_time"], 2) == c.BURN_TIME:
    print("------------------------------------- BURN OUT (PROPELLANT HAS BEEN DEPLETED) -------------------------------------\n")

  if state_list[-2]["velocity"] > 0 and state_list[-1]["velocity"] < 0:
    print("---------------------------------------------- DESCENT (VELOCITY < 0) ----------------------------------------------\n")


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

  print("----------------------------------------------- LANDING (HEIGHT = 0) -----------------------------------------------")
  print(f"time elapsed = {rocket_state["sim_time"]:>4.1f} s", end="  |  ")
  print(f"height = {rocket_state["height"]:>8.3f} m", end="  |  ")
  print(f"velocity = {rocket_state["velocity"]:>12.3f} m/s", end="  |  ")
  print(f"acceleration = {rocket_state["acceleration"]:>12.3f} m/s^2")
  print(f"", end="\t\t\t")
  print(f"  pitch = {math.degrees(rocket_state["pitch"]):>10.3f}°", end="  |  ")
  print(f"ang velocity = {math.degrees(rocket_state["angular_velocity"]):>3.3f} °/s", end="  |  ")
  print(f"ang acceleration = {math.degrees(rocket_state["angular_acceleration"]):>8.3f} °/s^2")
  print("--------------------------------------------------------------------------------------------------------------------")


apogee_state = max(state_list, key = lambda entry: entry["height"])                             # Rocket state where max height was achieved
maxp_state = max(state_list, key = lambda entry: entry["pitch"])                                # Rocket state where max pitch was achieved
maxv_state = max(state_list, key = lambda entry: entry["velocity"])                             # Rocket state where max velocity was achieved
maxav_state = max(state_list, key = lambda entry: entry["angular_velocity"])                    # Rocket state where max angular velocity was achieved
maxa_state = max(state_list, key = lambda entry: abs(entry["acceleration"]))                    # Rocket state where max acceleration was achieved
maxaa_state = max(state_list, key = lambda entry: entry["angular_acceleration"])                # Rocket state where max angular acceleration was achieved
burnout_list = [entry for entry in state_list if round(entry["sim_time"], 2) == c.BURN_TIME]    # A list of rocket states where elapsed time is = burnout time (just one state)
burnout_state = burnout_list[0]                                                                 # Rocket state where the propellant was completely depleted

final_state()       # Runs the interpolation, replaces rocket_state's overshot values with the true landing state

# PRINT OUT
print("\n\n\n---------------------------- FINAL PRINT OUT ----------------------------")
print(f"Apogee Height: {apogee_state["height"]:.3f} m, reached at {apogee_state["sim_time"]:.2f} s")
print(f"\nMax Velocity: {maxv_state["velocity"]:.3f} m/s, reached at {maxv_state["sim_time"]:.2f} s")
print(f"\nMax Acceleration: {maxa_state["acceleration"]:.3f} m/s^2, reached at {maxa_state["sim_time"]:.2f} s")
print(f"\nMax Pitch: {math.degrees(maxp_state["pitch"]):.3f}°, reached at {maxp_state["sim_time"]:.2f} s")
print(f"\nMax Angular Velocity: {math.degrees(maxav_state["angular_velocity"]):.3f} °/s, reached at {maxav_state["sim_time"]:.2f} s")
print(f"\nMax Angular Acceleration: {math.degrees(maxaa_state["angular_acceleration"]):.3f} °/s^2, reached at {maxaa_state["sim_time"]:.2f} s")
print(f"\nBurnout Height: {burnout_state["height"]:.3f} m, Burnout Velocity: {burnout_state["velocity"]:.3f} m/s, reached at {burnout_state["sim_time"]:.2f} s")

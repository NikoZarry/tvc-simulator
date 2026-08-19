"""
Phase 4: Telemetry logs, static charts, live animations
- create static plots of the data achieved from the rocket's flight
"""

# Imports
import csv
import math

import matplotlib.pyplot as plt

import constants as c


def static_plotter(t_burnout):    # Main telemetric plotting function

  variables = {"height": [], "mass": [], "velocity": [], "acceleration": [], "sim_time": [],
          "pitch": [], "angular_velocity": [], "angular_acceleration": [], "delta": []}
  # Fresh dict built every call, not module-level, so repeated calls (e.g. different GUST_TORQUE runs)
  # never carry over stale data from a previous call

  with open("state_values.csv", "r", newline="") as f:            # Reads this call's CSV fresh, tied to when the function runs, not when the module gets imported
    reader = csv.DictReader(f)
    for row in reader:
      for key in variables:  # noqa: PLC0206
        if key in ["pitch", "angular_velocity", "delta"]:         # These are stored in radians in the CSV, converted to degrees here for display only
          variables[key].append(math.degrees(float(row[key])))
        else:
          variables[key].append(float(row[key]))                  # Everything else stays in its native unit (m, kg, m/s, etc)

  fig, axs = plt.subplots(5, 1, sharex=True, figsize=(10,8))      # 5 stacked panels, shared time axis so burnout/gust lines align vertically across all of them

  fig.suptitle("TVC Rocket Flight — Full Ascent, Wind Gust, and PID Response")

  axs[0].plot(variables["sim_time"], variables["height"])
  axs[0].set_ylabel("height (m)")

  axs[1].plot(variables["sim_time"], variables["velocity"], color="tab:orange")
  axs[1].set_ylabel("velocity (m/s)")

  axs[2].plot(variables["sim_time"], variables["pitch"], color="tab:green")
  axs[2].set_ylabel("pitch (°)")

  axs[3].plot(variables["sim_time"], variables["angular_velocity"], color="tab:red")
  axs[3].set_ylabel("angular velocity (°/s)")

  axs[4].plot(variables["sim_time"], variables["delta"], color="tab:purple")
  axs[4].set_ylabel("delta (°)")

  axs[-1].set_xlabel("time (s)")     # Only the bottom panel gets an x-label, since all 5 share the same time axis


  for i in range(len(axs)):
    if i == 0:                       # Legend only rendered once, on the top panel, to avoid repeating it across all 5
      axs[i].axvline(x=t_burnout, color="red", linestyle="--", label="Burnout", alpha=0.5, linewidth=1)
      axs[i].axvspan(xmin=c.GUST_TIME, xmax=c.GUST_TIME+c.GUST_DURATION, color="gray", alpha=0.3, label=f"Wind Gust Window ({c.GUST_TORQUE} N·m)")   # Torque pulled live from constants.py, so the label updates itself if GUST_TORQUE is retuned
      axs[i].grid(True, alpha=0.3)
      axs[i].legend()
    else:                            # Remaining panels get the same markers, just without labels or a legend call
      axs[i].axvline(x=t_burnout, color="red", linestyle="--", alpha=0.5, linewidth=1)
      axs[i].axvspan(xmin=c.GUST_TIME, xmax=c.GUST_TIME+c.GUST_DURATION, color="gray", alpha=0.3)
      axs[i].grid(True, alpha=0.3)

  fig.tight_layout()     # Called last, after every element (legend, markers, grid) is on the figure, so spacing accounts for all of it

  fig.savefig("telemetry_static.png", dpi=150, bbox_inches="tight")

  plt.close(fig)          # Frees this figure so repeated calls to static_plotter() don't silently accumulate open figures in memory
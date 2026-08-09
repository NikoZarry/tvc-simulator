# TVC Rocket Ascent Simulator

2D Thrust Vector Control simulator built from scratch in Python. Models rocket ascent under gravity with an actively gimbaled engine and a custom PID controller for pitch stabilization.

**Status:** Phase 1 complete. Starting Phase 2 (rotational mechanics).

## What's working (Phase 1)

- Variable-mass rocket ascent under thrust, gravity, and drag
- Semi-implicit Euler integration at 100 Hz
- Direction-aware aerodynamic drag (opposes whichever way the rocket's currently moving)
- Linear interpolation for the true landing state, corrects the overshoot inherent to discrete timestep simulation
- Phased console output (burn, burnout, descent, landing) with a flight summary: apogee, max velocity, max acceleration, burnout height and velocity

## Roadmap

- [x] Phase 1: Translational dynamics, drag, landing interpolation, flight summary output
- [ ] Phase 2: Rotational mechanics, pitch angle, angular velocity, moment of inertia, gimbal-induced torque
- [ ] Phase 3: PID controller with anti-windup for pitch stabilization
- [ ] Phase 4: Telemetry logging, static matplotlib charts, live animation

## Current assumptions

- Constant average thrust (real thrust curve planned as a later fidelity pass)
- Constant sea-level air density (altitude-based model planned as a later fidelity pass)
- Placeholder airframe values (dry mass, drag coefficient, diameter) pending real numbers

## Repo structure

- `constants.py` — motor and physics constants
- `physics_plant.py` — simulation engine
- `controller.py` — PID controller (Phase 3, not started)
- `main.py` — driver script (not started)
- `visualizer_static.py` / `visualizer_live.py` — plotting and animation (Phase 4, not started)

# TVC Rocket Ascent Simulator

2D Thrust Vector Control simulator, built from scratch in Python. The gimbal is currently locked at a fixed angle (open-loop); a PID controller for active pitch correction is the next phase.

**Status:** Phase 2 complete. Starting Phase 3 (PID controller).

## What's working (Phase 1)

Translational dynamics, verified against hand calculations before moving on.

- Variable-mass ascent under thrust, gravity, and drag
- Semi-implicit Euler integration at 100 Hz
- Direction-aware drag (opposes whichever way the rocket is currently moving)
- Linear interpolation to correct the landing overshoot from discrete timestepping
- Phased console output (burn, burnout, descent, landing) plus a flight summary: apogee, max velocity, max acceleration, burnout height and velocity

## What's working (Phase 2)

Rotational mechanics, built the same way as translation: one function per physical quantity (torque, moment of inertia, angular acceleration, angular velocity, pitch).

- Thrust splits by gimbal angle into a translational component (T cos δ) and a torque-producing component (T sin δ); both are now accounted for
- Rotational state (pitch, angular velocity, angular acceleration) is stored internally in radians, matching the physics behind τ = Iα, and converted to degrees only at print time
- Caught and fixed a units bug where angular acceleration was silently computed in radians but printed with a degrees label
- Verified against both boundary conditions: zero gimbal deflection produces zero rotation for the entire flight, a fixed nonzero deflection held through the full burn produces sustained, uncontrolled spin, the expected result with no correction in place
- Flight summary extended to include max pitch, max angular velocity, and max angular acceleration

## Roadmap

- [x] Phase 1: Translational dynamics, drag, landing interpolation, flight summary
- [x] Phase 2: Rotational mechanics, pitch, angular velocity, moment of inertia, gimbal torque
- [ ] Phase 3: PID controller with anti-windup
- [ ] Phase 4: Telemetry logging, static charts, live animation

## Current assumptions

- Constant average thrust; real thrust curve planned as a later fidelity pass
- Constant sea-level air density; altitude-based model planned as a later fidelity pass
- Placeholder airframe values (mass, drag coefficient, diameter, length), not yet based on measured hardware
- Moment of inertia treats the rocket as a uniform rod (uniform mass density, cylindrical body), doesn't yet account for nose cone taper or the motor's actual off-center mass
- Gimbal deflection is currently hardcoded; nothing reads pitch and corrects it yet, that's what Phase 3 adds

## Repo structure

- `constants.py`, motor and physics constants
- `physics_plant.py`, the simulation engine
- `controller.py`, PID controller (Phase 3, not started)
- `main.py`, driver script (not started)
- `visualizer_static.py` / `visualizer_live.py`, plotting and animation (Phase 4, not started)

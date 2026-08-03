# Thrust Curve constants (AeroTech J350W)
PROP_MASS = 0.375     # kg, mass of the propellant
MOTOR_MASS = 0.665    # kg, mass of the motor (including propellant)
BURN_TIME = 1.5       # s, time it takes to use all the propellant
AVG_THRUST = 445      # N, average thrust throughout ascent

# Rocket-specific estimates
DRY_ROCKET_MASS = 4   # kg, PLACEHOLDER: airframe + recovery + payload, no motor or propellant

# Derived constants
INITIAL_MASS = DRY_ROCKET_MASS + MOTOR_MASS   # kg, mass of the entire rocket at liftoff
FINAL_MASS = (DRY_ROCKET_MASS + MOTOR_MASS) - PROP_MASS
BURN_RATE = PROP_MASS / BURN_TIME             # kg/s, rate at which propellant is expelled

# Simulation / environment constants
GRAVITY = -9.81       # m/s^2
DT = 0.01             # s, 100 checks per second (100 Hz)
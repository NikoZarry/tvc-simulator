# Imports
import math

# Simulation / environment constants
PI = math.pi          # dimensionless
GRAVITY = -9.81       # m/s^2
DT = 0.01             # s, 100 checks per second (100 Hz)
AIR_DENSITY = 1.225   # kg/m^3, standard sea-level air density

# Thrust Curve constants (AeroTech J350W)
PROP_MASS = 0.375     # kg, mass of the propellant
MOTOR_MASS = 0.665    # kg, mass of the motor (including propellant)
BURN_TIME = 1.5       # s, time it takes to use all the propellant
AVG_THRUST = 445      # N, average thrust throughout ascent

# Rocket-specific estimates
DRY_ROCKET_MASS = 4     # kg, PLACEHOLDER: airframe + recovery + payload, no motor or propellant
DRAG_COEFFICIENT = 0.5  # dimeonsionless, PLACEHOLDER: represents how much a shape resists air flow
DIAMETER = 0.102        # m, PLACEHOLDER: diameter of the rocket's body tube

# Derived constants
INITIAL_MASS = DRY_ROCKET_MASS + MOTOR_MASS     # kg, mass of the entire rocket at liftoff
FINAL_MASS = INITIAL_MASS - PROP_MASS           # kg, final mass of the rocket, when all propellant is depleted
BURN_RATE = PROP_MASS / BURN_TIME               # kg/s, rate at which propellant is expelled
CROSS_SECTION_AREA = PI * (DIAMETER / 2) ** 2   # m^2, cross-sectional area of the rocket's circular body

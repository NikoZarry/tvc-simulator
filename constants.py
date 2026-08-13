# Imports
import math

# Simulation / environment constants
PI = math.pi          # dimensionless
GRAVITY = -9.81       # m/s^2
DT = 0.01             # s, 100 checks per second (100 Hz)
AIR_DENSITY = 1.225   # kg/m^3, standard sea-level air density
DELTA = 5             # degrees, angle of the nozzle with respect to the rocket's axis

# Thrust Curve constants (AeroTech J350W)
PROP_MASS = 0.375     # kg, mass of the propellant
MOTOR_MASS = 0.665    # kg, mass of the motor (including propellant)
BURN_TIME = 1.5       # s, time it takes to use all the propellant
AVG_THRUST = 445      # N, average thrust throughout ascent

# Rocket-specific estimates (PLACEHOLDERS)
DRY_ROCKET_MASS = 4     # kg, airframe + recovery + payload, no motor or propellant
DRAG_COEFFICIENT = 0.5  # dimeonsionless, represents how much a shape resists air flow
DIAMETER = 0.102        # m, diameter of the rocket's tube body
LENGTH = 1.8            # m, length of the rocket from tail to nose

# Derived constants
INITIAL_MASS = DRY_ROCKET_MASS + MOTOR_MASS                 # kg, mass of the entire rocket at liftoff
FINAL_MASS = INITIAL_MASS - PROP_MASS                       # kg, final mass of the rocket, when all propellant is depleted
BURN_RATE = PROP_MASS / BURN_TIME                           # kg/s, rate at which propellant is expelled
CROSS_SECTION_AREA = PI * (DIAMETER / 2) ** 2               # m^2, cross-sectional area of the rocket's circular body
LEG_DISTANCE = LENGTH / 2                                   # m, distance from pivot to torque application

# Assuming uniform mass density, constant mass, and cylindrical throughout entire rocket
MOMENT_OF_INERTIA = (1/12) * INITIAL_MASS * (LENGTH ** 2)   # kg*m^2, rocket's resistance to being rotated

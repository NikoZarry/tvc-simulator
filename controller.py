"""
Phase 3: PID Implementation
- Implemement PID function for pitch stabalization
"""

# Imports
import constants as c

PID_state = {
    "accumulated_error": 0
}

# Functions

def PID_controller(current_pitch, current_angular_velocity):
    error = -current_pitch
    rate_error = -current_angular_velocity
    PID_state["accumulated_error"] = PID_state["accumulated_error"] + error * c.DT
    accumulated_error = PID_state["accumulated_error"]

    P = c.KP * error
    I = c.KI * accumulated_error
    D = c.KD * rate_error

    delta = P + I + D

    clamped_delta = max(-c.MAX_GIMBAL_ANGLE, min(delta, c.MAX_GIMBAL_ANGLE))

    return clamped_delta

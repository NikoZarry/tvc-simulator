"""
Phase 3: PID Implementation
- Implemement PID function for pitch stabalization
"""

# Imports
import constants as c

PID_state = {                  # stores the accumulated error as time goes on
    "accumulated_error": 0
}

delta_list = []                # stores each updating delta


# Functions

def PID_controller(current_pitch, current_angular_velocity):            # function that controls the main PID system for pitch stabilization
    error = -current_pitch                   # error = target_pitch (0) - current pitch, tells you how "off" current pitch is from the target
    rate_error = -current_angular_velocity   # d(error)/dt = -d(pitch)/dt = -(angular velocity), tells you the rate at which error is changing
    accumulated_error = PID_state["accumulated_error"] + error * c.DT   # accumulated error = accumulated error + error * dt,  accumulates error over time so the controller can correct for persistent, sustained offset


    P = c.KP * error                                                            # proportional contribution to delta
    I = c.KI * accumulated_error                                                # integral contribution to delta
    D = c.KD * rate_error                                                       # derivative contribution to delta

    delta = P + I + D                                                           # delta = sum of the PID contributions

    clamped_delta = max(-c.MAX_GIMBAL_ANGLE, min(delta, c.MAX_GIMBAL_ANGLE))    # clamps delta to ensure that it doesn't surpass MAX_GIMBAL_ANGLE in either direction


    # Anti-windup: only let the integral term accumulate when doing so is actually useful.

    if abs(clamped_delta) != c.MAX_GIMBAL_ANGLE:               # gimbal isn't saturated, integrate normally
        PID_state["accumulated_error"] = accumulated_error

    else:                                                      # gimbal is pinned at its limit   

        # Only keep accumulating if error is already pulling delta back off the limit (opposite sign of clamped_delta)
        # Same sign would mean the raw, unclamped PID output still wants even more deflection than the actuator can give,
        # so integrating further would just inflate accumulated_error with no real correction to show for it          

        if error * clamped_delta < 0:                           
            PID_state["accumulated_error"] = accumulated_error   

    delta_list.append(clamped_delta)                                

    return clamped_delta                                                                

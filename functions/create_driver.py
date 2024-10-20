import bpy
import XInput


def record_input():
    state = XInput.get_state(0)
    button_values = XInput.get_button_values(state)
    joystick_values = XInput.get_thumb_values(state)
    trigger_values = XInput.get_trigger_values(state)
    for index, input in enumerate(list(button_values.values()) + [y for x in joystick_values for y in x] + list(trigger_values)):
        if input > 0.7 or input < -0.7:
            if index >= 14:
                return 'input_drivers.analog_inputs[' + str(index-14) +']'
            else:
                return 'input_drivers.button_inputs[' + str(index) +']'
    return None

def create_driver(button):
    pointer = button.button_pointer
    prop = button.button_prop
    index = -1
    if hasattr(prop, 'is_array') and prop.is_array:
        bpy.ops.ui.copy_data_path_button(full_path=True)
        index = int(button.window_manager.clipboard.rsplit('[',1)[1].removesuffix(']'))
        
    fcurve = pointer.driver_add(prop.identifier, index)
    driver = fcurve.driver
    driver.type = 'AVERAGE'
    variable = driver.variables.new()
    driver_target = variable.targets[0]
    driver_target.id_type = 'SCENE'
    driver_target.id = button.scene
    return driver_target

def register():
    return {'REGISTERED'}

def unregister():
    return {'UNREGISTERED'}
import bpy
import XInput

def start_input():
    print("Starting...")
    
    # Check if a controller is detected
    connected = XInput.get_connected()[0]
    if connected:
        print("Controller detected.")
        
        #Call
        bpy.ops.inputdrivers.input_handle()
        
    else:
        print("No controller detected.")
        print("Quitting...")


def xinput_handling():
    input_drivers = bpy.context.scene.input_drivers
    state = XInput.get_state(0)
    button_values = XInput.get_button_values(state)
    input_drivers.button_inputs = list(button_values.values())
    
    joystick_values = XInput.get_thumb_values(state)
    trigger_values = XInput.get_trigger_values(state)
    input_drivers.analog_inputs = [y for x in joystick_values for y in x] + list(trigger_values)
    
    bpy.context.scene.update_tag()


class InputHandle(bpy.types.Operator):
    """Operator which handles pygame events"""
    bl_idname = "inputdrivers.input_handle"
    bl_label = "XInput input handle"
    
    _timer = None
    
    def modal(self, context, event):
        if event.type == 'ESC' or not bpy.context.scene.input_drivers.active_input:
            self.cancel(context)
            return {'CANCELLED'}
        
        xinput_handling()
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        # Modal Operator run
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print("Quitting...")



def register():
    bpy.utils.register_class(InputHandle)
    
    return {'REGISTERED'}

def unregister():
    bpy.utils.unregister_class(InputHandle)
    
    return {'UNREGISTERED'}
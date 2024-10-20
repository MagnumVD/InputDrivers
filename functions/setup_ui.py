import bpy
import XInput
from bpy.types import Header, Menu, Panel
import os
from . import run_game
from . import create_driver

class InputProperties(bpy.types.PropertyGroup):
    active_input : bpy.props.BoolProperty(
        name = "Activate Input",
        default = False
    )
    
    active_recording : bpy.props.BoolProperty(
        name = "Activate Recording",
        default = False
    )
    
    button_inputs : bpy.props.BoolVectorProperty(
        name = "Button Inputs",
        size = 14,
        default = tuple(False for x in range(14))
    )
    
    analog_inputs : bpy.props.FloatVectorProperty(
        name = "Analog Inputs",
        size = 6,
        default = tuple(False for x in range(6))
    )



class RunGameOperator(bpy.types.Operator):
    """Activates/Deactivates the Input"""
    bl_idname = "inputdrivers.run_game"
    bl_label = "Toggle Game"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the properties
        input_drivers = context.scene.input_drivers
        # Toggle the active input property
        input_drivers.active_input = not input_drivers.active_input
        # Run the script "start_input"
        if input_drivers.active_input:
            run_game.start_input()
        return {'FINISHED'}



class RecordGameOperator(bpy.types.Operator):
    """Activates/Deactivates the Recording"""
    bl_idname = "inputdrivers.record_game"
    bl_label = "Toggle Recording"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        def snap(self, context):
            input_drivers = bpy.context.scene.input_drivers
            input_drivers.keyframe_insert(data_path="button_inputs",group="input_drivers")
            input_drivers.keyframe_insert(data_path="analog_inputs",group="input_drivers")
        # Get the properties
        input_drivers = context.scene.input_drivers
        # Toggle the active input property
        input_drivers.active_recording = not input_drivers.active_recording
        # add or remove snap
        if input_drivers.active_recording:
            bpy.app.handlers.frame_change_pre.append(snap)
        else:
            for handler in bpy.app.handlers.frame_change_pre:
                if handler.__name__ == "snap":
                    bpy.app.handlers.frame_change_pre.remove(handler)
        return {'FINISHED'}




class CreateDriverOperator(bpy.types.Operator):
    """Hooks up the value to a set input"""
    bl_label = "Hook to input"
    bl_idname = "inputdrivers.create_driver"
    bl_options = {'REGISTER', 'UNDO'}
    
    _timer = None
    driver_target = None
        
    @classmethod
    def poll(cls, context):
        # Check if a controller is detected
        connected = XInput.get_connected()[0]
        if not connected:
            return False
        
        #Check if it's the right property
        if hasattr(context, 'button_prop'):
            prop = context.button_prop
            if prop.rna_type.identifier in {'BoolProperty','FloatProperty'}:
                return True
        return False
    
    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}
        
        key = create_driver.record_input()
        if not key == None:
            self.driver_target.data_path = key
            print("Driver Created")
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def execute(self, context):
        wm = context.window_manager
        
        if hasattr(context, 'button_prop'):
            prop = context.button_prop
            if prop.rna_type.identifier in {'BoolProperty','FloatProperty'}:
                #Create the driver
                self.driver_target = create_driver.create_driver(context)
                print("Awaiting input...")
                # Modal Operator run
                self._timer = wm.event_timer_add(0.1, window=context.window)
                wm.modal_handler_add(self)
                return {'RUNNING_MODAL'}
        
        print("Driver not allowed there")
        return {'CANCELLED'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print("Cancelled")

class WM_MT_button_context(Menu):
    bl_label = "Add Viddyoze Tag"

    def draw(self, context):
        pass

def create_driver_menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(CreateDriverOperator.bl_idname)









def get_button_text(property):
    if not property:
        return "Start "
    else:
        return "Stop "

def get_button_depress(property):
    if not property:
        return False
    else:
        return True

class InputDriversPanel(bpy.types.Panel):
    """InputDrivers Panel"""
    bl_label = "InputDrivers"
    bl_idname = "INPUTDRIVERS_PT_InputDriversPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "InputDrivers"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        input_drivers = scene.input_drivers
        
        # Check if a controller is detected
        connected = XInput.get_connected()[0]
        if connected:
            layout.label(text="Controller detected")
        else:
            layout.label(text="Please connect a controller (first port)")
        layout.separator()
        
        run_button = layout.row()
        run_button.scale_y = 3.0
        run_button.operator("inputdrivers.run_game", 
                        text=get_button_text(bpy.context.scene.input_drivers.active_input) + "Input", 
                        depress = get_button_depress(bpy.context.scene.input_drivers.active_input)
        )
        layout.separator()
        record_button = layout.row()
        record_button.scale_y = 3.0
        record_button.operator("inputdrivers.record_game", 
                        text=get_button_text(bpy.context.scene.input_drivers.active_recording) + "Recording", 
                        depress = get_button_depress(bpy.context.scene.input_drivers.active_recording)
        )




properties = [InputProperties]

classes = [RunGameOperator,
           RecordGameOperator,
           WM_MT_button_context,
           CreateDriverOperator,
           
           InputDriversPanel
           ]

def register():
    for cls in properties:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.input_drivers = bpy.props.PointerProperty(type=InputProperties)
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.WM_MT_button_context.append(create_driver_menu_func)
    
    return {'REGISTERED'}

def unregister():
    bpy.types.WM_MT_button_context.remove(create_driver_menu_func)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.input_drivers
    
    for cls in properties:
        bpy.utils.unregister_class(cls)
    
    return {'UNREGISTERED'}

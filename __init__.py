bl_info = {
    "name": "InputDrivers",
    "author": "MagnumVD",
    "version": (0, 4, 0),
    "blender": (3, 6, 2),
    "location": "View3D > InputDrivers",
    "description": "Lets you set variables with XInput gamepads",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Interface",
}

import bpy
import os
from .functions import install_xinput


class Install_XInput_Operator(bpy.types.Operator):
    """Activates/Deactivates the Input"""
    bl_idname = "inputdrivers.install_packages"
    bl_label = "Import pip and xinput"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Run the script "install_packages"
        install_xinput.install_packages()
        print("Reloading scripts")
        bpy.ops.script.reload()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

class InputDrivers_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    dependencies_path: bpy.props.StringProperty(
        name="Install path",
        description="Directory where additional dependencies for the addon are downloaded",
        subtype='DIR_PATH',
        default=os.path.realpath(os.path.expanduser("~/MVD-addons dependencies/InputDrivers"))
    ) # type: ignore
    
    def draw(self,context):
        layout = self.layout
        layout.prop(self, "dependencies_path")
        layout.separator()
        if install_xinput.register() == {'REGISTERED'}:
            layout.label(text="XInput is installed, nothing to do here!")
        else:
            row = layout.row()
            
            labels = row.column()
            labels.label(text="XInput needs to be installed,")
            labels.label(text="please press the button after selecting your Install path:")
            
            operators = row.column()
            operators.scale_y = 2.0
            operators.operator("inputdrivers.install_packages",text="Install")

class TutorialPanel(bpy.types.Panel):
    """Tutorial Panel"""
    bl_label = "Tutorial"
    bl_idname = "INPUTDRIVERS_PT_TutorialPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "InputDrivers"
    bl_context = "objectmode"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Thanks for using this addon!")
        layout.label(text="To get you started, here's a basic explanation:")
        layout.separator()
        
        layout.label(text='Step 1 - Install:')
        layout.label(text="This addon uses a custom python package called xinput-python.")
        layout.label(text="You'll need to install that first, but it's pretty easy:")
        layout.separator()
        
        layout.label(text="Navigate into the preferences of the addon and press the")
        layout.label(text="button which has 'Install' written on it.")
        layout.separator()
        
        layout.label(text='Step 2 - Setup:')
        layout.label(text="I recommend to turn of steams native controller support,")
        layout.label(text="as it can interfere with the input here.")
        layout.separator()
        
        layout.label(text="XBox gamepads are natively supported, so you can use them")
        layout.label(text="right out of the box. For other gamepads such as")
        layout.label(text="Playstation controllers you can use a programm like")
        layout.label(text="DS4windows, which emulates an XBox gamepad.")
        layout.separator()
        
        layout.label(text='Step 3 - Controlling:')
        layout.label(text="Get yourself a value you want to control,")
        layout.label(text="right-click it and choose 'Hook to input'.")
        layout.label(text="now press a button or move a stick along the axis")
        layout.label(text="you want to hook that property to.")
        layout.separator()
        
        layout.label(text="Now just start the input on the panel and see it move!")
        layout.label(text="If you have the recording button enabled aswell,")
        layout.label(text="you can save your controlls while playing the timeline.")
        layout.label(text="That way, it's possible to rewatch and render your gameplay")

classes = [InputDrivers_Preferences,
           Install_XInput_Operator,
           TutorialPanel
           ]

def register():
    
    if install_xinput.register() == {'REGISTERED'}:
        from .functions import setup_ui
        from .functions import create_driver
        from .functions import run_game
        setup_ui.register()
        create_driver.register()
        run_game.register()
    
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    if install_xinput.unregister() == {'UNREGISTERED'}:
        from .functions import setup_ui
        from .functions import create_driver
        from .functions import run_game
        setup_ui.unregister()
        create_driver.unregister()
        run_game.unregister()

if __name__ == "__main__":
    register()
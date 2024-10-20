This is an upload from an old experimental project.
It will be maintained, but probably not developed.

# InputDrivers

InputDrivers is an addon for controlling properties in your scene with a gamepad.

You can greate games with simulation nodes, use it to drive physics simulations or let it help you animate stuff.
The setup is done with almost no user input compared to other addons, so it's really fast to get ready and integrate into your scenes!

This addon also features a recorder for your inputs, so you can replay your actions.

## Installation

Go into the preferences and install the addon. After that in the drop down menu under the addon, you can set an installation dir and then install the dependencies. This can take a little bit of time and will freeze blender. You can track the progress in the system console.

Now, you can find InputDrivers in your image editor in the masking tab.

## Versions and compatibility

### OSs
I use XInput to get the controller data which is only available on Windows systems.

Using the addon on a different OS like linux has a high chance to crash or just not work (not tested).

### Controllers

PS4/5 controllers need an emulator to work, as they aren't supported by XInput. I recommend DS4Windows for that.

### Blender versions
The addon was tested with the following blender versions:

* 3.6
* 4.0
* 4.2
* 4.3

Older versions or custom blender forks probably work, I just didn't test them.

## License

InputDrivers as a whole is licensed under the GNU General Public License, Version 3. 
Individual files may have a different, but compatible license.

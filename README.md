blender-io_scene_fdm
====================

Blender exporter to FlightGear for animations and flight dynamics model configuration files.

Installation
------------

1. Copy or symlink the io_scene_fdm directory to the blender/2.6/scripts/addons directory. For linux this could be ~/.blender/2.6/scripts/addons or ~/.config/blender/2.69/scripts/addons.
2. Active plugin in Blender User Preferences ("Import-Export: Flightgear Plane & FDM")
3. It's a good idea to also install https://github.com/majic79/Blender-AC3D

Basic Usage
-----------

In the object property tab there is a new panel called "FlightGear". One object in the scene needs to be the root of all animated objects. This is indicated by setting its "Object Type" in the "FlightGear" panel to "Fuselage". This object will also contain all properties which are used to drive the animations.
Objects can be animated by using drivers. For example to let an object rotate round its y-axis right click on the Y rotation element and select "Add single driver". In the "FlightGear" panel there should now appear an "Animations" block listing all possible animations, i.e., all added drivers. Click on "Enable animation" to enable to create an animation for FlightGear.
Rotate the object to its initial position and press the new "Start" button. Afterwards rotate the object to the position at the end of the animation and press "End". The object will no rotate back to the specified intial position.
Now press "Select property" and either use an existing property or enter the name of a new property to create a new one. All properties are custom properties of the parent Fuselage object. You can use the "Custom Properties" panel of the Fuselage object to change property values and test the animations.

Export
------

1. Export model (File > Export > AC3D (.ac))
2. Export animations (File > Export > FlightGear FDM (.xml))
3. Use the created *.ac and *.model.xml files

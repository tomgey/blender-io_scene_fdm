bl_info = {
  "name": "Flightgear Plane & FDM",
  "author": "Thomas Geymayer",
  "version": (0, 1, 'a'),
  "blender": (2, 60, 7),
  "api": 42503,
#  "location": "File > Import-Export",
  "description": "Create and export Flightgear FDM and plane",
  "warning": "Pre Alpha",
  "wiki_url": "",
  "tracker_url": "",
  "category": "Import-Export"
}

# Blender module reloading...
if "bpy" in locals():
	import imp
	imp.reload(props)
	imp.reload(ui)
else:
	import bpy
	from io_blender2fgfs import props
	from io_blender2fgfs import ui

def register():
	bpy.utils.register_module(__name__)
	props.register()

def unregister():
	props.unregister()
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()
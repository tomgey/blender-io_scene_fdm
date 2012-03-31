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
	from io_scene_fdm import props
	from io_scene_fdm import ui

def menu_func_export(self, context):
  self.layout.operator(ExportFlightgearFDM.bl_idname, text='Flightgear FDM (.xml)')

def register():
	bpy.utils.register_module(__name__)
	props.register()
	bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
	props.unregister()
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
	register()

from bpy_extras.io_utils import ExportHelper
import time, datetime

class ExportFlightgearFDM(bpy.types.Operator, ExportHelper):
	'''Export to Flightgear FDM (.xml)'''
	bl_idname = 'export_scene.export_fgfs_fdm'
	bl_label = 'Export Flightgear FDM'
	bl_options = {'PRESET'}
	
	filename_ext = '.xml'
	
	def execute(self, context):
		t = time.mktime(datetime.datetime.now().timetuple())
		
		obs = []
		for ob in bpy.data.objects:
			if not ob.is_visible(context.scene) or ob.fgfs.type == 'DEFAULT':
				continue
			obs.append(ob)
	
		for ob in [o for o in obs if o.fgfs.type == 'STRUT']:
			print('Strut: '+ob.name)
	
		t = time.mktime(datetime.datetime.now().timetuple()) - t
		print('Finished exporting in', t, 'seconds')
	
		return {'FINISHED'}
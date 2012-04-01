'''
Write aircraft data to file(s)

@author: tom
'''

ft2m = 0.3048

import bpy, time, datetime
from bpy_extras.io_utils import ExportHelper
from . import aircraft, util

class Exporter(bpy.types.Operator, ExportHelper):
	'''Export to Flightgear FDM (.xml)'''
	bl_idname = 'export_scene.fdm'
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
	
		ground_reactions = util.XMLDocument('ground_reactions')
		model = util.XMLDocument('PropertyList')
	
		i = 0
		for ob in [o for o in obs if o.fgfs.type == 'STRUT']:
			gear = aircraft.gear.parse(ob)
			c = ground_reactions.createChild('contact')
			c.setAttribute('type', 'BOGEY')
			c.setAttribute('name', ob.name)
			
			l = c.createChild('location')
			l.setAttribute('unit', 'M')
			l.createChild('x', round(gear['location'].x, 3))
			l.createChild('y', round(gear['location'].y, 3))
			l.createChild('z', round(gear['location'].z, 3))
			
			c.createPropChild('static_friction', 0.8)
			c.createPropChild('dynamic_friction', 0.5)
			c.createPropChild('rolling_friction', 0.02)
			
			strut = gear['strut']
			c.createPropChild('spring_coeff', strut.spring_coeff, 'N/M')
			c.createPropChild('damping_coeff', strut.damping_coeff, 'N/M/SEC')
			c.createPropChild('max_steer', 60, 'DEG')
			
			c.createPropChild('brake_group', gear['gear'].brake_group)
			c.createPropChild('retractable', 1)
			
			a = model.createChild('animation')
			a.createPropChild('type', 'translate')
			a.createPropChild('object-name', ob.name)
			
			# jsbsim sets compression-norm to compression-ft, so to avoid confusion
			# we don't use it
			a.createPropChild('property', 'gear/gear['+str(i)+']/compression-ft')
			a.createPropChild('offset-m', -gear['current-compression'])
			a.createPropChild('factor', ft2m)
			
			ax = a.createChild('axis')
			ax.createChild('x', 0)
			ax.createChild('y', 0)
			ax.createChild('z', 1)
			
			i += 1
#    <interpolation>
#      <entry><ind> 0 </ind><dep>  -0.17 </dep></entry>
#      <entry><ind> 1 </ind><dep>  0.1 </dep></entry>
#    </interpolation>
		
		f = open(self.filepath, 'w')
		ground_reactions.writexml(f, " ", " ", "\n")
		f.close()
		
		f = open(self.filepath+'.model.xml', 'w')
		model.writexml(f, " ", " ", "\n")
		f.close()
	
		t = time.mktime(datetime.datetime.now().timetuple()) - t
		print('Finished exporting in', t, 'seconds')
	
		return {'FINISHED'}
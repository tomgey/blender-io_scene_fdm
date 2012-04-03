'''
Write aircraft data to file(s)

@author: tom
'''
import math, mathutils
from os import path

ft2m = 0.3048

import bpy, time, datetime
from bpy_extras.io_utils import ExportHelper
from . import aircraft, util

class AnimationsFGFS:
	'''Exporter for flightgear animations'''
	
	def __init__(self):
		self.model = util.XMLDocument('PropertyList')

	def save(self, filename):
		f = open(filename + '.model.xml', 'w')
		self.model.writexml(f, "", "\t", "\n")
		f.close()

	def addGear(self, gear, i):
		'''
		@param ob_strut	Gear data
		@param i				Gear index
		'''
		node = 'gear/gear['+str(i)+']/'
		
		# Compression
		a = self._createAnimation(gear['ob'].name, 'translate')
		a.createPropChild('property', node + 'compression-norm')
		a.createPropChild('offset-m', -gear['current-compression'])
		a.createPropChild('factor', ft2m) # TODO check yasim
		a.createVectorChild('axis', [0,0,1])
		
		# Steering
		if gear['gear'].steering_type == 'STEERABLE':
			a = self._createAnimation(gear['ob'].name, 'rotate')
			a.createPropChild('property', node + 'steering-norm')
			a.createPropChild('factor', math.degrees(gear['gear'].max_steer))
			a.createCenterChild(gear['ob'])
			a.createVectorChild('axis', [0,0,-1])
		else:
			# TODO check CASTERED
			pass
		
		# Wheel spin
		wheel_names = [w['ob'].name for w in gear['wheels']]
		a = self._createAnimation(wheel_names, 'spin')
		a.createPropChild('property', node + 'rollspeed-ms')

		first_wheel = gear['wheels'][0]
		dist = first_wheel['diameter'] * math.pi
		a.createPropChild('factor', 60 / dist) # dist per revolution to rpm
		a.createCenterChild(first_wheel['ob'])
		a.createVectorChild('axis', [0,-1,0])
		
	def _createAnimation(self, obs, anim_type):
		'''
		@param obs				Single or list of object names to be animated
		@param anim_type	Animation type
		'''
		a = self.model.createChild('animation')
		a.createPropChild('type', anim_type)
		if isinstance(obs, str):
			obs = [obs]
		for name in obs:
			a.createPropChild('object-name', name)

		return a

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
		exp_anim = AnimationsFGFS()
	
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
			
			if gear['gear'].steering_type == 'FIXED':
				max_steer = 0
			elif gear['gear'].steering_type == 'CASTERED':
				max_steer = 360
			else:
				max_steer = gear['gear'].max_steer
			c.createPropChild('max_steer', max_steer, 'DEG')
			
			c.createPropChild('brake_group', gear['gear'].brake_group)
			c.createPropChild('retractable', 1)
			
			exp_anim.addGear(gear, i)
			
			i += 1
#    <interpolation>
#      <entry><ind> 0 </ind><dep>  -0.17 </dep></entry>
#      <entry><ind> 1 </ind><dep>  0.1 </dep></entry>
#    </interpolation>
		
		f = open(self.filepath, 'w')
		ground_reactions.writexml(f, " ", " ", "\n")
		f.close()
		
		file_name = path.splitext(self.filepath)
		exp_anim.save(file_name[0])
	
		t = time.mktime(datetime.datetime.now().timetuple()) - t
		print('Finished exporting in', t, 'seconds')
	
		return {'FINISHED'}
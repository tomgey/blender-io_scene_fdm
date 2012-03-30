import bpy

def template_propbox(layout, label):
	col = layout.column(align=True)
	box = col.box()
	box.label(label)
	return col.box()

def layoutDefault(layout, ob):
	pass

def layoutFuselage(layout, ob):
	props = ob.fgfs.fuselage
	
	layout.label("Weights [kg]")
	layout.prop(props, 'empty_weight')
	
	layout.label("Moments of inertia [kg*m²]")
	col = layout.column(align=True)
	col.prop(props, 'ixx')
	col.prop(props, 'iyy')
	col.prop(props, 'izz')

def layoutStrut(layout, ob):
	strut = ob.data.fgfs.strut
	gear = ob.fgfs.gear
	
	instance_info = "(" + str(ob.data.users) + " instances)"

	box = template_propbox(layout, "Strut Options " + instance_info)
	box.label("Static compression [N*m⁻¹]")
	row = box.row(align=True)
	row.alignment = 'LEFT'
	row.prop(strut, 'spring_coeff', text = "Rate")
	
	unit_damping = "[N*m⁻¹*s⁻¹]"
	unit_damping_sq = "[N*m⁻²*s⁻²]"
	
	if strut.damping_coeff_squared:
		unit = unit_damping_sq
	else:
		unit = unit_damping
	
	box.label("Damping (compression) " + unit)
	row = box.row(align=True)
	row.alignment = 'LEFT'
	row.prop(strut, 'damping_coeff', text = "Rate")
	row.prop(strut, 'damping_coeff_squared', text = "Square",
																					 toggle = True)
	
	if strut.damping_coeff_rebound_squared:
		unit = unit_damping_sq
	else:
		unit = unit_damping
	
	box.label("Damping (rebound) " + unit)
	row = box.row(align=True)
	row.alignment = 'LEFT'
	row.prop(strut, 'damping_coeff_rebound', text = "Rate")
	row.prop(strut, 'damping_coeff_rebound_squared', text = "Square",
																									 toggle = True)
	
	box = template_propbox(layout, "Gear Options")
	box.prop(gear, 'brake_group')
	box.prop(gear, 'steering_type')
	if gear.steering_type == 'STEERABLE':
		box.prop(gear, 'max_steer')

# assign layouts to types
layouts = {
	'DEFAULT': layoutDefault,
	'FUSELAGE': layoutFuselage,
	'STRUT': layoutStrut,
	'WHEEL': layoutDefault
}

class FlightgearPanel(bpy.types.Panel):
	bl_label = "Flightgear"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	@classmethod
	def poll(self, context):
		if context.object and context.object.type == 'MESH':
			return True

	def draw(self, context):
		layout = self.layout
		ob = context.active_object
		
		layout.prop(ob.fgfs, 'type')
		layouts[ob.fgfs.type](layout, ob)

#	def _drawPlaneRoot(self, layout, ob):
#	layout.label('Aircraft')
#	
#	gears = util.getAllChildren(ob, 'Gear')
#	
#	if len(gears) < 3:
#	layout.label('Warning: Only %d gears found (Min. 3 needed)!' % len(gears))
#	
#	for child in gears:
#	layout.label(child.name)

import bpy

def template_propbox(layout, label):
	col = layout.column(align=True)
	box = col.box()
	box.label(label)
	return col.box()

def box_error(layout, text):
	box = layout.box()
	box.label(text, 'ERROR')

def box_info(layout, text):
	box = layout.box()
	box.label(text, 'INFO')

class DialogOperator(bpy.types.Operator):
	bl_idname = "fdm.dialog_select_prop"
	bl_label = "Select Property"
	
	def getProperties(self, context):
		return [(p, p, p) for p in bpy.data.objects['C130J-Fuselage'].keys() if p[0] == '/']

	prop = bpy.props.EnumProperty(items = getProperties)
	new_prop = bpy.props.StringProperty()
	target = bpy.props.StringProperty()

	def draw(self, context):
		layout = self.layout
		layout.prop(self, 'prop', "Use")
		layout.label("or")
		layout.prop(self, 'new_prop', "Create new")

	def execute(self, context):
		ob = context.active_object
		prop = self.prop

		if len(self.new_prop) > 0:
			prop = self.new_prop
			if prop[0] != '/':
				prop = '/' + prop
			bpy.data.objects['C130J-Fuselage'][prop] = 0

		i = self.target.split(':')

		driver = ob.animation_data.drivers[int(i[0])].driver
		driver.type = 'SUM'
		
		var = driver.variables[int(i[1])]
		var.type = 'SINGLE_PROP'

		target = var.targets[0]
		target.id_type = 'OBJECT'
		target.id = bpy.data.objects['C130J-Fuselage']
		target.data_path = '["' + prop + '"]'

		return {'FINISHED'}
	
	def invoke(self, context, event):
		return bpy.context.window_manager.invoke_props_dialog(self)

def layoutDefault(layout, ob):
	if not ob.animation_data:
		return
	
	for i_driver, driver in enumerate(ob.animation_data.drivers):
		for i_var, var in enumerate(driver.driver.variables):
			# We can only pass one argument to the operator, therefore we have to
			# combine the indices into one string
			indices = str(i_driver) + ':' + str(i_var)

			layout.label(var.targets[0].data_path)
			layout.operator('fdm.dialog_select_prop').target = indices

def layoutAnimated(layout, ob):
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
	
	num_wheels = len([o for o in ob.children if o.fgfs.type == 'WHEEL'])
	if not num_wheels:
		box_error(layout, "No wheels attached! (At least one is needed)")
	else:
		box_info(layout, str(num_wheels) + " wheels attached.")

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

def layoutTank(layout, ob):
	tank = ob.fgfs.tank
	
	box = template_propbox(layout, "Tank: " + ob.name)
	box.prop(tank, 'content')
	
	if tank.content == 'FUEL':
		unit = "[m³]"
	else:
		unit = "[l (dm³)]"
		
	col = box.column(align=True)
	col.prop(tank, 'capacity', text = "Capacity " + unit)
	col.prop(tank, 'unusable', text = "Unusable [%]")
	col.prop(tank, 'level', text = "Fill level [%]")

# assign layouts to types
layouts = {
	'DEFAULT': layoutDefault,
	'ANIMATED': layoutAnimated,
	'PICKABLE': layoutDefault,
	'FUSELAGE': layoutFuselage,
	'STRUT': layoutStrut,
	'WHEEL': layoutDefault,
	'TANK': layoutTank,
}

class FlightgearPanel(bpy.types.Panel):
	bl_label = "Flightgear"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	@classmethod
	def poll(self, context):
		if context.object and context.object.type in ['MESH', 'EMPTY']:
			return True

	def draw(self, context):
		layout = self.layout
		ob = context.active_object
		fuselage = ob
		while fuselage and fuselage.fgfs.type != 'FUSELAGE':
			fuselage = fuselage.parent
		layout.label(fuselage.name if fuselage else "NO FUSELAGE!")
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

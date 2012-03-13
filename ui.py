import bpy

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
		props = ob.fgfs
	
		layout.prop(props, 'type')
		
		if props.type == 'STRUT':
			props = ob.data.fgfs
			layout.label("Static compression [N*m⁻¹]")
			row = layout.row(align=True)
			row.alignment = 'LEFT'
			row.prop(props, 'spring_coeff', text = "Rate")
			
			unit_damping = "[N*m⁻¹*s⁻¹]"
			unit_damping_sq = "[N*m⁻²*s⁻²]"
			
			if props.damping_coeff_squared:
				unit = unit_damping_sq
			else:
				unit = unit_damping
			
			layout.label("Damping (compression) " + unit)
			row = layout.row(align=True)
			row.alignment = 'LEFT'
			row.prop(props, 'damping_coeff', text = "Rate")
			row.prop(props, 'damping_coeff_squared', text = "Square",
																							 toggle = True)
			
			if props.damping_coeff_rebound_squared:
				unit = unit_damping_sq
			else:
				unit = unit_damping
			
			layout.label("Damping (rebound) " + unit)
			row = layout.row(align=True)
			row.alignment = 'LEFT'
			row.prop(props, 'damping_coeff_rebound', text = "Rate")
			row.prop(props, 'damping_coeff_rebound_squared', text = "Square",
																											 toggle = True)
			
			layout.label("Options")
			layout.prop(props, 'brake_group')
			layout.prop(props, 'steering_type')
			if props.steering_type == 'STEERABLE':
				layout.prop(props, 'max_steer')
	
#	if ob.flightgear_type == 'Gear':
#	self._drawGear(layout, ob)
#	elif ob.flightgear_type == 'Aircraft':
#	self._drawPlaneRoot(layout, ob)
	
#	def _drawGear(self, layout, ob):
#	layout.label('Gear')
#	
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

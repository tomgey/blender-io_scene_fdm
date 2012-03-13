import bpy, math

class StrutProperties(bpy.types.PropertyGroup):
	spring_coeff = bpy.props.FloatProperty(
		name = "Spring coefficient",
		description = "Spring constant from Hooke's law (Static load/strut displacement = N/m)",
		subtype = 'UNSIGNED',
		min = 0,
		options = {'HIDDEN'}
	)
	damping_coeff = bpy.props.FloatProperty(
		name = "Damping coefficient",
		description = "Damping coefficient (Force proportional to strut displacement rate on compression = N/m/s)",
		subtype = 'UNSIGNED',
		min = 0,
		options = {'HIDDEN'}
	)
	damping_coeff_squared = bpy.props.BoolProperty(
		name = "Square damping",
		description = "Enable squared damping",
		options = {'HIDDEN'}
	)
	damping_coeff_rebound = bpy.props.FloatProperty(
		name = "Rebound damping coefficient",
		description = "Damping coefficient (Force proportional to strut displacement rate on rebound = N/m/s)",
		subtype = 'UNSIGNED',
		min = 0,
		options = {'HIDDEN'}
	)
	damping_coeff_rebound_squared = bpy.props.BoolProperty(
		name = "Square rebound damping",
		description = "Enable squared rebound damping",
		options = {'HIDDEN'}
	)
	brake_group = bpy.props.EnumProperty(
		name = "Brake group",
		description = "Brake group (Set to None for gears without brake)",
		items = [
			('LEFT', "Left", "Left"),
			('RIGHT', "Right", "Right"),
			('CENTER', "Center", "Center"),
			('NOSE', "Nose", "Nose"),
			('TAIL', "Tail", "Tail"),
			('NONE', "None", "None")
		],
		default = 'NONE',
		options = {'HIDDEN'}
	)
	steering_type = bpy.props.EnumProperty(
	  name = "Steering",
	  description = "Set steerability of gear",
		items = [
			('STEERABLE', 'Steerable', 'Steerable'),
			('FIXED', 'Fixed', 'Fixed (Steering disabled)'),
			('CASTERED', 'Castered', 'Castered (Free rotation)')
		],
		default = 'FIXED',
		options = {'HIDDEN'}
	)
	max_steer = bpy.props.FloatProperty(
		name = "Max steering",
		description = "Maximum steering angle (negative inverts steering)",
		subtype = 'ANGLE',
		unit = 'ROTATION',
		default = math.radians(60),
		min = math.radians(-360),
		max = math.radians(360),
		soft_min = math.radians(-80),
		soft_max = math.radians(80),
		options = {'HIDDEN'}
	)

class MeshProperties(bpy.types.PropertyGroup):
	pass

class ObjectProperties(bpy.types.PropertyGroup):
	type = bpy.props.EnumProperty(
		name = 'Object Type',
		description='Type for object in Flightgear',
		items = [
			('DEFAULT', "Default", "Object with no special handling."),
			('STRUT', 'Landing Gear Strut', 'Can be rotated while steering and is moved up and down according to compression. Needs at least on wheel as child.'),
			('WHEEL', 'Wheel', 'Is rotated according to speed while taxiing around. Has to be child of a Landing Gear Strut.')
		],
		default='DEFAULT',
		options = {'HIDDEN'}#,
		#update = _onTypeChange,
	)

def register():
	bpy.types.Object.fgfs = bpy.props.PointerProperty(
		type = ObjectProperties,
		name = "Flightgear",
		description = "Flightgear Settings"
	)
	bpy.types.Mesh.fgfs = bpy.props.PointerProperty(
		type = StrutProperties,
		name = "Flightgear",
		description = "Flightgear Settings"
	)

if __name__ == "__main__":
	register()

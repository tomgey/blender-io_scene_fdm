'''
Created on 10.12.2011

@author: tom
'''
import xml.dom.minidom as dom

class XMLDocument(dom.Document):
		'''
		XML helper class to simplify dom creation
		'''

		def __init__(self, name_root_element):
				'''
				Constructor
				'''
				super().__init__()
				self.__root = self.createElement(name_root_element)
				self.appendChild(self.__root)
				
		def root(self):
				'''
				Get the root element
				'''
				return self.__root

		def createElement(self, tag_name):
				e = XMLElement(tag_name)
				e.ownerDocument = self
				return e
		
		def createChild(self, tag_name, text = ''):
				return self.root().createChild(tag_name, text)

				
class XMLElement(dom.Element):
		
		def __init__(self, tag_name):
				super().__init__(tag_name)
				
		def createChild(self, tag_name, text = ''):
				e = XMLElement(tag_name)
				e.ownerDocument = self.ownerDocument
				self.appendChild(e)
				
				if len(str(text)):
						t = e.ownerDocument.createTextNode(str(text))
						e.appendChild(t)
				return e
		
		def createPropChild(self, tag_name, value, unit=''):
				'''
				Create a xml element representing a (numeric) property with an optional
				unit attribute
				'''
				fs = '%s'
				if( type(value) == float ):
						fs = '%.3f'
				else:
						value = str(value)

				c = self.createChild(tag_name, fs % value)
				if len(unit):
						c.setAttribute('unit', unit)				
				return c
			
		def createVectorChild(self, tag_name, vec, unit_suffix = ''):
				v = self.createChild(tag_name)
				v.createPropChild('x' + unit_suffix, vec[0])
				v.createPropChild('y' + unit_suffix, vec[1])
				v.createPropChild('z' + unit_suffix, vec[2])
				
				return v
			
		def createCenterChild(self, ob):
			'''
			Create a node with the center of the given object
			
			@param ob	Object
			'''
			return self.createVectorChild(
				'center',
				ob.matrix_world.translation,
				unit_suffix = '-m'
			)
		
		def writexml(self, writer, indent="", addindent="", newl=""):
				if (		 len(self.childNodes) == 1
								 and self.childNodes[0].nodeType == dom.Node.TEXT_NODE ):
						writer.write(indent)
						super().writexml(writer)
						writer.write(newl)
				else:
						super().writexml(writer, indent, addindent, newl)

def getAllChildren(ob, filter_type = ''):
	'''
	Get all children of the given object optionally filtered by a flightgear
	object type.
	'''
	children = []

	for child in ob.children:
		if filter_type == '' or child.fgfs.type == filter_type:
			children.append(child)
		children.extend( getAllChildren(child, filter_type) )

	return children
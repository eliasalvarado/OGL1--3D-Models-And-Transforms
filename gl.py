import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from Model import Model
from obj import Obj

class Renderer(object):
	def __init__(self, screen):
		_, _, self.width, self.height = screen.get_rect()

		self.clearColor = [0, 0, 0]

		glEnable(GL_DEPTH_TEST)
		# glGenerateMipmap(GL_TEXTURE_2D)
		glViewport(0, 0, self.width, self.height)

		self.scene = []

		self.activeShader = None
		
		self.directionalLight = glm.vec3(0,0,-1)

		self.camPosition = glm.vec3(0,0,0)
		self.camRotation = glm.vec3(0,0,0)

		self.projectionMatrix = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

	def setShader(self, vertex_shader, fragment_shader):
		if vertex_shader and fragment_shader:
			self.activeShader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
	
	def loadModel(self, filename, textureFile = None, potition = (0,0,0), rotation = (0,0,0), scale = (1,1,1)):
		modelData = Obj(filename=filename)
		data = []
		
		for face in modelData.faces:
			vertCount = len(face)
			
			v0 = modelData.vertices[face[0][0] - 1]
			vt0 = modelData.texCoords[face[0][1] - 1]
			vn0 = modelData.normals[face[0][2] - 1]
			[data.append(i) for i in v0]
			[data.append(vt0[i]) for i in range (2)]
			[data.append(i) for i in vn0]
			
			v1 = modelData.vertices[face[1][0] - 1]
			vt1 = modelData.texCoords[face[1][1] - 1]
			vn1 = modelData.normals[face[1][2] - 1]
			[data.append(i) for i in v1]
			[data.append(vt1[i]) for i in range (2)]
			[data.append(i) for i in vn1]	
			
			v2 = modelData.vertices[face[2][0] - 1]
			vt2 = modelData.texCoords[face[2][1] - 1]
			vn2 = modelData.normals[face[2][2] - 1]
			[data.append(i) for i in v2]
			[data.append(vt2[i]) for i in range (2)]
			[data.append(i) for i in vn2]
			
			if vertCount == 4:
				v3 = modelData.vertices[face[3][0] - 1]
				vt3 = modelData.texCoords[face[3][1] - 1]
				vn3 = modelData.normals[face[3][2] - 1]
				
				[data.append(i) for i in v0]
				[data.append(vt0[i]) for i in range (2)]
				[data.append(i) for i in vn0]
				
				[data.append(i) for i in v2]
				[data.append(vt2[i]) for i in range (2)]
				[data.append(i) for i in vn2]
				
				[data.append(i) for i in v3]
				[data.append(vt3[i]) for i in range (2)]
				[data.append(i) for i in vn3]

		model = Model(data=data, potition=potition, rotation=rotation, scale=scale)
		if textureFile:
			model.loadTexture(textureFile)
		
		self.scene.append(model)

	def getViewMatrix(self):
		identity = glm.mat4(1)

		translate = glm.translate(identity, self.camPosition)

		pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
		yaw = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
		roll = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))

		rotation = pitch * yaw * roll

		return glm.inverse(translate * rotation)

	def render(self):
		glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if self.activeShader:
			glUseProgram(self.activeShader)

			glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))
			glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(self.projectionMatrix))
			
			# glUniform1f(glGetUniformLocation(self.activeShader, "time"), self.ela)
			glUniform3fv(glGetUniformLocation(self.activeShader, "directionalLight"), 1, glm.value_ptr(self.directionalLight))

		for obj in self.scene:
			if self.activeShader:
				glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))
			obj.render()
	



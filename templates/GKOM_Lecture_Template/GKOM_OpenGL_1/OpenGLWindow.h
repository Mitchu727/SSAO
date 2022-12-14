#pragma once

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <iostream>

#include "Program.h"
#include "Utilities.h"

class OpenGLWindow
{
public:

	OpenGLWindow();
	~OpenGLWindow();

	bool InitWindow();

	void InitScene();

	void MainLoop();

private:

	GLFWwindow* _window;

	Program simpleProgram;

	GLuint triangleVAO;

	void processInput();

	glm::vec2 windowResolution;

};

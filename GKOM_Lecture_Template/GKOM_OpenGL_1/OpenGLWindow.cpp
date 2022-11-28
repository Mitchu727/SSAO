#include "OpenGLWindow.h"

void FramebufferSizeChangeCallback(GLFWwindow* window, int width, int height);

OpenGLWindow::OpenGLWindow()
{
	_window = nullptr;

    triangleVAO = 0;

    windowResolution = glm::vec2(800, 600);
}

OpenGLWindow::~OpenGLWindow()
{
    glfwTerminate();
}

bool OpenGLWindow::InitWindow()
{
    if (!glfwInit())
    {
        std::cerr << "GLFW initialization failed!" << std::endl;
        return false;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

    _window = glfwCreateWindow(windowResolution.x, windowResolution.y, "GKOM_OpenGL_1", NULL, NULL);

    if (_window == NULL)
    {
        std::cerr << "GLFW window creation failed!" << std::endl;
        glfwTerminate();
        return false;
    }

    glfwMakeContextCurrent(_window);

    if (glewInit())
    {
        std::cerr << "GLEW window creation failed!" << std::endl;
        glfwTerminate();
        return false;
    }

    glfwSetFramebufferSizeCallback(_window, FramebufferSizeChangeCallback);
}

void OpenGLWindow::InitScene()
{
    simpleProgram.Load("simpleshader.vs", "simpleshader.fs");

    triangleVAO = LoadTriangle();
}

void OpenGLWindow::MainLoop()
{
    while (!glfwWindowShouldClose(_window))
    {
        glClearColor(0.1f, 0.2f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        simpleProgram.Activate();

        glBindVertexArray(triangleVAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        processInput();

        glfwSwapBuffers(_window);
        glfwPollEvents();
    }
}

void OpenGLWindow::processInput()
{
    if (glfwGetKey(_window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
    {
        glfwSetWindowShouldClose(_window, true);
    }
}

void FramebufferSizeChangeCallback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}
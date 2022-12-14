#include "OpenGLWindow.h"

int main()
{
    Program::setProgramsDirectory("../Resources/Shaders/");
    
    OpenGLWindow openglWindow;

    openglWindow.InitWindow();

    openglWindow.InitScene();

    openglWindow.MainLoop();

    return 0;
}
#include "Program.h"

std::string Program::_programsDirectory = "";

Program::Program()
{
    _programID = 0;
}

void Program::setProgramsDirectory(std::string programDirectory)
{
    _programsDirectory = programDirectory;
}

std::string Program::getProgramsDirectory()
{
    return _programsDirectory;
}

GLuint Program::GetID()
{
    return _programID;
}

void Program::Activate()
{
    glUseProgram(_programID);
}

void Program::Deactivate()
{
    glUseProgram(0);
}

GLuint Program::GetUniformID(std::string uniformName)
{
    return _uniformsID.at(uniformName);
}

bool Program::Load(std::string vertexShaderFilePath, std::string fragmentShaderShaderPath)
{
    GLuint vertexShader;
    GLuint fragmentShader;

    std::string vertexShaderSource;
    std::string fragmentShaderSource;

    bool status;

    vertexShaderFilePath = _programsDirectory + "/" + vertexShaderFilePath;
    fragmentShaderShaderPath = _programsDirectory + "/" + fragmentShaderShaderPath;

    status = readFile(vertexShaderFilePath, vertexShaderSource);

    if (!status)
    {
        std::cerr << "Error loading vertex shader file " << vertexShaderFilePath << std::endl;
        return false;
    }

    status = readFile(fragmentShaderShaderPath, fragmentShaderSource);

    if (!status)
    {
        std::cerr << "Error loading fragment shader file " << fragmentShaderShaderPath << std::endl;
        return false;
    }

    status = compileShader(GL_VERTEX_SHADER, &vertexShader, vertexShaderSource);

    if (!status)
    {
        return false;
    }

    status = compileShader(GL_FRAGMENT_SHADER, &fragmentShader, fragmentShaderSource);

    if (!status)
    {
        return false;
    }

    status = linkProgram(vertexShader, fragmentShader);

    if (!status)
    {
        return false;
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    setupUniforms();

    return true;
}

bool Program::compileShader(GLenum shaderType, GLuint* shaderID, std::string shaderSource)
{
    GLuint shader;
    const char* shaderSourceCStr;
    int compilationSuccess;

    shaderSourceCStr = shaderSource.c_str();

    shader = glCreateShader(shaderType);
    glShaderSource(shader, 1, &shaderSourceCStr, NULL);
    glCompileShader(shader);

    glGetShaderiv(shader, GL_COMPILE_STATUS, &compilationSuccess);
    if (!compilationSuccess)
    {
        char infoLog[512];

        glGetShaderInfoLog(shader, 512, NULL, infoLog);

        switch (shaderType)
        {
        case GL_VERTEX_SHADER:
            std::cerr << "Vertex shader compilation failed:\n" << infoLog << std::endl;
            break;
        case GL_FRAGMENT_SHADER:
            std::cerr << "Fragment shader compilation failed:\n" << infoLog << std::endl;
            break;
        }

        glDeleteShader(shader);

        return false;
    }

    *shaderID = shader;

    return true;
}

bool Program::linkProgram(const GLuint vertexShaderID, const GLuint fragmentShaderID)
{
    GLuint program;

    int linkingSuccess;

    program = glCreateProgram();

    if(vertexShaderID)
        glAttachShader(program, vertexShaderID);

    if (fragmentShaderID)
        glAttachShader(program, fragmentShaderID);

    glLinkProgram(program);

    glGetProgramiv(program, GL_LINK_STATUS, &linkingSuccess);
    if (!linkingSuccess)
    {
        char infoLog[512];

        glGetProgramInfoLog(program, 512, NULL, infoLog);

        std::cerr << "Shader program linking failed: \n" << infoLog << std::endl;

        glDeleteProgram(program);

        return false;
    }
    
    _programID = program;;

    return true;
}

void Program::setupUniforms()
{
    const GLsizei maxUniformSize = 64;
    GLchar name[maxUniformSize];
    GLsizei uniformNamelength;
    GLint uniformsCount;
    GLint uniformSize;
    GLenum uniformType;

    glGetProgramiv(_programID, GL_ACTIVE_UNIFORMS, &uniformsCount);

    for (GLuint i = 0; i < uniformsCount; i++)
    {
        glGetActiveUniform(_programID, i, maxUniformSize, &uniformNamelength, &uniformSize, &uniformType, name);

        _uniformsID[name] = glGetUniformLocation(_programID, name);
    }
}

bool Program::readFile(std::string filePath, std::string& content) {

    content.clear();

    std::ifstream fileStream(filePath, std::ios::in);

    if (!fileStream.is_open()) {
        return false;
    }

    std::string line = "";
    while (!fileStream.eof()) {
        std::getline(fileStream, line);
        content.append(line + "\n");
    }

    fileStream.close();

    return true;
}
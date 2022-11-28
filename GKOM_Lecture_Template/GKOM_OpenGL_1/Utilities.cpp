#include "Utilities.h"
#include <numbers>

GLuint LoadTriangle()
{
    GLuint VBO;
    GLuint VAO;

    std::vector<glm::vec2> positions;

    positions.push_back(glm::vec2(-0.4, -0.3));
    positions.push_back(glm::vec2( 0.4, -0.3));
    positions.push_back(glm::vec2( 0.0,  0.6));

    struct Vertex
    {
        glm::vec2 position;
    };

    std::vector<Vertex> BufferData;

    for (int i = 0; i < positions.size(); i++)
    {
        BufferData.push_back({ positions[i] });
    }

    glGenBuffers(1, &VBO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(Vertex) * BufferData.size(), BufferData.data(), GL_STATIC_DRAW);

    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)0);

    glEnableVertexAttribArray(0);

    return VAO;
}

GLuint LoadCircle()
{
    GLuint VBO;
    GLuint VAO;

    glm::vec2 circleMiddle = glm::vec2(0.3f, -0.2f);
    float circleRadius = 0.4f;
    unsigned int segments = 50;

    std::vector<glm::vec2> positions;

    positions.push_back(circleMiddle + glm::vec2(-0.8, -0.3));

    for (int i = 0; i <= segments; i++)
    {
        float phi = float(i) / segments * 2 * std::numbers::pi;

        float x = circleMiddle.x + circleRadius * std::cos(phi);
        float y = circleMiddle.y + circleRadius * std::sin(phi);

        positions.push_back(glm::vec2(x, y));
    }

    struct Vertex
    {
        glm::vec2 position;
    };

    std::vector<Vertex> BufferData;

    for (int i = 0; i < positions.size(); i++)
    {
        BufferData.push_back({ positions[i] });
    }

    glGenBuffers(1, &VBO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(Vertex) * BufferData.size(), BufferData.data(), GL_STATIC_DRAW);

    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)0);

    glEnableVertexAttribArray(0);

    return VAO;
}
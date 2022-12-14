#version 330

in vec2 out_position;
out vec4 f_color;

uniform vec2 center;
uniform float scale;
uniform int iter;
uniform float ratio;


void main() {
    vec2 c;
    // obliczenie środka układu współrzędnych na obrazie
    c.x = ratio*out_position.x * scale - center.x;
    c.y = out_position.y * scale - center.y;
    vec2 z = c; // liczba zespolona, po której będzie odbywać się iteracja
    float xtemp = 0; // zmienna do tymczasowego przechowywania wartości x
    int i=0;
    for (i = 0; i < iter; i++)
    {
        xtemp = z[0]*z[0] - z[1]*z[1] + c[0];
        z.y = 2*z[0]*z[1] + c[1];
        z.x = xtemp;
        if (z[0]*z[0] + z[1]*z[1] > 4)
        {
            // jeśli moduł liczby zespolonej jest większy od dwóch to punkt nie należy do zbioru Mandelbrota
            break;
        }
    };
    if (i != iter) {
        // jeżeli niewykonano całej pętli to wtedy punkt nie należy do zbioru Mandelbrota, pokoloruj na jakiś kolor
        f_color = vec4(1.0, 0.0, 1.0, 1.0f);
    } else {
        // w innym wypadku punkt należy do zbioru mandelbrota i jest kolorowany na czarno
        f_color = vec4(0.0, 0.0, 0.0, 1.0f);
    }
}



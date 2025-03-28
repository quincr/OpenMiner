#version 330 core

struct Material {
    sampler2D diffuse;
}; 

in vec2 TexCoord;
out vec4 FragColor;
uniform Material material;

void main() {
    vec4 result = texture(material.diffuse, TexCoord);
    if (result.a < 1.0){
        discard;
    }

    FragColor = vec4(result.rgb, 1.0);
}
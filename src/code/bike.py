# import glfw
# from OpenGL.GL import *

# def carregar_obj(arquivo_obj):
#     vertices = []  # Lista de vértices
#     faces = []     # Lista de faces (índices)
#     normais = []   # Lista de normais
#     texturas = []  # Lista de coordenadas de textura

#     with open(arquivo_obj, 'r') as arquivo:
#         for linha in arquivo:
#             if linha.startswith('v '):  # Vértice
#                 partes = linha.strip().split()
#                 x, y, z = map(float, partes[1:4])  # Extrai coordenadas
#                 vertices.append((x, y, z))

#             elif linha.startswith('vn '):  # Normal
#                 partes = linha.strip().split()
#                 nx, ny, nz = map(float, partes[1:4])  # Extrai componentes
#                 normais.append((nx, ny, nz))

#             elif linha.startswith('vt '):  # Coordenadas de textura
#                 partes = linha.strip().split()
#                 u, v = map(float, partes[1:3])  # Extrai u, v
#                 texturas.append((u, v))

#             elif linha.startswith('f '):  # Face
#                 partes = linha.strip().split()[1:]  # Remove "f"
#                 face = []
#                 for parte in partes:
#                     indices = parte.split('/')
#                     v_idx = int(indices[0]) - 1  # Índice do vértice
#                     t_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None  # Índice de textura
#                     n_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None  # Índice de normal
#                     face.append((v_idx, t_idx, n_idx))
#                 faces.append(face)

#     return vertices, faces, normais, texturas

    
# def draw_object(vertices, faces, normais, texturas):
#     glBegin(GL_TRIANGLES)  # Inicia a definição de triângulos
#     for face in faces:
#         for vertex in face:
#             v_idx, t_idx, n_idx = vertex

#             # Adiciona a textura, se disponível
#             if t_idx is not None and texturas:
#                 glTexCoord2fv(texturas[t_idx])

#             # Adiciona a normal, se disponível
#             if n_idx is not None and normais:
#                 glNormal3fv(normais[n_idx])

#             # Adiciona o vértice
#             glVertex3fv(vertices[v_idx])
#     glEnd()  # Finaliza a definição dos triângulos




# arquivo = "D:\\trabalhoDeCG\\src\\objects\\bike\\bikee.obj"
# vertices, faces, normais, texturas = carregar_obj(arquivo)
# draw_object(vertices, faces, normais, texturas)



# # print("Vértices:", vertices)
# # print("Faces:", faces)
# # print("Normais:", normais)
# # print("Texturas:", texturas)


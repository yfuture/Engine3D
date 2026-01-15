import pygame
import numpy as np

def init():
	pygame.init()
	tela = pygame.display.set_mode((900, 500), pygame.RESIZABLE)
	pygame.display.set_caption("Cubo 3D Painter Algorithm")
	clock = pygame.time.Clock()
	return tela, clock

def multiplica_m(a, b):
	return np.dot(a, b)

def rotacao_x(a):
	#print(np.array([[1,0,0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]]))
	return np.array([[1,0,0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
	
def rotacao_y(a):
	return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])

def rotacao_z(a):
	return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
	
def render(tela, pontos_2d, faces_ordenadas):
	tela.fill((20, 20, 30))
	
	for _,face,cor in faces_ordenadas:
		pygame.draw.polygon(tela, cor, [pontos_2d[i] for i in face])
	
	pygame.display.update()
	
def main():
	tela, clock = init()
	
	pontos_cubo = np.array([[-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1], [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1]])
	
	faces = [([0,1,2,3], (200,50,50)), ([4,5,6,7], (50,50,200)), ([0,4,5,1], (50,200,50)), ([3,2,6,7], (200,200,50)), ([1,5,6,2], (50,200,200)), ([0,4,7,3], (200,50,200))]
	escala = 200
	ang_x = ang_y = ang_z = 0
	
	while True:
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				
			#elif event.type == pygame.KEYDOWN:
			#	if event.key == pygame.K_UP:
			#		ang_x += 0.01
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			ang_x += 0.01
		if keys[pygame.K_DOWN]:
			ang_x -= 0.01
		if keys[pygame.K_LEFT]:
			ang_y += 0.01
		if keys[pygame.K_RIGHT]:
			ang_y -= 0.01
		if keys[pygame.K_q]:
			ang_z += 0.01
		if keys[pygame.K_e]:
			ang_z -= 0.01
		
		
		#ang_x += 0.01
		#ang_y += 0.013
		#ang_z += 0.008
		
		rx = rotacao_x(ang_x)
		ry = rotacao_y(ang_y)
		rz = rotacao_z(ang_z)
		
		pontos_rot = []
		for p in pontos_cubo:
			pr = multiplica_m(rx, p)
			pr = multiplica_m(ry, pr)
			pr = multiplica_m(rz, pr)
			pontos_rot.append(pr)
			
		pontos_rot = np.array(pontos_rot)
		
		pontos_2d = []
		for p in pontos_rot:
			x = int(p[0] * escala + tela.get_width() / 2)
			y = int(p[1] * escala + tela.get_height() /2)
			pontos_2d.append((x, y))
			
		faces_ordenadas = []
		for face, cor in faces:
			z_medio = np.mean([pontos_rot[i][2] for i in face])
			faces_ordenadas.append((z_medio, face, cor))
		
		faces_ordenadas.sort(key=lambda f: f[0], reverse=True)
		
		render(tela, pontos_2d, faces_ordenadas)
		
		
		
if __name__ == "__main__":
	main()

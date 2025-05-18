import math, pygame
import numpy as np
from polygon import clicked_points, clicked_points2, best_weight
from car_hand import calculation, update_position
from ai import forward, initial, active


#개선점
#1. fitness 자세하게
#2. feedback loop 구현

pygame.init()
pygame.font.init()

# Constants ==
myFont = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()
acceleration = 0.1
friction = 0.05
background = pygame.image.load("map2.png")
car = pygame.image.load("car.png")
car = pygame.transform.scale(car, (50, 50))
pygame.display.set_caption("D L C")
pygame.display.set_icon(pygame.image.load("car.png"))
screen = pygame.display.set_mode((1000, 600))
mutation_rate=0.3
dead_cars = 0
generation = 0
drawing = True
pre = 0
best = False
best_weight = [np.array(w).copy() for w in best_weight]


# def ==
def point_in_triangle(pt, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def point_in_quad(location, quad):
    # quad는 [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
    return (point_in_triangle(location, quad[0], quad[1], quad[2]) or
            point_in_triangle(location, quad[0], quad[2], quad[3]))



# class ==
class Car:
    identi = 0

    def __init__(self):
        Car.identi += 1
        self.id = Car.identi
        self.speed = 0
        self.angle = 0
        self.car_rotated = 0 #기본설정
        self.fitness = 0
        self.n=0
        self.car_rect = car.get_rect()
        self.carx = 500
        self.cary = 500        
        self.car_rect.center = (self.carx, self.cary)  # Reset car position
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.alive = True

    def dead(self, all_agent):
        global dead_cars, best_car
        self.speed = 0
        self.alive = False
        dead_cars += 1
    
    def reset(self, best_car):
        self.speed = 0
        self.angle = 0
        self.car_rotated = 0 #기본설정
        self.fitness = 0
        self.n=0
        self.car_rect = car.get_rect()
        self.carx = 500
        self.cary = 500        
        self.car_rect.center = (self.carx, self.cary)  # Reset car position
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.alive = True  # Reset car position
        if self.id != best_car.id:
            self.weight = [w.copy() for w in best_car.weight]
            self.mutate_weights()
        if best == True and self.id == 2:
            self.weight = [w.copy() for w in best_weight]
        
    
    
    

        

    def mutate_weights(self):
        new_weights = []
        for w in self.weight:
            mutation_mask = np.random.rand(*w.shape) < mutation_rate
            noise = np.random.normal(0, 0.2, size=w.shape)
            w = w + mutation_mask * noise
            new_weights.append(w)
        self.weight = new_weights



    def cast_ray(self, angle, max_distance=150):
        angle = -angle
        for dist in range(max_distance):
            test_x = int(self.carx + math.cos(math.radians(angle)) * dist)
            test_y = int(self.cary + math.sin(math.radians(angle)) * dist)

            if 0 <= test_x < background.get_width() and 0 <= test_y < background.get_height():
                color = background.get_at((test_x, test_y))[:3]
                #pygame.draw.line(screen, (255, 0, 0), (self.carx, self.cary), (test_x, test_y), 3)
                if color == (255, 255, 255):  # 하얀색에 닿았을 때
                    return dist
        return max_distance  # 안 닿았으면 최대 거리 리턴



  # List to store points
cars = [Car() for _ in range(40)] 
for agent in cars:
    agent.weight = initial()
  # Initialize weights

def reset_all(cars):
        global start_time, dead_cars, generation, mutation_rate, drawing
        generation += 1
        
        
        

        for agent in cars:
            agent.reset(best_car)
        
        dead_cars = 0
        start_time = pygame.time.get_ticks()
        if best_car.fitness > 30:
            mutation_rate = 0.1
        drawing = True



best_car = max(cars, key=lambda c: c.fitness)
start_time = pygame.time.get_ticks()
#print(best_car.weight)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_all(cars)
            if event.key == pygame.K_b:
                best = True

    screen.blit(background, (0, 0))
    elapsed_sec = (pygame.time.get_ticks() - start_time) // 1000
    
    """
    if drawing:
        for i in range(len(points)):
            pygame.draw.circle(screen, (255, 0, 0), points[i], 5)
        drawing = False
    """

    #up, down, left, right = keyboard_input()
    
  # Forward pass
    #agent.up, agent.down, agent.left, agent.right = new function after
    for agent in cars:
        if not agent.alive:
            continue
        agent.speed, agent.angle, agent.carx, agent.cary = calculation(agent.up, agent.down, agent.left, agent.right, agent.speed, friction, acceleration, agent.angle, agent.carx, agent.cary)
        agent.car_rect.center = (agent.carx, agent.cary)  # Update the car's position

        agent.car_rotated, agent.car_rect = update_position(agent.car_rect, agent.carx, agent.cary, agent.angle, agent.car_rotated, car)  # Update the car's position based on speed and angle
        # Update the car's rectangle position
        
        # Cast rays
        agent.front = agent.cast_ray(agent.angle)
        agent.left1v = agent.cast_ray(agent.angle + 30) #왼쪽
        agent.left2v = agent.cast_ray(agent.angle + 60)
        agent.right1v = agent.cast_ray(agent.angle - 30) #오른쪽 
        agent.right2v = agent.cast_ray(agent.angle - 60)
        agent.distances = [agent.front, agent.left1v, agent.left2v, agent.right1v, agent.right2v]

        if any(d < 20 for d in agent.distances):
            # Collision detected, stop the car
            agent.dead(cars)
 # Reset car position
        
        normalized_distances = np.array(agent.distances) / 150
        agent.output = forward(normalized_distances, agent.weight)
        actions = active(agent.output)

        agent.speed += (agent.output[0] - agent.output[1] + 0.4) * 0.2

        
        #if agent.id == best_car.id:
            #print(agent.output, agent.speed)

        agent.up, agent.down, agent.left, agent.right = actions

        """
        if point_in_quad(agent.car_rect.center, make_quads(agent.n)):
            agent.fitness += 1.8
            agent.n += 2
        """
        agent.fitness = min(range(len(clicked_points)), key=lambda i: (clicked_points[i][0] - agent.carx) ** 2 + (clicked_points[i][1] - agent.cary) ** 2
        )


        #fitness_text = myFont.render(f"Fitness: {fitness}", True, (0, 0, 0))

        # Draw the rays
        

        # Drawing
        screen.blit(agent.car_rotated, agent.car_rect.topleft)
         
    
    # Draw the points

        if elapsed_sec > 1 and agent.fitness < 2:
            agent.dead(cars)

        if dead_cars == len(cars):
            reset_all(cars)
        elif dead_cars == len(cars) - 1 and agent.id == best_car.id:
            if  best_car.id == agent.id or agent.fitness > best_car.fitness:
                reset_all(cars)

                


    best_car = max(cars, key=lambda c: c.fitness)
    #fitness_text = myFont.render(f"Best Fitness: {best_car.fitness:.3f}", True, (0, 0, 0))
    #screen.blit(fitness_text, (10, 10))
    screen.blit(myFont.render(f"Generation: {generation}", True, (0, 0, 0)), (430, 0)) 


    pygame.display.update()
    clock.tick(60)
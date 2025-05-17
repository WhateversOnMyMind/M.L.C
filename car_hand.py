import math, pygame


def keyboard_input():
    keys = pygame.key.get_pressed()
    up = keys[pygame.K_UP]
    down = keys[pygame.K_DOWN]
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]
    return up, down, left, right

def calculation(up, down, left, right, speed, friction, acceleration, angle, carx, cary):
    # Calculate the new speed and angle based on keyboard input
    if up:
        speed += acceleration
    if down:
        speed -= acceleration
    if left:
        angle += 3
    if right:
        angle -= 3

    speed -= friction  # Apply friction to speed

    # Limit the speed to a maximum value
    speed = min(max(speed, 0), 8)

    carx = max(0, min(carx, 1000))  # Keep car within screen bounds
    cary = max(0, min(cary, 600))  # Keep car within screen bounds

    carx += speed * math.cos(math.radians(angle))
    cary -= speed * math.sin(math.radians(angle))

    return speed, angle, carx, cary



def update_position(car_rect, carx, cary, angle, car_rotated, car):
    # Update the car's position based on speed and angle
    
    # Update the car's rectangle position
    car_rotated = pygame.transform.rotate(car, angle)
    car_rect = car_rotated.get_rect(center=(carx, cary))

    return car_rotated, car_rect

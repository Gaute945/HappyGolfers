# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1910, 1080))
clock = pygame.time.Clock()
running = True
dt = 0
t = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
camera_x = player_pos.x
camera_y = player_pos.y

g = 9.80665 * 100 # m/s^2
vy = -1100 # start vy m/s
vx = 100 # start vx m/s

def circle_rect_collision(circle_pos, radius, rect):
        cx, cy = circle_pos

        # Closest point on rect to circle center
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        # Distance
        dx = cx - closest_x
        dy = cy - closest_y

        return (dx * dx + dy * dy) <= (radius * radius)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            vy -= 400
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            vx -= 400
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            vx += 400

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    
    brect = pygame.Rect(0, screenHeight - 10, screenWidth, 10)  # floor
    trect = pygame.Rect(0, 0, screenWidth, 10)                  # ceiling
    rrect = pygame.Rect(screenWidth - 10, 0, 10, screenHeight)  # right wall
    lrect = pygame.Rect(0, 0, 10, screenHeight)                 # left wall
    
    pygame.draw.rect(screen, (0, 0, 255), brect)
    pygame.draw.rect(screen, (0, 0, 255), trect)
    pygame.draw.rect(screen, (0, 0, 255), rrect)
    pygame.draw.rect(screen, (0, 0, 255), lrect)
    pygame.draw.circle(screen, (255, 0, 0), player_pos, 50)

    #player_pos = pygame.mouse.get_pos()
    player_pos.y += vy * dt + 0.5 * g * dt**2
    player_pos.x += vx * dt
    vy += g * dt

    if circle_rect_collision(player_pos, 50, brect):
        player_pos.y = brect.top - 50
        vy *= -0.75 #Coefficient of restitution
        print(vy)
    
    if circle_rect_collision(player_pos, 50, trect):
        player_pos.y = trect.bottom + 50
        vy *= -0.75
        print(vy)
        
    if circle_rect_collision(player_pos, 50, rrect):
        player_pos.x = rrect.left - 50
        vx *= -0.75
        print(vy)
        
    if circle_rect_collision(player_pos, 50, lrect):
        player_pos.x = lrect.right + 50
        vx *= -0.75
        print(vy)
        
    camera_x = player_pos.x - screenHeight / 2
    camera_y = player_pos.y - screenHeight / 2

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000 # since last frame
    t += dt # total time

pygame.quit()
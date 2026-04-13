# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
t = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
g = 9.80665 # m/s^2
vy = -10 # start v m/s

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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    rect = pygame.Rect(0, screen.get_height() - 100, screen.get_width(), 100)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        vy = -10
        t = 1
        print("space")

    pygame.draw.rect(screen, (0, 0, 255), rect)
    pygame.draw.circle(screen, (255, 0, 0), player_pos, 50)

    #player_pos = pygame.mouse.get_pos()
    player_pos.y += vy*t + 1/2*g*t**2 # v0yt - 1/2*g*dt^2

    if circle_rect_collision(player_pos, 50, rect):
        player_pos.y = rect.top - 50
        t = 0
        vy *= 0.8 #Coefficient of restitution
        print(vy)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000 # since last frame
    t += dt # total time

pygame.quit()
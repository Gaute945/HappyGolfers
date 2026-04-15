import pygame

pygame.init()
screen = pygame.display.set_mode((1910, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
WORLD_WIDTH = SCREEN_WIDTH
WORLD_HEIGHT = SCREEN_HEIGHT
RADIUS = 50

player_pos = pygame.Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
g = 9.80665 * 100
vy = -1100
vx = 100

# World rects — fixed forever, never touched again
brect = pygame.Rect(0, WORLD_HEIGHT - 50, WORLD_WIDTH, 50)
trect = pygame.Rect(0, 0, WORLD_WIDTH, 50)
rrect = pygame.Rect(WORLD_WIDTH - 50, 0, 50, WORLD_HEIGHT)
lrect = pygame.Rect(0, 0, 50, WORLD_HEIGHT)

def circle_rect_collision(circle_pos, radius, rect):
    cx, cy = circle_pos
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx * dx + dy * dy) <= (radius * radius)

def draw_rect_world(surface, color, rect, cam_x, cam_y):
    pygame.draw.rect(surface, color, pygame.Rect(
        rect.x - cam_x,
        rect.y - cam_y,
        rect.width,
        rect.height
    ))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            vy -= 400
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            vx -= 400
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            vx += 400

    # Physics — world space
    player_pos.y += vy * dt + 0.5 * g * dt**2
    player_pos.x += vx * dt
    vy += g * dt

    # Collision — world space
    if circle_rect_collision(player_pos, RADIUS, brect):
        player_pos.y = brect.top - RADIUS
        vy *= -0.75
    if circle_rect_collision(player_pos, RADIUS, trect):
        player_pos.y = trect.bottom + RADIUS
        vy *= -0.75
    if circle_rect_collision(player_pos, RADIUS, rrect):
        player_pos.x = rrect.left - RADIUS
        vx *= -0.75
    if circle_rect_collision(player_pos, RADIUS, lrect):
        player_pos.x = lrect.right + RADIUS
        vx *= -0.75

    # Camera — updated after physics
    cam_x = player_pos.x - SCREEN_WIDTH / 2
    cam_y = player_pos.y - SCREEN_HEIGHT / 2

    # Draw — screen space only
    screen.fill("purple")
    draw_rect_world(screen, (0, 0, 255), brect, cam_x, cam_y)
    draw_rect_world(screen, (0, 0, 255), trect, cam_x, cam_y)
    draw_rect_world(screen, (0, 0, 255), rrect, cam_x, cam_y)
    draw_rect_world(screen, (0, 0, 255), lrect, cam_x, cam_y)

    pygame.draw.circle(screen, (255, 0, 0),
        (player_pos.x - cam_x, player_pos.y - cam_y), RADIUS)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
import pygame
import sys
import random
from shapely.geometry import LineString
from math import radians, cos, sin, atan2, degrees

# Pencere boyutu
WIDTH, HEIGHT = 1500, 1000
W, H = 1420, 600
# X ve Y eksenindeki aralıklar
X_INTERVAL, Y_INTERVAL = 120, 165
# Nokta boyutu
POINT_SIZE = 1
# Renkler
BLACK = (181, 181, 181)
WHITE = (54, 54, 54)
RED = (193, 255, 193)
BLUE = (54, 54,54)
R = (169, 0, 0)



# Kırmızı noktaların konumlarını depolamak için bir liste oluşturuyoruz
red_points = []
# Tüm eğri noktalarını depolamak için bir liste oluşturuyoruz
all_curve_points = []

## Araç değişkenleri
car_img_original = pygame.image.load('car2.png')
car_img = pygame.transform.scale(car_img_original, (120, 60))
car_position = [WIDTH // 2, HEIGHT - 110]
car_speed = 5
car_angle = 0

def draw_car(screen, image, position, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=position).center)
    screen.blit(rotated_image, new_rect.topleft)

def update_car_position(keys, position, angle):
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx -= car_speed
    if keys[pygame.K_RIGHT]:
        dx += car_speed
    if keys[pygame.K_UP]:
        dy -= car_speed
    if keys[pygame.K_DOWN]:
        dy += car_speed

    # Köşegen hareketi hesapla
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        dx = -car_speed / 1.414  # cos(45°)
        dy = -car_speed / 1.414  # sin(45°)
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        dx = car_speed / 1.414
        dy = -car_speed / 1.414
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        dx = -car_speed / 1.414
        dy = car_speed / 1.414
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        dx = car_speed / 1.414
        dy = car_speed / 1.414

    # Pozisyonu güncelle
    position[0] += dx
    position[1] += dy

    # Araç açısını hesapla
    if dx != 0 or dy != 0:
        angle = radians(90) - atan2(dy, dx)
        angle = degrees(angle)  # Dereceye çevir
    return angle


def generate_red_points(start_column=100):
    for x in range(start_column, W, X_INTERVAL):
        random_y = random.randint(400, H)
        red_points.append((x, random_y))


def draw_points(screen):
    for point in red_points:
        pygame.draw.circle(screen, RED, point, POINT_SIZE)

def draw_bezier_curves(screen):
    # Her dört noktayı kullanarak Bezier eğrisi çiz
    for i in range(0, len(red_points) - 3, 3):
        start_point = red_points[i]
        control1_point = red_points[i + 1]
        control2_point = red_points[i + 2]
        end_point = red_points[i + 3]
        draw_bezier_curve(screen, start_point, control1_point,
                          control2_point, end_point)
    
    

def draw_bezier_curve(screen, start, control1, control2, end, segments=50):
    global all_curve_points 
    curve_points = []
    # Bezier eğrisini çizmek için her bir parçayı hesapla
    for i in range(segments):
        t = i / segments
        x = (1 - t) ** 3 * start[0] + 3 * (1 - t) ** 2 * t * control1[0] + 3 * \
            (1 - t) * t ** 2 * control2[0] + t ** 3 * end[0]
        y = (1 - t) ** 3 * start[1] + 3 * (1 - t) ** 2 * t * control1[1] + 3 * \
            (1 - t) * t ** 2 * control2[1] + t ** 3 * end[1]
        curve_points.append((int(x), int(y)))

        next_t = (i + 1) / segments
        next_x = (1 - next_t) ** 3 * start[0] + 3 * (1 - next_t) ** 2 * next_t * control1[0] + 3 * \
            (1 - next_t) * next_t ** 2 * control2[0] + next_t ** 3 * end[0]
        next_y = (1 - next_t) ** 3 * start[1] + 3 * (1 - next_t) ** 2 * next_t * control1[1] + 3 * \
            (1 - next_t) * next_t ** 2 * control2[1] + next_t ** 3 * end[1]
        pygame.draw.line(screen, BLUE, (int(x), int(y)),
                         (int(next_x), int(next_y)), 6)
    all_curve_points.extend(curve_points)

def draw_offset_line(screen, offset_blue_line):
    # Ofsetli çizginin koordinatları üzerinde döngü çalıştır
    offset_points = list(offset_blue_line.coords)
    for i in range(len(offset_points) - 1):
        pygame.draw.line(screen, WHITE, offset_points[i], offset_points[i + 1], 6)

def draw_button(screen, message, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def reset_track():
    global red_points
    red_points.clear()
    generate_red_points()





def main():
    global all_curve_points
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("F1 Yarışı")
    clock = pygame.time.Clock()

    # Resmi yükle
    image = pygame.image.load('f2.png')
    image1 = pygame.image.load('backk.png')
    image2 = pygame.image.load('bayrak.png')
    image3 = pygame.image.load('arka.png')

    background_image = pygame.image.load('a.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) 
   
    car_angle = 0
    generate_red_points()  # Kırmızı noktaların konumlarını bir kere oluşturuyoruz
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # 'S' tuşuna basıldığında ekran görüntüsü kaydedilir
                    pygame.image.save(screen, 'track_screenshot.png')
        
        keys = pygame.key.get_pressed()
        car_angle = update_car_position(keys, car_position, car_angle)


        #screen.blit(background_image, (0, 0))
        screen.fill((205, 183, 158))
        draw_car(screen, car_img, car_position, car_angle)
    
        
        # Resmi çiz
        screen.blit(image3, (0, 0 ))
        screen.blit(image, (WIDTH - 500, HEIGHT - 15 - image.get_height()))
        screen.blit(image1, ((WIDTH - image1.get_width()), HEIGHT  - image1.get_height()))
        screen.blit(image2, (0, HEIGHT - image2.get_height()))

        draw_button(screen, "Reset", WIDTH - 258 , HEIGHT - 65, 60, 60, R, (0, 0, 139),  reset_track)
        pygame.draw.rect(screen, R, (0, 0, WIDTH, HEIGHT), 5)
        pygame.draw.rect(screen, R, (0, 200, 1300, 800), 3)


        draw_points(screen)
        all_curve_points = []  # all_curve_points listesini sıfırlıyoruz
        draw_bezier_curves(screen)  # Bezier eğrilerini çiziyoruz
        start_point = all_curve_points[-1]
        control1_point = (420, 1000)
        control2_point = (420, 1000)
        end_point = all_curve_points[0]
        draw_bezier_curve(screen, start_point, control1_point,
                        control2_point, end_point) 
        
        blue_line = LineString(all_curve_points)
        #Mavi çizginin paralel ofsetini al ve bir LineString nesnesi olarak sakla
        offset_distance = 86  # Örnek ofset mesafesi
        offset_blue_line = blue_line.parallel_offset(offset_distance, 'right')  # Sol tarafta ofset alındı
        draw_offset_line(screen, offset_blue_line)
        
       
        pygame.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()


import os
import pygame
import random

pygame.init()

# 화면 크기 설정
screen_width = 800  # 가로
screen_height = 600  # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("reaction game")

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화
current_path = os.path.dirname(__file__)  # 현재 파일 위치 변환
image_path = os.path.join(current_path, "images")  # 이미지 폴더 위치 변환

# 배경
background_color_start = (255, 255, 0)  # 위
background_color_end = (255, 255, 255)  # 아래

# 배경에 그을 줄
line_color_start = (255, 0, 255)  # 보라색
line_color_end = (255, 255, 255)  # 검은색
num_lines = 4
line_width = 2
line_gap = screen_width // (num_lines + 1)

# 키 입력시 날아가는 것 (=무기)
weapon_blue = pygame.image.load(os.path.join(image_path, "weapon_1.png"))
weapon_red = pygame.image.load(os.path.join(image_path, "weapon_2.png"))
weapon_size = weapon_blue.get_rect().size
weapon_width = weapon_size[0]

# 무기 여러 발 발사 가능
b_weapons = []
r_weapons = []

# 무기 이동 속도
weapon_speed = 10

# 떨어지는 스틱
stick = pygame.image.load(os.path.join(image_path, "stick.png"))
stick_size = stick.get_rect().size
stick_width = weapon_size[0]
stick_x_pos_option = [0, 160, 480, 640]
special_stick_x_pos_option = 320
sticks = []

# 시간 경과를 추적하기 위한 변수
current_time = 0
time_interval = 500  # 0.5초

# 충돌한 스틱의 위치에서 폭발 효과를 재생
def explode(x, y):
    explosions.append((x, y, pygame.time.get_ticks()))  # 폭발 효과를 리스트에 추가

# 폭발 효과 유지 시간 (밀리초)
explosion_duration = 1000  # 1초

# 화면에 그려진 폭발 효과를 저장하는 리스트
explosions = []

# 스틱 속도 및 가속도
stick_speed = 1
acceleration = 0.001

# 이벤트 루프
running = True  # 게임 진행 중?
while running:
    dt = clock.tick(120)  # 초당 프레임

    # 이벤트 처리 및 게임 로직
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                weapon_x_pos = 0
                weapon_y_pos = 600
                b_weapons.append([weapon_x_pos, weapon_y_pos])
            elif event.key == pygame.K_f:
                weapon_x_pos = 160
                weapon_y_pos = 600
                r_weapons.append([weapon_x_pos, weapon_y_pos])
            elif event.key == pygame.K_j:
                weapon_x_pos = 480
                weapon_y_pos = 600
                r_weapons.append([weapon_x_pos, weapon_y_pos])
            elif event.key == pygame.K_k:
                weapon_x_pos = 640
                weapon_y_pos = 600
                b_weapons.append([weapon_x_pos, weapon_y_pos])
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = 320
                weapon_y_pos = 600
                b_weapons.append([weapon_x_pos, weapon_y_pos])

    # 무기 위치 조정
    b_weapons = [[w[0], w[1] - weapon_speed] for w in b_weapons]
    r_weapons = [[w[0], w[1] - weapon_speed] for w in r_weapons]

    b_weapons = [[w[0], w[1]] for w in b_weapons if w[1] > 0]
    r_weapons = [[w[0], w[1]] for w in r_weapons if w[1] > 0]

    current_time += dt

    # 스틱 랜덤으로 생성
    if current_time >= time_interval:
        stick_x_pos = random.choice(stick_x_pos_option)  # 스틱의 x 좌표를 랜덤으로 선택
        special_stick = random.randint(1,30)    # 1~30 이 범위가 줄 수록 special stick이 자주 등장
        if special_stick == 1:
            sticks.append([special_stick_x_pos_option, 0])
        sticks.append([stick_x_pos, 0])
        current_time = 0

    # 스틱 속도 업데이트 (가속도 적용)
    stick_speed += acceleration

    # 스틱 위치 조정
    sticks = [[w[0], w[1] + stick_speed] for w in sticks]


    def is_collision(weapon_x, weapon_y, stick_x, stick_y):
        weapon_rect = weapon_blue.get_rect()
        weapon_rect.left = weapon_x
        weapon_rect.top = weapon_y

        stick_rect = stick.get_rect()
        stick_rect.left = stick_x
        stick_rect.top = stick_y

        return weapon_rect.colliderect(stick_rect)

    # 무기와 스틱의 충돌 감지 및 처리
    for weapon_x_pos, weapon_y_pos in b_weapons[:]:
        for stick_x_pos, stick_y_pos in sticks[:]:
            if is_collision(weapon_x_pos, weapon_y_pos, stick_x_pos, stick_y_pos):
                b_weapons.remove([weapon_x_pos, weapon_y_pos])
                sticks.remove([stick_x_pos, stick_y_pos])
                explode(stick_x_pos, stick_y_pos)  # 충돌한 위치에서 폭발 효과 재생
                break

    for weapon_x_pos, weapon_y_pos in r_weapons[:]:
        for stick_x_pos, stick_y_pos in sticks[:]:
            if is_collision(weapon_x_pos, weapon_y_pos, stick_x_pos, stick_y_pos):
                r_weapons.remove([weapon_x_pos, weapon_y_pos])
                sticks.remove([stick_x_pos, stick_y_pos])
                explode(stick_x_pos, stick_y_pos)  # 충돌한 위치에서 폭발 효과 재생
                break

    # 그라데이션 배경 그리기
    for y in range(screen_height):
        # 배경의 그라데이션 색상 결정
        background_lerped_color = pygame.Color(
            *[int(
                background_color_start[c] + (background_color_end[c] - background_color_start[c]) * (y / screen_height))
              for c in range(3)])
        pygame.draw.line(screen, background_lerped_color, (0, y), (screen_width, y))

    # 선 색상 그라데이션 적용
    for i in range(1, num_lines + 1):
        x = i * line_gap

        # 각 선에 대한 색상 그라데이션
        for y_pos in range(screen_height):
            line_lerped_color = pygame.Color(
                *[int(line_color_start[c] + (line_color_end[c] - line_color_start[c]) * (y_pos / screen_height)) for c
                  in range(3)])
            pygame.draw.line(screen, line_lerped_color, (x, y_pos), (x, y_pos), line_width)

    for weapon_x_pos, weapon_y_pos in b_weapons:
        screen.blit(weapon_blue, (weapon_x_pos, weapon_y_pos))

    for weapon_x_pos, weapon_y_pos in r_weapons:
        screen.blit(weapon_red, (weapon_x_pos, weapon_y_pos))

    for stick_x_pos, stick_y_pos in sticks:
        screen.blit(stick, (stick_x_pos, stick_y_pos))

    # 폭발 효과 그리기
    ex_current_time = pygame.time.get_ticks()
    for explosion in explosions[:]:
        explosion_x, explosion_y, explosion_time = explosion
        # 폭발 효과를 그린 후 일정 시간이 지나면 제거
        if ex_current_time - explosion_time < explosion_duration:
            pygame.draw.circle(screen, (255, 0, 0), (explosion_x, explosion_y), 20)  # 원의 반지름은 20으로 설정.
        else:
            explosions.remove(explosion)

    pygame.display.update()

pygame.quit()

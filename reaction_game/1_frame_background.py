import os
import pygame

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
num_lines = 7
line_width = 2
line_gap = screen_width // (num_lines + 1)

# 이벤트 루프
running = True  # 게임 진행 중?
while running:
    dt = clock.tick(30)  # 초당 프레임

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 그라데이션 배경 그리기
    for y in range(screen_height):
        # 배경의 그라데이션 색상 결정
        background_lerped_color = pygame.Color(
            *[int(
                background_color_start[c] + (background_color_end[c] - background_color_start[c]) * (y / screen_height))
              for c in range(3)])
        pygame.draw.line(screen, background_lerped_color, (0, y), (screen_width, y))

    # 선 색상의 그라데이션 적용
    for i in range(1, num_lines + 1):
        x = i * line_gap


        # 각 선에 대한 색상 그라데이션
        for y_pos in range(screen_height):
            line_lerped_color = pygame.Color(
                *[int(line_color_start[c] + (line_color_end[c] - line_color_start[c]) * (y_pos / screen_height)) for c
                  in range(3)])
            pygame.draw.line(screen, line_lerped_color, (x, y_pos), (x, y_pos), line_width)

    pygame.display.update()

pygame.quit()
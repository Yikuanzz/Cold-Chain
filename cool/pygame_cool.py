import os
import time
import pygame
import random

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = width, height = 920, 640

# Setting the screen
screen = pygame.display.set_mode(size)
screen.fill(WHITE)
pygame.display.set_caption("Micro Grid Running Process")

# Loading the images
p_PV_Path = os.getcwd() + "\\images\\光伏板.png"
p_PV = pygame.image.load(p_PV_Path).convert()
p_PV = pygame.transform.scale(p_PV, (120, 100))

p_CD_Path = os.getcwd() + "\\images\\制冷设备.png"
p_CD = pygame.image.load(p_CD_Path).convert()
p_CD = pygame.transform.scale(p_CD, (130, 130))

p_Battery1_Path = os.getcwd() + "\\images\\蓄电池.png"
p_Battery1 = pygame.image.load(p_Battery1_Path).convert()
p_Battery1 = pygame.transform.scale(p_Battery1, (90, 90))

p_Battery2_Path = os.getcwd() + "\\images\\动力电池.png"
p_Battery2 = pygame.image.load(p_Battery2_Path).convert()
p_Battery2 = pygame.transform.scale(p_Battery2, (100, 120))


def rand():
    if random.random() < 0.5:
        num = random.randint(1, 2)
    else:
        num = -random.randint(1, 2)
    return num


def r_msg(msg):
    # Draw the frame
    pygame.draw.rect(screen, BLACK, (620, 10, 280, 625), 1)
    # Set the preference
    fp = os.getcwd() + "\\Fonts\\fn1.ttf"
    # Set the font style
    f1 = pygame.font.Font(fp, 24)
    f2 = pygame.font.Font(fp, 26)
    fa = pygame.font.Font(fp, 26)

    # Content_1
    title_t = "运行次数:"
    title_pv = "光伏发电量:          W"
    title_b1 = "蓄电池组电量:           %"
    title_b2 = "动力电池组电量:         %"
    title_l_1 = "制冷设备"
    title_l_2 = "耗电量:                   kw/h"
    title_a_1 = "当前微电网"
    title_a_2 = "选择策略:"
    block = "                                           "

    # Content_2
    step_t = str(msg[0])
    battery1 = str(msg[1])
    battery2 = str(msg[2])
    pv = str(msg[3])
    load = str(msg[4])
    action_1 = None
    action_2 = None
    if msg[5] == 0:
        action_1 = "动力电池组+光伏能源"
        action_2 = "给制冷机组供电"
    elif msg[5] == 1:
        action_1 = "动力电池组"
        action_2 = "给制冷机组供电"
    elif msg[5] == 2:
        action_1 = "蓄电池组+光伏能源"
        action_2 = "给制冷机组供电"
    elif msg[5] == 3:
        action_1 = "蓄电池组"
        action_2 = "给制冷机组供电"
    elif msg[5] == 4:
        action_1 = "光伏能源"
        action_2 = "给蓄电池组充电"
    elif msg[5] == 5:
        action_1 = "光伏能源"
        action_2 = "给动力电池组充电"

    # Render font content one
    text_title_1 = f1.render(title_t, True, (255, 0, 0), (255, 255, 255))
    text_title_pv = f1.render(title_pv, True, (255, 0, 0), (255, 255, 255))
    text_title_b1 = f1.render(title_b1, True, (255, 0, 0), (255, 255, 255))
    text_title_b2 = f1.render(title_b2, True, (255, 0, 0), (255, 255, 255))
    text_title_l_1 = f1.render(title_l_1, True, (255, 0, 0), (255, 255, 255))
    text_title_l_2 = f1.render(title_l_2, True, (255, 0, 0), (255, 255, 255))
    text_title_a_1 = f1.render(title_a_1, True, (255, 0, 0), (255, 255, 255))
    text_title_a_2 = f1.render(title_a_2, True, (255, 0, 0), (255, 255, 255))
    text_block = f1.render(block, True, (255, 255, 255), (255, 255, 255))

    # Render font content two (255, 102, 0)
    text_step_t = f2.render(step_t, True, (255, 102, 0), (255, 255, 255))
    text_battery1 = f2.render(battery1, True, (255, 102, 0), (255, 255, 255))
    text_battery2 = f2.render(battery2, True, (255, 102, 0), (255, 255, 255))
    text_pv = f2.render(pv, True, (255, 102, 0), (255, 255, 255))
    text_load = f2.render(load, True, (255, 102, 0), (255, 255, 255))
    text_action_1 = fa.render(action_1, True, (0, 0, 0), (255, 255, 255))
    text_action_2 = fa.render(action_2, True, (0, 0, 0), (255, 255, 255))

    # Content_1 Rect
    title_t_rect = (630, 20)
    title_pv_rect = (630, 100)
    title_b1_rect = (630, 180)
    title_b2_rect = (630, 260)
    title_l_1_rect = (630, 340)
    title_l_2_rect = (640, 370)
    title_a_1_rect = (630, 450)
    title_a_2_rect = (640, 480)

    # Content_2 Rect
    text_step_t_rect = (740, 19)
    text_pv_rect = (770, 99)
    text_battery1_rect = (800, 179)
    text_battery2_rect = (820, 259)
    text_load_rect = (750, 369)
    text_action_1_rect = (640, 520)
    text_action_2_rect = (640, 560)

    # Draw content one in the screen
    screen.blit(text_title_1, title_t_rect)
    screen.blit(text_title_pv, title_pv_rect)
    screen.blit(text_title_b1, title_b1_rect)
    screen.blit(text_title_b2, title_b2_rect)
    screen.blit(text_title_l_1, title_l_1_rect)
    screen.blit(text_title_l_2, title_l_2_rect)
    screen.blit(text_title_a_1, title_a_1_rect)
    screen.blit(text_title_a_2, title_a_2_rect)

    # Draw content two in the screen
    screen.blit(text_step_t, text_step_t_rect)
    screen.blit(text_pv, text_pv_rect)
    screen.blit(text_battery1, text_battery1_rect)
    screen.blit(text_battery2, text_battery2_rect)
    screen.blit(text_load, text_load_rect)
    screen.blit(text_block, text_action_1_rect)
    screen.blit(text_action_1, text_action_1_rect)
    screen.blit(text_block, text_action_2_rect)
    screen.blit(text_action_2, text_action_2_rect)


def picture_msg(msg):
    # The preset
    fp = os.getcwd() + "\\Fonts\\fn1.ttf"
    # Set the font style
    f = pygame.font.Font(fp, 18)

    # The content
    battery1 = str(msg[1])
    battery2 = str(msg[2])
    pv = str(msg[3])

    # Set the preference
    text_pv = f.render(pv, True, (0, 155, 0), (255, 255, 255))
    text_bat1 = f.render(battery1, True, (0, 155, 0), (255, 255, 255))
    text_bat2 = f.render(battery2, True, (0, 155, 0), (255, 255, 255))

    # Set the position
    pv_rect = (345, 70)
    bat1_rect = (60, 580)
    bat2_rect = (340, 310)

    # Draw into the screen
    screen.blit(text_pv, pv_rect)
    screen.blit(text_bat1, bat1_rect)
    screen.blit(text_bat2, bat2_rect)


def draw_lines():
    # Drawing the picture
    # To show info
    pygame.draw.rect(screen, BLACK, (10, 10, 230, 40), 1)
    # To show PV
    pygame.draw.rect(screen, BLACK, (10, 60, 400, 140), 1)
    # To show Battery1
    pygame.draw.rect(screen, BLACK, (10, 535, 600, 100), 1)
    # To show Battery2
    pygame.draw.rect(screen, BLACK, (10, 300, 380, 180), 1)
    # To show Device
    pygame.draw.rect(screen, BLACK, (450, 170, 150, 310), 1)
    # To draw the line from PV to Device
    pygame.draw.line(screen, BLACK, (410, 110), (545, 110), 1)
    pygame.draw.line(screen, BLACK, (410, 135), (515, 135), 1)
    pygame.draw.line(screen, BLACK, (545, 110), (545, 170), 1)
    pygame.draw.line(screen, BLACK, (515, 135), (515, 170), 1)
    # To draw the line from PV to Battery
    pygame.draw.line(screen, BLACK, (180, 200), (180, 300), 1)
    pygame.draw.line(screen, BLACK, (220, 200), (220, 300), 1)
    # To draw the line from Battery to Device
    pygame.draw.line(screen, BLACK, (390, 370), (450, 370), 1)
    pygame.draw.line(screen, BLACK, (390, 400), (450, 400), 1)
    # To draw the line from Battery to Device
    pygame.draw.line(screen, BLACK, (545, 480), (545, 535), 1)
    pygame.draw.line(screen, BLACK, (515, 480), (515, 535), 1)
    # To draw the Battery to Battery
    pygame.draw.line(screen, BLACK, (180, 480), (180, 535), 1)
    pygame.draw.line(screen, BLACK, (220, 480), (220, 535), 1)


def write_words():
    # Font path
    fp = os.getcwd() + "\\Fonts\\fn1.ttf"
    # Set the font style
    f = pygame.font.Font(fp, 24)
    f_info = pygame.font.Font(fp, 18)
    f_4 = pygame.font.Font(fp, 30)
    # Set the text content
    content_0 = "光伏能源系统"
    content_info_0 = "PV_Power:       W"
    content_1 = "动力电池组"
    content_info_1 = "Battery_Cap:      %"
    content_2 = "蓄电池"
    content_info_2 = "Cap:       %"
    content_3 = "制冷设备"
    content_4 = "光伏冷链微电网"
    # Render the text
    """
        first param : the text content
        second param : the smooth
        third param : the font color
        fourth param : the background color
    """
    text_0 = f.render(content_0, True, (0, 0, 255), (150, 150, 150))  # (255, 255, 255)
    text_1 = f.render(content_1, True, (0, 0, 255), (150, 150, 150))  # (0, 0, 0)
    text_2 = f.render(content_2, True, (0, 0, 255), (150, 150, 150))  # (0, 0, 255)
    text_3 = f.render(content_3, True, (0, 0, 255), (150, 150, 150))  # (150, 150, 150)
    text_4 = f_4.render(content_4, True, (255, 255, 255), (0, 0, 0))
    info_0 = f_info.render(content_info_0, True, (255, 0, 0), (255, 255, 255))
    info_1 = f_info.render(content_info_1, True, (255, 0, 0), (255, 255, 255))
    info_2 = f_info.render(content_info_2, True, (255, 0, 0), (255, 255, 255))
    # Text Position
    textRect_0 = (10, 60)
    infoRect_0 = (250, 70)
    textRect_1 = (10, 300)
    infoRect_1 = (230, 310)
    textRect_2 = (10, 535)
    infoRect_2 = (15, 580)
    textRect_3 = (480, 180)
    textRect_4 = (20, 12)
    # Draw the picture in the screen
    screen.blit(text_0, textRect_0)
    screen.blit(info_0, infoRect_0)
    screen.blit(text_1, textRect_1)
    screen.blit(info_1, infoRect_1)
    screen.blit(text_2, textRect_2)
    screen.blit(info_2, infoRect_2)
    screen.blit(text_3, textRect_3)
    screen.blit(text_4, textRect_4)


def show_background():
    # PV
    screen.blit(p_PV, (20, 90))
    screen.blit(p_PV, (140, 90))
    screen.blit(p_PV, (260, 90))
    # Device
    screen.blit(p_CD, (460, 210))
    screen.blit(p_CD, (460, 340))
    # Battery 1
    screen.blit(p_Battery1, (100, 540))
    screen.blit(p_Battery1, (200, 540))
    screen.blit(p_Battery1, (300, 540))
    screen.blit(p_Battery1, (400, 540))
    screen.blit(p_Battery1, (500, 540))
    # Battery 2
    screen.blit(p_Battery2, (10, 340))
    screen.blit(p_Battery2, (100, 340))
    screen.blit(p_Battery2, (190, 340))
    screen.blit(p_Battery2, (280, 340))
    pygame.display.flip()


def run_game(t_time=50, action=4):
    p0 = []  # Store the point from PV to Cool
    p1 = []  # Store the point from PV to Battery2
    p2 = []  # Store the point from Battery2 to Cool
    p3 = []  # Store the point form Battery2 to Battery1
    p4 = []  # Store teh point form Battery1 to Cool
    position_0 = [405, 115]  # Initial position
    position_1 = [195, 200]  # Initial position
    position_2 = [380, 380]  # Initial position
    position_3 = [195, 470]  # Initial position
    position_4 = [525, 535]  # Initial position
    for t in range(t_time):
        # PV to Cool
        if (action == 0 or action == 2) and t < 10:
            r_x = random.randint(3, 6)
            r_y = random.randint(3, 6)
            p0.append(point(position=[position_0[0] + r_x, position_0[1] + r_y]))
            for p in p0:
                p.generate()

        # PV to Battery2
        if (action == 4 or action == 5) and t < 10:
            r_x = random.randint(3, 6)
            r_y = random.randint(3, 6)
            p1.append(point(position=[position_1[0] + r_x, position_1[1] + r_y]))
            for p in p1:
                p.generate()

        # Battery2 to Cool
        if (action == 1 or action == 0) and t < 10:
            r_x = random.randint(3, 6)
            r_y = random.randint(3, 6)
            p2.append(point(position=[position_2[0] + r_x, position_2[1] + r_y]))
            for p in p2:
                p.generate()

        # Battery2 to Battery1
        if action == 4 and t < 10:
            r_x = random.randint(3, 6)
            r_y = random.randint(3, 6)
            p3.append(point(position=[position_3[0] + r_x, position_3[1] + r_y]))
            for p in p3:
                p.generate()

        # Battery1 to Cool
        if action == 3 and t < 10:
            r_x = random.randint(3, 6)
            r_y = random.randint(3, 6)
            p4.append(point(position=[position_4[0] + r_x, position_4[1] + r_y]))
            for p in p4:
                p.generate()

        for p in p0:
            if p.cur_position[0] < 520:
                r_x = random.randint(10, 20)
                r_y = rand()
            else:
                r_x = rand()
                r_y = random.randint(10, 20)
            if p.cur_position[1] < 160:
                p.move(r_x, r_y, st=0.01)
            else:
                p.disappear()
            draw_lines()

        for p in p1:
            r_x = rand()
            r_y = random.randint(10, 20)

            if p.cur_position[1] < 280:
                p.move(r_x, r_y, st=0.02)
            else:
                p.disappear()
            draw_lines()

        for p in p2:
            r_x = random.randint(10, 20)
            r_y = rand()

            if p.cur_position[0] < 430:
                p.move(r_x, r_y, st=0.03)
            else:
                p.disappear()
            draw_lines()

        for p in p3:
            r_x = rand()
            r_y = random.randint(10, 20)

            if p.cur_position[1] < 515:
                p.move(r_x, r_y, st=0.04)
            else:
                p.disappear()
            draw_lines()

        for p in p4:
            r_x = rand()
            r_y = -random.randint(10, 20)

            if p.cur_position[1] > 500:
                p.move(r_x, r_y, st=0.04)
            else:
                p.disappear()
            draw_lines()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()


class point:
    def __init__(self, position, color=(255, 0, 0), radius=4):
        self.cur_position = position
        self.point_color = color
        self.point_radius = radius

    def generate(self):
        pygame.draw.circle(screen, self.point_color, (self.cur_position[0], self.cur_position[1]), self.point_radius)

    def disappear(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.cur_position[0], self.cur_position[1]), self.point_radius)

    def move(self, x, y, st):
        pygame.draw.circle(screen, (255, 255, 255), (self.cur_position[0], self.cur_position[1]), self.point_radius)
        self.cur_position[0] += x
        self.cur_position[1] += y
        pygame.draw.circle(screen, self.point_color, (self.cur_position[0], self.cur_position[1]), self.point_radius)
        time.sleep(st)


def run(obj_list):
    """obj_list=[time, bat1, bat2, pv, load, action]"""
    draw_lines()
    show_background()
    write_words()
    picture_msg(msg=obj_list)
    r_msg(msg=obj_list)
    run_game(action=obj_list[5])


if __name__ == '__main__':
    # 测试动画细节
    for i in range(1000):
        a = random.randint(0, 5)
        m = [i, 23, 45, 14, 550, a]
        run(m)

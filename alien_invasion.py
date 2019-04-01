# -*- coding: utf-8 -*-
import pygame
from settings import Settings
from pygame.sprite import Sprite
import game_functions as gf
from pygame.sprite import Group
from ship import Ship

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    #返回一个surface,将其存储在screen
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个存储子弹的编组
    bullets = Group()
    #创建一个存储外星人的编组
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings, screen, aliens)
    #开始游戏的循环
    while True:
        
        #监听键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)
        #根据发生的事件，更新飞船的位置
        ship.update()
        gf.update_bullets(bullets)
        #每次循环都重绘屏幕
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
# -*- coding: utf-8 -*-
import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

#检查事件

"""检查按下事件"""
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		"""当用户按下空格键并且屏幕上的子弹未用光所有限制数量时，新建一个子弹，并加入编
		组中"""
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

"""检查按键弹起事件"""
def check_keyup_events(event, ship):
	"""响应松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
	"""监听鼠标和键盘事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			"""
			if event.key == pygame.K_RIGHT:
				ship.moving_right = True
			elif event.key == pygame.K_LEFT:
				ship.moving_left = True
			"""
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			"""
			if event.key == pygame.K_RIGHT:
				ship.moving_right = False
			elif event.key == pygame.K_LEFT:
				ship.moving_left = False
			"""
			check_keyup_events(event, ship)


#更新屏幕
def update_screen(ai_settings, screen, ship, aliens, bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""
	#每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	aliens.draw(screen)		#aliens.blitme()只能绘制单个图像，如上面的ship，而
							#这里的aliens是一个Group，所以只能用draw同时绘制
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	"""让最新绘制的屏幕可见"""
	pygame.display.flip()


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	"""响应子弹和外星人的碰撞"""
	"""检查是否有子弹击中了外星人，如果击中，则删除相应的子弹和外星人"""
	# groupcollide函数：前两个参数为Group,后两个参数表示在检测到碰撞后，是否删除对象
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	"""当外星人全部被消灭后，创建一群新的外星人"""
	if len(aliens) == 0:
		#删除现有的子弹并创建一群新的外星人
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)

#更新子弹状态
def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹位置
	bullets.update()

	#删除已经消失的子弹 注意不能直接遍历bullets 因为bullets会因为其中子弹被删除而
    #动态改变
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#print(len(bullets))
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

#发射子弹
def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果没有达到限制，就发射一颗子弹"""
	if len(bullets) < ai_settings.bullet_allowed:
			#print("bullet_allowed:%d len(bullets):%d" %(ai_settings.bullet_allowed, len(bullets)))
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x/(2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可以容纳多少行外星人"""
	avaiable_space_y = (ai_settings.screen_height-(3 * alien_height) 
						- ship_height)
	number_rows = int(avaiable_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并把它放在当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + (2 * alien_width) * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

#创建外星人群
def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	'''计算一行可以容纳多少外星人'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
								  alien.rect.height)

	"""创建外星人群"""
	for row_number in range(number_rows):
		'''创建一行外星人'''
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    #检查是否有外星人到达了屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #剩余飞船数量减一
        stats.ships_left -= 1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放在屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''检查是否有外星人到达了屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 和飞船被撞击一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

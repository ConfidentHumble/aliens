# -*- coding: utf-8 -*-
import sys

import pygame
from bullet import Bullet
from alien import Alien

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

"""检查弹起事件"""
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

#更新子弹状态
def update_bullets(bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹位置
	bullets.update()

	#删除已经消失的子弹 注意不能直接遍历bullets 因为bullets会因为其中子弹被删除而
    #动态改变
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#print(len(bullets))

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

def get_number_rows(ai_settings, ):
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
def create_fleet(ai_settings, screen, aliens):
	"""创建外星人群"""
	'''计算一行可以容纳多少外星人'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	

	'''创建第一行外星人'''
	for alien_number in range(number_aliens_x):
		create_alien(ai_settings, screen, aliens, alien_number)

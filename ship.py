# -*- coding: utf-8 -*-

import pygame

class Ship():


	def __init__(self, ai_settings, screen):
		"""初始化飞船并设置其初始位置"""
		#用传入的screen设置ship的screen
		self.screen = screen
		#获取飞船的设置类
		self.ai_settings = ai_settings	
		"""加载飞船图像并获取其外接矩形"""
		self.image = pygame.image.load('images/ship.bmp')
		#将ship设置为传入的图像的矩形
		self.rect = self.image.get_rect()
		#将屏幕设置为传入屏幕的矩形
		self.screen_rect = self.screen.get_rect()

		"""将每艘新飞船放在屏幕的底部中央"""
		#将ship矩形的中点x坐标设置为屏幕矩形的中点x坐标（设置水平距离）
		self.rect.centerx = self.screen_rect.centerx
		#将ship矩形的底设置为屏幕矩形的底
		self.rect.bottom = self.screen_rect.bottom
		#设置向右移动标志
		self.moving_right = False
		#设置向左移动标志
		self.moving_left = False
		#因为ship.rect.centerx为整型 无法直接存储float值 所以设置一个中间量来存储
		self.center = float(self.rect.centerx)

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""根据移动标志调整飞船的位置"""
		#self是一个rect类，有个属性值为right 通过判断飞船的rect的right与屏幕的rect的right的大小关系 来判断飞船是否到达最右边边缘
		if self.moving_right and self.rect.right < self.screen_rect.right:
			#self.rect.centerx += 1
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			#self.rect.centerx -= 1
			self.center -= self.ai_settings.ship_speed_factor
		#根据self.center更新rect对象
		self.rect.centerx = self.center

import pygame
from pygame.sprite import Sprite

#从pygame.sprite继承Sprite类
class Bullet(Sprite):
	def __init__(self, ai_settings, screen, ship):
		#调用super()来继承Sprite
		super().__init__()
		self.screen = screen

		#用pygame设置一个矩形：位置在(0,0) 宽和高为子弹的尺寸
		self.rect = pygame.Rect(0, 0, 3, 15)
		#设置子弹的位置
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		#为了微调子弹的速度,用小数存储子弹的y坐标
		self.y = float(self.rect.y)
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		"""向上移动子弹"""
		self.y -= self.speed_factor
		#更新表示子弹的rect的位置
		self.rect.y = self.y

	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		#调用pygame的draw.rect函数:在screen上用color填充rect占据的屏幕部分
		pygame.draw.rect(self.screen, self.color, self.rect)


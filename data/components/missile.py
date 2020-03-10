import pygame

from . import galaga_sprite
from .. import tools

PLAYER_SPEED = 350
ENEMY_SPEED = 300
ENEMY_TYPE = tools.grab_sheet(246, 51, 3, 8)
PLAYER_TYPE = tools.grab_sheet(246, 67, 3, 8)


class Missile(galaga_sprite.GalagaSprite):
	def __init__(self, loc, vel, is_enemy):
		super(Missile, self).__init__(pygame.Rect(0, 0, 2, 10))

		self.vel = vel
		self.is_enemy = is_enemy
		self.rect.center = loc

		if self.is_enemy:
			self.image = ENEMY_TYPE
		else:
			self.image = PLAYER_TYPE

	def update(self, dt):
		if self.is_enemy:
			vel = self.vel * ENEMY_SPEED * dt
		else:
			vel = self.vel * PLAYER_SPEED * dt
		self.rect.x += round(vel.x)
		self.rect.y += round(vel.y)
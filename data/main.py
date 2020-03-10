from typing import Union

import pygame

from data import constants as c
from data.states import main_menu, play_state, statistics, demo, new_high_score, state


class Control(object):
	"""
	Main class for running the game states and window
	"""
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.fps: int = c.FPS
		self.paused: bool = False
		self.running: bool = True
		self.screen: pygame.Surface = pygame.display.get_surface()

		# state variables
		self.state_dict: dict = {}
		self.state_name: str = 'None'
		self.state: Union[state.State, None] = None

	def setup_states(self, state_dict: dict, start_state: state.State):
		self.state_dict = state_dict
		self.state_name = start_state
		self.state = self.state_dict[self.state_name]({})

	def flip_state(self):
		persist = self.state.cleanup()
		prev, self.state_name = self.state_name, self.state.next
		self.state = self.state_dict[self.state_name](persist)

	def events(self):
		for event in pygame.event.get():
			t = event.type
			if t == pygame.QUIT:
				self.running = False
			elif t == pygame.KEYDOWN:
				k = event.key
				if k == pygame.K_ESCAPE:
					self.running = False
			self.state.get_event(event)
		return pygame.key.get_pressed()

	def main(self):
		while self.running:
			dt = self.clock.tick(self.fps) / 1000 # convert milliseconds to seconds
			keys = self.events()
			if not self.paused:
				self.state.update(dt, keys)

			if self.state.done:
				self.flip_state()
			elif self.state.quit:
				self.running = False

			self.state.display(self.screen, dt)
			pygame.display.update()


def main():
	the_app = Control()
	state_dict = {
		c.MENU_STATE: main_menu.Menu,
		c.PLAY_STATE: play_state.Play,
		c.NEW_SCORE_STATE: new_high_score.HighScore,
		c.PLAY_STATS: statistics.Stats,
		c.MENU_DEMO: demo.Demo
	}
	the_app.setup_states(state_dict, c.INITIAL_STATE)
	the_app.main()
import os, sys

game_engine_path = os.path.abspath('../CameraGameEngine')
sys.path.insert(1, game_engine_path)
from camera_game_engine import CameraGameEngine

from home_scene import HomeScene
from playing_scene import PlayingScene
from gameover_scene import GameoverScene

class FlappyGame(CameraGameEngine):
	def setup(self):
		self.playBackgroundMusic("./assets/audio/play.mp3")
		
		self.registerScene("HOME", HomeScene(self))
		self.registerScene("PLAYING", PlayingScene(self))
		self.registerScene("GAMEOVER", GameoverScene(self))
		self.initScene("HOME")

if __name__ == '__main__':
	FlappyGame('Flappy Webcam Game', 1)
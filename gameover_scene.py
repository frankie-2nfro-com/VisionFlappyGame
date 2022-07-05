from camera_game_engine import GameScene
import cv2

class GameoverScene(GameScene):
	def setup(self):
		self.elements["BG"] = {"type":"jpg", "file":"./assets/images/gameover_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text", "message":"Press 'p' to play again", "x":30, "y":690, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2}
			
	def reset(self):
		self.stage.setCapture(False) 

	def keyInToggle(self, key):
		if key & 0xFF == ord('p'):
			self.stage.jumpScene("HOME")
from random import randint
from camera_game_engine import GameScene
import cv2

from gesture_detect import HandDetector

# next version:
# add decoration image (cloud, city, etc)
# level up game (like increase speed)


class PlayingScene(GameScene):
	def setup(self):
		self.__detector = HandDetector()
		self.elements["bg"] = { "type":"jpg", "file":"./assets/images/bg.jpg", "x":0, "y":0, "w":1280, "h":720}		


	def reset(self):
		self.stage.setCapture(True) 

		self.bird_y = 350
		self.tube1_x = 1280
		self.tube1_y_delta = randint(-100, 100)

		self.tube2_x = 1280
		self.tube2_y_delta = randint(-100, 100)

		self.tube3_x = 1280
		self.tube3_y_delta = randint(-100, 100)

		self.point = 0
		self.__user_choice = ""


	def keyInToggle(self, key):
		if key & 0xFF == ord('w'):
			self.bird_up()
		elif key & 0xFF == ord('s'):
			self.bird_dn()

	def update(self):
		# get gesture and control the bird
		hand, res, dummy_x, dummy_y = self.__detector.chopHand(self.stage.originalFrame)
		self.__user_choice = self.__user_choice_by_gesture(res)
		if self.__user_choice == "S":
			self.bird_up()
		elif self.__user_choice == "R":
			self.bird_dn()

		# update tubes position
		self.tube1_x = self.tube1_x - 5
		if self.tube1_x < -200:
			self.tube1_x = 1280
			self.tube1_y_delta = randint(-100, 100)

		if self.tube1_x <= 770 or self.tube2_x < 1280:
			self.tube2_x = self.tube2_x - 5
			if self.tube2_x < -200:
				self.tube2_x = 1280
				self.tube2_y_delta = randint(-100, 100)
		
		if self.tube2_x <= 770 or self.tube3_x < 1280:
			self.tube3_x = self.tube3_x - 5
			if self.tube3_x < -200:
				self.tube3_x = 1280
				self.tube3_y_delta = randint(-100, 100)

		# update element and display
		self.elements["pipe1"] = { "type":"png","file":"./assets/images/pipe_d.png", "x":self.tube1_x, "y":-350+self.tube1_y_delta, "w":200, "h":620}		
		self.elements["pipe2"] = { "type":"png","file":"./assets/images/pipe_u.png", "x":self.tube1_x, "y":450+self.tube1_y_delta, "w":200, "h":620}
		
		self.elements["pipe3"] = { "type":"png","file":"./assets/images/pipe_d.png", "x":self.tube2_x, "y":-350+self.tube2_y_delta, "w":200, "h":620}		
		self.elements["pipe4"] = { "type":"png","file":"./assets/images/pipe_u.png", "x":self.tube2_x, "y":450+self.tube2_y_delta, "w":200, "h":620}		

		self.elements["pipe5"] = { "type":"png","file":"./assets/images/pipe_d.png", "x":self.tube3_x, "y":-350+self.tube3_y_delta, "w":200, "h":620}		
		self.elements["pipe6"] = { "type":"png","file":"./assets/images/pipe_u.png", "x":self.tube3_x, "y":450+self.tube3_y_delta, "w":200, "h":620}		

		self.elements["bird"] = { "type":"png","file":"./assets/images/bird.png", "x":50, "y":self.bird_y, "w":180, "h":136, "animate":"images", "images_freq": 3}		

		self.elements["PIP"] = { "type":"pip", "x":1030, "y":550, "w":240, "h":160 }

		self.elements["BIRD_POINT"] = {"type":"text", "message":"Point: " + str(self.point), "x":30, "y":40, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2}


	def afterRender(self):
		# check collision and show game over if hit the tube
		self.collision_detect()

		# add point if pass through the tube
		if self.tube1_x == -150 or self.tube2_x == -150 or self.tube3_x == -150:
			self.__pointUp()


	def bird_up(self):
		self.bird_y = self.bird_y - 5
		if self.bird_y < 0:
			self.bird_y = 0


	def bird_dn(self):
		self.bird_y = self.bird_y + 5
		if self.bird_y + 136 > 720:
			self.bird_y = 720-136
	
		
	def collision_detect(self):
		if self.tube1_x > -150 and self.tube1_x < 230:
			if -350+self.tube1_y_delta+620 > self.bird_y + 20:
				self.__gameover()
			if 450+self.tube1_y_delta < self.bird_y+136 - 20:
				self.__gameover()

		if self.tube2_x > -150 and self.tube2_x < 230:
			if -350+self.tube2_y_delta+620 > self.bird_y + 20:
				self.__gameover()
			if 450+self.tube2_y_delta < self.bird_y+136 - 20:
				self.__gameover()

		if self.tube3_x > -150 and self.tube3_x < 230:
			if -350+self.tube3_y_delta+620 > self.bird_y + 20:
				self.__gameover()
			if 450+self.tube3_y_delta < self.bird_y+136 - 20:
				self.__gameover()


	def __user_choice_by_gesture(self, gesture):
		# decode the value from the modal
		return {5:"P", 9:"S", 0:"R", 6:"R"}.get(gesture, "")


	def __pointUp(self):
		self.stage.playFxMusic("./assets/audio/point.mp3")
		self.point = self.point + 1


	def __gameover(self):
		self.stage.playFxMusic("./assets/audio/die.mp3")
		self.stage.jumpScene("GAMEOVER")

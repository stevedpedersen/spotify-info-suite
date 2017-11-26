
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

class Frame(QLabel):

	# when QLabel is clicked, emit a signal with an object param
	clicked = pyqtSignal(object)

	def __init__(self, controller, view, x, y, w, h, title, limit=0):
		super().__init__(view)
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.object_title = title
		self.setObjectName((self.object_title))
		self.char_limit = limit
		self.display_title_label = QLabel(self)
		self.display_text_label = QLabel(self)
		self.display_images_label = QLabel(self)
		self.layout = QVBoxLayout(self)
		self.controller = controller
		self.view = view
		self.setGeometry(self.x, self.y, self.w, self.h)
		self.frame_components = []
		self.images_list = []

		self.image_label = QLabel(self)

		self.metacritic_exists = False
		self.mc_album_thumb = QLabel(self)
		self.mc_title = QLabel(self)
		self.mc_critic = QLabel(self)
		self.mc_user = QLabel(self)

	def set_display_title(self, title, x, y):
		# self.display_title_label = QLabel(self)
		self.display_title_label.setText(title)
		self.display_title_label.move(x, y)
		self.display_title_label.resize(int(self.w*0.96), 35) # limit width to 93% of frame
		self.display_title_label.setObjectName('frame_title')
		self.display_title_label.setWordWrap(True)
		self.frame_components.append(self.display_title_label)

	def set_display_text(self, text, x=5, y=45,obj=''):
		# self.display_text_label = QLabel(self)
		min_y = self.display_title_label.height() + 8
		scroll_height = self.h - (y+min_y)
		if self.display_text_label.text() == '':

			self.display_text_label.setText(text)
			self.display_text_label.setGeometry(x, y, self.w, self.h)
			name = 'frame_text' if obj == '' else obj
			self.display_text_label.setObjectName(name)
			self.display_text_label.setWordWrap(True)

			self.display_text_label.setStyleSheet('')
			self.frame_components.append(self.display_text_label)
			scroll = QScrollArea()
			scroll.setWidget(self.display_text_label)
			scroll.setWidgetResizable(True)			
			scroll.setFixedHeight(scroll_height)	
			# scroll.ensureVisible(0, scroll_height-y*4.5)

			self.display_text_label.setAlignment(Qt.AlignTop)
			self.layout.addWidget(scroll)
		else:
			self.display_text_label.setText(text)
			self.display_text_label.setAlignment(Qt.AlignTop)
			# self.layout.setAlignment(Qt.AlignTop)

	# TODO: maybe pass in a dict that has the pixmap, width and height of each
	# 	rather than separate lists
	def add_musikki_artist_images(self, images, widths, heights):
		x, y = 10, 45
		w, h = self.w - x*2, self.h - y - 40
		self.current_image = 0
		# print('current image: ', self.current_image)
		#
		# print("SIZE: ", len(images))
		# print("w: ", w)
		# print("h: ", h)
		# print("w2: ", self.w)
		# print("h2: ", self.h)
		print('images: ', len(images))

		for i in range(len(images)):
			if widths[i] > heights[i]:
				if w > widths[i]:
					# print('image is wider than it is tall and less wide than the frame')
					w = widths[i]
				image = images[i].scaledToWidth(w)
				self.images_list.append(image)
			else:
				if h > heights[i]:
					# print('image is taller than it is wide and less tall than the frame')
					h = heights[i]
				image = images[i].scaledToHeight(h)
				self.images_list.append(image)

		print('IMAGES LIST: ', self.images_list)

		# self.image_label.setStyleSheet('border: 1px solid #0f0f0f;')
		self.image_label.resize(w, h)
		self.image_label.setPixmap(self.images_list[self.current_image])
		self.image_label.move(x, y)
		self.image_label.setAlignment(Qt.AlignCenter)
		self.create_image_buttons()
		self.image_label.show()
		self.musikki_images_added is True
		# for i, image in enumerate(images):
		# 	# w, h = widths[i], heights[i]
		# 	w, h = self.w, self.h - y
		# 	image = image.scaledToWidth(w)
			
		# 	self.image_label = QLabel(self)
		# 	# self.image_label.setStyleSheet('border: 1px solid #0f0f0f;')
		# 	self.image_label.resize(w, h)			
		# 	self.image_label.setPixmap(image)
		# 	self.image_label.move(x + x*i, y)
		# 	self.image_label.show()

	def add_flickr_artist_images(self, images, widths, heights):
		x, y = 10, 45
		w, h = self.w - x*2, self.h - y - 40
		self.current_image = 0
		# print('current image: ', self.current_image)
		#
		# print("SIZE: ", len(images))
		# print("w: ", w)
		# print("h: ", h)
		# print("w2: ", self.w)
		# print("h2: ", self.h)
		print('images: ', len(images))

		for i in range(len(images)):
			if widths[i] > heights[i]:
				if w > widths[i]:
					# print('image is wider than it is tall and less wide than the frame')
					w = widths[i]
				image = images[i].scaledToWidth(w)
				self.images_list.append(image)
			else:
				if h > heights[i]:
					# print('image is taller than it is wide and less tall than the frame')
					h = heights[i]
				image = images[i].scaledToHeight(h)
				self.images_list.append(image)

		print('IMAGES LIST: ', self.images_list)

		# self.image_label.setStyleSheet('border: 1px solid #0f0f0f;')
		self.image_label.resize(w, h)
		self.image_label.setPixmap(self.images_list[self.current_image])
		self.image_label.move(x, y)
		self.image_label.setAlignment(Qt.AlignCenter)
		self.create_image_buttons()
		self.image_label.show()
		self.flickr_images_added is True

	def next_image(self):
		if self.images_list is not None:
			if self.current_image < len(self.images_list) - 1:
				self.current_image = self.current_image + 1
				print('current image: ', self.current_image)
				print('length: ', len(self.images_list))
				self.image_label.setPixmap(self.images_list[self.current_image])
				print('New NEXT_IMAGE: ', self.images_list[self.current_image])

	def prev_image(self):
		if self.images_list is not None:
			if self.current_image > 0:
				self.current_image = self.current_image - 1
				print('current image: ', self.current_image)
				print('length: ', len(self.images_list))
				self.image_label.setPixmap(self.images_list[self.current_image])
				print('New PREV_IMAGE: ', self.images_list[self.current_image])

	def get_display_text_label(self):
		return self.display_text_label
	def get_display_title_label(self):
		return self.display_title_label

	def get_display_image_labels(self):
		return self.display_images_label

	def set_expand_button(self):
		self.expand_button = QPushButton('Expand', self.view)
		self.frame_components.append(self.expand_button)

	def add_metacritic_content(self, review):
		
		pixmap = QPixmap()
		pixmap.loadFromData(review.pixmap)
		padding = 20
		if pixmap.height() > pixmap.width():
			pixmap = pixmap.scaledToHeight(self.h - padding)
		else:
			pixmap = pixmap.scaledToWidth(self.w/4 - padding)
		
		if not self.metacritic_exists:	
			# create the layout
			x = padding/10
			y = 0
			w = self.w / 4
			h = self.h
					
			self.mc_album_thumb.setGeometry(x,y, w,h)
			self.mc_album_thumb.setPixmap(pixmap)
			self.mc_album_thumb.setAlignment(Qt.AlignCenter)

			self.mc_title.setText(review.artist + ' - '+ review.album)
			self.mc_title.setObjectName('mc_title')
			self.mc_title.setGeometry(self.w/3.8, self.h/10, self.w*0.75,20)
			self.mc_title.setWordWrap(True)
			self.mc_title.setStyleSheet('')

			self.mc_critic.setText(
				'Critic Score:   '+ str(review.critic_rating)[0]+'.'+str(review.critic_rating)[1]+
				'  ('+str(review.critic_count)+' reviews)'			
			)
			self.mc_critic.setObjectName('mc_critic')
			self.mc_critic.setGeometry(self.w/3.8, self.h/2.5, self.w*0.75,20)
			self.mc_critic.setWordWrap(True)
			self.mc_critic.setStyleSheet('')

			self.mc_user.setText(
				'User Score:    '+ str(review.user_rating)+ '  ('+str(review.user_count)+' reviews)'
			)		
			self.mc_user.setObjectName('mc_user')
			self.mc_user.setGeometry(self.w/3.8, self.h/1.5, self.w*0.75,20)
			self.mc_user.setWordWrap(True)
			self.mc_user.setStyleSheet('')

			self.frame_components.extend([
				self.mc_album_thumb, self.mc_title, self.mc_critic, self.mc_user
			])

			# metacritic components have been created--no need to do it again when song changes.
			self.metacritic_exists = True
		
		else:
			# otherwise, update the text and image
			self.mc_album_thumb.setPixmap(pixmap)
			self.mc_title.setText(review.artist + ' - '+ review.album)
			self.mc_critic.setText(
				'Critic Score:   '+ str(review.critic_rating)[0]+'.'+str(review.critic_rating)[1]+
				'  ('+str(review.critic_count)+' reviews)'	
			)
			self.mc_user.setText(
				'User Score:    '+ str(review.user_rating)+ '  ('+str(review.user_count)+' reviews)'
			)

		self.show_frame_components()

	# Clears Metacritic frame and creates default image & text
	def default_metacritic_content(self, default_image):
		padding = 20
		if default_image.height() > default_image.width():
			default_image = default_image.scaledToHeight(self.h - padding)
		else:
			default_image = default_image.scaledToWidth(self.w/4 - padding)

		if not self.metacritic_exists:
			x = padding/10
			y = 0
			w = self.w / 4
			h = self.h
				
			self.mc_album_thumb.setGeometry(x,y, w,h)
			self.mc_album_thumb.setAlignment(Qt.AlignCenter)
			self.mc_title.setObjectName('mc_title')
			self.mc_title.setGeometry(self.w/3.8, self.h/10, self.w*0.75,20)
			self.mc_title.setWordWrap(True)

		self.mc_album_thumb.setPixmap(default_image)
		self.mc_title.setText('No results on Metacritic')
		self.mc_title.setStyleSheet('')
		self.mc_critic.hide()
		self.mc_user.hide()



	def create_playback_buttons(self):
		self.playpause_button = QPushButton('Play/Pause', self.view)
		self.prev_button = QPushButton('Prev', self.view)
		self.next_button = QPushButton('Next', self.view)
		self.frame_components.extend([
			self.playpause_button, self.prev_button, self.next_button
		])
				
		self.playpause_button.setObjectName('playpause_button')
		self.prev_button.setObjectName('prev_button')		
		self.next_button.setObjectName('next_button')	

		self.prev_button.resize(self.prev_button.sizeHint() * 1.3)	
		self.playpause_button.resize(self.playpause_button.sizeHint() * 1.3)	
		self.next_button.resize(self.next_button.sizeHint() * 1.3)	

		prevw = self.prev_button.width()
		playw = self.playpause_button.width()
		nextw = self.next_button.width()
		spacer = self.w / 30 if self.w / 30 < 16 else 15
		total = prevw + playw + nextw + spacer*2
		leftover = self.w - total
		prev_x = leftover / 2
		play_x = prev_x + spacer + prevw
		next_x = play_x + spacer + playw

		# print how much space is to the left of Prev btn and to the right of Next btn
		# print('Left: ', prev_x, '\nRight: ', self.w - (next_x + self.next_button.width()))
		# print('spacer: ', spacer)

		self.prev_button.move(prev_x, self.display_title_label.height()+20)	
		self.playpause_button.move(play_x, self.display_title_label.height()+20)	
		self.next_button.move(next_x, self.display_title_label.height()+20)	

	def hide_frame_components(self):
		for f in self.frame_components:
			f.hide()

	def show_frame_components(self):
		for f in self.frame_components:
			f.show()

	def create_image_buttons(self):
		self.next_image_button = QPushButton('>', self.view)
		self.prev_image_button = QPushButton('<', self.view)
		self.frame_components.extend([
			self.next_image_button, self.prev_image_button
		])

		self.next_image_button.setObjectName('next_image_button')
		self.prev_image_button.setObjectName('prev_image_button')

		self.next_image_button.resize(40, 30)
		self.prev_image_button.resize(40, 30)
		next_x = 900
		prev_x = 850
		self.next_image_button.move(next_x, 302)
		self.prev_image_button.move(prev_x, 302)

	def get_playback_prev_button(self):
		return self.prev_button

	def get_playback_play_button(self):
		return self.playpause_button

	def get_playback_next_button(self):
		return self.next_button

	def get_frame_components(self):
		return self.frame_components

	def mousePressEvent(self, event):
		self.clicked.emit(self)

	def get_image_next_button(self):
		return self.next_image_button

	def get_image_prev_button(self):
		return self.prev_image_button

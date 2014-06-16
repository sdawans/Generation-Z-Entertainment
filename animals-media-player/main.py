import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from  kivy.uix.image import AsyncImage
from pygame import mixer
import random
import time
import os
import config
kivy.require('1.0.7')

from kivy.app import App

animals_dir = config.ANIMALS_DIR
if not animals_dir.endswith(os.path.sep):
    animals_dir += os.path.sep

class MediaButton(Button):
    played = False
    def set_image(self, image):
        self.background_normal = image
        self.background_down = image
    def set_sound(self, sound):
        self.sound = sound

class Animalsmediaplayer(FloatLayout):
    def __init__(self, app):
        self.last_media = None
        self.app = app
        FloatLayout.__init__(self)

    def button_pressed(self, instance, value):
        current_time = time.time()
        if current_time - value.starttime > 2:
            if self.last_media != None and self.last_media != value:
                self.app.refresh_media(self.last_media)
            self.last_media = value
            mixer.music.load(value.sound)
            value.played = True
            value.starttime = time.time()
            mixer.music.play()

class AnimalsmediaplayerApp(App):
    mixer.init()
    # List of animals based on subdirectories in the animals folder
    # Ignore anything that's not a directory.
    animals = os.walk(animals_dir).next()[1]

    def refresh_media(self, media):
        if media.played == True:

            num_animal = random.randint(0,len(self.animals)-1)
            animal_dir = animals_dir + self.animals[num_animal]
            animal_dir_files = os.listdir(animal_dir)

            images = []
            tracks = []

            for f in animal_dir_files:
                print f
                if f.endswith('.mp3'):
                    tracks.append(os.path.join(animal_dir,f))
                elif f.endswith('.jpg') or f.endswith('.png'):
                    images.append(os.path.join(animal_dir,f))

            image = images[random.randint(0,len(images)-1)] if len(images) > 1 else images[0]
            track = images[random.randint(0,len(tracks)-1)] if len(tracks) > 1 else tracks[0]

            media.set_sound(track)
            media.set_image(image)
            media.played = False
        return

    def build(self):
        root = Animalsmediaplayer(self)
        even = True #Override every other button
        for media in root.children[0].children:
            media.played = True
            media.starttime = 0
            self.refresh_media(media)
        return root

if __name__ == '__main__':
    AnimalsmediaplayerApp().run()

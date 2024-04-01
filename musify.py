from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
from keras.preprocessing.image import load_img, img_to_array
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.core.window import Window
from PIL import Image as PILImage
from kivy.lang import Builder
from kivymd.app import MDApp
import tensorflow as tf
import numpy as np
import csv

Window.size = (310, 580)

class CameraScreen(Screen):
    pass

class TreatmentScreen(Screen):
    pass

class Musify(MDApp):

    song_name = StringProperty()
    song_artist = StringProperty()
    label = StringProperty()
    def build(self):

        screenmanager = ScreenManager()
        screenmanager.add_widget(Builder.load_file("main.kv"))
        screenmanager.add_widget(Builder.load_file("camera.kv"))
        song_screen = Builder.load_file("song_recommend.kv")
        screenmanager.add_widget(song_screen)
        screenmanager.add_widget(Builder.load_file("player.kv"))
        return screenmanager
    
    def capture_image(self):
        current_screen = self.root.current_screen
        if current_screen.name == 'camera':
            camera_widget = current_screen.ids.camera_id
            if camera_widget.texture:
                img_texture = camera_widget.texture
                if img_texture:
                    pil_image = PILImage.frombytes('RGBA', img_texture.size, img_texture.pixels)
                    pil_image = pil_image.convert('L')
                    pil_image = pil_image.resize((48, 48))  # Resize the image to the desired input size
                    image_array = img_to_array(pil_image)
                    image_array = image_array / 255.0
                    self.model = tf.keras.models.load_model('EmotionDetectionModel.h5')
                    prediction = self.model.predict(np.expand_dims(image_array, axis=0))
                    predicted_class = np.argmax(prediction, axis=1)
                    class_names = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]


                    predicted_class_name = class_names[predicted_class[0]]

                    self.label = f"{predicted_class_name}"
                    return self.label

# Caution
# Do not change the code unnecessarly
    
    def read_csv(self, filename):
        data = []
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data
    

    def on_item_release(self, song):
        # Handle the on_release event for each item
        app = MDApp.get_running_app()
        app.root.current = "player"
        self.song_name = song['Song Name']
        self.song_artist = song['Artist']


    def create_list_items(self, screen, emotion):
        # Read data from the CSV file
        data = self.read_csv("song_data.csv")

        # Filter data based on emotion
        filtered_data = [song for song in data if song['Emotion'] == emotion]

        # Create TwoLineAvatarListItem dynamically based on the filtered data
        for song in filtered_data:
            item = TwoLineAvatarListItem(
                text=song['Song Name'],
                secondary_text=song['Artist']
            )
            item.add_widget(ImageLeftWidget(source="images\song_logo.png"))
            item.bind(on_release= lambda instance, song=song: self.on_item_release(song))
            screen.ids.md_list.add_widget(item)
            # item.canvas.after.add(Color(rgba=(0.2, 0.5, 0.7, 1)))
            # item.canvas.after.add(
            #     RoundedRectangle(pos=item.pos, size=item.size, radius=[dp(18), dp(18), dp(18), dp(18)]))
    def on_play_button_release(self):
        play_button = self.root.get_screen("player").ids.play_button

        # Check the current icon and change it accordingly
        if play_button.icon == "play":
            play_button.icon = "pause"
            # Add code for play action
        else:
            play_button.icon = "play"
            # Add code for pause action
            

if __name__ == "__main__":
    
    LabelBase.register(name="Poppins", fn_regular="Poppins-Bold.ttf")
    LabelBase.register(name="Poppinsl", fn_regular="Poppins-Light.ttf")

    Musify().run()


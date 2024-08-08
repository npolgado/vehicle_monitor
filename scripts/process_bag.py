# To change the kivy default settings
# we use this module config
from kivy.config import Config
 
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

from kivy.app import App

from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.filechooser import FileChooser, FileChooserListView
import matplotlib.pyplot as plt
import numpy as np
import os


BACKGROUND = (0.1, 0.1, 0.1, 0.1)
BAG_PATH = '/media/ubuntu/T7'

# create the layout class
class Filechooser(BoxLayout):
    def __init__(self, **kwargs):
        super(Filechooser, self).__init__(**kwargs)
        self.orientation = 'vertical'

    def select(self, *args):
        try: self.label.text = args[1][0]
        except: pass

class BagVis(BoxLayout):
    def __init__(self, **kwargs):
        super(BagVis, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.orientation = 'vertical'

        # Create the file finder view of the root folder
        self.fc = FileChooserListView(size_hint=(1, 0.3))
        self.fc.path = os.path.expanduser('~/Documents/Github/vehicle_monitor')
        self.fc.bind(selection=self.on_file_selection)
        self.add_widget(self.fc)

        # Create the 2x2 grid of Matplotlib plots
        self.plot_area = BoxLayout(size_hint=(1, 0.6))
        self.add_widget(self.plot_area)

        fig, ax = plt.subplots(2, 2, figsize=(8, 8))
        plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)


        self.plot = FigureCanvasKivyAgg(fig)
        
        for i in range(4):
            ax[i//2, i%2].bar([0], np.random.rand(1))
        
        self.plot_area.add_widget(self.plot)

        # slider for timeline
        self.timeline = Slider(min=0, max=100, value=0, size_hint = (1, 0.1))
        self.add_widget(self.timeline)

        # Create the control buttons
        self.button_area = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.start_button = Button(text='Start', on_press=self.start_processing)
        self.stop_button = Button(text='Stop', on_press=self.stop_processing)
        self.exit_button = Button(text='Exit', on_press=self.exit_app)
        self.button_area.add_widget(self.start_button)
        self.button_area.add_widget(self.stop_button)
        self.button_area.add_widget(self.exit_button)
        self.add_widget(self.button_area)

        self.is_playing = False

    def process_bag(self, bag_path):
        import rosbag
        bag = rosbag.Bag(bag_path)
        for topic, msg, t in bag.read_messages(topics=['chatter', 'numbers']):
            print(msg)
        bag.close()

    def on_file_selection(self, instance, value):
        path = os.path.expanduser(value[0])
        print('Selected:', path)

        # if the file has a .bag extension, process the bag
        if path.endswith('.bag'):
            self.process_bag(path)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_processing(self, instance):
        # Add your start processing logic here
        pass

    def stop_processing(self, instance):
        # Add your stop processing logic here
        pass

    def exit_app(self, instance):
        # Exit the application
        App.get_running_app().stop()

class MyApp(App):
    def build(self):
        self.root = BagVis()
        return self.root
if __name__ == '__main__':
    MyApp().run()
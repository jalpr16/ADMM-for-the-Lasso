
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import regression
import numpy as np
import copy

num_fields = 0 # the number of fields in the data, including the y field
num_data = 0
field_names = []
field_X = np.array([])
field_y = np.array([])
beta = np.array([])

class RootWidget(FloatLayout):
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.options = OptionsWidget()
        self.add_widget(self.options)


class OptionsWidget(GridLayout):

    def __init__(self, **kwargs):
        super(OptionsWidget, self).__init__(**kwargs)

        Builder.load_file('program.kv')
        Builder.apply(self)

        field_X_average = [float(np.sum(field_X[:,i]) / num_data) for i in range(num_fields-1)]

        print(beta)

        self.add_widget(Label(text = "parameters", font_size = '12sp', size_hint = (2, 1)))
        self.add_widget(Label())
        self.add_widget(Label(text = "values", font_size = '12sp', size_hint = (.1, 1)))
        self.add_widget(Label(text = "{:.2f}".format(beta[0]), font_size = '12sp', size_hint = (.1, 1)))

        self.sliders = []
        for i in range(num_fields-1):
            self.sliders.append(Slider(value = field_X_average[i], min = 0., max = field_X_average[i] * 3,
                                       background_width = '16sp', cursor_size = (24, 24)))
            self.sliders[-1].bind(value = self.on_slider_value)
            self.sliders[-1].label = Label(text = "{:.2f}".format(field_X_average[i]),
                                           font_size = '12sp', size_hint = (.1, 1))
            self.add_widget(Label(text = field_names[i], font_size = '12sp', size_hint = (1, 1)))
            self.add_widget(self.sliders[-1])
            self.add_widget(self.sliders[-1].label)
            self.add_widget(Label(text = "{:.2f}".format(beta[i+1]), font_size = '12sp', size_hint = (.1, 1)))

        self.add_widget(Label(text = field_names[-1], font_size = '12sp', size_hint = (2, 1)))
        self.add_widget(Label())
        self.add_widget(Label())
        self.y_label = Label(font_size = '12sp', size_hint = (.1, 1))
        self.add_widget(self.y_label)

    def on_slider_value(self, instance, value):
        instance.label.text = "{:.2f}".format(value)
        self.y_label.text = "{:.2f}".format(
            np.sum(np.insert(np.array([self.sliders[i].value for i in range(num_fields-1)]), 0, 1) * beta))


class RootApp(App):

    def __init__(self, **kwargs):
        super(RootApp, self).__init__(**kwargs)

        global field_X, field_y, num_fields, num_data, field_names, beta
        field_X, field_y = regression.data_loader("data.txt")
        num_fields = len(field_X[0]) + 1
        num_data = field_y.size

        reg = regression.Regression(field_X, field_y, 1, 1)
        reg.run(100)
        beta = copy.deepcopy(reg.beta).reshape(num_fields)

        with open("data_index.txt", 'r') as file:
            for line in file:
                field_names.append(line)

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    RootApp().run()
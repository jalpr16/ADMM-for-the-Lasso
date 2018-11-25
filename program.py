
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button

import regression
import numpy as np
import copy
import sys

num_fields = 0         # the number of fields in the data, including the y field
num_data = 0           # the number of data
field_names = []
field_X = np.array([]) # x values as a 2-D array
field_y = np.array([]) # y values as a 2-D array, each row containing one y value for each data
beta = np.array([])    # β values calculated in regression.py

class RootWidget(ScrollView):
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.do_scroll = False, True
        self.bar_width = 10
        self.options = OptionsWidget()
        self.add_widget(self.options)


class OptionsWidget(GridLayout):

    def __init__(self, **kwargs):
        super(OptionsWidget, self).__init__(**kwargs)
        
        self.bind(minimum_height = self.setter('height'))

        Builder.load_file('program.kv')
        Builder.apply(self)

        field_X_average = [float(np.sum(field_X[:,i]) / num_data) for i in range(num_fields-1)]
        field_X_max = [float(max(field_X[:,i])) for i in range(num_fields-1)]

        self.options_box.height = 40 * (num_fields-1)
        self.sliders = []
        for i in range(num_fields-1):
            self.sliders.append(Slider(value = field_X_average[i],
                                       min = 0., max = field_X_max[i] * 2,
                                       size_hint = (1, 1),
                                       background_width = '16sp', cursor_size = (24, 24)))
            self.sliders[-1].bind(value = self.on_slider_value)
            self.sliders[-1].label = Label(text = "{:.2f}".format(field_X_average[i]),
                                           font_size = '12sp', size_hint = (.3, 1))
            box = BoxLayout(size_hint = (1, None), height = 40)
            box.add_widget(Label(text = field_names[i], font_size = '12sp',
                                 size_hint = (1, 1)))
            box.add_widget(self.sliders[-1])
            box.add_widget(self.sliders[-1].label)
            box.add_widget(Label(text = "{:.2f}".format(beta[i+1]), font_size = '12sp',
                                 size_hint = (.3, 1)))
            self.options_box.add_widget(box) 

        self.predicted_y_name.text = 'predicted ' + field_names[-1]
        self.actual_y_name.text = 'actual ' + field_names[-1]
        self.actual_y_button.bind(on_press = self.on_actual_y_value)

    def on_slider_value(self, instance, value):
        instance.label.text = "{:.2f}".format(value)
        self.predicted_y.text = "{:.2f}".format(
            np.sum(np.insert(np.array([self.sliders[i].value for i in range(num_fields-1)]), 0, 1) * beta))
        self.actual_y_idx.text = ""
        self.actual_y.text = ""

    def on_actual_y_value(self, *args):
        idx = np.random.randint(num_data)
        for i in range(num_fields-1):
            self.sliders[i].value = float(field_X[idx, i])
        self.actual_y_idx.text = "data #" + str(idx)
        self.actual_y.text = str(field_y[idx, 0])


class PredictorApp(App):

    def __init__(self, file_data_name = str("data.txt"), file_index_name = str("data_index.txt"), 
                 lamb = 1, rho = 1, epochs = 100, *args, **kwargs):
        super(PredictorApp, self).__init__(**kwargs)

        global field_X, field_y, num_fields, num_data, field_names, beta
        field_X, field_y = regression.data_loader(file_data_name)
        num_fields = len(field_X[0]) + 1
        num_data = field_y.size

        reg = regression.Regression(field_X, field_y, lamb, rho)
        reg.run(epochs)
        beta = copy.deepcopy(reg.beta).reshape(num_fields)

        with open(file_index_name, 'r') as file:
            for line in file:
                if line[-1] == '\n':
                    field_names.append(line[:-1])
                else:
                    field_names.append(line)

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    args = sys.argv[3:]
    for i in range(len(args)):
        if i < 2:
            try:
                args[i] = float(args[i])
            except ValueError:
                print("ValueError: λ, ρ values must be real numbers")
                break
        else:
            try:
                args[i] = int(args[i])
            except ValueError:
                print("ValueError: the number of epochs must be an integer")
                break
    else:
        PredictorApp(*sys.argv[1:3], *args).run()
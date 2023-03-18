from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
import sqlite3
import json

with open("foods.json") as f:
    db = json.load(f)


def convert(fr, to, item ,amount):

    mydict = db[item]

    diff = mydict[to] / mydict[fr]

    sumup = amount * diff

    return sumup


class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='main', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal
    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal

class MainScreenBox(BoxLayout):
    def __init__(self, screen ,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(Label(text="Unit Converter App", size_hint=(1, 0.75)))
        self.add_widget(ScrButton(screen, direction="up", goal="convert", text="Convert Units", size_hint=(1, 0.1)))

class MainScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreenBox(self))

class PostConvertButton(Button):
    def __init__(self, textbox, label,  **kwargs):
        super().__init__(**kwargs)
        self.textbox = textbox
        self.label = label

    def on_press(self):
        self.fullfiled = self.parent.parent.fromu != "" and self.parent.parent.tou != "" and self.parent.parent.item != "" and len(self.textbox.text) > 0

        if self.fullfiled:
            print("i wanna take drugs")

            fr = self.parent.parent.fromu
            to = self.parent.parent.tou
            item = self.parent.parent.item
            amount = int(self.textbox.text)
            result = convert(fr,to, item, amount)

            self.label.text = f"{amount} {fr} of {item} is {result} {to}"

        #print(f"{self.fullfiled}, fromu {self.parent.parent.fromu}, tou {self.parent.parent.tou}, item {self.parent.parent.item}")

class ConvertBox(BoxLayout):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)

        self.fromu = ""
        self.tou = ""
        self.item = ""

        self.hbox = BoxLayout(size_hint_y = 0.1)
        self.orientation = "vertical"
        self.textbox = TextInput(size_hint=(0.5,1), input_filter=("int"))
        self.from_indicator = Button(text="Select item", size_hint = (1, 0.1))
        self.from_dropdown = DropDown(auto_dismiss=True, size_hint_x=1, size_hint_y=0.1)
        for i in db:
            btn = Button(text=i, size_hint_y=None, height=self.from_dropdown.height/3)
            btn.bind(on_release=lambda btn: self.flow(btn, self.item, self.from_indicator, self.from_dropdown))


            self.from_dropdown.add_widget(btn)
        self.from_dropdown.dismiss()

        self.from_indicator.bind(on_release=self.from_dropdown.open)

        self.to_indicator = Button(text="Select item", size_hint = (1, 0.1))
        self.to_dropdown = DropDown(auto_dismiss=True, size_hint_x=1, size_hint_y=0.1)                                         
        for i in ["kg", "grams", "cups", "oz", "liters"]:
            btn = Button(text=i, size_hint_y=None, height=self.to_dropdown.height/3)
            #btn.bind(on_release=lambda btn: self.on_select_to_item(btn))
            #btn.bind(on_release=self.to_dropdown.dismiss)
            btn.bind(on_release=lambda btn: self.flow1(btn, self.fromu,self.to_indicator, self.to_dropdown))
            self.to_dropdown.add_widget(btn)
        self.to_indicator.bind(on_release=self.to_dropdown.open)
        self.to_dropdown.dismiss()

        self.amount_indicator = Button(text="Select item", size_hint = (1, 0.1))
        self.amount_dropdown = DropDown(auto_dismiss=True, size_hint_x=1, size_hint_y=0.1)                                         
        for i in ["kg", "grams", "cups", "oz", "liters"]:
            btn = Button(text=i, size_hint_x=0.4, size_hint_y=None, height=self.amount_dropdown.height/3)
            btn.bind(on_release=lambda btn: self.on_select_theother(btn))

            btn.bind(on_release=self.amount_dropdown.dismiss)
            btn.bind(on_release=lambda btn: self.flow2(btn, self.tou, self.amount_indicator, self.amount_dropdown))
            self.amount_dropdown.add_widget(btn)
        self.amount_indicator.bind(on_release=self.amount_dropdown.open)
        self.amount_dropdown.dismiss()
        
        self.hbox.add_widget(self.textbox)
        self.result_label = Label(text="X [unit] is Y in [unit]", size_hint_y = 0.1)
        self.hbox.add_widget(PostConvertButton(self.textbox,self.result_label, text="submit", size_hint=(0.5,1)))
        
        

        # add the DropDown widgets to the main layout
        self.add_widget(ScrButton(screen, direction="down", goal="main", text="Home", size_hint=(1,0.1)))
        self.add_widget(self.from_indicator)
        self.add_widget(Label(text="What are you converting from?",size_hint=(1,0.1)), )
        self.add_widget(self.from_dropdown)
        self.add_widget(self.to_indicator)
        self.add_widget(Label(text="What are you converting to?",size_hint=(1,0.1)), )
        self.add_widget(self.to_dropdown)
        self.add_widget(self.amount_indicator)
        self.add_widget(Label(text="How much of from are you converting? ",size_hint=(1,0.1)), )
        self.add_widget(self.amount_dropdown)
        self.add_widget(self.hbox)
        self.add_widget(self.result_label)
      
    def flow(self, btn, param, param2, dropdown):
        param2.text = btn.text
        self.item = btn.text
        print(param)
        dropdown.dismiss()

    def flow1(self, btn, param, param2, dropdown):
        param2.text = btn.text
        self.fromu = btn.text
        print(param)
        dropdown.dismiss()

    def flow2(self, btn, param, param2, dropdown):
        param2.text = btn.text
        self.tou = btn.text
        print(param)
        dropdown.dismiss()
    

        

    def toggle_dropdown1(self, *args):
        self.dropdown1.open(self.choice_indicator)
    def set_from_indicator_text(self, btn):
        self.from_indicator.text = btn.text
        self.from_dropdown.dismiss()

    def on_select_to_item(self, btn):
        self.to_indicator.text = btn.text
        self.to_dropdown.dismiss()

    def on_select_theother(self, btn):
        self.amount_indicator.text = btn.text
        self.amount_dropdown.dismiss()



class ConvertScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_widget(ConvertBox(self))
 
class UnitConvertApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScr(name='main'))
        sm.add_widget(ConvertScreen(name='convert'))
        return sm

UnitConvertApp().run()
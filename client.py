from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
import requests

class ProductCard(MDCard):
    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = "300dp", "150dp"
        self.padding = "4dp"
        self.orientation = "vertical"
        self.spacing = "4dp"
        self.elevation = 8
        self.radius = [15]

        self.md_bg_color = [1, 1, 1, 1]

        self.add_widget(MDLabel(
            text=product['name'],
            theme_text_color="Primary",
            halign="center",
            font_size="14sp"
        ))

        self.add_widget(MDLabel(
            text=product['description'],
            theme_text_color="Secondary",
            halign="center",
            font_size="12sp"
        ))

        rating = product.get('rating', 'Н/Д')
        in_stock = product.get('in_stock', 0)
        self.add_widget(MDLabel(
            text=f"Цена: {product['price']} | Рейтинг: {rating} | В наличии: {in_stock} шт",
            theme_text_color="Secondary",
            halign="center",
            font_size="12sp"
        ))

Builder.load_string('''
<MainBoxLayout>:
    orientation: 'vertical'
    spacing: dp(8)
    MDTextField:
        id: name_input
        hint_text: "Наименование товара"
        size_hint_x: None
        width: "160dp"
        pos_hint: {"center_x": 0.5}
    MDTextField:
        id: min_price_input
        hint_text: "Минимальная цена"
        input_filter: "int"
        size_hint_x: None
        width: "160dp"
        pos_hint: {"center_x": 0.5}
    MDTextField:
        id: max_price_input
        hint_text: "Максимальная цена"
        input_filter: "int"
        size_hint_x: None
        width: "160dp"
        pos_hint: {"center_x": 0.5}
    MDTextField:
        id: keywords_input
        hint_text: "Ключевые слова"
        size_hint_x: None
        width: "160dp"
        pos_hint: {"center_x": 0.5}
    MDRaisedButton:
        id: search_button
        text: "Поиск"
        pos_hint: {"center_x": 0.5}
        on_release: app.on_search()
    ScrollView:
        GridLayout:
            id: products_box
            cols: 2
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(8)
            padding: dp(8)
            adaptive_height: True
''')

class MainBoxLayout(MDBoxLayout):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return MainBoxLayout()

    def on_search(self):
        name = self.root.ids.name_input.text.strip()
        min_price = self.root.ids.min_price_input.text.strip()
        max_price = self.root.ids.max_price_input.text.strip()
        keywords = self.root.ids.keywords_input.text.strip()

        params = {
            'name': name,
            'min_price': min_price if min_price.isdigit() else None,
            'max_price': max_price if max_price.isdigit() else None,
            'description': keywords,
        }

        self.root.ids.products_box.clear_widgets()

        try:
            response = requests.get('http://127.0.0.1:5000/products', params=params)
            if response.status_code == 200:
                for product in response.json():
                    card = ProductCard(product)
                    self.root.ids.products_box.add_widget(card)
            else:
                print(f"Ошибка сервера: {response.status_code}")
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")

if __name__ == "__main__":
    MainApp().run()

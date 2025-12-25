from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader


class Proton2App(App):

    def build(self):
        self.sound = None

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.title_label = Label(
            text="质子 2 号 · 基础版",
            font_size=28,
            size_hint=(1, 0.25)
        )
        layout.add_widget(self.title_label)

        self.btn_a = Button(
            text="按钮一",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_a.bind(on_press=self.on_btn_a)
        layout.add_widget(self.btn_a)

        self.btn_b = Button(
            text="按钮二",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_b.bind(on_press=self.on_btn_b)
        layout.add_widget(self.btn_b)
self.btn_c = Button(
            text="按钮三",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_c.bind(on_press=self.on_btn_c)
        layout.add_widget(self.btn_c)

        return layout

    # —— 下面是占位功能（不会闪退） ——

    def _play_sound(self, file):
        try:
            if self.sound:
                self.sound.stop()
            self.sound = SoundLoader.load(file)
            if self.sound:
                self.sound.play()
        except Exception:
            pass

    def on_btn_a(self, *args):
        self.title_label.text = "按钮一：功能占位"

    def on_btn_b(self, *args):
        self.title_label.text = "按钮二：功能占位"

    def on_btn_c(self, *args):
        self.title_label.text = "按钮三：功能占位"


if __name__ == "__main__":
    Proton2App().run()

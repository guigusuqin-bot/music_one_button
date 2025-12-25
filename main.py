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

        # 顶部标题
        self.title_label = Label(
            text="质子 2 号 · 基础版",
            font_size=28,
            size_hint=(1, 0.25)
        )
        layout.add_widget(self.title_label)

        # 按钮一
        self.btn_a = Button(
            text="按钮一",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_a.bind(on_press=self.on_btn_a)
        layout.add_widget(self.btn_a)

        # 按钮二
        self.btn_b = Button(
            text="按钮二",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_b.bind(on_press=self.on_btn_b)
        layout.add_widget(self.btn_b)

        # 按钮三
        self.btn_c = Button(
            text="按钮三",
            font_size=22,
            size_hint=(1, 0.25)
        )
        self.btn_c.bind(on_press=self.on_btn_c)
        layout.add_widget(self.btn_c)

        return layout

    # —— 占位功能（保证不闪退） ——
    def _play_sound(self, file_path: str):
        """占位音频函数：目前不用也不会影响构建。"""
        try:
            if self.sound:
                self.sound.stop()
            self.sound = SoundLoader.load(file_path)
            if self.sound:
                self.sound.play()
        except Exception:
            # 捕获一切异常，防止因为音频问题闪退
            pass

    def on_btn_a(self, *args):
        self.title_label.text = "按钮一：功能占位"

    def on_btn_b(self, *args):
        self.title_label.text = "按钮二：功能占位"

    def on_btn_c(self, *args):
        self.title_label.text = "按钮三：功能占位"


if __name__ == "__main__":
    Proton2App().run()

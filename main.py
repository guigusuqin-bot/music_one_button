from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
import os


class MainUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 路径（相对 main.py / 项目根）
        self.bg_path = os.path.join("assets", "bg", "1.png")
        self.music_path = os.path.join("assets", "music", "music1.mp3")
        self.text_path = os.path.join("assets", "text", "1.txt")
        self.font_path = "NotoSansSC-VariableFont_wght.ttf"

        # 注册中文字体（Android/打包后不要用 exists 判断，直接 try）
        self.font_name = None
        try:
            LabelBase.register(name="CN", fn_regular=self.font_path)
            self.font_name = "CN"
        except Exception:
            self.font_name = None

        # 背景图
        self.bg = Image(source=self.bg_path, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        # 文本
        self.label = Label(
            text=self.load_text(),
            size_hint=(1, None),
            height="120dp",
            pos_hint={"x": 0, "y": 0.72},
            halign="center",
            valign="middle",
            font_name=self.font_name if self.font_name else None,
            font_size="22sp",
        )
        self.label.bind(size=self._update_text_size)
        self.add_widget(self.label)

        # 音乐（不自动播放；打包后不要用 exists 判断，直接 try load）
        self.sound = None
        try:
            self.sound = SoundLoader.load(self.music_path)
        except Exception:
            self.sound = None

        # 按钮：播放/停止
        self.btn = Button(
            text="播放/停止",
            size_hint=(0.6, 0.12),
            pos_hint={"center_x": 0.5, "y": 0.12},
        )
        self.btn.bind(on_press=self.toggle_music)
        self.add_widget(self.btn)

    def _update_text_size(self, *args):
        self.label.text_size = (self.label.width, None)
        self.label.texture_update()

    def load_text(self):
        try:
            with open(self.text_path, "r", encoding="utf-8") as f:
                return f.read().strip() or "（空文本）"
        except Exception:
            return "（未找到 1.txt 或编码错误）"

    def toggle_music(self, *args):
        if not self.sound:
            self.btn.text = "找不到 music1.mp3"
            return

        if self.sound.state == "play":
            self.sound.stop()
        else:
            self.sound.play()


class MyApp(App):
    def build(self):
        return MainUI()


if __name__ == "__main__":
    MyApp().run()

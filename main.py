from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
import os


class MusicApp(App):
    def build(self):
        # 注册中文字体（如果没放字体文件，不会崩溃，只是可能显示方块）
        if os.path.exists("NotoSansSC-Regular.otf"):
            LabelBase.register(name="NotoSansSC", fn_regular="NotoSansSC-Regular.otf")
            font_name = "NotoSansSC"
        else:
            font_name = None

        self.idx = 0
        self.sound = None

        root = FloatLayout()

        # 背景图（默认黑底；如果有 b1.png 会显示 b1）
        self.bg = Image(allow_stretch=True, keep_ratio=False)
        root.add_widget(self.bg)

        self.btn = Button(
            text="切歌",
            font_name=font_name if font_name else "",
            font_size=40,
            size_hint=(0.6, 0.18),
            pos_hint={"center_x": 0.5, "center_y": 0.15},
        )
        self.btn.bind(on_press=self.next_track)
        root.add_widget(self.btn)

        # 启动不自动播放：这里只设置初始背景，不播放音频
        self.update_background_only()
        return root

    def tracks_count(self):
        # 以 m1.mp3, m2.mp3... 为准，连续计数
        n = 0
        i = 1
        while True:
            if os.path.exists(f"m{i}.mp3") and os.path.exists(f"b{i}.png"):
                n += 1
                i += 1
            else:
                break
        return n

    def update_background_only(self):
        # 如果 b1.png 存在，显示对应背景，否则保持黑底
        bg_path = f"b{self.idx + 1}.png"
        if os.path.exists(bg_path):
            self.bg.source = bg_path
            self.bg.reload()

    def next_track(self, _):
        # 点击才切歌/播放；禁止任何自动播放
        count = self.tracks_count()
        if count <= 0:
            print("❌ 未找到成对资源：m1.mp3 + b1.png（以及后续 m2/b2 ...）")
            return

        # 停止上一首
        if self.sound:
            self.sound.stop()
            self.sound = None

        # 前进索引
        self.idx = (self.idx + 1) % count

        # 切背景
        bg_path = f"b{self.idx + 1}.png"
        self.bg.source = bg_path
        self.bg.reload()

        # 播放当前
        mp3_path = f"m{self.idx + 1}.mp3"
        self.sound = SoundLoader.load(mp3_path)
        if not self.sound:
            print(f"❌ 音频加载失败：{mp3_path}")
            return
        self.sound.play()


if __name__ == "__main__":
    MusicApp().run()

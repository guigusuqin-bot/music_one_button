import os

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button


class OneButtonMusicApp(App):
    def build(self):
        self.title = "music_one_button"

        # 统一资源路径
        base = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(base, "assets", "music")
        self.bg_dir = os.path.join(base, "assets", "bg")
        self.text_dir = os.path.join(base, "assets", "text")

        # 扫描可用“编号集合”
        self.ids = self._scan_available_ids()
        self.idx = -1  # 当前索引（-1表示还没开始）

        # UI
        root = FloatLayout()

        # 背景图（先给默认纯色占位：不崩）
        self.bg = Image(
            source="",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        root.add_widget(self.bg)

        # 叠加文字（中文直接用系统字体，不需要装字体）
        self.text_label = Label(
            text="按【切歌】开始",
            font_size="28sp",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            halign="center",
            valign="middle",
        )
        # 让 halign/valign 生效
        self.text_label.bind(size=self._sync_label_text_size)
        root.add_widget(self.text_label)

        # 唯一按钮：切歌
        self.btn = Button(
            text="切歌",
            font_size="30sp",
            size_hint=(0.6, 0.12),
            pos_hint={"center_x": 0.5, "y": 0.08},
        )
        self.btn.bind(on_press=self.on_next)
        root.add_widget(self.btn)

        # 音频对象
        self.sound = None

        # 如果资源为空，给提示但不崩
        if not self.ids:
            self.text_label.text = "assets 里没找到可用资源\n请放入 music/bg/text 并用 1、2、3 编号配对"
            self.btn.disabled = True

        return root

    def _sync_label_text_size(self, *_):
        self.text_label.text_size = self.text_label.size

    def _scan_available_ids(self):
        def list_ids(folder, exts):
            if not os.path.isdir(folder):
                return set()
            out = set()
            for name in os.listdir(folder):
                lower = name.lower()
                for ext in exts:
                    if lower.endswith(ext):
                        stem = os.path.splitext(name)[0]
                        if stem.isdigit():
                            out.add(int(stem))
                        break
            return out

        music_ids = list_ids(self.music_dir, (".mp3", ".wav", ".ogg"))
        bg_ids = list_ids(self.bg_dir, (".png", ".jpg", ".jpeg"))
        text_ids = list_ids(self.text_dir, (".txt",))

        # 取三者交集：保证每一组都有 music + bg + text
        common = sorted(list(music_ids & bg_ids & text_ids))
        return common

    def on_next(self, *_):
        if not self.ids:
            return

        # 切到下一组
        self.idx = (self.idx + 1) % len(self.ids)
        cur_id = self.ids[self.idx]

        music_path = os.path.join(self.music_dir, f"{cur_id}.mp3")
        if not os.path.exists(music_path):
            # 兜底：如果不是 mp3，尝试 wav/ogg
            for ext in (".wav", ".ogg"):
                p = os.path.join(self.music_dir, f"{cur_id}{ext}")
                if os.path.exists(p):
                    music_path = p
                    break

        bg_path = ""
        for ext in (".png", ".jpg", ".jpeg"):
            p = os.path.join(self.bg_dir, f"{cur_id}{ext}")
            if os.path.exists(p):
                bg_path = p
                break

        text_path = os.path.join(self.text_dir, f"{cur_id}.txt")

        # 1) 更新背景图（先验证可读，避免 Android 上偶发崩）
        if bg_path:
            try:
                CoreImage(bg_path)  # 验证图片可加载
                self.bg.source = bg_path
                self.bg.reload()
            except Exception:
                self.text_label.text = f"背景图加载失败：{cur_id}"
                # 背景失败不影响音乐

        # 2) 更新文字
        if os.path.exists(text_path):
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    txt = f.read().strip()
                self.text_label.text = txt if txt else f"第 {cur_id} 组"
            except Exception:
                self.text_label.text = f"文字读取失败：{cur_id}"
        else:
            self.text_label.text = f"第 {cur_id} 组"

        # 3) 播放音乐（重要：只在按按钮时播放；先停旧的）
        try:
            if self.sound:
                self.sound.stop()
                self.sound.unload()
                self.sound = None

            self.sound = SoundLoader.load(music_path)
            if self.sound:
                self.sound.play()
            else:
                self.text_label.text = f"音乐加载失败：{cur_id}"
        except Exception:
            self.text_label.text = f"播放失败：{cur_id}"


if __name__ == "__main__":
    OneButtonMusicApp().run()

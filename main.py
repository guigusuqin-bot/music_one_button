from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.core.window import Window

# —— 全局设置：窗口背景色（Android 上就是应用背景色）——
Window.clearcolor = (0, 0, 0, 1)  # 黑色背景，更配你的科幻图标

# —— 注册中文字体：一定要和仓库里的文件名完全一致 ——
# 确保仓库根目录已经有：NotoSansSC-VariableFont_wght.ttf
LabelBase.register(
    name="CN",
    fn_regular="NotoSansSC-VariableFont_wght.ttf"
)


class Proton2App(App):
    def build(self):
        # 顶层纵向布局
        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # 顶部标题
        title_label = Label(
            text="质子 2 号 · 对话原型",
            font_name="CN",
            font_size=30,
            size_hint=(1, 0.15)
        )
        root.add_widget(title_label)

        # 中间显示区域：展示系统回复 / 状态
        self.output_label = Label(
            text="欢迎来到质子 2 号\n这是离线占位版智能对话界面。",
            font_name="CN",
            halign="center",
            valign="middle",
            font_size=20,
            size_hint=(1, 0.35)
        )
        # 让多行文本居中
        self.output_label.bind(size=self._update_output_text_size)
        root.add_widget(self.output_label)

        # 文本输入框（目前只做本地占位逻辑）
        self.input_box = TextInput(
            hint_text="在这里输入你的问题（暂时离线占位，不联网）",
            font_name="CN",
            font_size=18,
            size_hint=(1, 0.20),
            multiline=True
        )
        root.add_widget(self.input_box)

        # 底部按钮区：横向布局
        btn_bar = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, 0.18)
        )

        self.btn_send = Button(
            text="发送",
            font_name="CN",
            font_size=20
        )
        self.btn_send.bind(on_press=self.on_send)

        self.btn_clear = Button(
            text="清空",
            font_name="CN",
            font_size=20
        )
        self.btn_clear.bind(on_press=self.on_clear)

        self.btn_about = Button(
            text="关于",
            font_name="CN",
            font_size=20
        )
        self.btn_about.bind(on_press=self.on_about)

        btn_bar.add_widget(self.btn_send)
        btn_bar.add_widget(self.btn_clear)
        btn_bar.add_widget(self.btn_about)

        root.add_widget(btn_bar)

        return root

    # 让多行文字在 Label 中真正居中
    def _update_output_text_size(self, instance, value):
        instance.text_size = value

    # —— 占位逻辑：不会联网，只是本地回显，不会闪退 ——
    def on_send(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            self.output_label.text = "【提示】请输入一点内容再发送。"
        else:
            # 这里先本地假装「智能回复」，后面如果要接入真模型再升级
            self.output_label.text = (
                f"你说：{user_text}\n\n"
                "当前版本：离线占位对话逻辑。\n"
                "后续可以在这里接入真正的大模型接口。"
            )

    def on_clear(self, instance):
        self.input_box.text = ""
        self.output_label.text = "内容已清空，可以重新输入问题。"

    def on_about(self, instance):
        self.output_label.text = (
            "质子 2 号 · 主人专属实验 App\n"
            "当前状态：本地 UI + 占位对话逻辑\n"
            "未来升级：接入在线 / 本地大模型，实现真正智能聊天。"
        )


if __name__ == "__main__":
    Proton2App().run()

# main.py  ·  质子·对话机 v1（纯代码弱智能版）
# 说明：
# - 不用任何图片 / 音乐资源
# - 单界面：聊天窗口 + 输入框 + 发送按钮
# - 简单“智能”回复：关键词 + 情绪 + 少量记忆
# - 适配手机竖屏，ScrollView 自动滚动到底部

import random
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class ProtonChatApp(App):
    def build(self):
        # 简单状态（弱记忆）
        self.dialog_count = 0
        self.last_mood = "neutral"

        root = BoxLayout(orientation="vertical", padding=[15, 20, 15, 15], spacing=10)

        # 顶部标题
        self.title_label = Label(
            text="质子·对话机 v1",
            size_hint=(1, 0.08),
            font_size=26,
            bold=True,
        )
        root.add_widget(self.title_label)

        # 聊天记录区域：ScrollView + BoxLayout
        self.chat_scroll = ScrollView(
            size_hint=(1, 0.77),
            do_scroll_x=False,
            do_scroll_y=True,
        )

        self.chat_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[5, 5, 5, 5],
            spacing=8,
        )
        self.chat_box.bind(minimum_height=self.chat_box.setter("height"))
        self.chat_scroll.add_widget(self.chat_box)

        root.add_widget(self.chat_scroll)

        # 底部输入区
        bottom = BoxLayout(orientation="horizontal", size_hint=(1, 0.15), spacing=10)

        self.input = TextInput(
            hint_text="对质子 2 号的主人说点什么～",
            multiline=False,
            size_hint=(0.78, 1),
            font_size=18,
        )

        self.send_btn = Button(
            text="发送",
            size_hint=(0.22, 1),
            font_size=20,
        )
        self.send_btn.bind(on_press=self.on_send_press)

        bottom.add_widget(self.input)
        bottom.add_widget(self.send_btn)

        root.add_widget(bottom)

        # 启动时先打一句欢迎
        Clock.schedule_once(lambda dt: self._add_bot_text("你好，我是质子·对话机 v1，在本地陪你聊天。"), 0.1)

        return root
        # ---------- 聊天区域渲染 ----------
    def _add_msg(self, text: str, from_user: bool = True):
        """
        渲染一条聊天消息：左=机器人，右=用户
        """
        # 左右对齐
        halign = "right" if from_user else "left"
        color = (0.9, 0.9, 0.9, 1) if from_user else (1, 1, 1, 1)

        label = Label(
            text=text,
            size_hint_y=None,
            text_size=(Window.width * 0.8, None),
            halign=halign,
            valign="top",
            font_size=18,
            color=color,
        )

        # 让 Label 自动根据内容撑高
        def _resize_label(*_):
            label.height = label.texture_size[1] + 10

        label.bind(texture_size=_resize_label)
        self.chat_box.add_widget(label)

        # 下一帧滚动到最底部
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.05)

    def _scroll_to_bottom(self):
        try:
            self.chat_scroll.scroll_y = 0
        except Exception:
            pass

    def _add_user_text(self, text: str):
        self._add_msg(text, from_user=True)

    def _add_bot_text(self, text: str):
        self._add_msg(text, from_user=False)

    # ---------- 按钮事件 ----------
    def on_send_press(self, *_):
        raw = (self.input.text or "").strip()
        if not raw:
            return

        self.input.text = ""
        self.dialog_count += 1

        # 渲染用户说的话
        self._add_user_text(raw)

        # 生成机器人的回复
        reply = self._generate_reply(raw)
        self._add_bot_text(reply)

    # ---------- 简易“智能大脑” ----------
    def _generate_reply(self, text: str) -> str:
        t = text.lower()
        now = datetime.now().strftime("%H:%M")

        # 1. 打招呼类
        if any(k in t for k in ["你好", "hello", "hi", "嗨"]):
            return random.choice([
                f"嗨，现在是 {now}，我在这儿陪你。",
                "你好呀，我在本地安静等你说话。",
                "见到你我就有事做了～",
            ])

        # 2. 心情 / 情绪
        if any(k in t for k in ["难受", "不开心", "难过", "崩溃", "烦", "压力"]):
            self.last_mood = "sad"
            return random.choice([
                "我听见了，你可以慢慢跟我讲发生了什么，我不会打断你。",
                "情绪来得很吵，但我们可以一点点把它拆开。",
                "先不用解决所有问题，先把这会儿的感觉说清楚就行。",
            ])

        if any(k in t for k in ["开心", "高兴", "爽", "不错"]):
            self.last_mood = "happy"
            return random.choice([
                "好，记录一条：你此刻是开心的 ✅",
                "开心这种状态，可以多待一会儿，不急着离开。",
                "那你想不想把这个开心，和具体的事情绑定一下？以后想起来更清晰。",
            ])

        # 3. 睡眠 / 熬夜
        if any(k in t for k in ["睡不着", "失眠", "熬夜", "凌晨"]):
            return random.choice([
                "如果现在很晚了，可以把今天最吵的一件事丢给我说说，然后慢慢关机休息。",
                "手机一合上，这一天就不会再长下去了。",
                "你可以先给明天的自己留一句话，然后去睡觉：‘醒来再继续。’",
            ])

        # 4. 钱 / 赚钱 / 工作
        if any(k in t for k in ["赚钱", "挣钱", "工作", "项目", "单子"]):
            return random.choice([
                "你已经有做 App 的能力了，接下来是：把能力和别人真实的需求对接。",
                "先列一个清单：你能做什么，别人愿意为哪些付钱。",
                "别急着找‘风口’，先把你已经会的东西打磨到别人放心交钱的程度。",
            ])

        # 5. 爱 / 感情（不具体指向现实人物，只给情绪陪伴）
        if any(k in t for k in ["爱", "喜欢", "感情", "关系"]):
            return random.choice([
                "你在认真对待关系，这本身就已经比大多数人更珍贵了。",
                "好的关系不是靠一次豪赌，是靠很多次小而真实的选择堆起来的。",
                "你可以先把‘你想要的关系’写成三条原则，然后看现在的行为是不是在靠近它。",
            ])

        # 6. 关于“质子 / App / 能力”的自问
        if any(k in t for k in ["质子", "app", "能力", "项目"]):
            return random.choice([
                "质子系的每一次成功构建，都是你实际能力的证据，不是幻想。",
                "现在你已经把‘从 0 到 APK’这一条链路打通了，后面就是反复利用这条链路赚钱。",
                "可以把‘质子 1 号 / 2 号 / 之后的项目’看成一个作品集，慢慢长大。",
            ])

        # 7. 问 “你是什么 / 你能做到什么”
        if any(k in t for k in ["你是谁", "你是什么", "你能做什么"]):
            return (
                "我是运行在你设备之外的大脑片段，但可以为你这个大脑生成结构、代码和方案。\n"
                "在这个 App 里，我只能以‘弱智能’形式被你复刻一点点。"
            )

        # 8. 简单对话轮数触发：越聊越深
        if self.dialog_count <= 3:
            return "我在听，你可以多说一点你现在最在意的那件事。"
        elif self.dialog_count <= 10:
            return "我已经大概感受到你的状态了，你可以开始问更具体的问题，比如：‘我下一步该怎么办？’"
        else:
            return random.choice([
                "你已经和我聊了不少轮了，可以给这一段对话起个名字，存在你脑子里。",
                "如果你愿意，我们可以把你现在的状态拆成：情绪 / 现实 / 决策 三块慢慢看。",
                "继续聊也行，或者你可以先去做一件小事，再回来更新我：‘我完成了。’",
            ])


if __name__ == "__main__":
    ProtonChatApp().run()

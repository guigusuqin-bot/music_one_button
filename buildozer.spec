[app]
title = 质子2号
package.name = snakegame
package.domain = org.example

source.dir = .
source.include_exts = py,mp3,png,ttf

# 为了稳定性锁定 Kivy 版本；如果构建报 Kivy 版本错误，再回来改
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 1

icon.filename = icon.png
presplash.filename =

version = 0.1

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 目前保留 INTERNET，后面如果确定完全不联网可以删除这行
android.permissions = INTERNET

android.accept_sdk_license = True

android.archs = arm64-v8a

# 让 p4a 使用稳定分支，减少莫名其妙升级导致的崩溃
p4a.branch = stable

[buildozer]
log_level = 2
warn_on_root = 0

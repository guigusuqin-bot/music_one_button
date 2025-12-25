[app]
title = 质子2号
package.name = snakegame
package.domain = org.example

source.dir = .
source.include_exts = py,mp3,png,ttf

requirements = python3,kivy

# 🔒 固定使用 python-for-android 的 stable 分支，配合 android.yml 里锁定的版本
p4a.branch = stable

orientation = portrait
fullscreen = 1

icon.filename = icon.png
presplash.filename =

version = 0.1

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.permissions = INTERNET

android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0

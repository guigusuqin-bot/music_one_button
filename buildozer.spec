[app]
title = music_one_button
package.name = music_one_button
package.domain = org.guigu

source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,ttf,txt,keep
source.exclude_exts = spec

version = 0.2

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# 不联网，不要权限（留空）
android.permissions =

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# 稳态：用 p4a 稳定分支
p4a.branch = master 

log_level = 2

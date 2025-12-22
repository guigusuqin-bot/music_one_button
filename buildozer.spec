[app]
title = music_one_button
package.name = music_one_button
package.domain = org.guigu
version = 0.1

source.dir = .
source.include_exts = py,mp3,png,jpg,jpeg,otf,ttf,txt,keep
source.exclude_exts = spec

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# 不联网：留空即可
android.permissions =

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# p4a 稳态
p4a.branch = stable

log_level = 2

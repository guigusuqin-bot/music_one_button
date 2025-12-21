[app]
title = music_one_button
package.name = music_one_button
package.domain = org.guigu

source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,ttf,txt,keep
source.exclude_exts = spec

version = 0.1

requirements = python3,kivy
orientation = portrait

fullscreen = 0

# 你的资源在 assets/ 下面，不需要额外写
# 重要：不联网、不需要权限
android.permissions =

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# 如遇到编译器版本问题再改，这里先保持最稳
p4a.branch = stable

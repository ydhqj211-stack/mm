[app]

title = SMS Watcher
package.name = smswatcher
package.domain = org.smswatcher

version = 1.0.0

requirements = python3,kivy,plyer,requests

orientation = portrait

fullscreen = 0

android.permissions = RECEIVE_SMS,READ_SMS,SEND_SMS

android.archs = arm64-v8a,armeabi-v7a

android.api = 27
android.minapi = 27
android.ndk_api = 21

android.allow_backup = True
android.enable_androidx = True

p4a.bootstrap = sdl2

[buildozer]

log_level = 2

warn_on_root = 1

build_dir = ./build

bin_dir = ./bin
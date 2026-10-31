
[app]

title = Video Studio 97

package.name = videostudio97
package.domain = org.example

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,atlas,json,html,css,js,txt,ttf,otf,mp4,webm

version = 2.0

requirements = python3,kivy,requests,plyer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 23
android.ndk = 28c
android.ndk_api = 23

android.archs = arm64-v8a

android.accept_sdk_license = True


[buildozer]

log_level = 2

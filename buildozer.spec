[app]

# (str) Title of your application
title = Salon Studio Pro

# (str) Package name
package.name = salonstudio

# (str) Package domain (needed for android packaging)
package.domain = com.salon.studio

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,html,css,json

# (str) Application version
version = 1.0

# (list) Application requirements
# pyjnius para acceso nativo a Android WebView
# numpy y pillow para procesamiento de imágenes
requirements = python3, kivy, pyjnius, numpy, pillow, android

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# Permisos para cámara, internet y audio
android.permissions = CAMERA, INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Accept SDK license agreement
android.accept_sdk_license_agreement = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Indicate if the application uses cleartext traffic
android.uses_cleartext_traffic = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

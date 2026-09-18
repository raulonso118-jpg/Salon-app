[app]
title = Salon Studio Pro
package.name = salonstudio
package.domain = com.salon.studio
source.dir = .
version = 1.0

# ⚙️ REQUISITOS: Agregué las extensiones indispensables para que tu HTML y CSS entren al APK
source.include_exts = py,png,jpg,kv,atlas,html,css

# 📦 DEPENDENCIAS: Asegúrate de agregar aquí cualquier otra librería que use tu main.py (ej: flask, requests, etc.)
requirements = python3,kivy,android

orientation = portrait

# 📸 PERMISOS: Vitales para que la cámara del cliente y el lienzo de simulación funcionen en Android
android.permissions = CAMERA, INTERNET, RECORD_AUDIO

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
# Eliminé la línea fija del NDK para que Buildozer descargue automáticamente la versión exacta compatible con la API 33 de forma limpia
android.accept_sdk_license_agreement = True

[app]

# (str) Title of your application
title = Salon Studio Pro

# (str) Package name
package.name = salonstudio

# (str) Package domain (needed for android packaging)
package.domain = com.salon.studio

# (str) Source code where the main.py lives (Corregido con espacio obligatorio)
source.dir = .

# (list) Source files to include (Asegura que tu HTML se guarde dentro del APK)
source.include_exts = py,png,jpg,kv,atlas,html,css

# (str) Application version
version = 1.0

# (list) Application requirements
# 🚀 CRÍTICO: Agregados numpy y pillow para tu procesador de imágenes por matrices
requirements = python3, kivy, numpy, pillow, android

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (list) Permissions
# 📸 CRÍTICO: Permisos necesarios para usar la cámara y simular el rostro en el celular
android.permissions = CAMERA, INTERNET, RECORD_AUDIO

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Accept SDK license agreement if needed
android.accept_sdk_license_agreement = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1

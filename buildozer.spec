[app]
title = Salon Studio Pro
package.name = salonstudio
package.domain = com.salon.studio
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,html
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.permissions = CAMERA,INTERNET
android.api = 33
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license_agreement = True

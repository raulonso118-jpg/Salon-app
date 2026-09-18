[app]
title = Salon Studio Pro
package.name = salonstudio
package.domain = com.salon.studio
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.0
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 24
android.ndk = 26b
android.archs = arm64-v8a
android.accept_sdk_license_agreement = True

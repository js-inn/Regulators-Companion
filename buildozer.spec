[app]
title = Octopus 2.0
package.name = octopus
package.domain = org.octopus
source.dir = .
source.exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3
orientation = portrait
android.api = 34
android.build_tools_version = 34.0.0
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET,NFC
android.features = android.hardware.nfc

[buildozer]
log_level = 2
warn_on_root = 1

p4a.bootstrap = sdl2

[app]
title = Octopus Node
package.name = octopusnode
package.domain = org.octopus
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy,pyjnius
android.permissions = INTERNET, NFC
android.features = android.hardware.nfc
android.manifest.intent_filters = <intent-filter><action android:name="android.nfc.action.TAG_DISCOVERED"/><category android:name="android.intent.category.DEFAULT"/></intent-filter>
orientation = portrait

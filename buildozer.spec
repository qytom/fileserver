[app]

# (str) Title of your application
title = FileServer

# (str) Package name
package.name = fileserver

# (str) Package domain (needed for android/ios packaging)
package.domain = com.fileserver

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
# Do not prefix with ./ or ../
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#
# (str) Path to a custom kivy_ios directory
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
#ios.kivy_ios_branch = master

# (bool) Whether or not to sign the code
#ios.codesign.allowed = false

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray, darkgray,
# grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy, olive, purple, silver, teal
#android.presplash_color = #ffffff

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/ for docs
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
# (See https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options-1 for all the supported permissions)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_WIFI_STATE, MANAGE_EXTERNAL_STORAGE

# (str) Android SDK mirror
android.sdk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Android NDK mirror
android.ndk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Gradle mirror
android.gradle_mirror = https://mirrors.tuna.tsinghua.edu.cn/gradle/

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False, 
# default, you will be shown the license when first running
# buildozer.
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name =

# (str) Extra xml to write directly inside of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml =

# (str) Extra xml to write directly inside of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML arguments:
#android.extra_manifest_application_xml =

# (str) Full name including package path of the Java class that extends Python Service
# use that parameter to set custom Java class which extends PythonService
#android.service_class_name =

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = @android:style/Theme.Holo.Light

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access it
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a directory containing files)
#android.add_src = 

# (list) Android AAR archives to add
#android.add_aars = 

# (list) Put these files or directories in the apk assets directory. 
# Either form may be used, and assets need not be in 'source.include_exts'.
#1) A directory name to add its content
#android.add_assets = directory/path/
#2) A file path
#android.add_assets = source/file.ext

# (list) Put these files or directories in the apk res directory. 
# The option may be used in three ways, and the value may contain one or more comma separated paths:
#1) A directory name to add its content. 
#android.add_resources = directory/path/
#2) A file path, 
#android.add_resources = source/file.ext
#3) A directory path and a target directory name
#android.add_resources = source/directory/path:destination/directory/path

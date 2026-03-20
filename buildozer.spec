[app]

# (str) Title of your application
title = FileServer

# (str) Package name
package.name = fileserver

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

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
# Do not prefix with ./ or /
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

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
orientation = all

# (list) List of services to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

# (str) Path to a custom kivy_ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
#ios.kivy_ios_branch = master

# (int) Target iOS version, should be >= 6.0
#ios.codesign.allowed = false

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names: red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray, darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy, olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/ for general documentation.
# Lottie files can be created using various tools, like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 24

# (str) Android NDK version to use
#android.ndk = 21

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = /home/runner/android-sdk

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path = 

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = @android:style/Theme.Holo.Light

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Path to a custom whitelist file
#android.whitelist_src = 

# (str) Path to a custom blacklist file
#android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process.
#android.add_jars = foo.jar,bar.jar,path/to/more/jars

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src = 

# (list) Android AAR archives to add
#android.add_aars = 

# (list) Gradle dependencies to add
#android.gradle_dependencies = 

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies'
# see https://developer.android.com/studio/write/java8-support for further information
# android.add_compile_options = "-source 1.8", "-target 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes
# android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"

# (list) packaging options to add
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle dependencies
# android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters = 

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the
dependencies section of the build.gradle)
#android.library_references = 

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library = 

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a, arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules = 

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned)
#p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

#
# iOS specific
#

# (str) Path to a custom kivy_ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios
#ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
# Get a list of available certificates: buildozer ios list_certs
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (int) Number of seconds to wait for ios build to complete
# Longer builds may need more time, set to 0 to disable
#ios.build_timeout = 300

# (str) Path to the profile to use for the debug build
#ios.profile.debug = 

# (str) Path to the profile to use for the release build
#ios.profile.release = 

# (str) Path to the certificate to use for signing the debug version
#ios.certificate.debug = 

# (str) Path to the certificate to use for signing the release version
#ios.certificate.release = 

# (str) The development team to use for signing the debug version
#ios.teamid.debug = 

# (str) The development team to use for signing the release version
#ios.teamid.release = 

# (str) Device family to target. Must be one of: iphone, ipad, universal
#ios.device = universal

# (str) Use this section to pass extra args to the actual iOS build tool
#ios.extra_args = 

#
# macOS specific
#

# (str) Path to the certificate to use for signing the debug version
#macos.codesign.debug = 

# (str) Path to the certificate to use for signing the release version
#macos.codesign.release = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.arch = armeabi-v7a

# (int) How much memory to allocate to Gradle in MB
# android.gradle_memory = 2048

# (bool) Gradle cache enabled (0 = False, 1 = True)
# android.gradle_cache = 1

# (str) Android SDK mirror
android.sdk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Android NDK mirror
android.ndk_mirror = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Android Gradle mirror
android.gradle_mirror = https://mirrors.tuna.tsinghua.edu.cn/gradle/

# Trigger new build

# (bool) Use the Buildozer Docker image (auto-detects if docker is available)
# use_docker = False

# (str) The full path to the docker binary.
# docker = /usr/bin/docker

# (str) The Docker image to use.
# docker_image = kivy/buildozer

# (bool) Add --no-site-packages flag to the PIP commands
# no_site_packages = 1

# (bool) If True, then skip trying to update the index of packages
# skip_update = 0

# (str) The tag to use for the docker image
# docker_tag = latest

# (str) The base directory where buildozer stores configuration and intermediate files
# build_root = ~/.buildozer

# (str) The base directory where buildozer stores its cache
# cache_dir = ~/.buildozer/cache

# (str) The default command to run when双击 the icon
# default_command = python -m kivy.app

# (str) Path to the python executable used for buildozer
# python = python3

# (bool) If True, then use the python at python for android builds
# use_python_for_build = True

# (str) The encoding used to read and write files
# encoding = utf-8

# (bool) Use this parameter to enable/disable the PEP8 style checks
# check_pep8 = True

# (bool) If True, then use the pep8 parameter to the python interpreter
# instead of the default pycodestyle
# use_pep8 = True

# (bool) If True, then check for code signing key conflicts
# check_codesign = True

# (bool) If True, then check for aandroid API version conflicts
# check_apk_api = True

# (bool) If True, then check for gradle version conflicts
# check_gradle = True

# (bool) If True, then skip the gradle wrapper download
# skip_gradle_wrapper = True

# (str) Custom requirement specs to use instead of PIP
# requirements_spec = 

# (str) A list of search paths for requirements
# separated by semicolons
# requirements_paths = 

# (str) The path to the build documentation
# build_docs = BUILD docs

# (str) The path to the build specification file
# spec_file = buildozer.spec

# (str) Maximum number of characters used in the version string
# version_max_length = 20

# (int) Number of times to retry the download of a library
# download_retries = 3

# (bool) Use the list of files instead of the folder content
# use_file_list = False

# (str) The path to a directory containing patches
# patches_dir = patches

# (str) The path to a directory containing local sdk
# local_sdk_dir = 

# (str) The path to a directory containing local aar files
# local_aar_dir = 

# (str) The path to a directory containing local lib files
# local_lib_dir = 

# (bool) If True, then the android parts will be compiled with Cython
# android.cython = True

# (bool) If True, then the ios parts will be compiled with Cython
# ios.cython = True

# (bool) If True, then cython files will be generated for the whole project
# cythonize = True

# (str) The path to the cython executable
# cython = cython

# (bool) If True, then python files will be compiled with Cython
# python.cythonize = True

# (bool) If True, then the generated python code will be optimized
# python.optimize = True

# (bool) If True, then the generated python code will be stripped
# python.strip = True

# (bool) If True, then the generated python code will be compressed
# python.compress = True

# (str) The path to the python-for-android directory
# p4a.source_dir = 

# (str) The path to the python-for-android recipes directory
# p4a.recipes_dir = 

# (str) The path to the python-for-android bootstrap directory
# p4a.bootstrap_dir = 

# (str) The path to the python-for-android distribution directory
# p4a.dist_dir = 

# (bool) If True, then the python-for-android distribution will be cleaned
# p4a.clean_dist_dir = False

# (str) The path to the python-for-android build directory
# p4a.build_dir = 

# (bool) If True, then the python-for-android build directory will be cleaned
# p4a.clean_build_dir = False

# (str) The path to the python-for-android virtualenv directory
# p4a.virtualenv_dir = 

# (bool) If True, then the python-for-android virtualenv will be cleaned
# p4a.clean_virtualenv_dir = False

# (str) The path to the python-for-android ndk directory
# p4a.ndk_dir = 

# (str) The path to the python-for-android sdk directory
# p4a.sdk_dir = 

# (str) The path to the python-for-android ant directory
# p4a.ant_dir = 

# (str) The path to the python-for-android tools directory
# p4a.tools_dir = 

# (str) The path to the python-for-android lib directory
# p4a.lib_dir = 

# (str) The path to the python-for-android include directory
# p4a.include_dir = 

# (str) The path to the python-for-android site-packages directory
# p4a.site_packages_dir = 

# (str) The path to the python-for-android dists directory
# p4a.dists_dir = 

# (str) The path to the python-for-android downloads directory
# p4a.downloads_dir = 

# (str) The path to the python-for-android cache directory
# p4a.cache_dir = 

# (str) The path to the python-for-android recipes cache directory
# p4a.recipe_cache_dir = 

# (str) The path to the python-for-android bootstrap cache directory
# p4a.bootstrap_cache_dir = 

# (str) The path to the python-for-android build cache directory
# p4a.build_cache_dir = 

# (str) The path to the python-for-android virtualenv cache directory
# p4a.virtualenv_cache_dir = 

# (str) The path to the python-for-android ndk cache directory
# p4a.ndk_cache_dir = 

# (str) The path to the python-for-android sdk cache directory
# p4a.sdk_cache_dir = 

# (str) The path to the python-for-android ant cache directory
# p4a.ant_cache_dir = 

# (str) The path to the python-for-android tools cache directory
# p4a.tools_cache_dir = 

# (str) The path to the python-for-android lib cache directory
# p4a.lib_cache_dir = 

# (str) The path to the python-for-android include cache directory
# p4a.include_cache_dir = 

# (str) The path to the python-for-android site-packages cache directory
# p4a.site_packages_cache_dir = 

# (str) The path to the python-for-android dists cache directory
# p4a.dists_cache_dir = 

# (str) The path to the python-for-android downloads cache directory
# p4a.downloads_cache_dir = 

# (str) The path to the python-for-android cache directory
# p4a.cache_dir = 

# (str) The path to the python-for-android recipes cache directory
# p4a.recipe_cache_dir = 

# (str) The path to the python-for-android bootstrap cache directory
# p4a.bootstrap_cache_dir = 

# (str) The path to the python-for-android build cache directory
# p4a.build_cache_dir = 

# (str) The path to the python-for-android virtualenv cache directory
# p4a.virtualenv_cache_dir = 

# (str) The path to the python-for-android ndk cache directory
# p4a.ndk_cache_dir = 

# (str) The path to the python-for-android sdk cache directory
# p4a.sdk_cache_dir = 

# (str) The path to the python-for-android ant cache directory
# p4a.ant_cache_dir = 

# (str) The path to the python-for-android tools cache directory
# p4a.tools_cache_dir = 

# (str) The path to the python-for-android lib cache directory
# p4a.lib_cache_dir = 

# (str) The path to the python-for-android include cache directory
# p4a.include_cache_dir = 

# (str) The path to the python-for-android site-packages cache directory
# p4a.site_packages_cache_dir = 

# (str) The path to the python-for-android dists cache directory
# p4a.dists_cache_dir = 

# (str) The path to the python-for-android downloads cache directory
# p4a.downloads_cache_dir = 

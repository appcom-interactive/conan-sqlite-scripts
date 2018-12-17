from conans import ConanFile, CMake, tools
import os

class SQLiteConan(ConanFile):
    name = "sqlite"
    version = "3.26.0"
    author = "Ralph-Gordon Paul (gordon@rgpaul.com)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "android_ndk": "ANY", "android_stl_type":["c++_static", "c++_shared"]}
    default_options = "shared=False", "android_ndk=None", "android_stl_type=c++_static"
    description = "SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine."
    url = "https://github.com/Manromen/conan-sqlite-scripts"
    license = "Public Domain"
    exports_sources = "cmake-modules/*", "CMakeLists.txt"

    def alternateVersion(self):
        splitVersion = self.version.split(".")

        major = splitVersion[0]
        minor = splitVersion[1]
        patch = splitVersion[2]

        if len(minor) == 1:
            minor = '0' + minor

        if len(patch) == 1:
            patch = '0' + patch

        return (major + minor + patch + "00")

    # download sources
    def source(self):
        url = "https://www.sqlite.org/2018/sqlite-amalgamation-%s.zip" % self.alternateVersion()
        tools.get(url)

    # compile using cmake
    def build(self):

        cmake = CMake(self)
        cmake.verbose = True

        cmake.definitions["SQLITE3_VERSION"] = self.alternateVersion()

        if self.settings.os == "Android":
            cmake.definitions["CMAKE_SYSTEM_VERSION"] = self.settings.os.api_level
            cmake.definitions["CMAKE_ANDROID_NDK"] = os.environ["ANDROID_NDK_PATH"]
            cmake.definitions["CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION"] = self.settings.compiler
            cmake.definitions["CMAKE_ANDROID_STL_TYPE"] = self.options.android_stl_type

        if self.settings.os == "iOS":
            ios_toolchain = "cmake-modules/Toolchains/ios.toolchain.cmake"
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = ios_toolchain
            if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                cmake.definitions["IOS_PLATFORM"] = "SIMULATOR"
            else:
                cmake.definitions["IOS_PLATFORM"] = "OS"

        if self.settings.os == "Macos":
            cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = tools.to_apple_arch(self.settings.arch)

        cmake.configure()
        cmake.build()
        cmake.install()

        lib_dir = os.path.join(self.package_folder,"lib")

        if self.settings.os == "iOS":
            # delete shared artifacts for static builds and the static library for shared builds
            if self.options.shared == False:
                for f in os.listdir(lib_dir):
                    if f.endswith(".a") and os.path.isfile(os.path.join(lib_dir,f)) and not os.path.islink(os.path.join(lib_dir,f)):
                        self.run("xcrun ranlib %s" % os.path.join(lib_dir,f))
                        # thin the library (remove all other archs)
                        self.run("lipo -extract %s %s -output %s" % (tools.to_apple_arch(self.settings.arch), os.path.join(lib_dir,f), os.path.join(lib_dir,f)))
            else:
                # thin the library (remove all other archs)
                for f in os.listdir(lib_dir):
                    if f.endswith(".dylib") and os.path.isfile(os.path.join(lib_dir,f)) and not os.path.islink(os.path.join(lib_dir,f)):
                        self.run("lipo -extract %s %s -output %s" % (tools.to_apple_arch(self.settings.arch), os.path.join(lib_dir,f), os.path.join(lib_dir,f)))

    def package(self):
        self.copy("*", dst="include", src='include')
        self.copy("*.lib", dst="lib", src='lib', keep_path=False)
        self.copy("*.dll", dst="bin", src='bin', keep_path=False)
        self.copy("*.so", dst="lib", src='lib', keep_path=False)
        self.copy("*.dylib", dst="lib", src='lib', keep_path=False)
        self.copy("*.a", dst="lib", src='lib', keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']

    def config_options(self):
        # remove android specific option for all other platforms
        if self.settings.os != "Android":
            del self.options.android_ndk
            del self.options.android_stl_type

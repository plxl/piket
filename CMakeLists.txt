cmake_minimum_required(VERSION 3.15)
project(piket LANGUAGES C)

# using "nedcenc" and "nevpk" from https://github.com/plxl/nedclib/blob/master/CMakeLists.txt requires BUILD_TOOLS=ON
set(BUILD_TOOLS ON CACHE BOOL "Build command-line tools" FORCE)

# fetch nedclib from git
include(FetchContent)
FetchContent_Declare(
  nedclib
  GIT_REPOSITORY https://github.com/plxl/nedclib.git
  GIT_TAG c239fd918af49594c080075769fd5cb3c5d0ba85
)
FetchContent_MakeAvailable(nedclib)

# set executables to find library next them
set_target_properties(nedclib nedcenc nevpk PROPERTIES
  BUILD_RPATH "$ORIGIN"
  INSTALL_RPATH "$ORIGIN"
)

# use the folder name within packages "src/piket/bin" for now
if(WIN32)
  set(PLATFORM "windows-amd64")
elseif(APPLE)
  set(PLATFORM "macos-universal")
else()
  set(PLATFORM "linux-amd64")
endif()
set(_install_location piket/bin/${PLATFORM})

# install binaries - build output: "piket/build/_deps/nedclib-build/"
install(PROGRAMS
    "${nedclib_BINARY_DIR}/nedcenc"
    "${nedclib_BINARY_DIR}/nevpk"
    DESTINATION ${_install_location}
)

# install libraries - build output: "piket/build/"
install(TARGETS nedclib
    LIBRARY DESTINATION ${_install_location}
    RUNTIME DESTINATION ${_install_location}
)

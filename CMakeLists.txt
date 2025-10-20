cmake_minimum_required(VERSION 3.15)
project(piket LANGUAGES C)

# using "nedcenc" and "nevpk" from https://github.com/plxl/nedclib/blob/master/CMakeLists.txt requires BUILD_TOOLS=ON
set(BUILD_TOOLS ON CACHE BOOL "Build command-line tools" FORCE)

# use the folder name within packages "src/piket/bin" for now
if(WIN32)
  set(PLATFORM "windows-amd64")
elseif(APPLE)
  set(PLATFORM "macos-universal")
else()
  set(PLATFORM "linux-amd64")
endif()

# library will be next to the executables
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "$ORIGIN")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

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

# located in "piket/build/"
file(GLOB _required_libs "${piket_BINARY_DIR}/libnedclib.*")
foreach(lib IN LISTS _required_libs)
message("found library: ${lib}")
endforeach()

# located in "piket/build/_deps/nedclib-build/"
set(_required_bins
  "${nedclib_BINARY_DIR}/nedcenc"
  "${nedclib_BINARY_DIR}/nevpk"
)
foreach(bin IN LISTS _required_bins)
    message("found binary: ${bin}")
endforeach()

# install things
set(_install_location piket/bin/${PLATFORM})
file(MAKE_DIRECTORY ${_install_location})
install(FILES ${_required_libs} DESTINATION ${_install_location})
install(PROGRAMS ${_required_bins} DESTINATION ${_install_location})

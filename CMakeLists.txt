cmake_minimum_required(VERSION 3.15)
project(piket LANGUAGES C)

# using "nedcenc" and "nevpk" from https://github.com/plxl/nedclib/blob/master/CMakeLists.txt requires BUILD_TOOLS=ON
set(BUILD_TOOLS ON CACHE BOOL "Build command-line tools" FORCE)

# fetch nedclib from git
include(FetchContent)
FetchContent_Declare(
  nedclib
  GIT_REPOSITORY https://github.com/plxl/nedclib.git
  GIT_TAG master # TODO: pin this
)
FetchContent_MakeAvailable(nedclib)

# set executables to find library next them
set_target_properties(nedclib nedcenc nevpk PROPERTIES
  BUILD_RPATH "$ORIGIN"
  INSTALL_RPATH "$ORIGIN"
)

set(_install_location piket/bin)

# install stuff
install(TARGETS nedclib nedcenc nevpk
    LIBRARY DESTINATION ${_install_location}
    RUNTIME DESTINATION ${_install_location}
)

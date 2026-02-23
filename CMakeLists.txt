cmake_minimum_required(VERSION 3.20)
project(data-structures-multi-compiler C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(USE_LLVM "Use LLVM/Clang instead of GNU GCC" OFF)
option(TARGET_ARM64 "Target ARM64 architecture" OFF)
option(TARGET_X86_64 "Target x86_64 architecture" OFF)
option(BUILD_SHARED_LIBS "Build shared libraries" ON)

if(USE_LLVM)
    set(CMAKE_C_COMPILER clang)
    set(CMAKE_CXX_COMPILER clang++)
else()
    set(CMAKE_C_COMPILER gcc)
    set(CMAKE_CXX_COMPILER g++)
endif()

if(TARGET_ARM64)
    set(CMAKE_SYSTEM_PROCESSOR aarch64)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -target aarch64-linux-gnu")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -target aarch64-linux-gnu")
elseif(TARGET_X86_64)
    set(CMAKE_SYSTEM_PROCESSOR x86_64)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -target x86_64-linux-gnu")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -target x86_64-linux-gnu")
endif()

set(CMAKE_C_FLAGS_DEBUG "-g -O0")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

add_subdirectory(src/compilers)

install(DIRECTORY include/ DESTINATION include)

cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(inOneWeekend)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(
    SYSTEM ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/include
)

link_directories(
    SYSTEM ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/lib
)
# 添加源文件
set(SOURCES
    main.cpp
    glad.c
)

# 添加可执行文件
add_executable(inOneWeekend ${SOURCES})

target_link_libraries(inOneWeekend glfw3.lib)
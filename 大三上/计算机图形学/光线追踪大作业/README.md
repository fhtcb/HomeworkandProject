# 光线追踪大作业
[冯海桐-522031910557]
## 文件结构
主要文件结构如下：
```
冯海桐-522031910557
├─GPU加速
│  ├─build
│  │  └─Release
│  │     └─main.exe
│  ├─HDR
│  ├─lib
│  ├─models
│  ├─shaders
│  ├─CMakeLists.txt
│  └─main.cpp
├─基本光线追踪
│  ├─build
│  │  └─Release
│  │     └─inOneWeekend.exe
│  ├─external
│  ├─CMakeLists.txt
│  ├─main.cpp
│  └─其他头文件
├─基本光线追踪效果图
└─GPU加速.mp4
```
`基本光线追踪`文件夹内是参考[《Ray Tracing in One Weekend》](https://raytracing.github.io/books/RayTracingInOneWeekend.html)实现的 CPU 光线追踪，其成果图在`基本光线追踪效果图`当中。

`GPU加速`文件夹内是参考 https://github.com/AKGWSB/EzRT 实现的基于 OpenGL 的 CPU 光线追踪，其演示视频在`GPU加速.mp4`当中。

## 使用方式
### 基本光线追踪
进入`基本光线追踪`文件夹，在命令行中输入：
```
.\build\Release\inOneWeekend.exe > image.ppm
```
即可在当前文件夹生成 ppm 图片，其效果应该与`基本光线追踪效果图`下的`chaos_balls.ppm`一致。
### GPU加速
进入`GPU加速`文件夹，在命令行中输入：
```
.\build\Release\main.exe
```
即可生成与演示视频一样的效果。
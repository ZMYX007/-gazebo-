# ROS Industrial Vision Pick-and-Place Demo

基于 ROS Noetic + Gazebo + MoveIt + OpenCV 的工业视觉引导抓取仿真项目。

## 功能
- 启动 UR5 机械臂在 Gazebo 中的仿真环境
- 通过固定 RGB 相机获取图像，利用 HSV 颜色空间定位红色方块
- 使用 OpenCV 进行图像处理，计算三维坐标
- MoveIt 运动规划避开桌面碰撞，控制机械臂移动到目标上方

## 文件结构
- `launch/pick_demo.launch`：主启动文件
- `src/detect_block.py`：视觉检测节点
- `src/vision_pick.py`：抓取执行脚本
- `worlds/pick_demo.world`：Gazebo 仿真世界

## 快速启动
```bash
roslaunch pick_vision pick_demo.launch
# 在另一个终端
rosrun pick_vision vision_pick.py

## 环境

 Ubuntu 20.04
 ROS Noetic
 OpenCV 3/4
 Gazebo 9.19

English| [简体中文](./README_cn.md)

# Feature Introduction

Line following task, that is, the robot car can autonomously follow a guiding line to move forward. When the guiding line goes left, the car turns left; when the guiding line goes right, the car turns right. This task is a basic task for wheeled robots, and there are multiple ways to achieve it, such as:

- By installing multiple photoelectric sensors (gray sensors), judging whether the sensor is on the line based on the sensor's return value, and then adjusting the robot's movement direction.
- By using a camera to obtain the position of the line in the image based on traditional image processing methods such as edge detection, and then adjusting the robot's movement direction.

The above common methods need to repeatedly adjust the threshold values by collecting images and conducting tests to achieve better recognition results when the lighting environment and the site change. Is it possible to make the robot adapt to environmental changes on its own without the need for manual threshold adjustments? Convolutional Neural Networks (CNN) is one of the most successful applications of deep learning algorithms, with good adaptability and robustness. With the rapid development of processors in recent years, CNN inference can now be performed on embedded devices. Here, CNN is used to realize the perception of the position of the guiding line in the line following task.

# Bill of Materials

The following robots are all compatible with RDK X3

| Robot Name           | Manufacturer | Reference Link                                               |
| :------------------- | ----------- | ------------------------------------------------------------ |
| OriginBot Smart Robot | Guyuehome       | [Click here](https://www.originbot.org/)                     |
| X3 Robo              | Lunqu       | [Click here](https://item.taobao.com/item.htm?spm=a230r.1.14.17.55e556912LPGGx&id=676436236906&ns=1&abbucket=12#detail) |
| Tracked Smart Car     | Waveshare   | [Click here](https://detail.tmall.com/item.htm?abbucket=9&id=696078152772&rn=4d81bea40d392509d4a5153fb2c65a35&spm=a1z10.5-b-s.w4011-22714387486.159.12d33742lJtqRk) |
| RDK X3 Robot         | Yabo Intelligent | [Click here](https://detail.tmall.com/item.htm?id=726857243156&scene=taobao_shop&spm=a1z10.1-b-s.w5003-22651379998.21.421044e12Yqrjm) |

# Instructions for Use

## Preparation

1. The robot has a motion chassis, camera, and RDK kit, with hardware already connected and tested;
2. ROS lower-level drivers are available, and the robot can receive "/cmd_vel" instructions for movement and move correctly based on the instructions.

## Robot Assembly
The following operating process takes OriginBot as an example, and the methods of use for other robots meeting the conditions are similar. Refer to the robot's official website's [user guide](https://www.originbot.org/guide/quick_guide/), complete the hardware assembly, image burning, and sample running of the robot, and confirm that the basic functions of the robot can run smoothly.

## Compile and Run
**1. Refer to [OriginBot instructions](https://github.com/nodehubs/originbot_minimal/blob/develop/README.md) to complete the installation of OriginBot basic functions**

**2. Compile**

After starting the robot, connect to the robot via SSH or VNC in the terminal, click the "One-click Deployment" button at the top right of this page, copy and run the following commands on the RDK system to install the relevant Nodes.

```bash
# Pull the code
mkdir -p ~/line_follower_ws/src && cd ~/line_follower_ws/src
git clone https://github.com/D-Robotics/line_follower.git -b feature-x5

# Compile
cd ..
source /opt/tros/humble/setup.bash
colcon build
```

**3. Run the line following function**

```shell
source ~/line_follower_ws/install/setup.bash
cp -r ~/line_follower_ws/install/line_follower_perception/lib/line_follower_perception/config/ .
ros2 run line_follower_perception line_follower_perception --ros-args -p model_path:=config/resnet18_224x224_nv12.bin -p model_name:=resnet18_224x224_nv12
```

Run mipi_cam

```shell
source /opt/tros/humble/local_setup.bash
ros2 launch mipi_cam mipi_cam.launch.py
```

Next, enter the motion control package of the robot, originbot_base, and run

```shell
source /opt/tros/humble/local_setup.bash
ros2 launch originbot_base robot.launch.py 
```

Build the scene with PVC tape, and the line following effect is shown in the figure below:
![](./imgs/demo.png)

# Introduction

![](./imgs/framework.png)

The entire system is shown in the above figure. The RDK obtains environmental data in front of the robot through the camera. The image data is inferred by a pre-trained CNN model to obtain the coordinates of the guiding line. Then, based on certain control strategies, the robot's motion is calculated, and the motion control commands are sent to the robot via UART to achieve closed-loop control of the entire system.

The PC is used for data annotation and training. In order to improve efficiency, the image data is sent to the PC via Ethernet for annotation using the RDK.

![](./imgs/roadmap.png)

The entire software engineering process includes 5 main steps:

- Data collection and annotation, obtain corresponding data according to the task goal and annotate it for model training;
- Model selection, select a suitable model structure according to the task goal to ensure that both performance and accuracy meet the requirements;
- Model training, train the model using annotated data to achieve the required accuracy;
- Model conversion, convert the trained floating-point model into a fixed-point model that can run on the RDK using the algorithm tool chain;
- Edge deployment, run the converted model on the RDK, obtain perceptual results, and control robot motion.

The system workflow is as follows:

![](./imgs/annotation.png)

# Interface Description

## Topics

### Publisher Topics

| Name                          | Message Type                                                | Description                                            |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| /cmd_vel                      | geometry_msgs/msg/Twist                                      | Publishes velocity commands to control robot movement   |
| /hbmem_img                      | rcl_interfaces/msg/HobotMemoryCommon                                      | Publishes image data                            |
| /camera_info                      | sensor_msgs/msg/CameraInfo                                      | Publishes camera calibration information                       |## Parameters

| Parameter Name | Type        | Explanation                                        | Required | Supported Configurations | Default Value                 |
| -------------- | ----------- | -------------------------------------------------- | -------- | ------------------------- | ------------------------------ |
| model_path     | std::string | The path to the model file used for inference      | No       | Configured based on actual model path | ./resnet18_224x224_nv12.bin |
| model_name     | std::string | The name of the model file used for inference      | No       | Configured based on actual model path | resnet18_224x224_nv12.bin |



# References

CNN-based Line Following Car: [Deep Line Following Car](https://developer.horizon.cc/documents_tros/tros_dev/line_follower)

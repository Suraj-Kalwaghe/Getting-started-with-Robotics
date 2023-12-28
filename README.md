<!-- <h1> Getting Started with Robotics </h1>

This repo showcases a small robotics project which gives a basic understanding about how to begin with ros and robotics in general. -->

# ROS and Robotics Starter Kit

Welcome to the **ROS and Robotics Starter Kit**! This repository serves as a comprehensive guide and resource for individuals looking to dive into ROS (Robot Operating System) and robotics development. This kit aims to equip you with essential information and resources to kickstart your robotics journey.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
<!-- - [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license) -->

## Getting Started

If you're new to ROS and robotics, follow these steps to get started:

1. **Clone this Repository:**
   ```bash
   git clone https://github.com/Suraj-Kalwaghe/Getting-started-with-Robotics.git
   cd Getting-started-with-Robotics
   ```
2. **ROS 2 Installation Guide**

ROS 2 (Robot Operating System 2) is the next generation of ROS, designed to improve and expand upon the capabilities of ROS 1. Follow the steps below to install ROS 2 on your system.

## Supported Platforms

ROS 2 supports various operating systems. The installation steps may vary slightly depending on your platform. The officially supported platforms include:

- Ubuntu 20.04 (Focal Fossa)
- Debian

## Prerequisites

Before installing ROS 2, make sure your system meets the following prerequisites:

- A supported platform (Ubuntu 22.04 is recommended)
- Internet connection
- sudo access

## Installation Steps

### 1. Set Up Your Sources List

```bash
    sudo sh -c 'echo "deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu focal main" > /etc/apt/sources.list.d/ros2-latest.list'
```

```bash
    sudo apt update && sudo apt install curl gnupg2 lsb-release
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
```

```bash
    sudo apt update
    sudo apt install -y --no-install-recommends \
  ros-foxy-ros-base
```

You can replace Foxy with your desired ROS distro Eg: Humble, galactic, etc
I would suggest you to use Humble since is suits best with UBUNTU 22.04 and the overall experience was pretty smooth.
Other destribution might conflict with the selected version of your ros. Hence, be careful while installing.

## Enviromment setup:

Source the ROS 2 setup file to add ROS 2 commands to your shell session:

```bash
    source /opt/ros/foxy/setup.bash
or
    source /opt/ros/humble/setup.bash
```

## Install Additional Development Tools (Optional)

```bash
    sudo apt install -y \
    python3-argcomplete \
    python3-colcon-common-extensions \
    python3-vcstool
```

## Verification

Inorder to verify the installation, run the following command:
'''bash
ros2 --version
'''
**Congratulations you have successfully installed ROS2 in your system.**
Note: Make sure to refer the additional documentation available at the official ros website for accurate information

> https://docs.ros.org/en/foxy/index.html

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64MultiArray
import math
from tf_transformations import euler_from_quaternion
import matplotlib.pyplot as plt

class PC_Node(Node):

    def __init__(self):
        super().__init__('PC_Node')
        self.imu_subscriber = self.create_subscription(Imu, '/imu_plugin/out', self.imu_callback, 10)
        self.joint_position_pub = self.create_publisher(Float64MultiArray, '/position_controller/commands', 10)
        self.wheel_velocities_pub = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 10)

        self.target_position = [10, 10]
        self.current_position = [0, 0]
        self.distance_threshold = 0.5
        self.desired_yaw = math.atan2(self.target_position[1], self.target_position[0])
        self.current_linear_velocity_x = 0.0
        self.current_linear_velocity_y = 0.0
        self.current_velocity = 0.0
        self.max_linear_velocity = 1.0
        self.prev_time = None
        self.current_yaw = 0
        self.dt = 0
        self.kp = 0.7
        self.err_yaw = 0
        
        self.error_values = []
        self.control_values = []
        self.time_values = []

    def imu_callback(self, imu_msg):
        current_time = imu_msg.header.stamp.sec + imu_msg.header.stamp.nanosec / 1e9
        self.get_logger().info("Heading to point B(10,10)")

        if self.prev_time is not None:
            self.dt = current_time - self.prev_time

        linear_acceleration_x = imu_msg.linear_acceleration.x
        self.current_velocity += linear_acceleration_x * self.dt

        yaw_rate = imu_msg.angular_velocity.z
        delta_yaw = yaw_rate * self.dt
        self.current_yaw += delta_yaw

        delta_x = self.current_velocity * math.cos(self.current_yaw) * self.dt
        delta_y = self.current_velocity * math.sin(self.current_yaw) * self.dt

        self.current_position[0] += delta_x
        self.current_position[1] += delta_y

        quaternion = (
            imu_msg.orientation.x,
            imu_msg.orientation.y,
            imu_msg.orientation.z,
            imu_msg.orientation.w)
        roll, pitch, yaw = euler_from_quaternion(quaternion)

        distance_to_target = math.sqrt((self.target_position[0] - self.current_position[0])**2 +
                                       (self.target_position[1] - self.current_position[1])**2)

        if abs(distance_to_target - self.distance_threshold) <= 0.5:  
            linear_velocity = 0.0
            steer_angle = 0.0
            self.get_logger().info("Reached desired point")
            # self.plot_graphs()

        else:
            self.desired_yaw = math.atan2(self.target_position[1] - self.current_position[1],
                                          self.target_position[0] - self.current_position[0])
            err_yaw = self.desired_yaw - self.current_yaw
            steer_angle = self.kp * err_yaw
            linear_velocity = 8.0

        wheel_velocities = Float64MultiArray()
        joint_positions = Float64MultiArray()
        wheel_velocities.data = [linear_velocity, -linear_velocity]
        joint_positions.data = [steer_angle, steer_angle]

        self.error_values.append(distance_to_target)
        self.control_values.append(steer_angle)
        self.time_values.append(current_time)

        self.joint_position_pub.publish(joint_positions)
        self.wheel_velocities_pub.publish(wheel_velocities)

        self.get_logger().info(f"Yaw: {yaw}")
        self.get_logger().info(f"ERR_YAW{err_yaw}")

        self.prev_time = current_time
    
    def plot_graphs(self):
        plt.figure(figsize=(12, 6))

        # Plot error vs. time
        plt.subplot(1, 2, 1)
        plt.plot(self.time_values, self.error_values, marker='o', linestyle='-', color='b')
        plt.xlabel('t (in sec)')
        plt.ylabel('Error')
        plt.title('Error vs Time')

        # Plot control vs. time
        plt.subplot(1, 2, 2)
        plt.plot(self.time_values, self.control_values, marker='o', linestyle='-', color='g')
        plt.xlabel('t (s)')
        plt.ylabel('Control')
        plt.title('Control wrt Time')
        plt.tight_layout()
        plt.show()

def main(args=None):
    rclpy.init(args=args)
    node = PC_Node()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    # node.plot_graphs()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

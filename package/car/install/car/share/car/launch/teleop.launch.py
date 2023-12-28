import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir

def generate_launch_description():
    return LaunchDescription([
        # Include the gazebo_ros empty world's launch file
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource([ThisLaunchFileDir(), 'empty_world.launch.py']),
            launch_arguments={'world_name': '/home/Optimus/Desktop/car_proj_ws/src/car/worlds'}.items()
        ),

        # Define the robot description parameter
        DeclareLaunchArgument('robot_description', default_value=""),
        Node(
            package='xacro',
            executable='xacro',
            name='xacro',
            output='screen',
            arguments=["'$(find car)/urdf/car.urdf.xacro'"],
            parameters=[{'robot_description': LaunchConfiguration('robot_description')}],
        ),

        # Add your robot name to the parameters
        DeclareLaunchArgument('car', default_value='car'),

        # Load controller variables from the config file
        Node(
            package='rosparam',
            executable='load',
            name='load_controller_params',
            output='screen',
            arguments=["$(find car)/config/config_controllers.yaml"],
            parameters=[{'namespace': 'car'}],
        ),

        # Node for publishing base footprint
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_gui': False}],
        ),

        # TF node for static transformation between map and base_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_base',
            output='screen',
            arguments=['1', '0', '0', '0', '0', '0', '1', '/map', '/base_link'],
        ),

        # Controller spawner to start controllers
        Node(
            package='controller_manager',
            executable='spawner',
            name='controller_spawner',
            output='screen',
            arguments=[
                '--namespace', 'car',
                'joint_state_controller', 'right_steering_controller',
                'left_steering_controller', 'rear_left_controller',
                'rear_right_controller'
            ],
        ),

        # Node to publish robot state
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
        ),

        # Node to spawn the robot into Gazebo's world
        Node(
            package='gazebo_ros',
            executable='spawn_entity',
            name='spawn_model',
            output='screen',
            arguments=[LaunchConfiguration('init_pose'), '-param', 'robot_description', '-urdf', '-model', 'car'],
        ),

        # Default node
        Node(
            package='rostopic',
            executable='rostopic',
            name='fake_joint_calibration',
            output='screen',
            arguments=['pub', '/calibrated', 'std_msgs/Bool', 'true'],
        ),
    ])

# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, LogInfo
# from launch.substitutions import LaunchConfiguration
# from launch_ros.actions import Node

# def generate_launch_description():
#     return LaunchDescription([
#         DeclareLaunchArgument('teleop_script', default_value='/home/soroush/car_proj_ws/src/car/src/teleop.py', description='/home/soroush/car_proj_ws/src/car/src/teleop.py'),

#         LogInfo(
#             condition=LaunchConfiguration('teleop_script') == '',
#             message="Please provide the path to the 'teleop.py' script using the 'teleop_script' argument."
#         ),

#         Node(
#             package='car',  # Replace with the name of your ROS 2 package
#             executable=LaunchConfiguration('teleop_script'),
#             name='keyboard_control_node',
#         ),
#     ])

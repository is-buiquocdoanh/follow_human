from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='usb_camera',
        parameters=[
            {"video_device": "/dev/video0"},
            {"image_size": [352, 288]},
            {"pixel_format": "YUYV"},
            {"frame_rate": 30},   # có thể sửa nếu muốn
        ]
    )

    return LaunchDescription([
        camera_node
    ])

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='usb_camera',
        output='screen',
        parameters=[
            {
                'video_device': '/dev/video2', # thay đổi nếu cần kiểm tra bằng lệnh 'v4l2-ctl --list-devices'
                'image_size': [640, 480],
                'pixel_format': 'YUYV',   # luôn ổn định
                'framerate': 30,
                'output_encoding': 'rgb8'
            }
        ],
        remappings=[
            # ('/image_raw', '/camera/image_raw'),
            # ('/camera_info', '/camera/camera_info')
        ]
    )

    return LaunchDescription([
        camera_node
    ])

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    republish = Node(
        package='image_transport',
        executable='republish',
        name='republish_compressed',
        arguments=[
            'compressed',  # input transport type
            'raw'          # output transport type
        ],
        remappings=[
            ('in/compressed', '/image_raw/compressed'),
            ('out', '/yolo_image_raw')
        ]
    )

    return LaunchDescription([
        republish
    ])

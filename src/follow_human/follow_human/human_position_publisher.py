#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
from yolov8_msgs.msg import HumanPosition, HumanPositionArray

import os
import numpy as np

class HumanPositionPublisher(Node):
    def __init__(self):
        super().__init__('human_position_publisher')

        # Load YOLOv8 model
        model_path = os.path.expanduser('~/robot_detect/src/robot_recognition/scripts/yolov8n.pt')
        self.model = YOLO(model_path)

        self.bridge = CvBridge()

        # Nhận ảnh từ camera
        self.subscription = self.create_subscription(
            Image,
            '/yolo_image_raw',
            self.image_callback,
            10
        )

        # Publish danh sách người
        self.publisher_ = self.create_publisher(HumanPositionArray, '/human_positions', 10)

        self.get_logger().info("✅ Human Position Publisher started!")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # results = self.model(frame)
        results = self.model(frame, imgsz=352)


        human_array_msg = HumanPositionArray()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls)
                label = self.model.names[cls]
                conf = float(box.conf)

                if label == 'person' and conf > 0.5:
                    xyxy = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = xyxy

                    x_center = (x1 + x2) / 2.0
                    y_center = (y1 + y2) / 2.0
                    w = x2 - x1
                    h = y2 - y1

                    person = HumanPosition()
                    person.x_center = float(x_center)
                    person.y_center = float(y_center)
                    person.width = float(w)
                    person.height = float(h)
                    person.confidence = float(conf)

                    human_array_msg.humans.append(person)

        if len(human_array_msg.humans) > 0:
            self.publisher_.publish(human_array_msg)
            self.get_logger().info(f"👥 {len(human_array_msg.humans)} humans detected")

def main(args=None):
    rclpy.init(args=args)
    node = HumanPositionPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

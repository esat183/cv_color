import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class DroneVisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.subscription = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()
        self.red_pos_saved = False
        
        self.get_logger().info('Drone Goruntu Isleme Dugumu Baslatildi!')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        if cv2.countNonZero(red_mask) > 1000:
            if not self.red_pos_saved:
                self.get_logger().info('KIRMIZI BULUNDU!')
                self.red_pos_saved = True

        if cv2.countNonZero(blue_mask) > 1000:
            self.get_logger().info('MAVI BULUNDU!')

        cv2.imshow("Drone Kamerasi", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = DroneVisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

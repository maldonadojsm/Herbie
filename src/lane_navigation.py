# !/usr/bin/env python
# title           :lane_navigation.py
# description     :Lane Navigation system that allows Herbie to drives autonomously while within two lanes.
# author          :Sebastian Maldonado
# date            :8/18/2020
# version         :0.0
# usage           :SEE README.md
# notes           :Enter Notes Here
# python_version  :3.6.8
# conda_version   :4.8.3
# =================================================================================================================

from image_preprocessing import *
import logging


class LaneKeepAssistSystem(object):
    """
    This following Python class allows herbie to navigate autonomously by using the side lanes on a road
    """

    def __init__(self, car=None):
        """
        Constructor
        :param car: PiCar object
        """
        logging.info("Configuring Lane Keep Assist System")
        self.current_steering_angle = 90
        self.car = car

    def drive_within_lanes(self, image):
        """
        Detect lanes and move the vehicle accordingly
        :param image: Video frame retrieved from the PiCamera
        :return:
        """
        display_image("Driving View", image)

        lanes, image = locate_lanes(image)
        driving_frame = self.steer_vehicle(image, lanes)

        return driving_frame

    def steer_vehicle(self, image, lanes):
        """
        Steers vehicle using Servos
        :param image: Video frame retrieved PiCamera
        :param lanes: Detected lanes returned by drive_within_lanes()
        :return: Heading image
        """
        if len(lanes) == 0:
            return image

        new_steer_angle = self.calculate_steering_angle(image, lanes)
        self.current_steering_angle = self.stabilize(self.current_steering_angle, new_steer_angle, len(lanes))

        if self.car is not None:
            self.car.front_wheels.turn(self.current_steering_angle)

        heading_image = generate_heading(image, self.current_steering_angle)
        display_image("Vehicle Heading", heading_image)

        return heading_image

    def stabilize(self, current_steering_angle, new_steering_angle, number_lanes, max_deviation_2l=5, max_deviation_1l=1):
        """
        Corrects steering angle if angle deviates from expected angles
        :param current_steering_angle: previous steering angle calculated by Herbie
        :param new_steering_angle: New steering angle calculated by Herbie
        :param number_lanes: Number of lanes detected
        :param max_deviation_2l: Max permitted steering angle permitted for two lane detection
        :param max_deviation_1l: Max permitted steering angle permitted for one lane detection
        :return: Modified steering angle
        """

        if number_lanes == 2:
            max_deviation_angle = max_deviation_2l

        else:
            max_deviation_angle = max_deviation_1l

        steering_deviation = new_steering_angle - current_steering_angle

        # Stabilize steering if different between current and new steering angle exceeds
        # accepted driving angle deviation
        if abs(steering_deviation) > max_deviation_angle:
            stable_steering_angle = int(current_steering_angle + max_deviation_angle * steering_deviation/ abs(steering_deviation))

        else:
            stable_steering_angle = new_steering_angle

        return stable_steering_angle

    def calculate_steering_angle(self, image, lanes):
        """
        Calculate steering angle
        :param image: Video frame rendered from PiCamera
        :param lanes: Detected lanes
        :return: Steering angle
        """
        if len(lanes) == 0:
            return -90

        h, w, _ = image.shape

        # One Lane Has Been Detected
        if len(lanes) == 1:

            x0, _, x1, _ = lanes[0][0]
            x_offset = x1 - x0

        # Two Lanes Have Been Detected
        else:
            _, _, lx1, _ = lanes[0][0]
            _, _, rx1, _ = lanes[1][0]

            camera_offset = 0.02 # Percent
            heading_line = int(w / 2 * (1 + camera_offset))
            x_offset = (lx1 + rx1) / 2 - heading_line

        y_offset = int(h / 2)

        steering_angle_radians = math.atan(x_offset / y_offset)
        steering_angle_degrees = int(steering_angle_radians * 180.0 / math.pi)
        steering_angle = steering_angle_degrees + 90

        return steering_angle





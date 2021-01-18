import cv2
import numpy as np
from tensorflow.keras.models import load_model
from lane_navigation import LaneKeepAssistSystem
from image_preprocessing import *
import logging


class DeepLearningLKAS(object):
    """
    A Lane Keep Assist System powered by Deep Learning. Inspired by Nvidia End-to-End ML architecture for self-driving cars.
    """
    def __init__(self, car=None, ml_model_path='/home/pi/Herbie/ml_models/lane_keep_assist_system/trained_models/DL_LKAS_FINAL.h5'):

        self.current_steering_angle = 90
        self.model = load_model(ml_model_path)
        logging.info("Configuring Deep Learning Lane Keep Assist System")
        self.car = car

    def drive_within_lanes(self, image):
        """
        Detect lanes using trained TF DL Model and move the vehicle according
        :param image: Video frame retrived from the PiCamera
        :return:
        """

        display_image("Driving View", image)
        # Predict steering angle using DL LKAS model
        self.current_steering_angle = self.predict_steering_angle(image)
        # Turn vehicle
        if self.car is not None:
            self.car.front_wheels.turn(self.current_steering_angle)

        heading_image = generate_heading(image, self.current_steering_angle)

        return heading_image

    def predict_steering_angle(self, image):
        """
        Predict steering angle using a DL model that ingests a frame from the PiCamera. We round the steering
        angle to the nearest integer given PiCar only turns using whole numbers.
        """

        processed_img = self.preprocess_image(image)
        array_img = np.asarray([processed_img])
        prediction = self.model.predict(array_img)[0]

        return int(prediction + 0.5)

    def preprocess_image(self, frame):
        """
        Transform raw video frame received by PiCamera such that it's compatible with Nvidia Model
        """

        h, _, _ = frame.shape
        frame = frame[int(h/2),: ,:, :]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        frame = cv2.GaussianBlur(frame, (3,3), 0)
        frame = cv2.resize(frame, (200, 66))
        frame = frame / 255

        return frame

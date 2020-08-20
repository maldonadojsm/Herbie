# !/usr/bin/env python
# title           :image_preprocessing.py
# description     :Enter Description Here
# author          :Sebastian Maldonado
# date            :8/19/2020
# version         :0.0
# usage           :SEE README.md
# notes           :Enter Notes Here
# python_version  :3.6.8
# conda_version   :4.8.3
# =================================================================================================================

import cv2
import numpy as np
import sys
import math

DISPLAY_IMAGE = False


def locate_edges(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Specifying Hue Range for Color Blue
    lower_bound = np.array([[30, 40, 0]])
    upper_bound = np.array([150, 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Find Edges in Image

    edges = cv2.Canny(mask, 200, 400)

    return edges


def isolate_lane_edges(edges):
    # Capture Height & Width of Image
    h, w = edges.shape
    mask = np.zeros_like(edges)

    # Isolate Bottom Half of Screen

    polygon = np.array([[(0, h * 0.5), (w, h * 0.5), (w, h), (0, h), ]], np.int32)

    # Fill Mask With Polygon
    cv2.fillPoly(mask, polygon, 255)

    # Extract isolated lane edges
    isolated_edges = cv2.bitwise_and(edges, mask)

    return isolated_edges


def locate_line_segments(isolated_edges):
    rho = 1
    theta = np.pi / 180
    threshold = 10
    min_line_length = 8
    max_line_gap = 4

    segments = cv2.HoughLinesP(isolated_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    return segments


def generate_lanes(image, segments):

    lanes = []

    if segments is None:
        return lanes

    h, w, _ = image.shape

    right_lane_segments = []

    left_lane_segments = []

    boundary = 1 / 3

    left_lane_boundary = w * (1 - boundary)

    right_lane_boundary = w * boundary

    # Classify Slopes By Their Direction. Positive Slopes -> Left Lane Lines, Negative Slopes -> Right Lane Lines
    for i in segments:

        for x0, y0, x1, y1 in i:

            if x0 == x1:
                continue

            poly_fit = np.polyfit((x0, x1), (y0, y1), 1)
            mx = poly_fit[0]
            b = poly_fit[1]

            if mx < 0:

                if x0 < left_lane_boundary and x1 < left_lane_boundary:
                    left_lane_segments.append((mx, b))

            else:
                if x0 > right_lane_boundary and x1 > right_lane_boundary:
                    right_lane_segments.append((mx, b))

    # Determine Average Slope of Left Lane Lines Segments

    left_lane_avg = np.average(left_lane_segments, axis=0)

    # Extract and store endpoints of line segments of left lane
    if len(left_lane_avg) > 0:
        lanes.append(generate_endpoints(image, left_lane_avg))

    # Same for Right Lane
    right_lane_avg = np.average(right_lane_segments, axis=0)

    if len(right_lane_avg) > 0:
        lanes.append(generate_endpoints(image, right_lane_avg))

    return lanes


def generate_endpoints(image, line):
    h, w, _ = image.shape
    mx, b = line

    y0 = h
    y1 = int(y0 * 0.5)
    x0 = max(-w, min(2 * w, int((y0 - b) / mx)))
    x1 = max(-w, min(2 * w, int((y1 - b) / mx)))

    return [[x0, y0, x1, y1]]


def locate_lanes(image):
    """

    :param image:
    :return:
    """
    edges = locate_edges(image)
    display_image("Image Edges", image)

    isolated_edges = isolate_lane_edges(edges)
    display_image("Isolated Edges", isolated_edges)

    lane_line_segments = locate_line_segments(isolated_edges)
    lane_line_segment_img = show_lane_lines(image, lane_line_segments)
    display_image("Lane Line Segments", lane_line_segment_img)

    driving_lanes = generate_lanes(image, lane_line_segments)
    driving_lanes_img = show_lane_lines(image, driving_lanes)
    display_image("Lane Lines", driving_lanes_img)

    return driving_lanes, driving_lanes_img


def show_lane_lines(image, lines, color=(0, 255, 0), width=2):
    lane_image = np.zeros_like(image)
    if lines is not None:
        for l in lines:
            for x0, x1, y0, y1 in l:
                cv2.line(lane_image, (x0, y0), (x1, y1), color, width)

    alpha = 0.8
    beta = 1
    gamma = 1
    lane_image = cv2.addWeighted(image, alpha, lane_image, beta, gamma)

    return lane_image


def display_image(image_title, image, display=DISPLAY_IMAGE):
    if display:
        cv2.imshow(image_title, image)


def generate_heading(image, steering_angle, color=(0, 0, 255), width=5):
    heading_image = np.zeros_like(image)
    h, w, _ = image.shape

    steering_angle_radians = steering_angle / 180.0 * math.pi

    x0 = int(w / 2)
    y0 = h
    x1 = int(x0 - h / 2 / math.tan(steering_angle_radians))
    y1 = int(h / 2)

    cv2.line(heading_image, (x0, y0), (x1, y1), color, width)
    alpha = 0.8
    beta = 1
    gamma = 1
    heading_image = cv2.addWeighted(image, alpha, heading_image, beta, gamma)

    return heading_image




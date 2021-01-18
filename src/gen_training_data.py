import cv2
import sys
from lane_navigation import LaneKeepAssistSystem

def extract_frame_and_steering_angle(file):
    """
    Script creates training data by breaking down a .avi video file into frames and then determining the steering angle of a given frame using the hand-coded LKAS system exclusively written in OpenCV. Saves result as .png file with label (steering angle) as part of the file nname: [filename]_[frame no.]_[label].png
    """

    lane_tracker = LaneKeepAssistSystem()
    video_stream  = cv2.VideoCapture(file)

    try:
        i = 0
        while video_stream.isOpened():
            _, frame = video_stream.read()
            lane_tracker.drive_within_lanes(frame)
            cv2.imwrite("%s_%03d_%03d.png" % (file, i, lane_tracker.current_steering_angle), frame)
            i += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        # Close video stream 
        video_stream.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    extract_frame_and_steering_angle(sys.argv[1])



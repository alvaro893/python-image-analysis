# https://www.learnopencv.com/blob-detection-using-opencv-python-c/
import cv2
import numpy as np;
import matplotlib.pylab as plt
window_name = "Blobs"

class BlobDetector:
    def __init__(self, source=0):
        if isinstance(source, str):
            self.image = cv2.imread(source, cv2.IMREAD_GRAYSCALE)
        else:
            self.video_cap = cv2.VideoCapture(source)
        self.params = cv2.SimpleBlobDetector_Params()
        self.is_running = True
        self.run()

    def create_ui(self):
        self.t_min = createTrackBars("Min Threshold", 100, 10)
        self.t_max = createTrackBars("Max Threshold", 1000, 200)
        self.t_circularity = createTrackBars("Filter by cirtularity", 10, 8)
        self.t_area = createTrackBars("min Area", 3000, 1500)
        self.t_convex = createTrackBars("convexity", 100, 87)
        self.t_min_inertia_ratio = createTrackBars("min inertia ratio", 100, 1)

    def run(self):
        while (self.is_running):
            # Read image
            try:
                if not hasattr(self, "image"):
                    ret, im = self.video_cap.read()
                else:
                    im = self.image
            except Exception:
                print "some error"
                self.is_running = False

            # Change thresholds
            self.params.minThreshold = get_trackbar_value(t_min)
            self.params.maxThreshold = get_trackbar_value(t_max)

            # Filter by Area.
            self.params.filterByArea = True
            self.params.minArea = get_trackbar_value(t_area)

            # Filter by Circularity
            self.params.filterByCircularity = True
            self.params.minCircularity = get_trackbar_value(t_circularity) / 10.0

            # Filter by Convexity
            self.params.filterByConvexity = True
            self.params.minConvexity = get_trackbar_value(t_convex) / 100.0

            # Filter by Inertia
            self.params.filterByInertia = True
            self.params.minInertiaRatio = get_trackbar_value(t_min_inertia_ratio) / 100.0

            # Create a detector with the parameters
            detector = cv2.SimpleBlobDetector_create(self.params)

            # Detect blobs.
            keypoints = detector.detect(im)

            # Draw detected blobs as red circles.
            # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
            im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # Show blobs detected
            add_label(im_with_keypoints, len(keypoints))

            # Show keypoints
            cv2.imshow(window_name, im_with_keypoints)
            print im_with_keypoints
            plt.imshow(im_with_keypoints, cmap='jet', interpolation='bicubic')
            plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
            plt.show()

            # time to wait milisecons
            key = cv2.waitKey(5) & 0xFF

            # escape when q key is pushed
            if key == ord("q") or key == ord("Q"):
                break

def createTrackBars(t_name, max_v, default):
    def nothing(a):
        pass
    cv2.namedWindow(window_name)
    cv2.createTrackbar(t_name, window_name, 0, max_v, nothing)
    cv2.setTrackbarPos(t_name, window_name, default)
    return t_name

def get_trackbar_value(t_name):
    return cv2.getTrackbarPos(t_name, window_name)

def add_label(frame, text):
    cv2.putText(frame, "detected: "+str(text) ,(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),1,cv2.LINE_AA)

t_min = createTrackBars("Min Threshold", 100, 10)
t_max = createTrackBars("Max Threshold", 1000, 200)

t_circularity = createTrackBars("Filter by cirtularity", 10, 8)
t_area = createTrackBars("min Area", 3000, 1500)
t_convex = createTrackBars("convexity", 100, 87)
t_min_inertia_ratio = createTrackBars("min inertia ratio", 100, 1)


b = BlobDetector()

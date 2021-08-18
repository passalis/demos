import cv2
import time

class VideoReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        try:  # OpenCV needs int to read from webcam
            self.file_name = int(file_name)
        except ValueError:
            pass
        self.cap = None
        
    def __iter__(self):
        self.cap = cv2.VideoCapture(self.file_name)
        if not self.cap.isOpened():
            raise IOError('Video {} cannot be opened'.format(self.file_name))
        return self

    def __next__(self):
        was_read, img = self.cap.read()
        if not was_read:
            raise StopIteration
        return img
    
    def close(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
    
class FPSCounter(object):
    
    def __init__(self):
        self.fps = -1
        self.start_time = 0
        
        
    def tic(self):
        self.start_time = time.time()
    
    def toc(self, img=None):
        cur_fps = 1.0/(time.time() - self.start_time)
        if self.fps == -1:
            self.fps = cur_fps
        else:
            self.fps = self.fps*0.8 + 0.2 * cur_fps
            
        if img is not None:
            self.draw(img)
            
    def draw(self, img):
        image = cv2.putText(img, "FPS: %.2f" % (self.fps,), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
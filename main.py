import time
import os
import cv2  
from PIL import Image
import argparse

def create_video(capture_dir = None):
    if not capture_dir:
        path = "captures"
        dirs = []
        for item in os.listdir(path):
            if not os.path.isfile(f"{path}/{item}"):
                dirs.append(f"{path}/{item}")
        capture_dir = sorted(dirs)[-1]
    
    video_name = 'timelapse.avi'
      
    images = sorted([img for img in os.listdir(capture_dir) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")])
    
     
    # Array images should only consider 
    # the image files ignoring others if any 
    print(images)
    
    frame = cv2.imread(os.path.join(capture_dir, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
  
    video = cv2.VideoWriter(filename=os.path.join(capture_dir,video_name),
                            fourcc=0,
                            fps=4,
                            frameSize=(width, height)
                            )  
  
    # Appending the images to the video one by one 
    for image in images:  
        video.write(cv2.imread(os.path.join(capture_dir, image)))  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 

def timelapse_loop(sleep_time=10):
    from picamera import PiCamera
    camera = PiCamera()

    start_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    os.mkdir(f"captures/{start_time}")
    try:
        camera.start_preview(alpha=200)
        i = 0
        while True:
            print(f" wait {i}")
            i+=1
            time.sleep(sleep_time)
            camera.capture(f'captures/{start_time}/img-{i:07d}.jpg')
            if i > 50:
                break
        
    except KeyboardInterrupt:
        camera.stop_preview()
        exit()
    finally:
        camera.stop_preview()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--sleep_time", type=int, help="The number of seconds between each frame capture.")
    args = parser.parse_args()
    print(args)
    if args.sleep_time:
        sleep_time = args.sleep_time
    else:
        sleep_time = None
    
#     timelapse_loop(60)
#     create_video()
    
    
if __name__ == "__main__":
    main()
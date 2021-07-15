from matplotlib import pyplot as plt
import numpy as np
import cv2

cap = cv2.VideoCapture('eye-test-18-22-0.mov')
#cap = cv2.VideoCapture('eye-goaround-17-16-0.mov')
#cap = cv2.VideoCapture('eye-fixate-17-16-0.mov')

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

print("Toral Frames: ", cap.get(cv2.CAP_PROP_FRAME_COUNT)) 

oldframe = np.zeros((256,1024))
countImg = np.zeros((256,1024))
Kernelsize = 2
kernel = np.ones((Kernelsize,Kernelsize),np.float32)

contribute = 0.5;



while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
  ImgR1 = gray[:,:256]
  ImgR2 = gray[:,256:512]
  ImgL1 = gray[:,512:768]
  ImgL2 = gray[:,768:1024]


  A3 = cv2.getRotationMatrix2D((100, 100), 30, 1)
  warped = cv2.warpAffine(ImgR1, A3, (256, 256), \
      flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)  




  gray = ((255-gray) > 220) *2
  #gray = ((gray) > 200) * 2

  if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:
    oldframe = gray
    continue
  
  newframe = gray*contribute + oldframe*(1-contribute)
  newframe = gray*2 + oldframe

  oldframe = newframe.astype(np.uint8)
  gray = gray.astype(np.uint8)

  cnts, _ = cv2.findContours(oldframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # Draw found contour(s) in input image
  #oldframe = cv2.drawContours(oldframe, cnts, -1, (255, 0, 255), 1)

  for cnt in cnts:   
    if cnt.size < 80 or cnt.size > 200:
      continue
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(countImg, ellipse, (255,0, 255), 1, cv2.LINE_AA)

  #print(DivIntegral.dtype)
  #newframe = gray-dst
  if ret == True:
    # Display the resulting frame
    try: 
      #cv2.imshow('Frame',abs(newframe-oldframe)/10)
      cv2.imshow('Frame',oldframe)
      cv2.imshow('Counto',countImg)
      cv2.imshow('Affined',warped)
      

      #cv2.imshow('Frame',newframe)
    except OSError as error:
      print(error)  

   # oldframe = newframe;
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  # Break the loop
  else:
    break
# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()



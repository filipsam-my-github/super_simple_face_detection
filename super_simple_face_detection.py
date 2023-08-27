import cv2, time, math,random
import numpy as np

W_CAM, H_CAM = 800, 800

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, W_CAM)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H_CAM)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

last_time = time.time()
dt = 0
chrome= np.array([0,0,0],dtype=np.float16)
while True:
    dt = time.time() - last_time
    last_time = time.time()
    
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.putText(img, f"fps: {math.ceil(1/(dt+0.00001))}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f"chrome: {chrome}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    for (x, y, w, h) in faces:
        if dt>1:
            dt=1
            
        chrome[2]+=np.float16(random.randint(65,130)*dt)
        
        for i in range(3)[::-1]:
            if i==np.float16(0):
                if chrome[i]>np.float16(255):
                    chrome= np.array([255,255,255],dtype=np.float16)
            elif chrome[i]>np.float16(255):
                chrome[i]-=np.float16(255)
                chrome[i-1]+=np.float16(random.randint(5,15)+random.randint(5,15)*(-1)*(i-2)*5+random.randint(1,10)*(-1)*(i-2))
        
        cv2.rectangle(img, (x, y), (x+w, y+h), (int(chrome[0]), int(chrome[1]), int(chrome[2])), 2)
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    
    if cv2.waitKey(1) == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()

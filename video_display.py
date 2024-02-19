import cv2

cap = cv2.VideoCapture("video_1.mp4")

while (1) :
    check , frame = cap.read()
    cv2.imshow("display",frame)
    cv2.setWindowProperty("display", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    x = 1000//60
    if cv2.waitKey(x) & 0xff == ord("e"):
        break
cap.release()
cv2.destroyAllWindows()
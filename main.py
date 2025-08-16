import cv2
import mediapipe as mp
import pyautogui 
import time 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

# Try to set webcam resolution same as screen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_h)

click_count=0
prev_x, prev_y = None, None
paused = False  # for two fingers up

# Create a resizable window
cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Tracking", screen_w, screen_h)  # start fullscreen size

while True:
    success, img = cap.read()
    if not success:
        break

    # Mirror camera
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            # Check finger states
            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y
            
            # is_right_hand = lm[17].x > lm[0].x  
            is_right_hand = (lm[5].x < lm[9].x) and (lm[13].x < lm[17].x)

            if is_right_hand:
                thumb_up = (lm[4].x <= lm[3].x) and (lm[3].y <= lm[4].y)
            else:
                thumb_up = (lm[4].x >= lm[3].x) and (lm[3].y <= lm[4].y) 

            # Pause if index and middle fingers up
            if index_up and middle_up:
                paused = True
            else:
                paused = False

            # Mouse movement with index finger only
            if index_up and not paused:
                x = lm[8].x
                y = lm[8].y

                if prev_x is not None and prev_y is not None:
                    dx = (x - prev_x) * 2000
                    dy = (y - prev_y) * 2000

                    screen_w, screen_h = pyautogui.size()
                    new_x = pyautogui.position().x + dx
                    new_y = pyautogui.position().y + dy
                    new_x = max(1, min(screen_w - 2.5, new_x))
                    new_y = max(1, min(screen_h - 2.5, new_y))

                    pyautogui.moveTo(new_x, new_y)

                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            # Left click if thumb up
            # Left click if thumb up
            if thumb_up:
                if thumb_start_time is None:
                    thumb_start_time = time.time()
                    clicked_once = False
                    double_clicked = False

                elapsed = time.time() - thumb_start_time

                # Single click after 1s
                if elapsed >= 0.75 and not clicked_once:
                    pyautogui.click()
                    click_count += 1
                    clicked_once = True

                # Double click after 1.5s (so total 3 clicks)
                if elapsed >= 2.25 and clicked_once and not double_clicked:
                    pyautogui.doubleClick()
                    click_count += 2
                    double_clicked = True

            else:
                # Reset when thumb goes down
                thumb_start_time = None
                clicked_once = False
                double_clicked = False
  
            # Draw landmarks normally
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            
            # Show coordinates of thumb tip (lm[4]) and joint (lm[3])
            text1 = f"lm4.x: {lm[4].x:.3f}, lm3.x: {lm[3].x:.3f}"
            text2 = f"lm4.y: {lm[4].y:.3f}, lm3.y: {lm[3].y:.3f}"

            # Convert to pixel coords
            lm4_px = (int(lm[4].x * w), int(lm[4].y * h))
            lm3_px = (int(lm[3].x * w), int(lm[3].y * h))
            text3 = f"lm4_px: {lm4_px}, lm3_px: {lm3_px}"

            # Draw text at top-left
            cv2.putText(img, text1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, text2, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, text3, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, f"is right hand: {is_right_hand}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, f"lm[4].x <= lm[3].x: {lm[4].x <= lm[3].x}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, f"lm[3].y <= lm[4].y: {lm[3].y <= lm[4].y}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(img, f"click count: {click_count}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


            # Draw GREEN circles if finger is UP
            if index_up:
                cx, cy = int(lm[8].x * w), int(lm[8].y * h)
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            if middle_up:
                cx, cy = int(lm[12].x * w), int(lm[12].y * h)
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            if thumb_up:
                cx, cy = int(lm[4].x * w), int(lm[4].y * h)
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # 🔥 Resize the camera frame to fit window size (stretch)
    window_rect = cv2.getWindowImageRect("Hand Tracking")
    window_w, window_h = window_rect[2], window_rect[3]

    if window_w > 0 and window_h > 0:  # only resize if window is valid
        img_resized = cv2.resize(img, (window_w, window_h))
        cv2.imshow("Hand Tracking", img_resized)
    else:
        cv2.imshow("Hand Tracking", img)  # fallback
    cv2.imshow("Hand Tracking", img_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

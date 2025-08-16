# 🖐️ Touchless Hand Tracking Mouse Control

This project uses **OpenCV**, **MediaPipe**, and **PyAutoGUI** to let you control your computer mouse **without touching it** — using only your hand gestures detected from your webcam!  

---

## ✨ Features
- **Hand Tracking** with MediaPipe  
- **Mouse Control**  
  - Move mouse with **index finger**  
  - **Thumbs Up → Single Click** (after 0.75s)  
  - **Thumbs Up → Double Click** (after 2.25s, total 3 clicks including the first one)  
- **Pause Mouse Movement** by raising **index + middle finger** together  
- **On-Screen Visualization**  
  - Green dots show which fingers are active  
  - Debug text with landmark coordinates and click counter  
- **Resizable Window** — camera frame automatically adjusts to window size  

---

## 📸 Demo
*(Insert GIF or screenshot of your program running here)*  

---

## 🚀 Installation

Clone this repository:
```bash
git clone https://github.com/yourusername/touchless-hand-tracking.git
cd touchless-hand-tracking
```

Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui
```

## ▶️ Usage

Run the script:
```bash
python main.py
```

Controls:

👉 Index finger up → Move mouse

✌️ Index + Middle finger up → Pause mouse movement

👍 Thumbs up
- Hold for 0.75s → Left Click
- Hold for 2.25s → Double Click (so total 3 clicks)
  
❌ Press Q → Quit the app

## ⚠️ Notes
Works best in good lighting with one hand visible

When the window is minimized, the program falls back to prevent resize crashes

Screen resolution is automatically detected for accurate mouse movement

## 🛠️ Built With

OpenCV – Computer Vision

MediaPipe – Hand Tracking

PyAutoGUI – Mouse Control

## 💚 Future Improvements
Right-click gesture support

Scroll with finger gestures

Multi-hand support

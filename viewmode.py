import os
import cv2
import torch
import json
import random
import numpy as np
import streamlit as st
import sys
import platform
import time
import smtplib
import imghdr
import urllib.request
from email.message import EmailMessage
from utils.general import non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.torch_utils import select_device, time_synchronized
from models.experimental import attempt_load
from utils.plots import plot_one_box
from datetime import datetime

# File paths and settings
SETTINGS_FILE = "settings.json"
SOUND_FOLDER = "alarm_sounds"
detected_folder = os.path.join(os.getcwd(), "detected_human")

# Define the model URL from GitHub raw link
model_url = "https://raw.githubusercontent.com/arhitecturalpro/IDS-Streamlit/main/bestlatest.pt"
model_path = "bestlatest.pt"

# Check if the model file exists; if not, download it
if not os.path.exists(model_path):
    print("Downloading model...")
    urllib.request.urlretrieve(model_url, model_path)
    print("Download complete!")

opt = {
    'weights': model_path,
    'img-size': 320,
    'conf-thres': 0.4,
    'iou-thres': 0.45,
    'device': 'cpu',
    'classes': [0]
}

# Email configuration for Gmail
# Replace these with your actual credentials and details.
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_COOLDOWN = 300  # seconds between email alerts
last_email_time = 0

# Global variable to store last screenshot path
last_screenshot_path = None

# Load settings from file (expects keys "alarm_enabled" and "alarm_sound")
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"alarm_enabled": True, "alarm_sound": "default.wav"}

# Save screenshot when a human is detected and update global path
last_screenshot_time = 0  
screenshot_interval = 4  # seconds

def save_screenshot(img):
    global last_screenshot_time, last_screenshot_path
    now = time.time()
    if now - last_screenshot_time >= screenshot_interval:
        date_folder = datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(detected_folder, date_folder)
        os.makedirs(folder_path, exist_ok=True)
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.join(folder_path, f"screenshot_{timestamp}.jpg")
        cv2.imwrite(filename, img)
        print(f"Screenshot saved: {filename}")
        last_screenshot_time = now
        last_screenshot_path = filename

# Email alert function: sends an email with attached screenshot if available.
def send_email_alert():
    global last_email_time, last_screenshot_path
    now = time.time()
    if now - last_email_time < EMAIL_COOLDOWN:
        return  # Prevent spamming emails
    msg = EmailMessage()
    msg['Subject'] = "Intrusion Alert: Human Detected"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg.set_content("Alert: An intrusion has been detected by your security system.")
    
    # If a screenshot exists, attach it
    if last_screenshot_path and os.path.exists(last_screenshot_path):
        with open(last_screenshot_path, 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(None, img_data)
            img_name = os.path.basename(last_screenshot_path)
        msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email alert sent.")
        last_email_time = now
    except Exception as e:
        print(f"Failed to send email: {e}")

# Global flag to track alarm state
alarm_active = False

# Check OS platform and import the appropriate sound library
if sys.platform == "win32":
    import winsound
else:
    from playsound import playsound
    
def play_alarm():
    settings = load_settings()
    alarm_sound = os.path.join(SOUND_FOLDER, settings["alarm_sound"])
    winsound.PlaySound(alarm_sound, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_alarm():
    if platform.system() == "Windows":
        import winsound
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        print("Alarm stopped (no sound support on this OS)")

def view_mode():
    """Display video feed with YOLOv7 object detection and notify via email when an intruder is detected."""
    
    # Sidebar: only include split layout selection
    split_layout = st.sidebar.selectbox('Select Split Layout', ['1 Screen', '2 Screens', '4 Screens'])
    
    # Load alarm enable state from settings
    settings = load_settings()
    alarm_toggle = settings.get("alarm_enabled", True)
    
    # Initialize video capture
    camera = cv2.VideoCapture(0)
    
    # Set up YOLOv7 model
    weights, imgsz = opt['weights'], opt['img-size']
    device = select_device(opt['device'])
    half = device.type != 'cpu'

    print("Loading model from:", weights)
    model = attempt_load(weights, map_location=device)
    model.eval()
    stride = int(model.stride.max())
    imgsz = letterbox(np.zeros((imgsz, imgsz)), imgsz, stride=stride)[0].shape[1]
    if half:
        model.half()
    names = model.module.names if hasattr(model, 'module') else model.names
    
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))
    
    # Prepare layout placeholders based on selected split layout
    if split_layout == '1 Screen':
        stframe = st.empty()
    elif split_layout == '2 Screens':
        col1, col2 = st.columns(2)
        stframe1 = col1.empty()
        stframe2 = col2.empty()
    elif split_layout == '4 Screens':
        col1, col2 = st.columns(2, gap="small")
        stframe1 = col1.empty()
        stframe2 = col2.empty()
        col3, col4 = st.columns(2, gap="small")
        stframe3 = col3.empty()
        stframe4 = col4.empty()
    
    global alarm_active
    alarm_active = False
    
    # Main detection loop
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Mirror frame and overlay timestamp
        frame = cv2.flip(frame, 1)
        img0 = frame.copy()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(img0, now_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Preprocess image for inference
        img = letterbox(img0, imgsz, stride=stride, auto=False)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Run inference and apply non-max suppression
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, opt['conf-thres'], opt['iou-thres'], classes=opt['classes'], agnostic=False)

        human_detected = False
        for det in pred:
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    if int(cls) == 0 and conf >= 0.5:
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, img0, label=label, color=(128, 0, 128), line_thickness=2)
                        human_detected = True
                        save_screenshot(img0)
        
        # Alarm and email alert logic
        if human_detected:
            if not alarm_active:
                alarm_active = True
                if alarm_toggle:
                    play_alarm()
                send_email_alert()  # Send an email alert with attached screenshot
        else:
            if alarm_active:
                alarm_active = False
                stop_alarm()
    
        # Display the processed video feed in the selected layout
        img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
        if split_layout == '1 Screen':
            stframe.image(img0, channels="RGB", use_container_width=True)
        elif split_layout == '2 Screens':
            stframe1.image(img0, channels="RGB", use_container_width=True)
            stframe2.image(img0, channels="RGB", use_container_width=True)
        elif split_layout == '4 Screens':
            stframe1.image(img0, channels="RGB", use_container_width=True)
            stframe2.image(img0, channels="RGB", use_container_width=True)
            stframe3.image(img0, channels="RGB", use_container_width=True)
            stframe4.image(img0, channels="RGB", use_container_width=True)

    camera.release()
    stop_alarm()

if __name__ == "__main__":
    view_mode()

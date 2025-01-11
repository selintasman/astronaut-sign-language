import mediapipe as mp
import cv2, math, datetime
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

# GUI starting:
win = Tk()
width=win.winfo_screenwidth()
height=win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))

# Resize the background image to match the window dimensions
backg = PhotoImage(file="background.png")
bg_image = Image.open("background.png")
bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
bg = ImageTk.PhotoImage(bg_image)

# Create a label with the resized background image
bg_label = Label(win, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

win.title('Sign Language Recognition')
mylabel1= Label(win,text='A(stronaut) Sign Language',font=('Arial',26,'bold'),bd=5,bg='#20262E',fg='#F5EAEA',relief=GROOVE,width=5000 ).pack(pady=20,padx=500)

# Name and Rollno Label:
namee = Label(win,text='Cosmic Explorer', font=('Arial',14,'bold'),relief=GROOVE,width = 22,bd=5, fg="#F5EAEA", bg="#20262E")
namee.place(x=1200,y=650)
rollno = Label(win,text='Location: Mars', font=('Arial',14,'bold'),relief=GROOVE,width = 22,bd=5, fg="#F5EAEA", bg="#20262E")
rollno.place(x=1200,y=700)

# Function to update the clock
def update_clock():
    now = datetime.datetime.now()
    clock.config(text=now.strftime("%H:%M:%S"))
    clock.after(1000, update_clock)

# Create the clock label
clock = Label(win, font=("Arial", 20),relief=GROOVE,width = 15,bd=5, fg="#F5EAEA", bg="#20262E")
clock.pack(anchor=NW, padx=150, pady=10)
clock.place(x=100,y=350)
# Create the calendar label
cal = Label(win, font=("Arial", 20),relief=GROOVE,width = 15,bd=5, fg="#F5EAEA", bg="#20262E")
cal.pack(anchor=NW, padx=150, pady=10)
cal.place(x=100,y=400)
update_clock()
cal.config(text=datetime.date.today().strftime("%B %d, %Y"))


# Mediapipe Solution Using oop and Gestures:
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
class SignLanguageConverter:
    current_gesture= None
    global CountGesture
    CountGesture = StringVar()
    def init(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.current_gesture = None
    
    def detect_gesture(self, image):
        with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.current_gesture = self.get_gesture(hand_landmarks)
    
    def get_gesture(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        index_finger_tip = hand_landmarks.landmark[8]
        middle_finger_tip = hand_landmarks.landmark[12]
        ring_finger_tip = hand_landmarks.landmark[16]
        little_finger_tip = hand_landmarks.landmark[20]

        # Check if hand is in thumbs up gesture
        if thumb_tip.y < index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < little_finger_tip.y:
            CountGesture.set('Sounds Good')
            return "Thumbs Up"

        # Check if hand is in thumbs down gesture
        elif thumb_tip.y > index_finger_tip.y > middle_finger_tip.y > ring_finger_tip.y > little_finger_tip.y:
            CountGesture.set('Not approved')
            return "Thumbs Down"
        
        # Check if hand is in stop gesture
        elif index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < little_finger_tip.y:
            CountGesture.set('Stop, right away!')
            return "Stop"

        # Check if hand is in no gesture
        elif middle_finger_tip.y < index_finger_tip.y < thumb_tip.y < ring_finger_tip.y < little_finger_tip.y:
            CountGesture.set('No, this is not possible')
            return "No"

        # Check if hand is in fist gesture
        elif little_finger_tip.y < thumb_tip.y:
            CountGesture.set('Heading into orbit')
            return "fist"
        
        else:
            wrist = hand_landmarks.landmark[0]
            index_finger_tip = hand_landmarks.landmark[8]
            index_finger = (index_finger_tip.x, index_finger_tip.y, index_finger_tip.z)
            wrist_coords = (wrist.x, wrist.y, wrist.z)
            vector = (index_finger[0] - wrist_coords[0], index_finger[1] - wrist_coords[1], index_finger[2] - wrist_coords[2])
            vector_len = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
            vector_unit = (vector[0] / vector_len, vector[1] / vector_len, vector[2] / vector_len)
            reference_vector = (0, 0, -1)  # the vector pointing towards the camera
            dot_product = vector_unit[0] * reference_vector[0] + vector_unit[1] * reference_vector[1] + vector_unit[2] * reference_vector[2]
            angle = math.acos(dot_product) * 180 / math.pi  # angle in degrees
            if 20 < angle < 80:
                CountGesture.set('Mission was successful!!')
                return "sucess"
            else:
                return None
        
    def get_current_gesture(self):
        return self.current_gesture
    
    def release(self):
        self.hands.close()

# Exit feature in GUI:
def lbl():
    global label1
    label1.destroy()
def lbl2():
    global label1
    cv2.destroyAllWindows()
    label1.destroy()

exit_label = tk.Label(win,
                      text='Exit',
                      padx=95,
                      bg="#20262E",
                      fg="#F5EAEA",
                      relief=GROOVE,  
                      width=7,
                      bd=5,
                      font=('Arial', 14, 'bold'))
exit_label.place(x=1200, y=400)

exit_label.bind("<Button-1>", lambda event: win.destroy())


# Calling of functions and solution:
sign_lang_conv = SignLanguageConverter()
cap = cv2.VideoCapture(0)
label1 = Label(bg_label, width=640, height=480)
label1.place(x=450, y=150)

def select_img():
    ret, frame = cap.read()  # Capture frame from webcam
    if not ret:
        print("Failed to grab frame")
        return

    # Flip the frame horizontally (mirror effect)
    frame = cv2.flip(frame, 1)

    sign_lang_conv.detect_gesture(frame)
    gesture = sign_lang_conv.get_current_gesture()
    if gesture:
        cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Draw landmarks on the hand
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(framergb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    
    crrgesture = Label(win, text='Current Gesture:', font=('Arial', 18, 'bold'), bd=5, bg='#20262E', width=15, fg='#F5EAEA', relief=GROOVE)
    status = Label(win, textvariable=CountGesture, font=('Arial', 18, 'bold'), bd=5, bg='#20262E', width=30, fg='#F5EAEA', relief=GROOVE)
    status.place(x=580, y=700)
    crrgesture.place(x=200, y=700)
    win.after(1, select_img)

# running the GUI
select_img()
win.mainloop()
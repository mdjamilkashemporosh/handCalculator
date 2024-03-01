import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (255, 255, 255), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 1)
        cv2.putText(img, self.value, (self.pos[0] + 27, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

equation = ""
button_last_click_times = {}

calculation_space = (10, 400, 570, 50)

button_positions = [
    (10, 10), (100, 10), (190, 10), (280, 10),
    (10, 100), (100, 100), (190, 100), (280, 100),
    (10, 190), (100, 190), (190, 190), (280, 190),
    (10, 280), (100, 280), (190, 280), (280, 280),
]

button_values = [
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '/', '.', '=',
]

buttons = [Button(pos, 80, 80, value) for pos, value in zip(button_positions, button_values)]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    current_time = time.time()
    # Draw the buttons
    for button in buttons:
        button.draw(img)

    # Draw the calculation space
    cv2.rectangle(img, (calculation_space[0], calculation_space[1]),
                  (calculation_space[0] + calculation_space[2], calculation_space[1] + calculation_space[3]),
                  (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (calculation_space[0], calculation_space[1]),
                  (calculation_space[0] + calculation_space[2], calculation_space[1] + calculation_space[3]),
                  (50, 50, 50), 1)
    cv2.putText(img, equation, (calculation_space[0] + 10, calculation_space[1] + 30), cv2.FONT_HERSHEY_PLAIN,
                1.5, (50, 50, 50), 2)

    
    
    if hands:
        if hands and 'lmList' in hands[0]:
            lmList = hands[0]['lmList']
            if len(lmList) >= 13:
                point1 = lmList[8]
                point2 = lmList[12]
                distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

                for button in buttons:
                    button_x, button_y = button.pos
                    button_width, button_height = button.width, button.height

                    if distance < 50 and button_x < point1[0] < button_x + button_width and button_y < point1[1] < button_y + button_height:
                        if button.value == '=':
                            try:
                                result = str(eval(equation))
                                equation = result
                            except:
                                equation = "Error"
                        elif button.value == 'C':
                            equation = ""
                        else:
                            # Check if enough time has passed since the last click
                            if button.value not in button_last_click_times or current_time - button_last_click_times[button.value] >= 2.0:
                                equation += button.value
                                button_last_click_times[button.value] = current_time  # Update the last click time for this button
                            
                        cv2.rectangle(img, button.pos, (button_x + button.width, button_y + button.height),
                                      (121, 63, 223), cv2.FILLED)
                        cv2.rectangle(img, button.pos, (button_x + button.width, button_y + button.height),
                                      (50, 50, 50), 3)
                        cv2.putText(img, button.value, (button_x + 27, button_y + 50), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 255, 255), 2)
                    else:
                        button.draw(img)
                        # cv2.putText(img, button.value, (button_x + 10, button_y + 25), cv2.FONT_HERSHEY_PLAIN,
                        #             1.5, (50, 50, 50), 2)
            
            # Display the equation being built
            # cv2.putText(img, equation, (calculation_space[0] + 10, calculation_space[1] + 30), cv2.FONT_HERSHEY_PLAIN,
            #             1.5, (50, 50, 50), 2)

        else:
            print("Not enough landmarks in lmList.")
    else:
        print("No hands or lmList data available.")
        if hands and 'lmList' in hands[0]:
            lmList = hands[0]['lmList']
            if len(lmList) >= 13:
                point1 = lmList[8]
                point2 = lmList[12]
                distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

                for button in buttons:
                    button_x, button_y = button.pos
                    button_width, button_height = button.width, button.height

                    if distance < 50 and button_x < point1[0] < button_x + button_width and button_y < point1[1] < button_y + button_height:
                        if button.value == '=':
                            try:
                                result = str(eval(equation))
                                equation = result
                            except:
                                equation = "Error"
                        elif button.value == 'C':
                            equation = ""
                        else:
                            # Append the button's value to the equation
                            equation += button.value
                            
                        cv2.rectangle(img, button.pos, (button_x + button.width, button_y + button.height),
                                      (0, 255, 0), cv2.FILLED)
                        cv2.rectangle(img, button.pos, (button_x + button.width, button_y + button.height),
                                      (50, 50, 50), 3)
                        # cv2.putText(img, button.value, (button_x + 10, button_y + 25), cv2.FONT_HERSHEY_PLAIN,
                        #             1.5, (50, 50, 50), 2)
                    else:
                        button.draw(img)
                        # cv2.putText(img, button.value, (button_x + 10, button_y + 25), cv2.FONT_HERSHEY_PLAIN,
                        #             1.5, (50, 50, 50), 2)
                
                # Display the equation being built
                # cv2.putText(img, equation, (calculation_space[0] + 10, calculation_space[1] + 30), cv2.FONT_HERSHEY_PLAIN,
                #             1.5, (50, 50, 50), 2)

            else:
                print("Not enough landmarks in lmList.")
        else:
            print("No hands or lmList data available.")



    cv2.imshow("Calculator", img)
        # Capture keyboard events
    key = cv2.waitKey(1)
    if key == 27:  # 'Esc' key
        equation = ""  # Reset the equation

cap.release()
cv2.destroyAllWindows()

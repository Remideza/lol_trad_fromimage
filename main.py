import math

import cv2
import pytesseract
from mss import mss
import numpy as np
import time
from PIL import Image
from numpy import asarray
from googletrans import Translator
import traceback

pytesseract.pytesseract.tesseract_cmd = r'K:\Code\Tesseract\tesseract.exe'

WINDOWPOS = [[725,873],[1100,1450]]
LINESIZE = 14
LANG_FROM_TESS = "kor"
LANG_FROM_GTRAD = "ko"
LANG_TO_GTRAD = "en"

DEBUG_WINDOW = False
DEBUG_IMAGE = False

#TODO: Better image cleaning using text colors (blue for names, white for messages, red for ennemies, yellow for private messages)
#TODO: When a message use a CRLF, the "per line" traduction is not the right method since the sentence is cutted in half thus resulting in a bad traduction
#TODO: Add a champions name reference file to better traduce champ names since they're not in google traduction references

def get_cleaned_text_img(binaryinv = True):
    if(DEBUG_IMAGE):
        # Work via a screenshot for testing
        img =  asarray(Image.open('test2.png'))
    else:
        # Grab screen directly
        img = np.array(np.array(sct.grab({'left': 0, 'top': 0, 'width': 1920, 'height': 1080})))

    array = img[WINDOWPOS[0][0]:WINDOWPOS[0][1], WINDOWPOS[1][0]:WINDOWPOS[1][1]]
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    if binaryinv:
        t, array = cv2.threshold(array, 110, 255, cv2.THRESH_BINARY_INV)

    return array


sct = mss()
translator = Translator()

#Display the current screen textline positions, if it doesn't fit perfectly, the textbox might have been moved, try fiddling with config
#Each screen display must show a different line of the text
screen = get_cleaned_text_img(False)
cv2.imshow('preview', screen)
cv2.waitKey(3000)

for i in range(screen.shape[0], 0, -LINESIZE):
    screen_as_np = screen[i - LINESIZE:i, 0:WINDOWPOS[1][1] - WINDOWPOS[1][0]]
    if i - LINESIZE < 0:
        break
    cv2.imshow('preview', screen_as_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1)

cv2.destroyAllWindows()
print("Starting the main loop")
time.sleep(5)

#Main loop
while True:
    try:
        screen = get_cleaned_text_img()
        printlines = False
        textlines = []
        #Splitting the text in lines for better traduction
        for i in range(screen.shape[0],0,-LINESIZE):
            screen_as_np = screen[i-LINESIZE:i,0:WINDOWPOS[1][1]-WINDOWPOS[1][0]]
            screen_as_np = np.pad(screen_as_np, pad_width=20, mode='constant', constant_values=255)
            if i-LINESIZE<0:
                break

            text = pytesseract.image_to_string(screen_as_np, lang=LANG_FROM_TESS)
            # cleaning the line from chariots and bad parentheses detection
            text = text.replace('\n','').replace('\r','')
            if (text):
                #Splitting the line into 3 parts (summoner name, champion name, text) if possible, to traduce with more precision
                if ')' in text:
                    line = ""
                    msgt = text.split(')')[1]

                    if msgt != None and msgt != text:
                        headername = text.replace(msgt,'')
                        if "(" in headername:
                            summname, champname = headername.split('(')[0], headername.split('(')[1].replace(')','')
                            if summname != headername or champname != headername:
                                line = translator.translate(summname, src=LANG_FROM_GTRAD, dest=LANG_TO_GTRAD).text.replace('\n','').replace('\r','') + \
                                    "(" + translator.translate(champname, src=LANG_FROM_GTRAD, dest=LANG_TO_GTRAD).text.replace('\n','').replace('\r','') + ") : "
                            else:
                                line = translator.translate(headername, src=LANG_FROM_GTRAD, dest=LANG_TO_GTRAD).text.replace('\n','').replace('\r','') + " : "
                            line += translator.translate(msgt, src=LANG_FROM_GTRAD, dest=LANG_TO_GTRAD).text.replace('\n', '').replace('\r', '')
                    textlines = [line] + textlines
                else:
                    textlines = [translator.translate(text, src=LANG_FROM_GTRAD, dest=LANG_TO_GTRAD).text.replace('\n','').replace('\r','')] + textlines
                printlines=True
            else:
                textlines = [""] + textlines

            if(DEBUG_WINDOW):
                cv2.imshow('i', screen_as_np)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(1)

        if printlines: #Don't print if no text detected
            print("----------------------------------------------------------------------------------------------------------")
            for l in textlines:
                print(l)
            print("----------------------------------------------------------------------------------------------------------")
            time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
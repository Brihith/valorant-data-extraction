import time, numpy as np, pyautogui as py, cv2 as cv, pandas as pd, easyocr

reader = easyocr.Reader(['en'])

def analyze(rounds):
    return_value1, return_value2 = rounds_ss(rounds)
    rounds = pd.DataFrame(columns=['first_kill','time','opponent','planted','round_win'])

    first_kills = [list[0] for list in return_value1]
    rounds['time'] = first_kills

    plant = [list[0].lower() for list in return_value2]

    # rounds['planted'] = plant
    # planted = rounds['planted'].astype(str).query('planted')
    # rounds['planted'] = planted
    # print(rounds)

def rounds_ss(total_rounds):

    """ This function will go to the timeline page of the match in question and screenshot every page of the timeline.
    It will then run the OCR function for all the rounds in the match as specified and append them  to a list. This
    list will be returned to the analyze function. """

    time.sleep(2)
    py.leftClick(x=1020, y=190, duration=0.37)
    py.leftClick(x=187, y=333, duration=0.37)
    tl_ss = []
    time.sleep(0.5)


    for i in range(total_rounds):

        py.moveRel(56, 0, duration=0.12)
        py.leftClick()

        if i == 11:
            py.moveRel(-20, 0, duration=0.2)
            continue

        image = py.screenshot()
        cv_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
        tl_ss.append(cv_image)

        time.sleep(0.15)

    # The preprocessing and ocr can either be done in this function or another.
    image = py.screenshot()
    cv_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    tl_ss.append(cv_image)

    timestamps, plants = rounds_ocr(tl_ss)

    return timestamps, plants



def scoreboard_ocr():

    """Any preprocessing or other shenanigans here. And then perform OCR and return match metadata, individual player
        stats aswell as match score / outcome. This can be a data frame. Also distinctly return total no of rounds."""

    py.leftClick(x=875, y=190, duration=0.35)
    scoreboard_ss = py.screenshot()
    scoreboard_ss = cv.cvtColor(np.array(scoreboard_ss), cv.COLOR_RGB2BGR)

    # return

def rounds_ocr(all_round_images):

    """Perform OCR And preprocessing of all the rounds to extract, which player got the first kill, when they get it
    if the spike was planted or not. Possibly in a dataframe?"""

    all_round_images_cropped = [images[505:970, 980:1040] for images in all_round_images]
    timestamps = [reader.readtext(image, detail=0) for image in all_round_images_cropped]

    all_round_images_cropped_plants = [images[505:970,1150:1230] for images in all_round_images]
    plants = [reader.readtext(image, detail=0) for image in all_round_images_cropped_plants]

    # Perform your preprocessing and OCR here. If all preprocessing is the same, we can make that a seperate function.
    return timestamps, plants

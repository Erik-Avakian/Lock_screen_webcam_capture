"""
This script puts you in lockscreen and captures pictures from your webcam
It then makes one of those pictures your lockscreen wallpaper!
"""

import os
import time
import ctypes
from random import choice

import cv2


def change_lock_screen_image(image_dir: str, executable: str) -> None:
    """Sets a random image from a folder as a lockscreen wallpaper"""

    list_of_images: list[str] = os.listdir(image_dir)

    # Pick one file
    image: str = choice(list_of_images)
    path_to_file: str = f"{image_dir}\\{image}"

    # Set lockscreen image to an image
    os.system(f"{executable} setlockimage {path_to_file}")


def lock_screen() -> None:
    """Just locks the screen"""

    ctypes.windll.user32.LockWorkStation()


def capture_webcam(image_dir) -> None:
    """Captures 3 pictures and saves it to a directory"""

    # Define a video capture object
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # pylint:disable=no-member

    beautify = 1

    while beautify < 2:
        # Capture the video frame
        # By frame
        ret, frame = cam.read()

        if not ret:
            raise ValueError("No Ret")

        for i in range(3):
            cv2.imwrite(  # pylint:disable=no-member
                f"{image_dir}\\image_{i}.jpeg", frame
            )
            time.sleep(0.3)  # to make each picture wait a bit
        beautify += 1

    cam.release()
    cv2.destroyAllWindows()  # pylint:disable=no-member


def main(cwd: str, image_dir: str, executable: str) -> None:
    """
    Main loop

    Locks the screen
    Takes 3 pictures
    Changes lockscreen wallpaper
    """
    # Lock the screen
    lock_screen()

    capture_webcam(image_dir)

    # Remove this if you don't want the "Nice Try" pictures before webcam pics
    for troll in [f"{cwd}\\nice.jpg", f"{cwd}\\try.jpg"]:
        os.system(f"{executable} setlockimage {troll}")

    change_lock_screen_image(image_dir, executable)


if __name__ == "__main__":
    CURRENT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIRECTORY: str = f"{CURRENT_DIRECTORY}\\webcam_captures"
    EXECUTABLE: str = f"{CURRENT_DIRECTORY}\\igcmdWin10.exe"

    # Create directory if it does not already exist
    if "webcam_captures" not in os.listdir(CURRENT_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    main(cwd=CURRENT_DIRECTORY, image_dir=IMAGE_DIRECTORY, executable=EXECUTABLE)

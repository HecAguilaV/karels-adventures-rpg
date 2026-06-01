import json
from notopenai import NotOpenAI
import os
from graphics import Canvas

# go to cs106a.stanford.edu/notopenai and get your free api key
CLIENT = NotOpenAI(api_key="your_api_key_here")
STORY_NAME = "original_big"
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Infinte Story")
    print("Infinite Story")
    # TODO: your code here

def show_illustration(canvas, scene_key):

    illustration_path = f"img/{scene_key}.jpg"
    if os.path.exists(illustration_path):
        canvas.clear()
        canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, illustration_path)
        canvas.create_rectangle(0, CANVAS_HEIGHT - 32, 200, CANVAS_HEIGHT, color="#ffffff")
    else:
        canvas.clear()
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "black")
        canvas.create_rectangle(80, 80,
                                CANVAS_WIDTH - 80,
                                CANVAS_HEIGHT - 80,
                                color = "lightblue")



if __name__ == "__main__":
    main()

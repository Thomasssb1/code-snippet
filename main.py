from io import StringIO
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from PIL import ImageColor

from lexical_analysis import LexicalAnalysis
from config_file import configFile
from color import Color

import numpy as np
import streamlit as st


def main(file, state, **kwargs) -> Image:
    state.set_state("running")
    with state.container:
        if file is None:
            return
        # Padding all around the text in px
        PADDING = kwargs["padding"]

        st.write("Setting up the configurations...")
        font = ImageFont.truetype("config/CascadiaCode.ttf", 16)

        if "isCli" in kwargs.keys() and kwargs["isCli"]:
            f = open(file, "r")
        else:
            f = StringIO(file.getvalue().decode("utf-8"))

        config_file = configFile("config/config.json", kwargs["language"])

        image = Image.new("RGB", (PADDING, PADDING), color=config_file.background.color)
        d = ImageDraw(image)

        st.write("Performing lexical analysis...")
        text = f.read()
        lex = LexicalAnalysis(text, config_file)

        print(kwargs["between_lines"])
        cleaned_text = lex.preprocess(between_lines=kwargs["between_lines"])
        tokens = lex.tokenisation(cleaned_text, config_file)

        st.write("Generating the image...")
        bbox = d.multiline_textbbox(xy=(0, 0), text=cleaned_text, font=font)
        image = image.resize((bbox[2] + (PADDING * 2), bbox[3] + (PADDING * 2)))
        d = ImageDraw(image)

        last_point = (PADDING, PADDING)

        for i in range(0, len(tokens)):
            token = tokens[i]

            text_bbox = d.textbbox(xy=last_point, text=token[1], font=font)

            x = text_bbox[2]
            y = last_point[1]

            if i + 1 < (len(tokens) - 1) and "\n" in tokens[i + 1][1]:
                x = PADDING
                y = text_bbox[3]

            d.text(
                xy=last_point,
                text=token[1],
                fill=(0, 0, 0) if not isinstance(token[0], Color) else token[0].color,
                font=font,
            )
            last_point = (x, y)

        image.save("test.png", "PNG")

        state.set_text("Success!")
        return image


if __name__ == "__main__":
    main()

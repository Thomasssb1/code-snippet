from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw

from lexical_analysis import LexicalAnalysis
from config_file import configFile

def main():
    # Padding all around the text in px
    PADDING = 15
    
    image = Image.new("RGB", (PADDING, PADDING), (255, 255, 255))

    font = ImageFont.load_default()
    d = ImageDraw(image)

    with open("test.java", "r") as f:
        text = f.read()

        config_file = configFile("config/styles.json")
        lex = LexicalAnalysis(text, config_file)
        cleaned_text = lex.preprocess()
        print(cleaned_text)

        bbox = d.multiline_textbbox(xy=(0,0), text=cleaned_text, font=font)
        image = image.resize((bbox[2] + (PADDING*2), bbox[3] + (PADDING*2)))
        d = ImageDraw(image)
        d.multiline_text((PADDING, PADDING), cleaned_text, (0,0,0), font=font)
    
        image.save("test.png", "PNG")

if __name__ == "__main__":
    main()
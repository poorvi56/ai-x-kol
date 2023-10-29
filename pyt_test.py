#!/usr/bin/python3

import cv2
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

example_image = "images/img_test.jpg"


def kerasread():
    import keras_ocr as ko
    kimg = [ko.tools.read(example_image)]
    pipeline = ko.pipeline.Pipeline(scale=1)

    predict = pipeline.recognize(kimg)

    pred_img = predict[0]
    return pred_img

def pytessread():
    import pytesseract as pyt
    
    pyt.pytesseract_cmd = "pyt"

    img = cv2.imread(example_image)
    img = cv2.resize(img, (800,800))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pyt.image_to_string(gray)
    return text

database = "db/brand_list.txt"
beanie = ["Baby Boucle", "Patons Bamboo Baby", "Bernat Giggles", "Bernat Li'l Tots", "Bernat Softee Baby", "Bernat Satin", "Bernat Satin Sport"
          "Caron Simply Soft", "Comfy Worsted Cotton Blend", "I Love This Cotton", "K+C Element and Essentials", "Lion Basic Stitch Anti-Pilling"
          "Lion Feels Like Butta", "Lion Flikka", "Lion Fun Fur", "Lion Heartland", "Lion Heartland Tweed", "Lion Jeans", "Lion Landscapes"
          "Lion Mandala Ombre", "Lion Pima Cotton", "Loops & Threads Charisma Baby", "Loops & Threads Coastal Cotton", "Loops & Threads Soft & Shiny"
          "Main Street Yarns Shiny", "Main Street Yarns Soft", "Premier Basix Marls", "Premier Everyday", "Prepier Cotton Batik", "Premier Cotton Sprout"
          "Premier Puzzle Cotton", "Premier Sweet Roll", "Red Heart Buttercup", "Red Heart Colorscape", "Red Heart GumDrop", "Red Heart Soft"
          "Red Heart Soft Baby Steps", "Red Heart Sweet Baby", "Shine Worsted Cotton Blend", "Yarn Bee Aurora Borealis", "Yarn Bee Denim in Color"
          "Yarn Bee Fur-Even Style", "Yarn Bee Glowing", "Yarn Bee Soft & Sleek", "Yarn Bee Soft Secret", "Yarn Bee Sugar Wheel"]
blanket = ["Berroco Comfort", "Bernat Softee Baby", "Baby Bee Sweet Delights", "Caron Simply Soft", "Cascade Avalon", "Cascade Cherub Aran"
           "Cascade Sunseeker Shade", "King Cole Cotton Soft DK", "Knit One Crochet Two Baby Boo", "Lion Baby Soft", "Loops & Threads Snuggly Wuggly"
           "Main Street Yarns Shiny + Soft", "Plymouth Dream Baby", "Plymouth Dream DK", "Plymouth Dream Paintpot", "Plymouth ToyBox Collection Candy"
           "Premier Anti-Pilling Everyday Baby", "Sirdar Snuggly Bunny", "Sirdar Snuggly DK"]

ratios = []



if __name__ == "__main__":
    print(len(beanie))
    print(len(blanket))

    yarn_type = int(input("Beanie(1) or Blanket(2):  "))
    print("Using pytesseract")
    text = pytessread()
    if text != '':
        comp = text.split('\n')
        fcomp = [string for string in comp if string!=""]
        print("Input text fields:", fcomp)

        ratios = []

        for s in fcomp:
            ratios.append(process.extractOne(s, database))
        print("Final Ratios:", ratios)
        match = max(ratios)
        print("Final Match:", match)
    else:
        print("pytesseract failed")
            
        print("Using keras")
        pred_img = kerasread() 
        out = []

        for text, box in pred_img:
            print(text)
            if text == '':
                print("keras failed")
            out.append(text)

        for s in out:
            ratios.append(process.extractOne(s, blanket))
        print("Final Ratios:", ratios)
        match = max(ratios)
        print("Final Match:", match[0])

    confirm = input("is this your yarn")
    if confirm == "n":
        print("no match found")
    else:
        if yarn_type == 1:
            if match[0] in beanie:
                types = "beanies"
                print(match[0] + " is good for " + types)
            else:
                print("Try another yarn")
        else:
            if match[0] in blanket:
                types = "blankets"
                print(match[0] + " is good for " + types)
            else:
                print("Try another yarn")

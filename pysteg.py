from Steg import *
import optparse
import os
import sys

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option("-e", "--encrypt", dest="hide", action="store_true", help="Hide the Text in Image", default=False)
    parser.add_option("-d", "--decrypt", dest="unhide", action="store_true", help="Retrieve the Text in Image", default=False)
    parser.add_option("-f", "--image", dest="img_file", type="string", help="Target Picture to Hide/Retrieve Text")
    parser.add_option("-p", "--path", dest="path", type="string", default=".", help="Destination of the Target Image")

    opt, args = parser.parse_args()
    return opt, parser

def validate(hide, unhide, image_file, path):
    if not hide and not unhide:
        return False
    if hide == unhide:
        return False
    if len(image_file) < 5:
        return False
    if len(path) <= 0:
        return False

    return True

def main():
    options, parser = parse_args()
    
    hide = options.hide
    unhide = options.unhide
    img_file = options.img_file
    path = options.path
    
    isvalid = validate(hide, unhide, img_file, path)

    if not isvalid:
        print("Invalid Usage!")
        parser.usage
        sys.exit(1)
    else:
        img_file_path = os.path.join(path, img_file)
        steg = Steg(img_file_path)

        if hide == True:
            message = input("Enter the Text to hide into the given Image: ")
            res = steg.hide(message)
            
            if res != True:
                print("Error occured in Hiding the Text!")
                print(res)
                sys.exit(1)

        if unhide == True:
            result = steg.retrieve()
            result = result.decode() if type(result) == bytes else result
            print(result)

if __name__ == "__main__":
    main()

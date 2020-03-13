from PIL import Image
import os
import sys

def convert(file_name, path, op_file):
    img_path = os.path.join(path, file_name)

    try:
        img = Image.open(img_path)
        img.save(os.path.join(path, op_file + ".png"))
    except Exception as err:
        print(err)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 3:
        print("Invalid number of arguments!")
        print("Usage: python3 %file file_name path output_file_name")
        sys.exit(1)

    convert(args[0], args[1], args[2])



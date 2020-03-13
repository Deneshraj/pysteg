from PIL import Image
import binascii

class Steg:
    def __init__(self, img_file):
        self.file_name = img_file
        self.img = Image.open(img_file)
        self.delimiter = str("1" * 15 + "0")

    def rgb_hex(self, red, green, blue):
        """Converts the RGB value to HEX code"""
        return "#{:02x}{:02x}{:02x}" . format(red, green, blue)
    
    def hex_rgb(self, hexcode):
        """Returns the RGB value of the corresponding HEX code"""
        hexcode = hexcode.lstrip("#")
        rgb = tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))
        return rgb

    def str_bin(self, msg):
        """Converts the Given String Message to Binary Form"""
        msg = msg.encode()
        return bin(int(binascii.hexlify(msg), 16))[2:]

    def bin_str(self, binary):
        """Converts the Given Binary string to Original message"""
        if binary == "":
            return "No Data found on the Image"
        message =  binascii.unhexlify("%x" %(int("0b" + binary, 2)))
        return message

    def encode(self, hexcode, digit):
        """Encodes the Given digit into the hexcode"""
        max_val_tuple = tuple(str(x) for x in range(0, 6))
        if hexcode[-1] in max_val_tuple:
            return hexcode[:-1] + digit
        
        return None

    def decode(self, hexcode):
        """Decodes and gives the Original Binary String from the Hexcodes"""
        if hexcode[-1] in ('0', '1'):
            return hexcode[-1]
        
        return None

    def hide(self, message):
        binary = self.str_bin(message) + self.delimiter
        try:
            self.img = self.img.convert("RGBA")
        except Exception as e:
            pass
        
        if self.img.mode == ("RGBA"):
            datas = self.img.getdata()

            new_data = []
            digits = 0

            is_writeable = self.is_data_writeable(datas, len(binary))
            if not is_writeable:
                return "Can't Write the Data to the Image!"
            
            for item in datas:
                if digits < len(binary):
                    hex_code = self.rgb_hex(item[0], item[1], item[2])
                    new_pix = self.encode(hex_code, binary[digits])

                    if new_pix == None:
                        new_data.append(item)
                    else:
                        red, green, blue = self.hex_rgb(new_pix)
                        new_data.append((red, green, blue, 255))
                        digits += 1

                else:
                    new_data.append(item)

            self.img.putdata(new_data)
            self.img.save(self.file_name, "PNG")

            return True

        return "Incorrect Type of Image or Incorrect Mode, Couldn't Hide..."
    
    def retrieve(self):
        binary = ""
        try:
            self.img = self.img.convert("RGBA")
        except Exception as e:
            pass

        if self.img.mode == ("RGBA"):
            self.img = self.img.convert("RGBA")
            datas = self.img.getdata()

            for item in datas:
                hex_code = self.rgb_hex(item[0], item[1], item[2])
                digit = self.decode(hex_code)

                if digit != None:
                    binary += digit

                    if binary[-16:] == self.delimiter:
                        return self.bin_str(binary[:-16])
                    
            return self.bin_str(binary[:-16])

        return "Incorrect Type of Image or Incorrect Mode, Couldn't Hide..."

    def is_data_writeable(self, datas, bin_data_len):
        data_len = bin_data_len

        for item in datas:
            hex_code = self.rgb_hex(item[0], item[1], item[2])
            if hex_code[-1] in ('0', '1', '2', '3', '4', '5'):
                data_len -= 1

            if data_len == 0:
                return True
        return False

# def main():
#     file_name = input("Enter the Image File to Hide the Message in: ")
#     steg = Steg(file_name)
#     message = input("Enter the Message to Hide: ")
#     res = steg.hide(message)

#     if res == True:
#         print("Successfully Hidden!")
#         print("Decoding...")
        
#         unhidden = steg.retrieve()
#         print(unhidden)
#     else:
#         print(res)


# if __name__ == "__main__":
#     main()
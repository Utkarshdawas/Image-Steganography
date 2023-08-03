from PIL import Image
import numpy as np
import sys
import codecs
from encrypt import encrypt_text, decrypt_text

def to_utf(data):
    Unicode_data = ''
    for d in data:
        binary_int = int(d,2)
        byte_number = binary_int.bit_length() + 7 
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode("utf-8", 'ignore')       
        
        Unicode_data = Unicode_data + ascii_text        

    return Unicode_data

def encode(image,data):
   
    arr = np.array(image)
    # print(arr.shape)
    
    red = arr[..., 0]  
    green = arr[..., 1]  
    blue = arr[..., 2]  
    
    height,width = red.shape
    bluePending = True
    greenPending = True
    redPending = True

    i = 0
    j = -1
    count = 0
    c = 0
    for char in data:
        for bit in char:  
            count += 1
            if bluePending == True:
                if i < height:
                    if j < width:                       
                        j+=1     
                    if j >= width:
                        i+=1
                        j=0
                        
                    if i < height:
                        if bit=='1':
                            blue[i][j] = blue[i][j] | 1 
                        elif bit=='0':
                            blue[i][j] = blue[i][j] & (blue[i][j] -1)   
                        c += 1  
                    else:
                        bluePending = False
                        i = 0
                        j = -1
       
                else:
                    bluePending = False  
                    i = 0
                    j = -1                                                              
                
            if bluePending == False and redPending == True:
                if i < height:
                    if j < width:                        
                        j+=1
                    if j >= width:
                        i+=1
                        j=0   
                        
                    if i < height:
                        if bit=='1':
                            red[i][j] = red[i][j] | 1 
                        elif bit=='0':
                            red[i][j] = red[i][j] & (red[i][j] -1) 
                        c += 1
                    else:
                        redPending = False
                        i = 0
                        j = -1                    
                    
                else:
                    redPending = False  
                    i = 0
                    j = -1
            if bluePending == False and redPending == False:
                if i < height:
                    if j < width:                        
                        j+=1
                    if j >= width:
                        i+=1
                        j=0   
                        
                    if i < height:
                        if bit=='1':
                            green[i][j] = green[i][j] | 1 
                        elif bit=='0':
                            green[i][j] = green[i][j] & (green[i][j] -1) 
                        c += 1
                    else:
                        greenPending = False  
                        sys.exit("More Pixels!")       
                else:
                    greenPending = False  
                    i = 0
                    j = -1
                    break
                  
    if greenPending == False:
        sys.exit("More Pixels! ")        

    w, h = image.size
    test = np.zeros((h, w, 3), dtype=np.uint8)
    
    test[:,:,0] = red
    test[:,:,1] = green
    test[:,:,2] = blue

    filename = (str("encoded_image") +'.jpg')
    img = Image.fromarray(test, 'RGB')    
    img.save('./'+ filename)
    # img.show()    
    print(f"Image Steganography is complete and the generated image is '{filename}'")
    return [img, count]


def decode(image, count):  
    # image.show()  
    arr = np.array(image)
    red = arr[..., 0]  
    green = arr[..., 1]
    blue = arr[..., 2] 

    height,width = red.shape
    total_size = height*width
    data = []
    data_len = 0
    data_byte = ''

    if count < total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if data_len < 8:
                        data_byte = data_byte + str((blue[i][j] & 1))
                        data_len+=1
                    else:
                        data.append(data_byte)                        
                        data_len = 0
                        data_byte = '' 

                        data_byte = data_byte + str((blue[i][j] & 1))
                        data_len+=1
                        
                    new_count+=1
                else:
                    break

    elif count > total_size and count < 2*total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):                                    
                if data_len < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    data_len+=1
                else:
                    data.append(data_byte)                        
                    data_len = 0
                    data_byte = '' 

                    data_byte = data_byte + str((blue[i][j] & 1))
                    data_len+=1
        data_len = 0
        data_byte = ''                                                        
                
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if data_len < 8:
                        data_byte = data_byte + str((red[i][j] & 1))
                        data_len+=1
                    else:
                        data.append(data_byte)                        
                        data_len = 0
                        data_byte = '' 

                        data_byte = data_byte + str((red[i][j] & 1))
                        data_len+=1
                        
                    new_count+=1
                else:
                    break
    else: 
        new_count = 0
        for i in range(height):
            for j in range(width):                                    
                if data_len < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    data_len+=1
                else:
                    data.append(data_byte)                        
                    data_len = 0
                    data_byte = '' 

                    data_byte = data_byte + str((blue[i][j] & 1))
                    data_len+=1
        data_len = 0
        data_byte = ''

        for i in range(height):
            for j in range(width):                                    
                if data_len < 8:
                    data_byte = data_byte + str((red[i][j] & 1))
                    data_len+=1
                else:
                    data.append(data_byte)                        
                    data_len = 0
                    data_byte = '' 

                    data_byte = data_byte + str((red[i][j] & 1))
                    data_len+=1
        data_len = 0
        data_byte = ''                                                        
                
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if data_len < 8:
                        data_byte = data_byte + str((green[i][j] & 1))
                        data_len+=1
                    else:
                        data.append(data_byte)                        
                        data_len = 0
                        data_byte = '' 

                        data_byte = data_byte + str((green[i][j] & 1))
                        data_len+=1
                        
                    new_count+=1
                else:
                    break    
                
    utf_data = to_utf(data)
    tmp = utf_data.replace('\0','')    
    return tmp

def to_binary(data):
    bin_data = []

    for i in data:
        bin_data.append(format(ord(i), '08b'))
    
    return bin_data

###################################################################################################
# Driver Code

# Encoding
#secret = input("Enter the secret:\n")
def main():
    print()
    with open('./input.txt', 'r') as file:
        text = file.read()
    key = bytes(input("Enter Key to encrypt the input file (24 char long) -  "), "utf-8")
    cipher_text = encrypt_text(key, text)
    data = to_binary(cipher_text)

    image =  Image.open("./input_image.jpg",'r')
    encoded_img, saveCount = encode(image, data)
    print("Please save key (Number of bits in the text) - ", saveCount)
    print()

    # Decoding
    image2 =  Image.open("./encoded_image.jpg",'r')
    count2 = int(input("Enter the key to decode the text from the given encoded image - "))
    decoded_data = decode(encoded_img, count2)
    plain_text = decrypt_text(key, decoded_data)

    file = codecs.open('./decoded.txt', 'w')
    file.write(plain_text)

    print("Decoded Message Saved in 'decoded.txt' file")
    file.close()
    print()

if __name__ == "__main__":
    main()
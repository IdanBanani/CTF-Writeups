from Crypto.Util.strxor import strxor_c
import base64

with open("ciphertext") as f:
    text = f.read()
    text = base64.b64decode(text)

    ans =''.join([chr(255 - c_int) for c_int in text])
    print(ans)
    # print(strxor_c(base64.b64decode(text), 0xFF))


    # 255

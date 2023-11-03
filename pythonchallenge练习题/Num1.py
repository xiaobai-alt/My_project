# import requests
#
# for i in range(0, 239):
#     url = f'http://www.pythonchallenge.com/pc/def/{i}.html'
#
#     resp = requests.get(url)
#     while resp.status_code == 200:
#         print(resp.url)
#         break

# b = 2**38
# print(b)


# str1 = "map"
# str2 = ''
# for s in str1:
#     if ord(s) == 32:
#         str2 += s
#     elif ord('a') <= ord(s) <= ord('z'):
#         s = chr(ord('a') + (ord(s) - ord('a') + 2) % 26)
#         str2+=s
# print(str2)
# import requests
#
# url = 'http://www.pythonchallenge.com/pc/def/ocr.html'
#
# resp = requests.get(url).text
# print(resp)


# rm = b"""{}!@#$%^&*()_-+=[]\n"""
# str4 = str1.translate(None, rm)
# print(str4)

txt = open('./txt文本/1.txt', mode='r').read().replace('\n', '')
txt1 = txt.split('')
print(txt1)
# for i in range(0, len(txt)):
#     if txt[i].islower():
#         for j in range(1, 4):
#             if (i+j) < len(txt):

                # translateTABLE = txt.maketrans(txt[i+j], txt[i+j].upper())
                # txt = txt.translate(translateTABLE)

    # n = txt.index(i)
    # for j in range(3):
    #     n -= 1
    #     if n >= 0:
    #         txt[n].upper()

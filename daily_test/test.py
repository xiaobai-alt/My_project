import random

def can_form_palindrome(word):
    # 在此处编写你的代码
    l1 = list(word.strip())
    i = 0
    while 1:
        random.shuffle(l1)
        print(l1)
        l2 = l1.copy()
        l1.reverse()
        if i == 30:
            return False
            break
        if l2 == l1:
            return True
            break
        else:
            i += 1
            continue

    # word1 = ''.join([i for i in l1])
    # if word1 == word:
    #     return True
    # else:



# 从用户处获取输入
word = input()
# 调用函数
print(can_form_palindrome(word))

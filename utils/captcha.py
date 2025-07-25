import random

def generate_captcha():
    a = random.randint(1,10)
    b = random.randint(1,10)

    return f"{a} + {b}", str(a+b)
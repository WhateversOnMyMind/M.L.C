import numpy as np
key_value = 0

def multiply(input, weights):
    return np.dot(input, weights)

def near_half(shape, std=0.1):
    arr = np.random.normal(0.5, std, size=shape)
    arr = np.clip(arr, 0, 1)
    return arr

def initial():
    w1 = near_half((5, 4))
    b1 = near_half(4) - 0.7   #평균 -0.2
    w2 = near_half((4, 3))
    b2 = near_half(3) - 0.7
    w3 = near_half((3, 4))
    b3 = near_half(4) - 0.7
    return w1, b1, w2, b2, w3, b3

def forward(input, weights):
    w1, b1, w2, b2, w3, b3 = weights
    layer1 = np.tanh(multiply(input, w1) + b1)
    layer2 = np.tanh(multiply(layer1, w2) + b2)
    output = np.tanh(multiply(layer2, w3) + b3)
    return output

def active(output):
    up = output[0] > 0.2
    down = output[1] > 0.5
    left = output[2] > 0.4
    right = output[3] > 0.4
    
    # 동시에 둘 다 True인 경우 정리
    if up and down:
        if output[0] + 0.2 > output[1]:
            down = False
        else:
            up = False
   
    if left and right:
        if output[2] > output[3]:
            right = False
        else:
            left = False
    
    return up, down, left, right


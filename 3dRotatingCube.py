from math import sin, cos, tan
import time
import os
import sys

cubeWidth=30.0
width=80
height=44
backgroundASCIICode=' '
distanceFromCam=100
K1=40

buffer=[backgroundASCIICode for _ in range(width*height)]
zBuffer=[0 for _ in range(width*height*4)]

def usleep(microseconds):
    time.sleep(microseconds / 1000000.0)

def float_range(start, stop, step): # making for sentence easier
    while start < stop:
        yield start
        start += step

def calculateX(i, j, k, A, B, C):
    return j * sin(A) * sin(B) * sin(C) - k * cos(A) * sin(B) * cos(C) \
        + j * cos(A) * sin(C) + k * sin(A) * sin(C) + i * cos(B) * cos(C) 

def calculateY(i, j, k, A, B, C):
    return j * cos(A) * cos(C) + k * sin(A) * cos(C) - j * sin(A) * sin(B) * sin(C) \
        + k * cos(A) * sin(B) * sin(C) - i * cos(B) * sin(C)

def calculateZ(i, j, k, A, B, C):
    return k * cos(A) * cos(B) - j * sin(A) * cos (B) + i * sin(B)

def calculateForPoint(i, j, k, ch, A, B, C):
    global buffer, zBuffer
    x = calculateX(i, j, k, A, B, C)
    y = calculateY(i, j, k, A, B, C)
    z = calculateZ(i, j, k, A, B, C) + distanceFromCam
    ooz = 1 / z
    xp = int(width / 2 + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)
    idx = xp + yp * width

    if ((idx >= 0) & (idx < width * height)):
        if ooz > zBuffer[idx]:
            zBuffer[idx] = ooz
            buffer[idx] = ch

def main():
    global buffer, zBuffer
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    # 시작할 때 딱 한 번만 화면을 전체 청소합니다.
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()

    A=0
    B=0
    C=0

    while 1:
        buffer[:] = [backgroundASCIICode for _ in range(width * height)]
        zBuffer[:] = [0.0 for _ in range(width * height)]
        for i in float_range(-cubeWidth/2, cubeWidth/2, 0.60):
            for j in float_range(-cubeWidth/2, cubeWidth/2, 0.60):
                calculateForPoint(i, j, -cubeWidth / 2, '@', A, B, C)
                calculateForPoint(cubeWidth / 2, j, i, '$', A, B, C)
                calculateForPoint(-cubeWidth / 2, j, -i, '~', A, B, C)
                calculateForPoint(-i, j, cubeWidth / 2, '#', A, B, C)
                calculateForPoint(i, -cubeWidth / 2, -j, ';', A, B, C)
                calculateForPoint(i, cubeWidth /2, j, '+', A, B, C)
        

        sys.stdout.write("\x1b[H\x1b[?25l")
        
        output = []
        for k in range(width * height):
            if k % width == 0 and k != 0:
                output.append('\n')
            output.append(buffer[k])

        print(''.join(output), end='', flush=True)   
    
        A += 0.05
        B += 0.05
        C += 0.05
        usleep(8000 * 2)
    
    return 


if __name__ == '__main__':
    main()
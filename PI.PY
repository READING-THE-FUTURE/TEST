# PI = 16*atan(1/5) - 4*atan(1/239)

DIGITS = 24          # 小数位
BASE = 256
SIZE = 12            # 50字节≈120十进制位

def add(a,b):
    c=0
    for i in range(SIZE):
        t=a[i]+b[i]+c
        a[i]=t&255
        c=t>>8

def sub(a,b):
    c=0
    for i in range(SIZE):
        t=a[i]-b[i]-c
        if t<0:
            t+=256
            c=1
        else:
            c=0
        a[i]=t

def mul_small(a,n):
    c=0
    for i in range(SIZE):
        t=a[i]*n+c
        a[i]=t&255
        c=t>>8

def div_small(a,n):
    r=0
    for i in range(SIZE-1,-1,-1):
        t=(r<<8)+a[i]
        a[i]=t//n
        r=t%n

def copy(a):
    return bytearray(a)

def make_scale():
    x=bytearray(SIZE)
    x[0]=1
    for _ in range(DIGITS):
        mul_small(x,10)
    return x

def atan_inv(k):
    s=bytearray(SIZE)

    term=make_scale()
    div_small(term,k)

    n=1
    sign=1

    while True:

        if max(term)==0:
            break

        t=copy(term)
        div_small(t,n)

        if sign>0:
            add(s,t)
        else:
            sub(s,t)

        div_small(term,k*k)

        n+=2
        sign=-sign
        print(n)

    return s

a=atan_inv(5)
b=atan_inv(239)

mul_small(a,16)
mul_small(b,4)

sub(a,b)

# 输出十进制
v=0
for i in range(SIZE-1,-1,-1):
    v=(v<<8)+a[i]

s=str(v)
print(s[:-DIGITS]+"."+s[-DIGITS:])
def f(a, *, b):
    print(a+b)


f(10, 20)
f(a=10, b=20)
f(10, b=20)

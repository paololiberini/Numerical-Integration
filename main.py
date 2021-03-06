import numpy as np
import matplotlib.pyplot as plt
from sympy import *


# Set 'x' as symbol for math functions
x = Symbol('x')


# Second derivative function
def secondDerivative(function, value):

    for i in range(0, 2): 
        function = function.diff(x)

    function = lambdify(x, function) 

    value = function(value) 

    return value


# Fourth derivative function
def fourthDerivative(function, value):

    for i in range(0, 4): 
        function = function.diff(x)

    function = lambdify(x, function)  

    value = function(value)  

    return value


# Trapezoidal rule plot function
def trapeziPlot(functionLambda, a, b, n, xValues):

    X = np.linspace(a, b, 100)  
    Y = functionLambda(X)   
    plt.plot(X, Y)  

    for i in range(n): 
        xs = [xValues[i], xValues[i], xValues[i + 1], xValues[i + 1]]      
        ys = [0, functionLambda(xValues[i]), functionLambda(xValues[i + 1]), 0]
        plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2)

    plt.show()


# Simpson rule plot function
def simpsonPlot(functionLambda, a, b, n, xValues):

    X = np.linspace(a, b, 100)  
    Y = functionLambda(X)
    plt.plot(X, Y)

    for i in range(0, len(xValues) - 1): 
        
        xp = np.linspace(xValues[i], xValues[i + 1], 3)
        yp = functionLambda(xp)

        z2 = np.polyfit(xp, yp, 2)
        p2 = np.poly1d(z2)

        subX = np.linspace(xValues[i], xValues[i + 1], 100)
        
        plt.fill_between(subX, p2(subX))

    plt.show()


# Trapezoidal rule function
def trapezi(function, a, b, n):

    h = (b - a) / n                                                 # Intervals dimension
    xValues = np.linspace(a, b, n + 1)                              # Creation of n intervals (points) between a and b (included)
    functionLambda = lambdify(x, function)                          # Creation of executable math function  
    
    s = functionLambda(a)                                           # Calc of values using Trapezoidal algorithm
    for i in range(1, len(xValues) - 1):
        s = s + 2 * functionLambda(xValues[i])
    s = s + functionLambda(b)  

    result = (h / 2) * s

    err = 0                                                         # Calc of error using Trapezoidal algorithm
    for i in range(0, len(xValues) - 1):    
        err = err + (-((h**3) / 12) * secondDerivative(function, xValues[i]))    

    print("Errore stimato: " + str(format(err, '.5f')))

    print("Approssimazione integrale: " + str(result) + "\n")

    trapeziPlot(functionLambda, a, b, n, xValues)

    return True


# Simpson rule function
def simpson(function, a, b, n):
    
    if(n % 2 != 0): 
        print('Il numero di sottointervalli per applicare Simpson deve essere pari')
        return False
    
    h = (b - a) / n                                                 # Intervals dimension
    xValues = np.linspace(a, b, n + 1)                              # Creation of n intervals (points) between a and b (included) 
    functionLambda = lambdify(x, function)                          # Creation of executable math function   

    s = 0                                                           # Calc of values using Simpson algorithm
    for i in range(1, len(xValues) - 1):
        if(i % 2 == 0):
            s = s + 2 * functionLambda(xValues[i])
        else:
            s = s + 4 * functionLambda(xValues[i])
    
    s = s + functionLambda(a) + functionLambda(b)
    result = (h / 3) * s

    err = 0                                                         # Calc of error using Simpson algorithm
    for i in range(0, len(xValues) - 1):
        err = err + (-((1 / 90) * ((h / 2)**5) * fourthDerivative(function, xValues[i])))

    print("Errore stimato: " + str(format(err, '.9f')))

    print("Approssimazione integrale: " + str(result) + "\n")

    simpsonPlot(functionLambda, a, b, n, xValues)

    return True

    
# Main
if __name__ == "__main__":

    turnOn = True
    a = 0
    b = 0
    n = 0
    function = 0
    
    print("Programma per il calcolo degli integrali tramite formula del Trapezio e Cavalieri-Simpson")

    while turnOn:
        print("1 - Inserire una funzione \n2 - Modificare i dati di analisi \n3 - Metodo del Trapezio \n4 - Metodo di Cavalieri-Simpson \n0 - Quit")
        choice = int(input("Selezionare un numero: "))
        print("\n")

        if choice == 1:
            goInputFunction = True
            while goInputFunction:
                try:
                    inputFunction = input("Funzione (y in funzione di x): ")
                    function = eval(inputFunction)
                    testFunction = lambdify(x, function)                    # Check the math function
                    goInputFunction = False
                except SyntaxError:
                    print("Sintassi della funzione non corretta.")
            
            goInputData = True
            while goInputData:  
                try:                                                        # Check the input values
                    a = int(input("Punto a: "))
                    b = int(input("Punto b: "))
                    n = int(input("Numero di sottointervalli: "))
                    goInputData = False
                except ValueError:
                    print("Inserire un tipo di dato intero")

        if choice == 2:
            goInputData = True
            while goInputData:  
                try:                                                        # Check the input values
                    a = int(input("Punto a: "))
                    b = int(input("Punto b: "))
                    n = int(input("Numero di nodi: "))
                    goInputData = False
                except ValueError:
                    print("Inserire un tipo di dato intero")

        if choice == 3 and function != 0 and n != 0 and a != b: 
            trapezi(function, a, b, n)

        if choice == 4 and function != 0 and n != 0 and a != b: 
            simpson(function, a, b, n)

        if choice == 0:
            turnOn = False
            quit()

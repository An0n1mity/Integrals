import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np

figure, axes = plt.subplots()

def f(x):
    return x**2

class Rectangle:
    def __init__(self, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4, area, type):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2
        self.x_3 = x_3
        self.y_3 = y_3
        self.x_4 = x_4
        self.y_4 = y_4
        self.area = area
        self.type = type

    

def Init_Rectangle(subdivision_start, subdivision_end, type):
    small_rectangle = Rectangle(0, 0, 0, 0, 0, 0, 0, 0, 0, type)

    small_rectangle.x_4 = subdivision_start
    small_rectangle.x_1 = subdivision_start
    small_rectangle.x_2 = subdivision_end
    small_rectangle.x_3 = subdivision_end

    #create linspace of the subdivision
    subdivision_linespace = np.linspace(subdivision_start,subdivision_end,100)
    y = f(subdivision_linespace)
    if type == "small":
        #find the smallest value of the function over the subdivision
        y_ = np.amin(y)
    else:
        y_ = np.amax(y)

    small_rectangle.y_1 = y_
    small_rectangle.y_2 = y_
    small_rectangle.y_3 = 0
    small_rectangle.y_4 = 0    

    #calculate the area of the rectangle
    small_rectangle.area = y_ * (subdivision_end-subdivision_start)


    return small_rectangle

def Draw_Rectangle(rectangle):
    subdivison_linespace = np.linspace(rectangle.x_1, rectangle.x_2, 100)
    y = f(subdivison_linespace)
    
    if rectangle.type == "small":
        y_ = np.amin(y)
        color = "blue"
    else:
        y_ = np.amax(y)
        color = "red"

    #draw the base of the rectangle
    axes.plot([rectangle.x_3, rectangle.x_4], [rectangle.y_3, rectangle.y_4], color = color)
    #draw the top of the rectangle
    axes.plot([rectangle.x_1, rectangle.x_2], [rectangle.y_1, rectangle.y_2], color = color)
    #draw the side edges
    axes.plot([rectangle.x_1, rectangle.x_4], [rectangle.y_1, rectangle.y_4], color = color)
    axes.plot([rectangle.x_2, rectangle.x_3], [rectangle.y_2, rectangle.y_3], color = color)

    #fill the area of the rectangle
    index = np.where(y == y_)[0][0]
    axes.fill_between(subdivison_linespace, y[index], color=color, alpha=0.3)

def Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisions):
    tmp_subdivisons = []
    for i in range(0, nb_subdivisions+1):
        tmp = i*((intervall_end-intervall_start)/nb_subdivisions) + intervall_start
        tmp_subdivisons.append(tmp)
    subdivisions = np.array(tmp_subdivisons)

    return subdivisions

def Rectangles_over_Subdivions(subdivisions):
    rectangles = []
    for i in range(0, len(subdivisions)-1):
        small_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "small")
        big_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "big")
        rectangles.append(small_rectangle)
        rectangles.append(big_rectangle)

    return rectangles

#Create small rectangles
intervall_start = -5
intervall_end = 5
small_area = 0
big_area = 0
subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, 10)
rectangles = Rectangles_over_Subdivions(subdivisions)
for i in range(0, len(rectangles)):
    Draw_Rectangle(rectangles[i])
    if(rectangles[i].type == "small"):
        small_area += rectangles[i].area
    else:
        big_area += rectangles[i].area

#functions value over an interval
x = np.linspace(-5, 5, 100)
y = f(x)


area = "Small Area {}\nBig Area {}".format(small_area, big_area)
#index of the minimal value over the interval

axes.set_ylabel('f(x)')
axes.set_xlabel('x')
axes.plot(x, y, label='quadratic')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
axes.text(0.05, 0.95, area, transform=axes.transAxes, fontsize=14, verticalalignment='top', bbox=props)
axamp = plt.axes([0.25, .03, 0.50, 0.02])
samp = Slider(axamp, 'Numbers', 0, 1000, valinit=10, valstep=1)

def update(val):
    axes.clear()
    nb_subdivisions = samp.val
    small_area = 0
    big_area = 0
    # update curve
    if nb_subdivisions:
        subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisions)
        rectangles = Rectangles_over_Subdivions(subdivisions)
        for i in range(0, len(rectangles)):
            Draw_Rectangle(rectangles[i])
            if(rectangles[i].type == "small"):
                small_area += rectangles[i].area
            else:
                big_area += rectangles[i].area

    
    area = "Small Area {}\nBig Area {}".format(small_area, big_area)
    # redraw canvas while idle
    axes.set_ylabel('f(x)')
    axes.set_xlabel('x')
    axes.plot(x, y, label='quadratic')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    axes.text(0.05, 0.95, area, transform=axes.transAxes, fontsize=14, verticalalignment='top', bbox=props)


# call update function on slider value change
samp.on_changed(update)
plt.show()

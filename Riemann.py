import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, TextBox
import numpy as np

class f:
    def __init__(self, expression, value, x):
        self.expression = expression
        self.value = value
        self.x = x
    
    def Calculate(self, expression):
        self.value = eval(expression)

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

def Init_Rectangle(subdivision_start, subdivision_end, type, function):
    small_rectangle = Rectangle(0, 0, 0, 0, 0, 0, 0, 0, 0, type)

    small_rectangle.x_4 = subdivision_start
    small_rectangle.x_1 = subdivision_start
    small_rectangle.x_2 = subdivision_end
    small_rectangle.x_3 = subdivision_end

    #create linspace of the subdivision
    subdivision_linespace = np.linspace(subdivision_start,subdivision_end,100)
    function.x = subdivision_linespace
    function.Calculate(function.expression)
    y = function.value
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
    y = np.linspace(rectangle.y_1, rectangle.y_2, 100)
    
    if rectangle.type == "small":
        y_ = np.amin(y)
        color = "blue"
    else:
        y_ = np.amax(y)
        color = "red"

    #fill the area of the rectangle
    axes.fill_between(subdivison_linespace, y, color=color, alpha=0.3)

def Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisions):
    tmp_subdivisons = []
    for i in range(0, nb_subdivisions+1):
        tmp = i*((intervall_end-intervall_start)/nb_subdivisions) + intervall_start
        tmp_subdivisons.append(tmp)
    subdivisions = np.array(tmp_subdivisons)

    return subdivisions

def Rectangles_over_Subdivions(subdivisions, function):
    rectangles = []
    for i in range(0, len(subdivisions)-1):
        small_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "small", function)
        big_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "big", function)
        rectangles.append(small_rectangle)
        rectangles.append(big_rectangle)

    return rectangles

def Subdivisons_to_Values(rectangles, function):

    tmp_y_data_s = []
    tmp_y_data_b = []

    for i in range(0, len(rectangles)):
        if rectangles[i].type == "small":
            tmp_y_data_s.append(np.linspace(rectangles[i].y_1, rectangles[i].y_2, 100))
        else:
            tmp_y_data_b.append(np.linspace(rectangles[i].y_1, rectangles[i].y_2, 100))


    y_data_s = []
    y_data_b = []

    for i in range(0, len(tmp_y_data_s)):
        for j in range(0, len(tmp_y_data_s[i])):
            y_data_s.append(tmp_y_data_s[i][j])

    for i in range(0, len(tmp_y_data_b)):
        for j in range(0, len(tmp_y_data_b[i])):
            y_data_b.append(tmp_y_data_b[i][j])
    
    return (y_data_s, y_data_b)

def Update_Plot(function, nb_subdivisons):

    #update the rectagnles
    intervall_start = -5
    intervall_end = 5

    subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisons)
    rectangles = Rectangles_over_Subdivions(subdivisions, function)
    for rectangle in rectangles:
        Draw_Rectangle(rectangle)
    y_data_s, y_data_b = Subdivisons_to_Values(rectangles, function)
    x = np.linspace(intervall_start, intervall_end, len(y_data_s))

    l_s.set_xdata(x)
    l_s.set_ydata(y_data_s)
    l_b.set_xdata(x)
    l_b.set_ydata(y_data_b)

    #Update the function
    function.x = x
    function.Calculate(function.expression)
    l_1.set_ydata(function.value)
    l_1.set_xdata(function.x)

    figure.canvas.draw()
    figure.canvas.flush_events()


#Draw the function
x = np.linspace(-5, 5, 100)
function = f("self.x**3", 0, x)
function.Calculate(function.expression)
y = function.value

intervall_start = -5
intervall_end = 5
small_area = 0
big_area = 0
subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, 10)
rectangles = Rectangles_over_Subdivions(subdivisions, function)

figure, axes = plt.subplots()
axes.set_xlim([-10, 10])
axes.set_ylim([-10, 10])
axes.grid()
axes.set_ylabel('f(x)')
axes.set_xlabel('x')
y_data_s, y_data_b = Subdivisons_to_Values(rectangles, function)
l_1, = plt.plot(x, y, label='quadratic')
x = np.linspace(-5, 5, 1000)
for rectangle in rectangles:
    Draw_Rectangle(rectangle)

l_s, = plt.plot(x, y_data_s)
l_b, = plt.plot(x, y_data_b)


figure.canvas.draw()
figure.canvas.flush_events()
"""
#Create small rectangles
intervall_start = -5
intervall_end = 5
small_area = 0
big_area = 0
subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, 10)
rectangles = Rectangles_over_Subdivions(subdivisions, function)
y_data = Subdivisons_to_Values(rectangles, function)
l.set_ydata(y_data[1])
figure.canvas.draw()
figure.canvas.flush_events()
axes.grid()

for i in range(0, len(rectangles)):
    Draw_Rectangle(rectangles[i])
    if(rectangles[i].type == "small"):
        small_area += rectangles[i].area
    else:
        big_area += rectangles[i].area



area = "Small Area {}\nBig Area {}".format(small_area, big_area)
#index of the minimal value over the interval


"""
area = 0
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
axes.text(0.05, 0.95, area, transform=axes.transAxes, fontsize=14, verticalalignment='top', bbox=props)
axamp = plt.axes([0.25, .03, 0.50, 0.02])
axbox = plt.axes([0.25, .9, 0.50, 0.1])

text_box = TextBox(axbox, 'Function', initial="x**3")
samp = Slider(axamp, 'Numbers', 0, 1000, valinit=10, valstep=1)

def update(val):
    nb_subdivisions = samp.val
    Update_Plot(function, nb_subdivisions)

def submit(text):
    #Update the function
    text = text.replace("x", "self.x")
    function.expression = text
    Update_Plot(function, 10)

    


# call update function on slider value change
samp.on_changed(update)
text_box.on_submit(submit)
plt.show()

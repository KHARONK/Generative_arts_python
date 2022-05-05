import turtle
from PIL import ImageGrab
from compressor import compress_file

# Shape background color.
turtle.bgcolor("black")

# Size of pencil
turtle.pensize(2)

# Draw circle cursor speed movement.
turtle.speed(0)

# Colors for pencil to use in drawing
col = ('red','violet', 'orange','yellow')

# Criteria to draw shape
def drawcircle(radius):
    for i in range(50):
      # Getting colors
      turtle.pencolor(col[i%4])

      # Radius of circle.
      turtle.circle(radius)
      radius = radius-2

def drawdesign():
    # Number of circles to loop to form shape.
    for _ in range(11):
        # Size of circle
        drawcircle(100)
        # Movement to draw circle.
        turtle.right(36)
        turtle.forward(36)

# Draw and save image
drawdesign()
turtle.hideturtle()
turtle.update()

screen = turtle.Screen()
turtle = turtle.Turtle(visible=False)
screen.tracer(False)
screen.tracer(True)
canvas = screen.getcanvas()

ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(),
                     canvas.winfo_rooty() + canvas.winfo_height())).save('circle_colored_pic.png', "png")

# From compressing algorithm
compress_file('working.txt','circle_compressed')

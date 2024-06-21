import turtle

# Function to draw the fractal
def draw_fractal(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        draw_fractal(t, length/3, depth-1)
        t.left(60)
        draw_fractal(t, length/3, depth-1)
        t.right(120)
        draw_fractal(t, length/3, depth-1)
        t.left(60)
        draw_fractal(t, length/3, depth-1)

# Setup the screen and turtle
screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")

drawer = turtle.Turtle()
drawer.speed(0)
drawer.color("white")

# Adjust position and angle
drawer.penup()
drawer.goto(-150, 100)
drawer.setheading(0)
drawer.pendown()

# Draw the fractal
draw_fractal(drawer, 300, 4)

# Hide the turtle and display the result
drawer.hideturtle()
screen.mainloop()

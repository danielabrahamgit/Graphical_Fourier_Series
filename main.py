import numpy as np
import matplotlib.pyplot as plt
import arcade
from scipy import signal
from math_utils import *

# Constants
# Height, width, title, and scale of window
HEIGHT = 800 
WIDTH  = 1000
SCALE  = 150
TITLE  = "Fourier Series Demo"
# Sampling frequency
Fs = 1000
# Number of fourier coefficients
num_coef = 20
# Time interval
t_start = -1
t_end   = 1.0
# Period of the signal and it's fundemental frequency
P = t_end - t_start
w0 = 2 * np.pi / P

# NUMBER of SAMPLES in thhe OUTPUT signal
NSO = 300
# Output signal buffer
sig_pts = np.array([[WIDTH, HEIGHT/2]] * NSO)

# time array
t = np.linspace(t_start, t_end, int(P * Fs))

# define 1 period of your signal
sig = signal.square(np.pi * t)

# Get first n fourier coefficients
c = n_fourier_coef(sig, num_coef)

# Helper function to transform complex numbers
# to pixel represntation
def complx_to_pixel(z):
    x = np.real(z) * SCALE + (WIDTH / 2)
    y = np.imag(z) * SCALE + (HEIGHT / 2)
    return x, y

# Used to move each draw forward by some amount of time
time_index = 0

# Length of output in time, you can fill these in
t_output = np.linspace(-10, 10, int(P * Fs))

# amount to increment time each frame call
# NOTE: the output buffer will only update whenever
#       the time_index is an integer
inc_amount = 0.1

# Drawing function, executed on each frame
def on_draw(delta_time):
    global time_index, sig_pts
    arcade.start_render()

    # Draw all the complex vectors
    z_prev = -1.2 + 0j
    z_curr = 0 + 0j
    for k in range(len(c)):
        z_curr = np.exp(1j * w0 * k * t_output[int(time_index)]) * c[k] * -1j + z_prev
        x0, y0 = complx_to_pixel(z_prev)
        x1, y1 = complx_to_pixel(z_curr)
        arcade.draw_line(x0, y0, x1, y1, arcade.color.WHITE, 1)
        arcade.draw_circle_outline(x0, y0, np.sqrt((x1 - x0) ** 2 + (y1 - y0)**2), arcade.color.ENGLISH_RED, 0.4)
        z_prev = z_curr
    
    # Last iteration ---> we have the tip stored in z-curr.
    # Use this fact to draw out the signal by appending the tip
    if (abs(time_index - int(time_index)) < inc_amount):
        sig_pts += [1, 0]
        sig_pts = np.vstack((np.array([[WIDTH - NSO, y1]]), sig_pts[:-1,:]))
    arcade.draw_line(x1, y1, WIDTH - NSO, y1, arcade.color.WHITE, 1)
    arcade.draw_line_strip(sig_pts, arcade.color.WHITE, 1)

    # increment the time
    time_index += inc_amount
    if time_index >= len(t_output):
        time_index = 0

# Setup rendering/drawing
arcade.open_window(WIDTH, HEIGHT, TITLE)
arcade.set_background_color(arcade.color.BLACK)

# Tell the computer to call the draw command at the specified interval.
arcade.schedule(on_draw, 1 / 200)

# Run the program
arcade.run()

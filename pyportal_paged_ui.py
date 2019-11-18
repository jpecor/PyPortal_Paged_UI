"""
`pyportal_paged_ui`
================================================================================
Tabbed/paged user interface screen for the Adafruit PyPortal

* Author: Jason Pecor

"""

import board
import time
import busio

from adafruit_pyportal import PyPortal
from adafruit_bitmap_font import bitmap_font
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from padded_button import PaddedButton
from adafruit_display_shapes.rect import Rect

# Setup UART
uart = busio.UART(board.D3, board.D4, baudrate=9600)

# The buttons on the TFT display will send keycodes just like a standard keyboard
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)

# Load the font to be used on the buttons
font = bitmap_font.load_font("/fonts/Dina.bdf")

# Colors
WHITE = 0xffffff
BLUE = 0x094A85
LIGHT_BLUE = 0x13BDF9
DARK_BLUE = 0x0D2035
LIGHT_GREEN = 0x009A6E
GREEN = 0x45E83A
ORANGE = 0xDF550F
RED = 0xDB1308
GREY = 0x3B3C3E
BLACK = 0x000000

# Prepare PyPortal for graphics 
pyportal = PyPortal(default_bg=0x000000)
button_margin = (2, 2)
tab_margin = (0,0)
page_margin = (0,0)

page0_color = DARK_BLUE
page1_color = RED
page2_color = BLUE
page3_color = ORANGE

active_fill = DARK_BLUE
active_outline = DARK_BLUE

# Create the main page and buttons
#
# This code is a bit verbose and clumsy, and it can be streamlined by pre-defining
# the sizes and anchor points for each button.  However, keeping it all here like
# this provides some additional context for making sense of what is passed into the
# init() function for each button which has proven helpful for me as I'm learning CP.
#
# Also, this uses a class called PaddedButton which is based on the Adafruit Button class
# It provides additional arguments for margin and padding.  

# Main background
main_page = Rect(0, 0, 320, 200, fill=page0_color, outline=page0_color, stroke=0)

# These buttons will serve as "tabs" at the bottom of the screen
tab0 = PaddedButton(x=0, y=180, width=80, height=60,
                    label="0", label_font=font, label_color=0xffffFF, label_y=40,
                    fill_color=page0_color, outline_color=page0_color, style=1,
                    selected_fill=page0_color, selected_outline=page0_color,
                    margin=tab_margin, padding=(0, 0))

tab1 = PaddedButton(x=80, y=180, width=80, height=60,
                    label="1", label_font=font, label_color=0xffffFF, label_y=40,
                    fill_color=page1_color, outline_color=page1_color, style=1,
                    selected_fill=page1_color, selected_outline=page1_color,
                    margin=tab_margin, padding=(0, 0))

tab2 = PaddedButton(x=160, y=180, width=80, height=60,
                    label="2", label_font=font, label_color=0xffffFF, label_y=40,
                    fill_color=page2_color, outline_color=page2_color, style=1,
                    selected_fill=page2_color, selected_outline=page2_color,
                    margin=tab_margin, padding=(0, 0))

tab3 = PaddedButton(x=240, y=180, width=80, height=60,
                    label="3", label_font=font, label_color=0xffffFF, label_y=40,
                    fill_color=page3_color, outline_color=page3_color, style=1,
                    selected_fill=page3_color, selected_outline=page3_color,
                    margin=tab_margin, padding=(0, 0))

# Now for the actual buttons that do something worthwhile
button_width = 80
button_height = 60
row1_y = 0
row2_y = 110

cmd00_button = PaddedButton(x=0, y=row1_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 0", label_font=font, label_color=0xffffFF, id=0,
                            style=1, margin=button_margin, padding=(5, 5))
cmd01_button = PaddedButton(x=80, y=row1_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 1", label_font=font, label_color=0xffffFF, id=1,
                            style=1, margin=button_margin, padding=(5, 5))
cmd02_button = PaddedButton(x=160, y=row1_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 2", label_font=font, label_color=0xffffFF, id=2,
                            style=1, margin=button_margin, padding=(5, 5))
cmd03_button = PaddedButton(x=240, y=row1_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,  
                            label="CMD 3", label_font=font, label_color=0xffffFF, id=3,
                            style=1, margin=button_margin, padding=(5, 5))

cmd04_button = PaddedButton(x=0, y=row2_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 4", label_font=font, label_color=0xffffFF, id=4,
                            style=1, margin=button_margin, padding=(5, 5))
cmd05_button = PaddedButton(x=80, y=row2_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 5", label_font=font, label_color=0xffffFF, id=5,
                            style=1, margin=button_margin, padding=(5, 5))
cmd06_button = PaddedButton(x=160, y=row2_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 6", label_font=font, label_color=0xffffFF, id=6,
                            style=1, margin=button_margin, padding=(5, 5))
cmd07_button = PaddedButton(x=240, y=row2_y, width=button_width, height=button_height,
                            fill_color=None, outline_color=0xFFFFFF,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="CMD 7", label_font=font, label_color=0xffffFF, id=7,
                            style=1, margin=button_margin, padding=(5, 5))

# Add all of the buttons to a list
pages = [main_page]

tabs = [tab0,
        tab1,
        tab2,
        tab3]

buttons =  [cmd00_button,
            cmd01_button,
            cmd02_button,
            cmd03_button,
            cmd04_button,
            cmd05_button,
            cmd06_button,
            cmd07_button
          ]

# And add to the display
touchables = []  # This is an awful name, but can't think of anything better

for tab in tabs:
    pyportal.splash.append(tab.group)
    touchables.append(tab)
for page in pages:
    pyportal.splash.append(page)  # main page is not a touch-responsive object - don't add to touchables
for button in buttons:
    pyportal.splash.append(button.group)
    touchables.append(button)

active_page = 0

# Capture touch actions
last_p = None  # Will be used to trap Off->On touch transition

while True:

    p = pyportal.touchscreen.touch_point

    if (p is not None) & (last_p is None):  # Only catch the Off->On transition

        (y, x, z) = p

        for i, b in enumerate(touchables):

            if b.contains(p):

                b.selected = True
                command = (10 * int(active_page)) + b.id
                
                # Not doing anything wiht the buttons right now.
                # Just dumping out the associated command
                if (b in buttons):
                    print("Button {} pressed on page {}. Running command {}".format(b.label,active_page,command))

                # Change the active page with the tab
                if b == tab0:
                    active_page = 0
                    print("Setting active page to {}".format(active_page))
                    active_fill = active_outline = page0_color
                    main_page.fill= page0_color
                    main_page.outline= page0_color

                elif b == tab1:
                    active_page = 1
                    print("Setting active page to {}".format(active_page))
                    active_fill = active_outline = page1_color
                    main_page.fill= page1_color
                    main_page.outline= page1_color
                    
                elif b == tab2:
                    active_page = 2
                    print("Setting active page to {}".format(active_page))
                    active_fill = active_outline = page2_color
                    main_page.fill= page2_color
                    main_page.outline= page2_color
                    
                elif b == tab3:
                    active_page = 3
                    print("Setting active page to {}".format(active_page))
                    active_fill = active_outline = page3_color
                    main_page.fill = page3_color
                    main_page.outline= page3_color

            else:
                b.selected = False

    else:
        # Toggle buttons back off when released
        for button in buttons:
            button.selected = False
            button.fillcolor = active_fill        

    # Capture state of p to setup one-shot compare
    time.sleep(0.5)
    last_p = p

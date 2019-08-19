# The MIT License (MIT)
#
# Copyright (c) 2019 Limor Fried for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`padded_button`
================================================================================
Modification of the Adafruit_CircuitPython_Display_Button class to include
margin and padding.  For use with the CircuitPython displayio core module.

* Author: Jason Pecor

"""

from micropython import const
import displayio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect

__version__ = ""
__repo__ = ""


def _check_color(color):
    # if a tuple is supplied, convert it to a RGB number
    if isinstance(color, tuple):
        r, g, b = color
        return int((r << 16) + (g << 8) + (b & 0xff))
    return color


class PaddedButton():
    # pylint: disable=too-many-instance-attributes, too-many-locals
    """Helper class for creating UI buttons for ``displayio``.

    :param x: The x position of the button.
    :param y: The y position of the button.
    :param width: The width of the button in pixels.
    :param height: The height of the button in pixels.
    :param name: The name of the button.
    :param style: The style of the button. Can be RECT, ROUNDRECT, SHADOWRECT, SHADOWROUNDRECT.
                  Defaults to RECT.
    :param fill_color: The color to fill the button. Defaults to 0xFFFFFF.
    :param outline_color: The color of the outline of the button.
    :param label: The text that appears inside the button. Defaults to not displaying the label.
    :param label_font: The button label font.
    :param label_color: The color of the button label text. Defaults to 0x0.
    :param selected_fill: Inverts the fill color.
    :param selected_outline: Inverts the outline color.
    :param selected_label: Inverts the label color.

    """
    RECT = const(0)
    ROUNDRECT = const(1)
    SHADOWRECT = const(2)
    SHADOWROUNDRECT = const(3)

    def __init__(self, *, x, y, width, height, name=None, style=RECT,
                 fill_color=0xFFFFFF, outline_color=0x0,
                 label=None, label_font=None, label_color=0x0,
                 label_x=-1, label_y=-1, id=-1,                 # PaddedButton
                 selected_fill=None, selected_outline=None,
                 selected_label=None, margin=None, padding=None): # PaddedButton

        # PaddedButton
        # Define padding around the button boundaries to constrain
        # calculation for the contains() method
        if padding is not None:
            self._padding = padding
        else:
            self._padding = (0, 0)  # (x,y) respectively
            
        # Margin provides space around the outside of the button
        self._margin = margin
        
        # PaddedButton
        if margin is not None:
            self.x = x + margin[0]
            self.y = y + margin[1]
            self.width = width - (2 * self.margin[0])
            self.height = height - (2 * self.margin[1])
        else: 
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        self._font = label_font
        self._selected = False
        self.group = displayio.Group()
        self.name = name
        self._label = label
        self._id = id         # PaddedButton
        self.body = self.fill = self.shadow = None

        self.fill_color = _check_color(fill_color)
        self.outline_color = _check_color(outline_color)
        self._label_color = label_color
        self._label_font = label_font
        self._label_x = label_x         # PaddedButton
        self._label_y = label_y         # PaddedButton

        # Selecting inverts the button colors!
        self.selected_fill = _check_color(selected_fill)
        self.selected_outline = _check_color(selected_outline)
        self.selected_label = _check_color(selected_label)

        if (self.selected_fill is None) and (fill_color is not None):
            self.selected_fill = (~self.fill_color) & 0xFFFFFF
        if self.selected_outline is None and outline_color is not None:
            self.selected_outline = (~self.outline_color) & 0xFFFFFF

        # print("id: {} selected_fill: {}".format(self._id,self.selected_fill))

        if (outline_color is not None) or (fill_color is not None):
            if style == PaddedButton.RECT:
                self.body = Rect(self.x, self.y, width, height,
                                    fill=self.fill_color, outline=self.outline_color)
            elif style == PaddedButton.ROUNDRECT:
                self.body = RoundRect(self.x, self.y, self.width, self.height, r=10,
                                        fill=self.fill_color, outline=self.outline_color)
            elif style == PaddedButton.SHADOWRECT:
                self.shadow = Rect(x + 2, y + 2, width - 2, height - 2,
                                    fill=outline_color)
                self.body = Rect(x, y, width - 2, height - 2,
                                    fill=self.fill_color, outline=self.outline_color)
            elif style == PaddedButton.SHADOWROUNDRECT:
                self.shadow = RoundRect(x + 2, y + 2, width - 2, height - 2, r=10,
                                        fill=self.outline_color)
                self.body = RoundRect(x, y, width - 2, height - 2, r=10,
                                        fill=self.fill_color, outline=self.outline_color)
            if self.shadow:
                self.group.append(self.shadow)

            self.group.append(self.body)

        self.label = label

        # else: # ok just a bounding box
        # self.bodyshape = displayio.Shape(width, height)
        # self.group.append(self.bodyshape)

    @property
    def label(self):
        """The text label of the button"""
        return self._label.text

    @label.setter
    def label(self, newtext):
        if self._label and (self.group[-1] == self._label):
            self.group.pop()

        self._label = None
        if not newtext or (self._label_color is None):  # no new text
            return     # nothing to do!

        if not self._label_font:
            raise RuntimeError("Please provide label font")
        self._label = Label(self._label_font, text=newtext)
        dims = self._label.bounding_box
        if dims[2] >= self.width or dims[3] >= self.height:
            raise RuntimeError("Button not large enough for label")

        # PaddedButton
        # Set an x,y location for the label
        if self._label_x > -1:
            x_loc = self.x + self._label_x
        else: 
            x_loc = self.x + (self.width - dims[2]) // 2
        if self._label_y > -1: 
            y_loc = self.y + self._label_y
        else:
            y_loc = self.y + self.height // 2
            
        self._label.x = x_loc
        self._label.y = y_loc

        # self._label.x = self.x + (self.width - dims[2]) // 2
        # self._label.y = self.y + self.height // 2

        self._label.color = self._label_color
        self.group.append(self._label)

        if (self.selected_label is None) and (self._label_color is not None):
            self.selected_label = (~self._label_color) & 0xFFFFFF

    @property
    def selected(self):
        """Selected inverts the colors."""
        return self._selected

    @selected.setter
    def selected(self, value):
        if value == self._selected:
            return   # bail now, nothing more to do
        self._selected = value
        if self._selected:
            new_fill = self.selected_fill
            new_out = self.selected_outline
            new_label = self.selected_label
        else:
            new_fill = self.fill_color
            new_out = self.outline_color
            new_label = self._label_color
        # print("id: {} new_fill: {}".format(self._id,new_fill))
        # update all relevant colros!
        if self.body is not None:
            # print("id: {} updating new_fill: {}".format(self._id,new_fill))
            self.body.fill = new_fill
            self.body.outline = new_out
        if self._label is not None:
            self._label.color = new_label


    # PaddedButton
    # New code for contains function
    def contains(self, point):
        """Used to determine if a point is contained within a button. For example,
        ``button.contains(touch)`` where ``touch`` is the touch point on the screen will allow for
        determining that a button has been touched.
        """
        x_min = self.x + self._padding[0]
        x_max = self.x + self.width - self._padding[0]
        y_min = self.y + self._padding[1]
        y_max = self.y + self.height - self._padding[1]

        return (x_min <= point[0] <= x_max) and (y_min  <= point[1] <= y_max)

    # def contains(self, point):
    #     """Used to determine if a point is contained within a button. For example,
    #     ``button.contains(touch)`` where ``touch`` is the touch point on the screen will allow for
    #     determining that a button has been touched.
    #     """
    #     return (self.x <= point[0] <= self.x + self.width) and (self.y <= point[1] <=
    #                                                             self.y + self.height)

    # PaddedButton additions
    @property
    def id(self):
        """Button ID.  Should be an integer."""
        return self._id

    @property
    def padding(self):
        """Sets the button outline padding"""
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value

    @property
    def margin(self):
        """Sets the button outline padding"""
        return self._margin

    @margin.setter
    def margin(self, value):
        self._margin = value

    @property
    def fillcolor(self):
        """Sets the fill color"""
        return self.fill_color

    @fillcolor.setter
    def fillcolor(self, fill):
        self.body.fill = fill

    @property
    def outlinecolor(self):
        """Sets the fill color"""
        return self.outline

    @outlinecolor.setter
    def outlinecolor(self, fill):
        self.body.outline = fill

    @property
    def labelcolor(self):
        """Sets the fill color"""
        return self._label_color

    @labelcolor.setter
    def labelcolor(self, value):
        self._label_color = value
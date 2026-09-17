from manim import *
import numpy as np

class Pulley(Scene):
    def construct(self):

        # GROUND
        ground_y = -2
        ground = Line(start=[-10, ground_y, 0], end=[10, ground_y, 0])

        # SLOPE
        start_x = -4
        theta = 30 * DEGREES
        slope_length = 7
        slope = Line(start=[start_x, ground_y, 0],
                     end=[start_x + slope_length*np.cos(theta), ground_y + slope_length*np.sin(theta), 0])

        # ANGLE
        angle = Angle(ground, slope, radius=0.8)
        angle_label = MathTex(rf"\theta", font_size=36).next_to(angle, RIGHT).shift(UP*0.1)

        angle_display = VGroup(angle, angle_label)

        # BOXES
        h = 2
        w = 3
        box_A = Rectangle(height=h, width=w, color=WHITE, fill_opacity=0.1)
        box_A.rotate(theta)

        self.add(ground, slope, angle_display)
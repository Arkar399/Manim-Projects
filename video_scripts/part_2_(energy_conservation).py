from manim import *
from manim_physics import *
import numpy as np

class EnergyConservation(SpaceScene):
    def construct(self):

        g = -9.81
        elasticity = 1.0

        # GROUND
        floor_y = -3
        floor = Line(start=[-10, floor_y, 0], end=[10, floor_y, 0])

        # make ball
        r = 0.6
        start_height = 3
        max_height = start_height
        start_x = -4 + r
        ball = Circle(radius=r, color=WHITE, fill_opacity=0.7, stroke_width=6)
        ball.move_to(np.array([start_x, start_height, 0]))

        # HEIGHT LINE
        height_line = always_redraw(
            lambda: Line(start=[-4.5, floor_y, 0], end=[-4.5, ball.get_center()[1] - r, 0], color=WHITE, stroke_width=2)
            )
        height_divot = always_redraw(
            lambda: Line(start=[-4.5, ball.get_center()[1] - r, 0], end=[-4.3, ball.get_center()[1] - r, 0], color=WHITE, stroke_width=2)
            )
        height_text = always_redraw(
            lambda: MathTex(rf"h", font_size=40).move_to([-5, height_line.get_midpoint()[1], 0])
            )

        # MIDDLE LINE
        middle_line = Line(start=[0, floor_y, 0], end=[0, 10, 0], color=WHITE, stroke_width=1, stroke_opacity=0.5)

        # TRACE LINE
        # trace_line = TracedPath(ball.get_center, stroke_color=WHITE, stroke_width=2, dissipating_time=0.2, fill_opacity=0.1)

        # PATH LINE
        path_line = always_redraw(
            lambda: DashedLine(start=[start_x, floor_y, 0], end=[start_x, ball.get_center()[1] - r, 0],
                               color=WHITE, stroke_width=1, stroke_opacity=1)
            )
        
        # BARS
        scl = 1
        bar_width = 0.6
        max_bar_height = scl * (max_height - floor_y - r)

        gpe_bar = always_redraw(
            lambda: Rectangle(
                width=bar_width, height=scl * (ball.get_center()[1] - r - floor_y),
                color=WHITE, fill_opacity=1)
                .next_to([3.5, floor_y, 0], UP, buff=0)
                )
        gpe_bar_frame = Rectangle(width=bar_width, height=max_bar_height,
                                  color=WHITE, fill_opacity=0).next_to([3.5, floor_y, 0], UP, buff=0)

        ke_bar = always_redraw(
            lambda: Rectangle(
                width=bar_width, height=max_bar_height - scl * (ball.get_center()[1] - r - floor_y),
                color=WHITE, fill_opacity=1)
                .next_to([1.5, floor_y, 0], UP, buff=0)
                )
        ke_bar_frame = Rectangle(width=bar_width, height=max_bar_height,
                                 color=WHITE, fill_opacity=0).next_to([1.5, floor_y, 0], UP, buff=0)

        total_energy_bar = Rectangle(width=bar_width, height=max_bar_height,
                                     color=WHITE, fill_opacity=1).next_to([5.5, floor_y, 0], UP, buff=0)

        # TEXT
        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UL, buff=0.5).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)

        elasticity_text = MathTex(rf"e = {elasticity}", font_size=48).move_to([ball.get_x(), -3.5, 0])
        GPE_text = MathTex(rf"GPE", font_size=52).next_to(gpe_bar_frame, UP, buff=0.5)
        KE_text = MathTex(rf"KE", font_size=52).next_to(ke_bar_frame, UP, buff=0.5)
        Total_text = MathTex(rf"Total", font_size=52).next_to(total_energy_bar, UP, buff=0.5)

        self.add(floor, middle_line, path_line, ball, elasticity_text, height_line, height_divot, height_text)
        self.add(gpe_bar, gpe_bar_frame, ke_bar, ke_bar_frame, total_energy_bar)
        self.add(GPE_text, KE_text, Total_text)
        self.add(g_arrow, g_text)

        self.make_rigid_body(ball, elasticity=1.0, friction=0.0)
        self.make_static_body(floor, elasticity=1.0, friction=0.0)

        self.wait(8.5)
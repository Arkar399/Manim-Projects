from manim import *
from manim_physics import *
import numpy as np

class RestitutionCoef(SpaceScene):

    def construct(self):

        self.GRAVITY = (0, -2)  #lowered gravity to drag out simulation   

        # GROUND
        floor_y = -3
        floor = Line(start=[-10, floor_y, 0], end=[10, floor_y, 0])

        # BALLS
        r = 0.25
        start_y = 2
        e_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 1.1]

        ball1 = Circle(radius=r, stroke_color=BLUE, fill_opacity=0).move_to([-4.5, start_y, 0])
        ball2 = Circle(radius=r, stroke_color=RED, fill_opacity=0).move_to([-3, start_y, 0])
        ball3 = Circle(radius=r, stroke_color=GREEN, fill_opacity=0).move_to([-1.5, start_y, 0])
        ball4 = Circle(radius=r, stroke_color=PURPLE, fill_opacity=0).move_to([0, start_y, 0])
        ball5 = Circle(radius=r, stroke_color=ORANGE, fill_opacity=0).move_to([1.5, start_y, 0])
        ball6 = Circle(radius=r, stroke_color=PINK, fill_opacity=0).move_to([3, start_y, 0])
        ball7 = Circle(radius=r, stroke_color=YELLOW, fill_opacity=0).move_to([4.5, start_y, 0])

        ball_list = [ball1, ball2, ball3, ball4, ball5, ball6, ball7]

        def add_ball(ball, e):
            self.make_rigid_body(ball, elasticity=e, friction = 0.0)
            self.add(ball)

        # TEXT
        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UP, buff=0.6).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)

        impossible_text = MathTex(rf"(e > 1)", font_size=24, color=RED).move_to(np.array([ball7.get_x(), floor_y - 0.8, 0]))

        def add_e_text(ball, e):
            text = MathTex(rf"e = {e}", font_size=32).move_to(np.array([ball.get_x(), floor_y - 0.4, 0]))
            self.add(text)

        # COLORED FLOOR




        for ball, e in zip(ball_list, e_list):
            add_ball(ball, e)
            add_e_text(ball, e)

        self.make_static_body(floor, elasticity=1.0, friction = 0.0)
        self.add(g_text, g_arrow, floor, impossible_text)

        self.wait(10)
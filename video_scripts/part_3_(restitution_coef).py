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
        r = 0.3
        start_y = 2
        spacing = 1.5
        e_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 1.1]
        colors = [BLUE, RED, GREEN, PURPLE, ORANGE, PINK, YELLOW]
        ball_list = []

        for i, e in enumerate(e_list):
            ball = Circle(radius=r, stroke_color=colors[i], fill_opacity=0)
            ball.move_to([-4.5 + i * spacing, start_y, 0])
            ball_list.append(ball)

        def add_ball(ball, e):
            self.make_rigid_body(ball, elasticity=e, friction = 0.0)
            self.add(ball)

        # TEXT
        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UP, buff=0.6).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)

        impossible_text = MathTex(rf"(e > 1)", font_size=24, color=RED).move_to(np.array([ball_list[-1].get_x(), floor_y - 0.8, 0]))

        def add_e_text(ball, e):
            text = MathTex(rf"e = {e}", font_size=32).move_to(np.array([ball.get_x(), floor_y - 0.4, 0]))
            self.add(text)

        for ball, e in zip(ball_list, e_list):
            add_ball(ball, e)
            add_e_text(ball, e)

        # COLORED FLOOR
        self.add(floor)
        self.make_static_body(floor, elasticity=1.0, friction = 0.0)

        for ball in ball_list:
            floor_color = ball.get_stroke_color()
            colored_floor = Line(start=[ball.get_x() - 0.7, floor_y, 0], end=[ball.get_x() + 0.7, floor_y, 0], color=floor_color)
            self.add(colored_floor)

        self.add(g_text, g_arrow, impossible_text)

        self.wait(10)
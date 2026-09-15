from manim import *
import numpy as np

class Collision(Scene):
    def construct(self):

        # BALL 1
        ball1 = Circle(radius=0.4, color=WHITE, fill_opacity=0)
        ball1.move_to([-7, 0, 0])
        ball1.velocity = np.array([5, 0, 0], dtype=float)
        ball1.mass = 4.0

        # BALL 2
        ball2 = Circle(radius=0.7, color=WHITE, fill_opacity=0)
        ball2.move_to([1, 0, 0])
        ball2.velocity = np.array([0, 0, 0], dtype=float)
        ball2.mass = 6.0

        balls = VGroup(ball1, ball2)

        # WALL
        wall = Line(start=[5, 10, 0], end=[5, -10, 0])
        wall_e = 0.8

        # ARROWS
        arrow1 = always_redraw(
            lambda: Arrow(start=ORIGIN, end=0.3*ball1.velocity,   #inaccurate scaling just to make arrow2 big enough
                          buff=0).move_to(ball1.get_top() + [0, 0.4, 0])
        )

        arrow2 = always_redraw(
            lambda: Arrow(start=ORIGIN, end=0.5*ball2.velocity,
                          buff=0).move_to(ball2.get_top() + [0, 0.4, 0])
        )

        def move_ball(m, dt):

            m.move_to(m.get_center() + (m.velocity * dt))


        def check_collision(m):

            distance = np.linalg.norm(ball1.get_center() - ball2.get_center())
            
            sum_of_radii = ball1.radius + ball2.radius
            
            if distance <= sum_of_radii:

                if ball2.velocity[0] < 0:   #ball2 returning to ball1
                    I = ball2.mass * ball2.velocity
                    ball1.velocity += (I // ball1.mass) * 0.7  #70% energy transfer

                    ball2.velocity -= (I // ball2.mass) * 0.7

                else:                       #first collision
                    I = ball1.mass * ball1.velocity
                    ball2.velocity += (I // ball2.mass) * 0.7

                    ball1.velocity -= (I // ball1.mass) * 0.7

            distance_from_wall = abs(ball2.get_x() - wall.get_x())

            if distance_from_wall <= ball2.radius:   #wall collision
                ball2.velocity = -ball2.velocity * wall_e

        # TEXT
        inwards_symbol = ImageMobject(r"C:\Users\Arkar Zaw\Downloads\inwards_symbol.png")
        inwards_symbol.scale(0.4)
        inwards_symbol.to_edge(UL, buff=0.5)
        g_text = MathTex(rf"g", font_size=48).next_to(inwards_symbol, RIGHT, buff=0.1)

        e_text = MathTex(rf"e = {wall_e}", font_size=48).next_to(wall, RIGHT, buff=0.3)

        formula_text = MathTex(rf"p = mv", font_size=56).to_edge(UP, buff=0.6)
        efficiency_text = MathTex(r"(70\% \text{ efficiency})", font_size=40).next_to(formula_text, DOWN)

        friction_text = Text(rf"*frictionless surface", font_size=20).to_edge(DR, buff=0.6).shift(LEFT*2)

        ball1_name = always_redraw(
            lambda: Text(rf"A", font_size=36).move_to(ball1.get_center())
        )

        ball2_name = always_redraw(
            lambda: Text(rf"B", font_size=48).move_to(ball2.get_center())
        )

        ball1_v = always_redraw(
            lambda: MathTex(rf"v_A = {round(abs(ball1.velocity[0]), 1)}m/s", font_size=32).next_to(ball1.get_bottom(), DOWN)
        )

        ball2_v = always_redraw(
            lambda: MathTex(rf"v_B = {round(abs(ball2.velocity[0]), 1)}m/s", font_size=32).next_to(ball2.get_bottom(), DOWN)
        )

        ball1_m = MathTex(rf"m_A = {ball1.mass} kg", font_size=48).to_edge(DL, buff=0.6).shift(UP*0.5)
        ball2_m = MathTex(rf"m_B = {ball2.mass} kg", font_size=48).to_edge(DL, buff=0.6)

        ball1.add_updater(move_ball)
        ball2.add_updater(move_ball)

        balls.add_updater(check_collision)


        self.add(balls, wall)
        self.add(arrow1, arrow2, ball1_v, ball2_v)
        self.add(g_text, inwards_symbol, e_text, ball1_name, ball2_name)
        self.add(efficiency_text, formula_text, friction_text, ball1_m, ball2_m)
        self.wait(7.4)
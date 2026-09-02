#Conservation of energy shown with a bouncing ball on a perfectly elastic plane

from manim import *
import numpy as np

class Speeds(Scene):
    def construct(self):

        t = ValueTracker(0)

        # GROUND
        line1 = Line(start=LEFT*10, end=RIGHT*10).shift(UP*1)
        line2 = line1.copy().next_to(line1, DOWN*9)
        line3 = line2.copy().next_to(line2, DOWN*9)

        # BALLS
        r = 0.3
        start_x = -5

        v1 = 0.5
        ball1 = Circle(radius=r, color=BLUE, fill_opacity=0.5)
        ball1.move_to(np.array([0, line1.get_y(), 0])).shift(UP*r+LEFT*5)

        v2 = 1
        ball2 = ball1.copy()
        ball2.move_to(np.array([0, line2.get_y(), 0])).shift(UP*r+LEFT*5)

        v3 = 3
        ball3 = ball2.copy()
        ball3.move_to(np.array([0, line3.get_y(), 0])).shift(UP*r+LEFT*5)

        # TEXT
        t_unit = Text("s", font_size=48)
        t_text = Text("t   =", font_size=48)
        t_value = DecimalNumber(0, num_decimal_places=1)
        t_and_unit = VGroup(t_value, t_unit).arrange(RIGHT, buff=0.25)
        t_display = VGroup(t_text, t_and_unit).arrange(RIGHT, buff=0.5).to_edge(UP)

        d1_unit = Text("m", font_size=28)
        d1_text = Text("d   =", font_size=28)
        d1_value = DecimalNumber(0, num_decimal_places=1)
        d1_and_unit = VGroup(d1_value, d1_unit).arrange(RIGHT, buff=0.25)
        d1_display = VGroup(d1_text, d1_and_unit).arrange(RIGHT, buff=0.25)
        d1_display.move_to(np.array([4, line1.get_y() + 1.6, 0]))

        d2_unit = Text("m", font_size=28)
        d2_text = Text("d   =", font_size=28)
        d2_value = DecimalNumber(0, num_decimal_places=1)
        d2_and_unit = VGroup(d2_value, d2_unit).arrange(RIGHT, buff=0.25)
        d2_display = VGroup(d2_text, d2_and_unit).arrange(RIGHT, buff=0.25)
        d2_display.move_to(np.array([4, line2.get_y() + 1.6, 0]))

        d3_unit = Text("m", font_size=28)
        d3_text = Text("d   =", font_size=28)
        d3_value = DecimalNumber(0, num_decimal_places=1)
        d3_and_unit = VGroup(d3_value, d3_unit).arrange(RIGHT, buff=0.25)
        d3_display = VGroup(d3_text, d3_and_unit).arrange(RIGHT, buff=0.25)
        d3_display.move_to(np.array([4, line3.get_y() + 1.6, 0]))

        v1_text = Text(f"v = {float(v1)}m/s", font_size=24)
        v2_text = Text(f"v = {float(v2)}m/s", font_size=24)
        v3_text = Text(f"v = {float(v3)}m/s", font_size=24)

        # UPDATERS
        t_value.add_updater(lambda m: m.set_value(t.get_value()))
        d1_value.add_updater(lambda m: m.set_value(v1*t.get_value()))
        d2_value.add_updater(lambda m: m.set_value(v2*t.get_value()))
        d3_value.add_updater(lambda m: m.set_value(v3*t.get_value()))

        ball1.add_updater(lambda m: m.move_to(np.array([start_x + (v1*t.get_value()),
                                                        ball1.get_y(),
                                                        0])))
        ball2.add_updater(lambda m: m.move_to(np.array([start_x + (v2*t.get_value()),
                                                        ball2.get_y(),
                                                        0])))
        ball3.add_updater(lambda m: m.move_to(np.array([start_x + (v3*t.get_value()),
                                                        ball3.get_y(),
                                                        0])))
        v1_text.add_updater(lambda m: m.next_to(ball1, UP))
        v2_text.add_updater(lambda m: m.next_to(ball2, UP))
        v3_text.add_updater(lambda m: m.next_to(ball3, UP))
        

        self.play(Create(line1), Create(line2), Create(line3))
        self.add(ball1, ball2,ball3)
        self.play(Write(v1_text), Write(v2_text), Write(v3_text))
        self.play(FadeIn(t_display), FadeIn(d1_display), FadeIn(d2_display), FadeIn(d3_display))

        self.play(t.animate.set_value(7), run_time=7, rate_func=linear)

        self.wait(0.5)

        self.play(t.animate.set_value(0), run_time=7, rate_func=linear)

        self.play(FadeOut(Group(*self.mobjects)))

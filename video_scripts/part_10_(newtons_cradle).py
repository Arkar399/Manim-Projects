from manim import *
import numpy as np

class NewtonsCradle(Scene):
    def construct(self):

        # FRAME
        frame_y = 3
        frame = Line(start=[-10, frame_y, 0], end=[10, frame_y, 0])

        # TICKS
        ticks = VGroup()
        tick_spacing = 0.6
        tick_length = 0.2
        
        for x in np.arange(-10, 10, tick_spacing):
            tick = Line(start=[x, frame_y, 0], end=[x + tick_length * 0.7, frame_y + tick_length, 0],
                        stroke_width=2, color=GRAY_A)
            ticks.add(tick)  

        # STILL BALLS
        r = 0.5
        length = 3.5
        positions = [
            [-2*r, frame_y-length, 0],
            [0, frame_y-length, 0],
            [2*r, frame_y-length, 0],
        ]

        for position in positions:

            string = Line(start=[position[0], frame_y, 0], end=[position[0], frame_y-length, 0], color=WHITE)
            
            ball = Dot(ORIGIN, radius=r, color=WHITE)
            ball.move_to(position)

            self.add(string)
            self.add(ball)

            # LABELS
            e_line = Line(start=ORIGIN, end=[0, 0.5, 0]).next_to(ball, DOWN)
            e_label = MathTex(r"e", font_size=40).next_to(e_line, DOWN)

            self.add(e_line, e_label)

        # MOVING BALLS
        angle1 = ValueTracker(45*DEGREES)
        angle2 = ValueTracker(0)

        string1 = always_redraw(
            lambda: Line(start=[-4*r, frame_y, 0],
                       end=[-4*r-length*np.sin(angle1.get_value()), frame_y-(length*np.cos(angle1.get_value())), 0],
                       color=WHITE)
        )
        ball1 = always_redraw(
            lambda: Dot(ORIGIN, radius=r, color=WHITE).move_to(string1.get_end())
        )

        string2 = always_redraw(
            lambda: Line(start=[4*r, frame_y, 0],
                       end=[4*r-length*np.sin(angle2.get_value()), frame_y-(length*np.cos(angle2.get_value())), 0],
                       color=WHITE)
        )
        ball2 = always_redraw(
            lambda: Dot(ORIGIN, radius=r, color=WHITE).move_to(string2.get_end())
        )

        e_line1 = always_redraw(
            lambda: Line(start=ORIGIN, end=[0, 0.5, 0]).next_to(ball1, DOWN)
        )
        e_label1 = always_redraw(
            lambda: MathTex(r"e", font_size=40).next_to(e_line1, DOWN)
        )
        e_line2 = always_redraw(
            lambda: Line(start=ORIGIN, end=[0, 0.5, 0]).next_to(ball2, DOWN)
        )
        e_label2 = always_redraw(
            lambda: MathTex(r"e", font_size=40).next_to(e_line2, DOWN)
        )

        # TEXT
        e_text = MathTex(rf"e = 1.0", font_size=56).to_edge(DOWN)

        self.add(frame, ticks)
        self.add(string1, ball1)
        self.add(string2, ball2)
        self.add(e_line1, e_label1, e_line2, e_label2)
        self.add(e_text)

        runtime = 0.6
        for _ in range(3):
            self.play(angle1.animate.set_value(0), run_time=runtime, rate_func=rate_functions.ease_in_quad)
            self.play(angle2.animate.set_value(-45*DEGREES), run_time=runtime, rate_func=rate_functions.ease_out_quad)
            self.play(angle2.animate.set_value(0), run_time=runtime, rate_func=rate_functions.ease_in_quad)
            self.play(angle1.animate.set_value(45*DEGREES), run_time=runtime, rate_func=rate_functions.ease_out_quad)
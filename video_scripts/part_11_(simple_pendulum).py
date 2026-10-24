from manim import *
import numpy as np

class SimplePendulum(Scene):
    def construct(self):

        # FRAME
        frame_y = 3.5
        frame = Line(start=[-2.5, frame_y, 0], end=[2.5, frame_y, 0])
        frame_leg1 = Line(start=[-2.5, frame_y, 0], end=[-3, frame_y+1, 0])
        frame_leg2 = Line(start=[2.5, frame_y, 0], end=[3, frame_y+1, 0])
        frame_dot = Dot([0, frame_y, 0], color=WHITE, radius=0.08)

        # PENDULUM
        r = 0.4
        length = ValueTracker(3)
        angle = ValueTracker(45*DEGREES)

        string = always_redraw(
            lambda: Line(start=[0, frame_y, 0],                               
                         end=[-2*length.get_value()*np.sin(angle.get_value()),       #*2 for scaling factor
                             frame_y-(2*length.get_value()*np.cos(angle.get_value())),
                             0],
                         color=WHITE)
        )
        ball = always_redraw(
            lambda: Dot(ORIGIN, radius=r, color=WHITE).move_to(string.get_end())
        )

        # ADDITIONAL
        tracedpath = TracedPath(ball.get_center, dissipating_time=0.05, stroke_opacity=0.5, stroke_width=4)

        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UL, buff=0.6).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)
        g_display = VGroup(g_arrow, g_text)

        # LABELS
        m_label = always_redraw(
            lambda: MathTex(rf"m", color=BLACK, font_size=40).move_to(ball.get_center())
        )

        T_formula = MathTex(r"T = 2\pi \sqrt{\frac{L}{g}}", font_size=52).to_edge(UR, buff=0.6)

        l_value = always_redraw(
            lambda: MathTex(rf"L = {2*length.get_value():.2f} m", font_size=52)
            .to_edge(DL, buff=0.6)
        )
        T_value = always_redraw(
            lambda: MathTex(rf"T = {2*PI*np.sqrt(2*length.get_value()/9.81):.2f} s", font_size=52) #*2 for scaling factor
            .next_to(l_value, UP)
        )

        # ADDING OBJECTS
        self.add(frame, frame_leg1, frame_leg2, frame_dot)
        self.add(string, ball, tracedpath)
        self.add(m_label, g_display, T_formula, l_value, T_value)

        # ANIMATION 
        # all run_time values are halved to be faster
        for _ in range(2):
            self.play(angle.animate.set_value(-45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                      rate_func=rate_functions.ease_in_out_quad)
            self.play(angle.animate.set_value(45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                      rate_func=rate_functions.ease_in_out_quad)

        self.play(angle.animate.set_value(-45*DEGREES), length.animate(rate_func=linear).set_value(2.5), 
                  run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                  rate_func=rate_functions.ease_in_out_quad)
        self.play(angle.animate.set_value(45*DEGREES), length.animate(rate_func=linear).set_value(2), 
                  run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                  rate_func=rate_functions.ease_in_out_quad)

        for _ in range(2):
            self.play(angle.animate.set_value(-45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                        rate_func=rate_functions.ease_in_out_quad)
            self.play(angle.animate.set_value(45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                        rate_func=rate_functions.ease_in_out_quad)

        self.play(angle.animate.set_value(-45*DEGREES), length.animate(rate_func=linear).set_value(2.5), 
                  run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                  rate_func=rate_functions.ease_in_out_quad)  
        self.play(angle.animate.set_value(45*DEGREES), length.animate(rate_func=linear).set_value(3), 
                  run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                  rate_func=rate_functions.ease_in_out_quad)

        for _ in range(1):
            self.play(angle.animate.set_value(-45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                        rate_func=rate_functions.ease_in_out_quad)
            self.play(angle.animate.set_value(45*DEGREES), run_time=2*PI*np.sqrt(length.get_value()/9.81)/4,
                        rate_func=rate_functions.ease_in_out_quad)

        

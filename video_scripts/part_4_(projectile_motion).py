from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):

        # FLOORS
        ground_y = -2.5
        ground = Line(start=[-10, ground_y, 0], end=[10, ground_y, 0], stroke_width=4, color=WHITE)

        ticks = VGroup()
        tick_spacing = 0.6
        tick_length = 0.2
        
        for x in np.arange(-10, 10, tick_spacing):
            tick = Line(start=[x, ground_y, 0], end=[x - tick_length * 0.7, ground_y - tick_length, 0],
                        stroke_width=2, color=GRAY_A)
            ticks.add(tick)  

        elevated_floor = Line(start=[-10, -1, 0], end=[-6, -1, 0], stroke_width=4, color=WHITE)
        elevated_floor_height = Line(start=[elevated_floor.get_end()[0], elevated_floor.get_y(), 0], end=[elevated_floor.get_end()[0], ground_y, 0],
                                           stroke_width=4, color=WHITE)
        elevated_floor_height_label = MathTex(rf"h_0", font_size=36).next_to(elevated_floor_height, LEFT)


        # BALL
        r = 0.3
        start_x = -6
        start_y = elevated_floor.get_y() + r
        ball = Circle(radius=r, color=WHITE, fill_opacity=0.5)
        ball.move_to([start_x, start_y, 0])

        ball_path = TracedPath(ball.get_center, stroke_color=WHITE, stroke_width=4, stroke_opacity=0.2)

        # FLIGHT EQUATIONS
        v0 = 10
        g = 9.81
        theta = 45 * DEGREES
        h = elevated_floor.get_y() - ground_y

        t_max = (v0 * np.sin(theta) + np.sqrt((v0 * np.sin(theta))**2 + 2 * g * h)) / g
        t = ValueTracker(0)

        def update_ball_position(t):
            x = start_x + v0 * np.cos(theta) * t
            y = start_y + v0 * np.sin(theta) * t - 0.5 * g * t**2
            
            return np.array([x, y, 0])
        ball.add_updater(lambda m: m.move_to(update_ball_position(t.get_value())))

        # HEIGHT LINE
        height_line = always_redraw(
            lambda: DashedLine(start=[ball.get_x(), ground_y, 0], end=[ball.get_x(), ball.get_y(), 0],
                               color=WHITE, stroke_width=2)
            )
        height_text = always_redraw(
            lambda: MathTex(rf"h", font_size=40).move_to([ball.get_x() + 0.4, (ground_y + (ball.get_y() - r)) / 2, 0])
            )

        # RANGE LINE
        range = start_x + v0 * np.cos(theta) * t_max
        gap = 0.6
        range_line = Line(start=[ball.get_x(), ground_y - gap, 0], end=[range, ground_y - gap, 0],
                          color=WHITE, stroke_width=2)
        
        range_divot1 = Line(start=[ball.get_x(), ground_y - gap, 0], end=[ball.get_x(), ground_y - gap+0.2, 0],
                            color=WHITE, stroke_width=2)
        range_divot2 = Line(start=[range, ground_y - gap, 0], end=[range, ground_y - gap+0.2, 0],
                            color=WHITE, stroke_width=2)
        
        range_divots = VGroup(range_divot1, range_divot2)

        range_label = MathTex(rf"R", font_size=48)
        range_label.move_to([range_line.get_midpoint()[0], ground_y - 1, 0])

        # START ARROW
        v0_arrow = Arrow(start=[start_x, start_y, 0], end=[start_x + v0 * np.cos(theta) * 0.15, start_y + v0 * np.sin(theta) * 0.15, 0],
                         color=WHITE, stroke_width=4, buff=0)
        horizontal_line = DashedLine(start=[start_x, start_y, 0], end=[start_x + v0 * np.cos(theta) * 0.15, start_y, 0],
                         color=WHITE, stroke_width=2, buff=0)
        angle_display = Angle(v0_arrow, horizontal_line, radius=0.5, other_angle=True, color=WHITE, stroke_width=2)

        # VY AND VX
        scale_factor = 0.15
        vy_arrow = always_redraw(
            lambda: Arrow(start=ball.get_center(), end=ball.get_center() + [0, (v0 * np.sin(theta) - g * t.get_value()) * scale_factor, 0],
                          buff=0)
            )
        vy_label = always_redraw(
            lambda: MathTex(rf"V_y", font_size=36).next_to(vy_arrow, LEFT)
            )
        
        vx_arrow = always_redraw(
            lambda: Arrow(start=ball.get_center(), end=ball.get_center() + [1, 0, 0],
                          buff=0)
            )
        vx_label = always_redraw(
            lambda: MathTex(rf"V_x", font_size=36).next_to(vx_arrow, RIGHT)
            )

        # HIGHEST POINT
        t_at_hp = v0*np.sin(theta) / g

        hp_x = start_x + v0 * np.cos(theta) * t_at_hp
        hp_y = start_y + v0 * np.sin(theta) * t_at_hp - 0.5 * g * t_at_hp**2

        hp_line = always_redraw(
            lambda: DashedLine(start=[hp_x, ground_y, 0], end=[hp_x, hp_y, 0], stroke_opacity=0.2)
            if height_line.get_x() > hp_x
            else VGroup()
            )

        # TEXT
        angle_label = MathTex(rf"\theta", font_size=36)
        angle_label.move_to(ball.get_center()).shift(RIGHT*0.7+UP*0.3)

        v0_label = MathTex(rf"V_0", font_size=48)
        v0_label.next_to(v0_arrow, UP)

        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UL, buff=0.6).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)
        g_display = VGroup(g_arrow, g_text)

        vy_equation = MathTex(rf"V_y = V_0sin(\theta)", font_size=48).to_edge(UR)
        vx_equation = MathTex(rf"V_x = V_0cos(\theta)", font_size=48).next_to(vy_equation, DOWN)
   
        self.add(ground, ticks, elevated_floor, elevated_floor_height, elevated_floor_height_label)
        self.add(ball, ball_path, hp_line, vy_arrow, vy_label, vx_arrow, vx_label)
        self.add(v0_arrow, v0_label, horizontal_line, angle_display, angle_label)
        self.add(height_line, height_text, range_line, range_divots, range_label)
        self.add(g_display, vy_equation, vx_equation)

        self.play(t.animate.set_value(t_max), run_time=6, rate_func=linear)
        ball_path.clear_updaters()

        self.wait(1)
        # self.play(LaggedStartMap(Create, ticks, lag_ratio=0.05, run_time=1.5))
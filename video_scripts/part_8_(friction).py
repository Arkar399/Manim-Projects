from manim import *
import numpy as np

class Friction(Scene):
    def construct(self):

        # GROUND
        ground_y = -2
        ground = Line(start=[-10, ground_y, 0], end=[10, ground_y, 0])

        # SLOPE
        start_x = -4
        theta = 30 * DEGREES
        slope_length = 9

        start_point = np.array([start_x, ground_y, 0])
        end_point = start_point + np.array([slope_length*np.cos(theta), slope_length*np.sin(theta), 0])

        support_line = Line(start=[end_point[0], ground_y, 0], end=[end_point[0], end_point[1], 0],
                            stroke_width=2)

        slope = Line(start=start_point, end=end_point)

        # ANGLE1
        angle1 = Angle(ground, slope, radius=0.8, stroke_opacity=0.5)
        angle_label1 = MathTex(rf"\theta", font_size=36).next_to(angle1, RIGHT).shift(UP*0.1)

        angle_display1 = VGroup(angle1, angle_label1)

        # BOX
        box = Rectangle(height=1.2, width=1.7, color=WHITE, fill_opacity=0)

        slope_vector = np.array([slope_length*np.cos(theta), slope_length*np.sin(theta), 0])
        unit_vector = slope_vector / np.linalg.norm(slope_vector)

        box.move_to([start_x, ground_y, 0], aligned_edge=DOWN)
        box.rotate(theta, about_point=start_point).shift(0.2*slope_vector)

        direction = ValueTracker(1)
        v = 1*unit_vector #arbitrary value

        def move_box(m, dt):

            m.move_to(m.get_center() +  (direction.get_value() * v * dt))

        box.add_updater(move_box)



        # ARROWS
        d_opacity = ValueTracker(1)
        driving_force = always_redraw(
            lambda: Arrow(start=box.get_center(),
                          end=box.get_center() + 2*unit_vector,
                          buff=0, color=GREEN).set_opacity(d_opacity.get_value())
        )

        weight_force = always_redraw(
            lambda: Arrow(start=box.get_center(), end=box.get_center() - [0, 2, 0],
                          buff=0, color=BLUE)
        )

        normal_force = always_redraw(
            lambda: Arrow(start=box.get_center(),
                          end=box.get_center() + [0, 1.4, 0],
                          buff=0, color=BLUE_A).rotate(theta, about_point=box.get_center())
        )

        normal_force_down = always_redraw(
            lambda: DashedLine(start=box.get_center(),
                               end=box.get_center() + [0, -1.5, 0],
                               buff=0, stroke_opacity=0.6).rotate(theta, about_point=box.get_center())
        )

        parallel_force = always_redraw(
            lambda: Arrow(start=box.get_center(),
                          end=box.get_center() + -1.6*unit_vector,
                          buff=0, color=YELLOW_A)
        )

        f_opacity1 = ValueTracker(1)
        f_opacity2 = ValueTracker(0)
        friction_force1 = always_redraw(
            lambda: Arrow(start=box.get_vertices()[2],
                          end=box.get_vertices()[2] + -0.8*unit_vector,
                          buff=0, color=RED).set_opacity(f_opacity1.get_value())
        )
        friction_force2 = always_redraw(
            lambda: Arrow(start=box.get_vertices()[3],
                          end=box.get_vertices()[3] + 0.8*unit_vector,
                          buff=0, color=RED).set_opacity(f_opacity2.get_value())
        )

        # ANGLE2   
        angle2 = always_redraw(
            lambda: Angle(weight_force, normal_force_down, radius=0.8, stroke_opacity=0.5)
        )

        angle_label2 = always_redraw(
            lambda: MathTex(rf"\theta", font_size=36).next_to(angle2, DOWN).shift(RIGHT*0.1)
        )

        angle_display2 = VGroup(angle2, angle_label2)

        # TEXT
        driving_label = always_redraw(
            lambda: MathTex(rf"F", color=GREEN, font_size=48).next_to(driving_force, UR)
            .set_opacity(d_opacity.get_value())
        )

        weight_label = always_redraw(
            lambda: MathTex(rf"mg", color=BLUE, font_size=48).next_to(weight_force, DOWN)
        )

        normal_label = always_redraw(
            lambda: MathTex(r"mg\cos(\theta)", color=BLUE_A, font_size=40).next_to(normal_force, UP)
        )

        parallel_label = always_redraw(
            lambda: MathTex(r"mg\sin(\theta)", color=YELLOW_A, font_size=40).next_to(parallel_force, DL)
        )

        friction_label1 = always_redraw(
            lambda: MathTex(r"F_f", color=RED, font_size=32).next_to(friction_force1, DOWN)
            .set_opacity(f_opacity1.get_value())
        )

        friction_label2 = always_redraw(
            lambda: MathTex(r"F_f", color=RED, font_size=32).next_to(friction_force2, DOWN)
            .set_opacity(f_opacity2.get_value())
        )

        F_value = ValueTracker(50)

        F_label = always_redraw(
            lambda: MathTex(f"F = {int(F_value.get_value())}N", color=GREEN, font_size=76).to_edge(DOWN, buff=0.7)
        )

        # ADDiTIONAL
        formula = MathTex(r"F_f = \mu \cdot mg \cos(\theta)", font_size=52).to_edge(UL, buff=0.5)

        g_arrow = MathTex(rf"\longleftarrow", font_size=48).to_edge(UR, buff=0.6).rotate(PI/2)
        g_text = MathTex(rf"g", font_size=48).next_to(g_arrow, RIGHT, buff=0.2)
        g_display = VGroup(g_arrow, g_text)

        center = always_redraw(
            lambda: Dot(radius=0.08, color=WHITE).move_to(box.get_center())
        )



        self.add(ground, support_line, slope, box, angle_display1, angle_display2)

        self.add(driving_force, weight_force, normal_force, normal_force_down,
                 parallel_force, friction_force1, friction_force2)
        
        self.add(driving_label, weight_label, normal_label, parallel_label,
                 friction_label1, friction_label2, F_label)

        self.add(formula, g_display, center)

        self.wait(4.5)

        # box.suspend_updating()

        self.play(direction.animate.set_value(-2), d_opacity.animate.set_value(0),
                  f_opacity1.animate.set_value(0), f_opacity2.animate.set_value(1),
                  F_value.animate.set_value(0), run_time=2)
        
        # box.resume_updating()

        self.wait(1)

        self.play(direction.animate.set_value(1), d_opacity.animate.set_value(1),
                  f_opacity1.animate.set_value(1), f_opacity2.animate.set_value(0),
                  F_value.animate.set_value(50), run_time=2)

        self.wait(4)

        self.play(direction.animate.set_value(-2), d_opacity.animate.set_value(0),
        f_opacity1.animate.set_value(0), f_opacity2.animate.set_value(1),
        F_value.animate.set_value(0), run_time=2)

        self.wait(1.5)
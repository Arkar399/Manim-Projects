from manim import *

class Refraction(Scene):
    def construct(self):

        n1 = 1.00
        n2 = ValueTracker(1.33)
        reflect_opacity = 0.5

        # PLANE
        plane = Line(start=[-10, 0, 0], end=[10, 0, 0])

        # RAYS
        theta_i = ValueTracker(45) * DEGREES
        length = 8.16 #distance from center to corner

        ray1 = always_redraw(
            lambda: Line(start=[0, plane.get_y(), 0],
                         end=[-length*np.sin(theta_i.get_value()), length*np.cos(theta_i.get_value()) + plane.get_y(), 0])
        )
        ray2 = always_redraw(
            lambda: Line(start=[0, plane.get_y(), 0],
                         end=[length*np.sin(theta_i.get_value()), length*np.cos(theta_i.get_value()) + plane.get_y(), 0],
                         stroke_opacity=reflect_opacity)
        )

        color_list = [BLUE_A, YELLOW_A, RED_A, GRAY, WHITE]
        color_index = ValueTracker(0)

        ray3 = always_redraw(
            lambda: Line(start=[0, plane.get_y(), 0],
                         end=[length*np.sin(np.arcsin((n1 / n2.get_value())*np.sin(theta_i.get_value()))),
                             -length*np.cos(np.arcsin((n1 / n2.get_value())*np.sin(theta_i.get_value()))) + plane.get_y(),
                              0])
            .set_color(color_list[int(color_index.get_value()) % len(color_list)]) #so ray can change color
        )

        # NORMAL LINE
        normal1 = DashedLine(start=[ray1.get_start()[0], plane.get_y(), 0], end=[ray1.get_start()[0], 2, 0],
                            stroke_opacity=0.8)
        normal2 = DashedLine(start=[ray1.get_start()[0], plane.get_y(), 0], end=[ray1.get_start()[0], -2, 0],
                            stroke_opacity=0.8)

        # ARROWS
        arrow1 = always_redraw(
            lambda: Arrow(start=LEFT, end=RIGHT, stroke_width=4)
            .move_to(ray1.get_midpoint())
            .rotate(theta_i.get_value()-PI/2)
            .set_stroke(opacity=0)
        )
        arrow2 = always_redraw(
            lambda: Arrow(start=ORIGIN, end=RIGHT*2, stroke_width=4)
            .move_to(ray2.get_midpoint())
            .rotate(PI/2-theta_i.get_value())
            .set_opacity(0.3)
            .set_stroke(opacity=0)
        )

        arrow3 = always_redraw(
            lambda: Arrow(start=ORIGIN, end=RIGHT*2, stroke_width=4)
            .move_to(ray3.get_midpoint())
            .rotate(np.arcsin((n1 / n2.get_value())*np.sin(theta_i.get_value()))-PI/2)
            .set_stroke(opacity=0)
            .set_color(color_list[int(color_index.get_value()) % len(color_list)])
        )

        # ANGLES
        i_angle1 = always_redraw(
            lambda: Angle(normal1, ray1, radius=1)
        )
        i_angle2 = always_redraw(
            lambda: Angle(ray2, normal1, radius=1, stroke_opacity=reflect_opacity)
        )

        r_angle = always_redraw(
            lambda: Angle(normal2, ray3, radius=1)
        )

        # LABELS
        i_label1 = always_redraw(
            lambda: MathTex(r"\theta_1", font_size=40).next_to(i_angle1, 0.7*UP).shift(0.3*LEFT*theta_i.get_value())
        )

        i_label2 = always_redraw(
            lambda: MathTex(r"\theta_1", font_size=40).next_to(i_angle2, 0.7*UP).shift(0.3*RIGHT*theta_i.get_value())
            .set_opacity(reflect_opacity)
        )

        r_label = always_redraw(
            lambda: MathTex(r"\theta_2", font_size=40)
            .next_to(r_angle, 0.7*DOWN)
            .shift(0.2*RIGHT*np.arcsin((n1 / n2.get_value())*np.sin(theta_i.get_value())))
        )

        # TEXT
        n1_text = MathTex(rf"n_1 = {n1:.2f}", font_size=40).to_edge(RIGHT).shift(UP*1)
        n2_text = always_redraw(
            lambda: MathTex(rf"n_2 = {round(n2.get_value(), 2)}", font_size=40).to_edge(RIGHT).shift(UP*0.5)
        )

        snells_law = MathTex(r"n_1\sin(\theta_1) = n_2\sin(\theta_2)", font_size=38).to_edge(UP, buff=0.3)

        theta_i_text = always_redraw(
            lambda: MathTex(rf"\theta_1 = {(theta_i.get_value()*180/PI):.1f}^\circ", 
                            font_size=48).to_edge(LEFT).shift(DOWN*0.6)
        )
        theta_r_text = always_redraw(
            lambda: MathTex(rf"\theta_2 = {(np.arcsin((n1 / n2.get_value())*np.sin(theta_i.get_value()))*180/PI):.1f}^\circ",
                            font_size=48).to_edge(LEFT).shift(DOWN*1.2)
        )

        air = MathTex(rf"Air", font_size=36).next_to(n1_text, LEFT)

        material1 = MathTex(rf"Water", font_size=36).next_to(n2_text, LEFT)
        material2 = MathTex(rf"Oil", font_size=36).next_to(n2_text, LEFT)
        material3 = MathTex(rf"Ethanol", font_size=36).next_to(n2_text, LEFT)
        material4 = MathTex(rf"Mercury", font_size=36).next_to(n2_text, LEFT)
        material5 = MathTex(rf"Aerogel", font_size=36).next_to(n2_text, LEFT)
        material6 = MathTex(rf"Water", font_size=36).next_to(n2_text, LEFT) #to return back to water

        # ANIMATION
        self.add(plane, normal1, normal2)
        self.add(i_angle1, i_angle2, r_angle)
        self.add(i_label1, i_label2, r_label)
        self.add(ray1, ray2, ray3)
        self.add(arrow1, arrow2, arrow3)
        self.add(n1_text, n2_text, theta_i_text, theta_r_text, air, material1, snells_law)

        # self.wait(0.5)

        self.play(theta_i.animate.set_value(60*DEGREES), run_time=1.5)

        self.play(theta_i.animate.set_value(30*DEGREES), run_time=1.5)

        self.play(theta_i.animate.set_value(75*DEGREES), run_time=1.5)

        self.play(theta_i.animate.set_value(45*DEGREES), run_time=1.5)


        self.play(n2.animate.set_value(1.47), color_index.animate(rate_func=linear).set_value(6),
                  ReplacementTransform(material1, material2), run_time=0.8) #oil
        self.wait(0.6)

        self.play(n2.animate.set_value(1.36), color_index.animate(rate_func=linear).set_value(12),
                  ReplacementTransform(material2, material3), run_time=0.8) #ethanol
        self.wait(0.6)

        self.play(n2.animate.set_value(1.74), color_index.animate(rate_func=linear).set_value(18),
                  ReplacementTransform(material3, material4), run_time=0.8) #mercury
        self.wait(0.6)

        self.play(n2.animate.set_value(1.03), color_index.animate(rate_func=linear).set_value(24),
                  ReplacementTransform(material4, material5), run_time=0.8) #aerogel
        self.wait(0.6)

        self.play(n2.animate.set_value(1.33), color_index.animate(rate_func=linear).set_value(30),
                  ReplacementTransform(material5, material6), run_time=0.8) #back to water

        # self.play(n2.animate.set_value(0.5), theta_i.animate.set_value(90*DEGREES), run_time=1.5)

        self.wait(1)
from manim import *

class GPE(Scene):
    def construct(self):
        mass = 5 #kg
        g = 9.81 #m/s^2
        height = ValueTracker(0) # we demonstrate change of height affecting GPE 

        title = Text("GPE = mgh", font_size=48).to_edge(UP)
        ball = Circle(radius=0.5, stroke_color=RED, fill_color=RED_D, fill_opacity=0.5).shift(DOWN*1)
        line = Line(start=LEFT*10, end=RIGHT*10, stroke_width=4).shift(DOWN*2.5)
        mass_text = Text(f"{mass} kg", font_size=20).move_to(ball)

        #initalize gpe display
        gpe_value = DecimalNumber(0, num_decimal_places=1)
        gpe_text = Text("Energy:", font_size=30)
        gpe_unit = Text("J", font_size=30)
        gpe_and_unit = VGroup(gpe_value, gpe_unit).arrange(RIGHT, buff=1)
        gpe_display = VGroup(gpe_text, gpe_and_unit).arrange(RIGHT, buff=1).to_edge(UR).shift(DOWN*0.3)

        #initalize height display
        height_value = DecimalNumber(0, num_decimal_places=1)
        height_text = Text("Height:", font_size=30)
        height_unit = Text("m", font_size=30)
        height_and_unit = VGroup(height_value, height_unit).arrange(RIGHT, buff=1)
        height_display = VGroup(height_text, height_and_unit).arrange(RIGHT, buff=1).next_to(gpe_display, DOWN)

        ball.add_updater(lambda m: m.move_to(np.array([0, line.get_center()[1] + height.get_value() + 0.5, 0])))
         #0.5 to account for radius
        mass_text.add_updater(lambda m: m.move_to(ball.get_center()))
        gpe_value.add_updater(lambda m: m.set_value(mass * g * height.get_value()))
        #formula here
        height_value.add_updater(lambda m: m.set_value(height.get_value()))

        self.play(Create(ball), Create(line), Write(title))
        self.play(Write(mass_text))
        self.play(FadeIn(gpe_display), FadeIn(height_display))

        self.play(height.animate.set_value(4), run_time=4, rate_func=linear) #changing height which controls the other mobjects
        self.wait(1)
        self.play(height.animate.set_value(0), run_time=4, rate_func=linear)

        self.wait(1)

        self.play(FadeOut(ball), FadeOut(line), FadeOut(title), FadeOut(mass_text), FadeOut(gpe_display), FadeOut(height_display))

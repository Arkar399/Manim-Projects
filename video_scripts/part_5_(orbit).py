from manim import *
import numpy as np

class Orbit(Scene):
    def construct(self):

        # values dont need to be to scale, just a demonstration
        G = 2
        M = 50

        # STAR
        r_star = 0.5
        star_start = np.array([1, 1, 0], dtype=float)
        star = Dot(point=star_start, radius=r_star, color="#f8ffa6")
        star_glow = Dot(radius=r_star+0.05, color="#f8ffa6", fill_opacity=0.4).move_to(star)

        # PLANET
        r = 0.15
        r_orbit = 3
        start_pos = star_start + np.array([r_orbit, 0, 0], dtype=float)
        planet = Dot(point=start_pos, radius=r, color=BLUE)
        planet.velocity = np.array([-3, 5, 0], dtype=float)

            # MOVEMENT CALCULATIONS
        def update_planet(m, dt):
            vector = m.get_center() - star.get_center()
            r_mag = np.linalg.norm(vector) #pythagoras theorem

            if r_mag < r_star: #prevents collision
                return
            
            unit_vector = vector/r_mag
            a =  unit_vector * (-G * M / (r_mag**2))

            m.velocity += a * dt
            m.move_to(m.get_center() + m.velocity * dt)

        # TRAIL
        trail = TracedPath(planet.get_center, dissipating_time=3.5, stroke_color=WHITE, stroke_width=2, stroke_opacity=0.6)

        # DIRECTION OF INITIAL V
        v0_arrow = Arrow(start=ORIGIN, end=0.4*planet.velocity, color=WHITE)
        v0_arrow.to_edge(DL, buff=2).shift(DOWN*0.3)
        cross_line1 = DashedLine(start=ORIGIN, end=[0, 0.4*planet.velocity[1], 0], stroke_opacity=0.4).move_to(v0_arrow)
        cross_line2 = cross_line1.copy().rotate(PI/2)

        cross = VGroup(cross_line1, cross_line2)

        # R LINE
        r_line = always_redraw(
            lambda: Line(start=planet.get_center(), end=star.get_center(), stroke_opacity=0.2)
            )

        # TEXT
        v0_text = Text(rf"Initial Velocity", font_size=24).next_to(v0_arrow, UP*2)
        v0_direction = MathTex(rf"({planet.velocity[0]}i + {planet.velocity[1]}j)", font_size=36).next_to(v0_arrow, DOWN*2)

        M_label = MathTex(rf"M", font_size=48, color=BLACK).move_to(star)

        m_line = always_redraw(
            lambda: Line(start=planet.get_center() + [0, r, 0],
                         end=planet.get_center() + [0, r, 0] + np.array([0, 1, 0])/3,
                         stroke_opacity=0.6)
            )
        m_text = always_redraw(
            lambda: MathTex(rf"m", font_size=36).next_to(planet, UP, buff=0.5)
            )

        m_label = VGroup(m_line, m_text)

        formula = MathTex(r"F = \frac{GMm}{r^2}", font_size=56).next_to(v0_arrow, UP*7.5)
        newtons_law = Text(rf"Newton's Law of Gravitation:", font_size=20).next_to(formula, UP*2)

        G_value = MathTex(r"G = 6.67 \times 10^{-11}", font_size=40).to_edge(UR, buff=0.5)

        r_label = always_redraw(
            lambda: MathTex(rf"r", font_size=36).next_to(r_line.get_midpoint(), rotate_vector(r_line.get_unit_vector(), PI/2),
                            buff=0.2)
                    if r_line.get_num_points() > 0 #write r only after line has been created
                    else VGroup()
            )

        not_to_scale = Text(rf"*not to scale", font_size=24).to_edge(DR)

        planet.add_updater(update_planet)

        self.add(star, star_glow, M_label)
        self.add(planet, trail, m_label)
        self.add(v0_arrow, cross, v0_text, v0_direction)
        self.add(r_line, r_label)
        self.add(formula, newtons_law, G_value, not_to_scale)

        self.wait(10.4)

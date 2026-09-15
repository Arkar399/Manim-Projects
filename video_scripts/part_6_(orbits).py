from manim import *
import numpy as np

class Orbits(Scene):
    def construct(self):

        # values dont need to be to scale, just a demonstration
        G = 25

        m_list = [11, 13, 17] #represents mass of its STAR
        c_list = ["#c2a96c", "#c94a40", "#5eb4c7"]

        # SUN dot
        sun = Dot(point=ORIGIN, radius=0.1, color=WHITE)

        # PLANETS
        r = 0.2
        start_pos = np.array([3, 0, 0], dtype=float)
        planets = VGroup()

        for i in range(len(m_list)):
            M = m_list[i]
            planet = Dot(radius=r, color=c_list[i])
            planet.move_to(start_pos)
            planet.velocity = [-1, 10, 0]
            planet.vector = [0, 0, 0]
            planet.mass = M

            planets.add(planet)

        def update_planet(m, dt):
            vector = m.get_center() - sun.get_center()
            vector_mag = np.linalg.norm(vector) #pythagoras theorem

            if vector_mag == 0: #prevents collision
                return
            
            unit_vector = vector/vector_mag

            a =  unit_vector * (-G*m.mass / (vector_mag**2))

            m.velocity += a * dt
            m.move_to(m.get_center() + m.velocity * dt)

            m.vector = unit_vector

        # LINES
        def create_line(planet):
            line = always_redraw(
                lambda: Line(start=sun.get_center(), end=planet.get_center(), stroke_opacity=0.2)
            )
            return line

        # LABELS
        def create_label(planet, i):
            label = always_redraw(
                lambda: MathTex(rf"M_{{\text{{star}}}} = {m_list[i]}", font_size=32).next_to(planet, UP)
            )
            return label

        # ARROWS
        def create_arrow(planet):
            arrow = always_redraw(
                lambda: Arrow(start=planet.get_center(), end=sun.get_center(),
                              color=WHITE).scale(0.3, scale_tips=True)
            )
            
            return arrow

        # TEXT
        formula = MathTex(r"v = \sqrt{\frac{GM}{r}}", font_size=48).to_edge(UR, buff=0.7)
        equation = MathTex(rf"F_g = F_c", font_size=56).to_edge(UL, buff=0.7)

        for i, planet in enumerate(planets):
            planet.add_updater(update_planet)
            self.add(planet)

            line = create_line(planet)
            self.add(line)

            label = create_label(planet, i)
            self.add(label)

            arrow = create_arrow(planet)
            self.add(arrow)

        self.add(sun, formula, equation)

        self.wait(12)
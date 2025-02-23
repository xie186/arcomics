from manim import *
from mpmath import mp
import numpy as np

# Function to get the first n digits of pi
def get_n_digits_of_pi(n):
    mp.dps = n
    return [3] + [int(i) for i in list(str(mp.pi))[2:]]

class PiCircle(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE 
        colors = [DARK_BROWN, ORANGE, PURPLE, PINK,
                  TEAL, BLUE, BLUE_E, BLUE_B, GREEN_E, GREEN_B]
        num_of_arcs = 10
        offset = 5 * DEGREES
        radius = 3.5
        arc_length = (TAU / num_of_arcs) - offset
        pi_circle = VGroup()

        pi = MathTex("\\pi", font_size=72).set_color(BLACK)
        pi_circle.add(pi)

        num_points = [
            np.array([(radius + 0.7) * np.sin(s),
                      (radius + 0.7) * np.cos(s), 0])
            for s in np.linspace(offset / 2 + arc_length / 2, TAU - arc_length / 2 - offset / 2, num_of_arcs)
        ]

        nums = VGroup(*[MathTex(str(i), font_size=36).set_color(BLACK) for i in range(num_of_arcs)])
        for i, num in enumerate(nums):
            num.move_to(num_points[i])
        pi_circle.add(nums)

        arcs_point = [
            (
                np.array([(radius + 0.3) * np.sin(s),
                          (radius + 0.3) * np.cos(s), 0]),
                np.array([(radius + 0.3) * np.sin(e),
                          (radius + 0.3) * np.cos(e), 0])
            )
            for s, e in zip(
                np.linspace(offset / 2, TAU - arc_length - offset / 2, num_of_arcs),
                np.linspace(arc_length + offset / 2, TAU - offset / 2, num_of_arcs)
            )
        ]

        arcs = VGroup(*[
            ArcBetweenPoints(
                p[0], p[1],
                color=colors[i],
                angle=-arc_length,
                stroke_width=20
            )
            for i, p in enumerate(arcs_point)
        ])
        pi_circle.add(arcs)

        curve_points = [
            np.array([radius * np.sin(s), radius * np.cos(s), 0])
            for s in np.linspace(offset / 2, TAU - arc_length - offset / 2, num_of_arcs)
        ]

        curve_dots = [Dot(p) for p in curve_points]
        curve_dots1 = curve_dots.copy()
        curve_pointer = [0] * len(curve_dots)

        n = 1000
        pi_n = get_n_digits_of_pi(n)
        path = VMobject(stroke_width=2, stroke_opacity=0.05)
        paths = VGroup()
        len_of_arc = 360 / num_of_arcs - offset / DEGREES

        for i in range(n - 1):
            new_path = path.copy()
            new_path.set_color_by_gradient(colors[pi_n[i]])
            #new_path.set_color(colors[pi_n[i]])
            p0 = curve_dots1[pi_n[i]].get_center()
            curve_pointer[pi_n[i + 1]] = -(0.01 * (i + 1) % len_of_arc) * DEGREES
            curve_dots1[pi_n[i + 1]] = curve_dots[pi_n[i + 1]].copy().rotate(
                curve_pointer[pi_n[i + 1]],
                about_point=ORIGIN
            )

            p1 = curve_dots1[pi_n[i + 1]].get_center()
            h = ORIGIN

            if pi_n[i] != pi_n[i + 1]:
                points = [bezier([p0, h, p1])(t) for t in np.linspace(0, 1, 3)]
                if np.allclose(points[1], ORIGIN, atol=0.1):
                    points = [ORIGIN]
                new_path.set_points_smoothly(points)
            pi_circle.add(new_path)
            paths.add(new_path)

        #self.camera.set_frame_width(2 * pi_circle.get_width())


        self.play(
            AnimationGroup(
                Create(arcs),
                Write(nums),
                lag_ratio=0.2
            ),
            run_time=5,
            rate_func=linear,
        )
        self.play(Write(pi), run_time=3)
        self.play(Create(paths), run_time=20, rate_func=linear)
        self.play(self.camera.frame.animate.set_width(2 * pi_circle.get_width()), run_time=2)
        self.wait()
        
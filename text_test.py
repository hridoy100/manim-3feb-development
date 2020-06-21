from big_ol_pile_of_manim_imports import *


class AudioTest(Scene):
    def construct(self):
        group_dots = VGroup(*[Dot() for _ in range(3)])
        group_dots.arrange_submobjects(RIGHT)
        for dot in group_dots:
            self.add_sound("click", gain=10)
            self.play(FadeIn(dot))
            self.wait()
        self.wait()


class SVGTest(Scene):
    def construct(self):
        svg = SVGMobject("finger")
        self.play(DrawBorderThenFill(svg, rate_func=linear))
        self.wait()


class ImageTest(Scene):
    def construct(self):
        img = ImageMobject("note")
        self.play(FadeIn(img))
        self.wait()
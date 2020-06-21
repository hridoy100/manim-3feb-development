from big_ol_pile_of_manim_imports import *

class Formula(Scene):
    def construct(self):
        formula_tex = TexMobject("""
            This is a regular text,
            \\displaystyle\\frac{x}{y},
            x^2+y^2=a^2
            """)
        formula_tex.scale(2)
        self.add(formula_tex)

from manim import *
import numpy as np

class VolumeIntegration(ThreeDScene):
    def construct(self):
        # Set up the 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # Create the axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 4, 1],
            x_length=6,
            y_length=6,
            z_length=5
        )
        
        # Function to rotate (x = y^2)
        def func(x):
            return x**2/2
            
        # Create the curve
        curve = ParametricFunction(
            lambda t: axes.c2p(t, func(t), 0),
            t_range=[-1, 2],
            color=BLUE
        )
        
        # Create labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        
        # Add initial elements
        self.add(axes, x_label, y_label, z_label)
        
        # Show the curve
        self.play(Create(curve))
        self.wait()
        
        # Create vertical lines (riemann sum visualization)
        dx = 0.2
        x_range = np.arange(-1, 2, dx)
        rects = VGroup()
        
        for x in x_range:
            height = func(x)
            rect = Surface(
                lambda u, v: axes.c2p(
                    x + u * dx,
                    height * np.cos(v),
                    height * np.sin(v)
                ),
                u_range=[0, 1],
                v_range=[0, TAU],
                checkerboard_colors=[BLUE_D, BLUE_E],
                fill_opacity=0.7
            )
            rects.add(rect)
        
        # Animate the creation of volume elements
        self.play(
            *[Create(rect) for rect in rects],
            run_time=3,
            rate_func=linear
        )
        self.wait()
        
        # Add formula
        formula = MathTex(
            r"V = \pi \int_{-1}^{2} (x^2/2)^2 dx"
        ).to_corner(UL)
        
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        
        # Rotate the scene to show the 3D nature
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # Final pause
        self.wait(2)
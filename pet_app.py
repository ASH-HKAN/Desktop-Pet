import os
import sys
import math
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

SIZE = 160
CENTER = SIZE // 2

# Physics constants
GRAVITY = 25.0              # pixels/s^2
FRICTION = 0.995            # Air resistance (1.0 = no friction)
GROUND_FRICTION = 0.85      # Speed reduction on ground
RESTITUTION = 0.75          # Bounciness (0.0 = no bounce, 1.0 = perfect)
THROW_SENSITIVITY = 0.8     # How fast velocity accumulates

def draw_3d_sphere(draw, cx, cy, radius, base_color, highlight_color, dark_color):
    """Renders a smooth 3D shaded sphere using radial layering."""
    for r in range(radius, 0, -1):
        t = (radius - r) / radius
        lx = cx - int(radius * 0.3 * (1 - t))
        ly = cy - int(radius * 0.3 * (1 - t))

        if t < 0.6:
            factor = t / 0.6
            cr = int(dark_color[0] * (1 - factor) + base_color[0] * factor)
            cg = int(dark_color[1] * (1 - factor) + base_color[1] * factor)
            cb = int(dark_color[2] * (1 - factor) + base_color[2] * factor)
        else:
            factor = (t - 0.6) / 0.4
            cr = int(base_color[0] * (1 - factor) + highlight_color[0] * factor)
            cg = int(base_color[1] * (1 - factor) + highlight_color[1] * factor)
            cb = int(base_color[2] * (1 - factor) + highlight_color[2] * factor)

        draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(cr, cg, cb, 255))

    # Specular glossy highlight
    spot_x = cx - int(radius * 0.35)
    spot_y = cy - int(radius * 0.35)
    spot_r = max(2, radius // 5)
    draw.ellipse([spot_x - spot_r, spot_y - spot_r, spot_x + spot_r, spot_y + spot_r], fill=(255, 255, 255, 230))

def create_super_cute_pet(state, frame_idx, total_frames):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Super cute Honey-Cream & Warm Peach Toy Palette
    BASE_COLOR = (255, 190, 90)
    HIGH_COLOR = (255, 235, 170)
    DARK_COLOR = (200, 120, 20)

    BELLY_BASE = (255, 235, 200)
    BELLY_HIGH = (255, 250, 225)
    BELLY_DARK = (230, 180, 130)

    EYE_DARK = (30, 20, 15)

    # Physics squash / stretch factors
    squish_x = 0
    squish_y = 0
    bounce = 0
    eye_mode = "normal"
    arm_raise = 0
    show_sigh = False

    if state == "idle":
        bounce = int(math.sin(frame_idx / total_frames * math.pi * 2) * 3)
        if frame_idx >= total_frames - 2:
            eye_mode = "big_puss_in_boots"
    elif state == "walk":
        bounce = abs(int(math.sin(frame_idx / total_frames * math.pi * 2) * 5))
        squish_x = int(math.sin(frame_idx / total_frames * math.pi * 2) * 3)
    elif state == "drag":
        squish_y = 10
        squish_x = -5
        eye_mode = "big_puss_in_boots"
        arm_raise = 14
    elif state == "fall":
        bounce = int(math.sin(frame_idx / total_frames * math.pi * 4) * 6)
        squish_y = -6
        squish_x = 4
        eye_mode = "big_puss_in_boots"
    elif state == "squish_impact":
        squish_y = -18
        squish_x = 14
        eye_mode = "dizzy"
    elif state == "dizzy":
        eye_mode = "dizzy"
    elif state == "sleep":
        bounce = int(math.sin(frame_idx / total_frames * math.pi * 2) * 2)
        eye_mode = "sleep"
        if frame_idx in [3, 4, 5]:
            show_sigh = True
    elif state == "prep_jump":
        squish_y = -8
        squish_x = 6
        eye_mode = "normal"
    elif state == "jump":
        squish_y = 8
        squish_x = -4
        eye_mode = "normal"

    # 3D Round Cute Ears
    draw_3d_sphere(draw, CENTER - 32, CENTER - 35, 16, BASE_COLOR, HIGH_COLOR, DARK_COLOR)
    draw_3d_sphere(draw, CENTER + 32, CENTER - 35, 16, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # 3D Main Body
    body_rx = 42 + squish_x
    body_ry = 38 + squish_y
    draw_3d_sphere(draw, CENTER, CENTER + 10 - bounce, body_rx, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # Chubby Belly
    draw_3d_sphere(draw, CENTER, CENTER + 20 - bounce, 26, BELLY_BASE, BELLY_HIGH, BELLY_DARK)

    # Cute Little Paws / Arms
    arm_y = CENTER + 8 - arm_raise
    draw_3d_sphere(draw, CENTER - 38, arm_y, 11, BASE_COLOR, HIGH_COLOR, DARK_COLOR)
    draw_3d_sphere(draw, CENTER + 38, arm_y, 11, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # FACE & EYES
    eye_y = CENTER + 2 - bounce
    left_x = CENTER - 18
    right_x = CENTER + 18

    if eye_mode in ["normal", "big_puss_in_boots"]:
        eye_rw = 15 if eye_mode == "big_puss_in_boots" else 10
        eye_rh = 17 if eye_mode == "big_puss_in_boots" else 12
        draw.ellipse([left_x - eye_rw, eye_y - eye_rh, left_x + eye_rw, eye_y + eye_rh], fill=EYE_DARK)
        draw.ellipse([right_x - eye_rw, eye_y - eye_rh, right_x + eye_rw, eye_y + eye_rh], fill=EYE_DARK)

        highlight_size = 6 if eye_mode == "big_puss_in_boots" else 4
        draw.ellipse([left_x - highlight_size, eye_y - highlight_size, left_x + 2, eye_y + 2], fill=(255, 255, 255, 255))
        draw.ellipse([right_x - highlight_size, eye_y - highlight_size, right_x + 2, eye_y + 2], fill=(255, 255, 255, 255))
        draw.ellipse([left_x + 2, eye_y + 3, left_x + 6, eye_y + 7], fill=(255, 255, 255, 200))
        draw.ellipse([right_x + 2, eye_y + 3, right_x + 6, eye_y + 7], fill=(255, 255, 255, 200))

        draw.arc([left_x - 10, eye_y - 18, left_x + 10, eye_y - 8], 180, 360, fill=DARK_COLOR, width=3)
        draw.arc([right_x - 10, eye_y - 18, right_x + 10, eye_y - 8], 180, 360, fill=DARK_COLOR, width=3)

    elif eye_mode == "sleep":
        draw.arc([left_x - 9, eye_y - 4, left_x + 9, eye_y + 6], 0, 180, fill=EYE_DARK, width=3)
        draw.arc([right_x - 9, eye_y - 4, right_x + 9, eye_y + 6], 0, 180, fill=EYE_DARK, width=3)

    elif eye_mode == "dizzy":
        for ex in [left_x, right_x]:
            draw.arc([ex - 9, eye_y - 9, ex + 9, eye_y + 9], 0, 270, fill=EYE_DARK, width=3)

    # Cute button nose
    draw_3d_sphere(draw, CENTER, CENTER + 12 - bounce, 5, (230, 90, 40), (255, 160, 110), (150, 40, 10))

    # Rosy pink blush cheeks
    draw.ellipse([left_x - 14, eye_y + 8, left_x - 2, eye_y + 16], fill=(255, 110, 130, 140))
    draw.ellipse([right_x + 2, eye_y + 8, right_x + 14, eye_y + 16], fill=(255, 110, 130, 140))

    # Smile
    draw.arc([CENTER - 7, CENTER + 18 - bounce, CENTER + 7, CENTER + 25 - bounce], 20, 160, fill=DARK_COLOR, width=3)

    # Optional: Zzz and Sigh cloud for sleep mode
    if eye_mode == "sleep" and not show_sigh:
        zx = CENTER + 35 + (frame_idx * 2)
        zy = CENTER - 30 - (frame_idx * 3)
        draw.text((zx, zy), "Z", fill=(100, 170, 255, 230))

    if show_sigh:
        cx = CENTER + 30 + (frame_idx - 3) * 4
        cy = CENTER - 12 - (frame_idx - 3) * 2
        draw.ellipse([cx, cy, cx + 20, cy + 14], fill=(245, 250, 255, 210), outline=(180, 205, 230, 230))
        draw.ellipse([cx + 10, cy - 6, cx + 26, cy + 8], fill=(245, 250, 255, 210))
        draw.line([cx - 8, cy + 8, cx, cy + 6], fill=(180, 205, 230, 190), width=2)

    return img

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "#010101")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Initialize monitor system
        self.init_monitor_system()

        self.floor = 0
        self.min_y = 0
        self.max_y = self.screen_height
        self.min_x = 0
        self.max_x = self.screen_width

        # Pet position
        self.x = self.max_x // 2
        self.y = self.floor - SIZE

        # Physics state
        self.vx = 0.0  # Velocity X
        self.vy = 0.0  # Velocity Y
        self.is_Throwing = False

        # Throwing mechanics
        self.drag_start_pos = None
        self.drag_mouse_positions = []
        self.drag_frame_count = 0
        self.max_drag_frames = 15

        # Create borderless canvas
        self.canvas = tk.Canvas(root, width=SIZE, height=SIZE, bg="#010101", highlightthickness=0)
        self.canvas.pack()

        # Bind events
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Double-Button-1>", self.double_click)
        self.canvas.bind("<Button-3>", self.show_menu)

        self.state = "idle"
        self.frame_idx = 0
        self.facing_left = True

        # Generate sprites
        self.sprite_cache = {}
        self.generate_sprites()

        # Start separate physics and animation loops
        self.last_time = 0
        self.animation_last_time = 0

        self.root.after(16, self.physics_update)      # Physics at ~60 FPS
        self.root.after(100, self.animation_update)   # Animation frames at ~10 FPS

    def init_monitor_system(self):
        """
        Initialize the monitor system based on platform.
        Supports Windows (ctypes) and fallback to single monitor for Linux.
        """
        if sys.platform == 'win32':
            self.init_windows_monitors()
        else:
            # Fallback for Linux/telnet: single monitor spanning entire screen
            self.min_y = 0
            self.max_y = self.root.winfo_screenheight()
            self.min_x = 0
            self.max_x = self.root.winfo_screenwidth()
            self.monitors = [{
                'rect': (self.min_x, self.min_y, self.max_x, self.max_y),
                'name': 'Monitor 1'
            }]
            self.floor = self.max_y - 180

    def init_windows_monitors(self):
        """Initialize monitor detection using ctypes on Windows."""
        try:
            import ctypes
            from ctypes import wintypes

            # Define necessary types
            wintypes.ULONG = ctypes.c_ulong
            wintypes.DWORD = ctypes.c_ulong
            wintypes.LONG = ctypes.c_long
            wintypes.ULONG_PTR = ctypes.c_ulong

            # Monitor info constants
            MONITORINFOF_PRIMARY = 0x00000001
            MONITORINFOF_MONITOR = 0x00000001
            MONITORINFOF_DESKTOP = 0x00000001

            # Monitor info structure
            class MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", wintypes.DWORD),
                    ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT),
                    ("dwFlags", wintypes.DWORD),
                ]

            # Define EnumDisplayMonitors callback
            ENUMHMONITOREXPROC = ctypes.WINFUNCTYPE(
                wintypes.BOOL,
                ctypes.c_void_p,
                ctypes.POINTER(wintypes.RECT),
                ctypes.POINTER(MONITORINFO),
                ctypes.wintypes.DWORD
            )

            # Callback function
            def monitor_enum_proc(hMonitor, hMonitorDC, lprcMonitor, dwData):
                # Get monitor info
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(MONITORINFO)

                ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info))

                rect = (lprcMonitor.cx, lprcMonitor.cy, lprcMonitor.right, lprcMonitor.bottom)
                monitors.append({
                    'rect': rect,
                    'name': f"Monitor {len(monitors) + 1}"
                })
                return True

            # Get screen coordinate mapping
            def mapping_callback(hMonitor, hMonitorDC, lprcMonitor, dwData):
                screen_info = ctypes.POINTER(wintypes.RECT)()
                ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(screen_info))
                return True

            monitors = []
            callback = ENUMHMONITOREXPROC(monitor_enum_proc)

            # Enumerate monitors
            if ctypes.windll.user32.EnumDisplayMonitors(None, None, callback, 0):
                self.monitors = monitors

                # Constrain pet to all monitor bounds
                self.min_x = min(m['rect'][0] for m in monitors)
                self.min_y = min(m['rect'][1] for m in monitors)
                self.max_x = max(m['rect'][2] for m in monitors)
                self.max_y = max(m['rect'][3] for m in monitors)
            else:
                # Fallback to single monitor
                self.monitors = [{
                    'rect': (0, 0, self.screen_width, self.screen_height),
                    'name': 'Main Monitor'
                }]
                self.max_x = self.screen_width
                self.max_y = self.screen_height

        except Exception as e:
            print(f"Error initializing monitors: {e}")
            # Fallback to single monitor
            self.monitors = [{
                'rect': (0, 0, self.screen_width, self.screen_height),
                'name': 'Fallback Monitor'
            }]
            self.max_x = self.screen_width
            self.max_y = self.screen_height

        # Determine floor based on Y position within any monitor bounds
        self.floor = self.max_y - 180

        # Find which monitor we're currently on
        self.current_monitor_idx = 0
        for i, monitor in enumerate(self.monitors):
            mx, my, mxw, mxh = monitor['rect']
            if self.x >= mx and self.x <= mx + SIZE and self.y >= my and self.y <= my + SIZE:
                self.current_monitor_idx = i
                break

    def get_current_monitor(self):
        """Get the monitor containing the pet's current position."""
        # If at bounds, prefer next/previous monitor
        mx, my, mw, mh = self.monitors[self.current_monitor_idx]['rect']

        if self.x <= mx + 5:
            self.current_monitor_idx = 0
        elif self.x >= mx + mw - 5:
            self.current_monitor_idx = len(self.monitors) - 1

        return self.monitors[self.current_monitor_idx]

    def start_drag(self, event):
        self.state = "drag"
        self.frame_idx = 0
        self.drag_start_pos = (event.x_root, event.y_root)
        self.drag_mouse_positions = []
        self.drag_frame_count = 0

    def drag(self, event):
        self.drag_frame_count += 1
        self.drag_mouse_positions.append((event.x_root, event.y_root))

        # Keep only recent positions for velocity calculation
        if len(self.drag_mouse_positions) > self.max_drag_frames:
            self.drag_mouse_positions.pop(0)

        self.x = event.x_root - self.drag_offset_x
        self.y = event.y_root - self.drag_offset_y
        self.root.geometry(f"{SIZE}x{SIZE}+{int(self.x)}+{int(self.y)}")

        # Auto-switch to the monitor we're dragging on
        current_monitor = self.get_current_monitor()
        mx, my, mw, mh = current_monitor['rect']
        if mx != self.min_x or my != self.min_y or mw != self.max_x - self.min_x or mh != self.max_y - self.min_y:
            self.current_monitor_idx = self.monitors.index(current_monitor)

    def end_drag(self, event):
        # Calculate throw velocity based on mouse movement during drag
        if len(self.drag_mouse_positions) > 2:
            # Take last few positions to calculate velocity
            last_n = min(10, len(self.drag_mouse_positions))
            positions = self.drag_mouse_positions[-last_n:]

            pixel_dx = positions[-1][0] - positions[0][0]
            pixel_dy = positions[-1][1] - positions[0][1]
            frames_delta = self.drag_frame_count

            # Calculate velocity in pixels per frame
            self.vx = pixel_dx / frames_delta * THROW_SENSITIVITY
            self.vy = pixel_dy / frames_delta * THROW_SENSITIVITY

        self.drag_start_pos = None
        self.drag_mouse_positions = []

        current_monitor = self.get_current_monitor()
        mx, my, mw, mh = current_monitor['rect']

        # Determine if we should be in freefall or on the floor
        if self.y < my + mh - SIZE:
            self.state = "fall"
        else:
            self.y = my + mh - SIZE
            self.state = "idle"

    def double_click(self, event):
        if self.state not in ["drag", "fall", "jump", "prep_jump"]:
            self.state = "prep_jump"
            self.frame_idx = 0

    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Play / Wake Up", command=self.wake_up)
        menu.add_command(label="Sleep", command=self.go_to_sleep)
        menu.add_command(label="Jump!", command=self.trigger_jump)
        menu.add_command(label="Walk Around", command=self.trigger_walk)
        menu.add_separator()
        menu.add_command(label="Exit Pet", command=self.root.destroy)
        menu.post(event.x_root, event.y_root)

    def wake_up(self):
        self.state = "idle"
        self.frame_idx = 0

    def go_to_sleep(self):
        self.state = "sleep"
        self.frame_idx = 0

    def trigger_jump(self):
        self.state = "prep_jump"
        self.frame_idx = 0

    def trigger_walk(self):
        self.state = "walk"
        self.frame_idx = 0
        self.facing_left = random.choice([True, False])

    def physics_update(self):
        """Physics simulation at 60 FPS (16ms interval)."""
        # Current monitor bounds
        current_monitor = self.get_current_monitor()
        mx, my, mw, mh = current_monitor['rect']

        # Floor for current monitor
        monitor_floor = my + mh - SIZE

        if self.state == "fall":
            # Apply gravity
            self.vy += GRAVITY

            # Apply velocity
            self.x += self.vx
            self.y += self.vy

            # Air resistance
            self.vx *= FRICTION
            self.vy *= FRICTION

            # Check for crossing monitor boundaries
            self.check_monitor_bounds(current_monitor)

            # Ground collision detection
            if self.y >= monitor_floor:
                self.y = monitor_floor

                # Bounce if we had significant velocity
                if abs(self.vy) > 15:
                    self.vy = -self.vy * RESTITUTION
                    self.vx *= GROUND_FRICTION
                    self.start_bouncing()

                    # Switch state to squish_impact
                    if abs(self.vy) > 20:
                        self.state = "squish_impact"
                        self.frame_idx = 0
                else:
                    # Low velocity - settle
                    self.y = monitor_floor
                    self.vy = 0
                    self.vx *= GROUND_FRICTION

                    if abs(self.vx) > 1:
                        self.state = "walk"
                        self.frame_idx = 0
                    else:
                        self.vx = 0
                        self.state = "idle"
                        self.frame_idx = 0

            # Wall collisions (elastic)
            if self.x < mx:
                self.x = mx
                self.vx = -self.vx * RESTITUTION
                self.vx *= GROUND_FRICTION
                if abs(self.vx) < 2:
                    self.vx = 0

            if self.x + SIZE > mx + mw:
                self.x = mx + mw - SIZE
                self.vx = -self.vx * RESTITUTION
                self.vx *= GROUND_FRICTION
                if abs(self.vx) < 2:
                    self.vx = 0

        elif self.state == "walk":
            # Apply friction after walk momentum dissipates
            self.vx *= GROUND_FRICTION

            if abs(self.vx) > 1:
                self.x += self.vx
                self.facing_left = self.vx < 0

                self.check_monitor_bounds(current_monitor)
            else:
                self.vx = 0
                self.state = "idle"

        elif self.state == "jump":
            # Mark as active physical object
            self.is_Throwing = True

        elif self.state == "prep_jump":
            self.facing_left = self.drag_mouse_positions[-1][0] < self.drag_mouse_positions[0][0] if self.drag_mouse_positions else True

        # Boundary checks for all states
        self.check_monitor_bounds(current_monitor)

        # Update window position (smooth frame-based movement)
        self.root.geometry(f"{SIZE}x{SIZE}+{int(self.x)}+{int(self.y)}")

        # Continue physics loop
        self.root.after(16, self.physics_update)

    def check_monitor_bounds(self, current_monitor):
        """Check if pet crossed into another monitor."""
        mx, my, mw, mh = current_monitor['rect']

        # Check if pet is not in current monitor bounds
        if self.x < mx or self.x + SIZE > mx + mw or self.y < my or self.y + SIZE > my + mh:
            # Find correct monitor
            for i, monitor in enumerate(self.monitors):
                mmx, mmy, mmw, mmh = monitor['rect']
                if (mx <= self.x <= mmx + mmw and my <= self.y <= mmy + mmh and
                    mx + SIZE >= mmx and self.y + SIZE <= mmy + mmh):
                    self.current_monitor_idx = i
                    break

    def start_bouncing(self):
        """Start bounce animation if not already bouncing."""
        if self.state not in ["fall", "squish_impact", "walk", "jump"]:
            self.state = "fall"
            self.frame_idx = 0

    def animation_update(self):
        """Animation frame update at ~10 FPS (100ms interval)."""
        # Increment animation frame
        self.frame_idx += 1

        # Handle state transitions based on frame count
        frame_count = self.get_frames_for_state(self.state)

        if self.frame_idx >= frame_count:
            # End of animation loop for this state
            self.frame_idx = 0

            # Mark as not throwing once we reach final state
            self.is_Throwing = False

            if self.state == "squish_impact":
                if abs(self.vy) < 20:
                    self.state = "idle" if abs(self.vx) <= 2 else "walk"
                else:
                    self.state = "fall"
            elif self.state == "dizzy":
                self.state = "idle"
            elif self.state == "prep_jump":
                self.state = "jump"
                self.vx = 8 if self.facing_left else -8  # Initial push
                self.vy = -18  # Jump height
            elif self.state == "jump":
                self.state = "fall"
            elif self.state == "idle":
                # Random transitions
                r = random.random()
                if r < 0.15:
                    self.state = "walk"
                    self.frame_idx = 0
                    self.facing_left = random.choice([True, False])
                elif r < 0.22:
                    self.state = "sleep"
                    self.frame_idx = 0
            elif self.state == "walk":
                # Random transitions from walk
                if random.random() < 0.20:
                    self.state = "idle"
                    self.frame_idx = 0

        # Step through current animation
        frames = self.sprite_cache[self.state]["left" if self.facing_left else "right"]
        if self.frame_idx < len(frames):
            current_frame = frames[self.frame_idx]
            self.canvas.delete("all")
            self.canvas.create_image(SIZE // 2, SIZE // 2, image=current_frame)

        # Continue animation loop
        self.root.after(100, self.animation_update)

    def get_frames_for_state(self, state):
        """Get frame count for a given state (fallback to 8 if unknown)."""
        return self.sprite_cache.get(state, {}).get("left", [None, None]) or [None, None]

    def generate_sprites(self):
        states = {
            "idle": 6,
            "walk": 8,
            "drag": 4,
            "fall": 6,
            "squish_impact": 4,
            "dizzy": 4,
            "sleep": 8,
            "prep_jump": 4,
            "jump": 6
        }
        for state, count in states.items():
            self.sprite_cache[state] = {
                "left": [],
                "right": []
            }
            for i in range(count):
                img = create_super_cute_pet(state, i, count)

                photo_left = ImageTk.PhotoImage(img)
                self.sprite_cache[state]["left"].append(photo_left)

                img_right = img.transpose(Image.FLIP_LEFT_RIGHT)
                photo_right = ImageTk.PhotoImage(img_right)
                self.sprite_cache[state]["right"].append(photo_right)

def main():
    root = tk.Tk()
    root.title("Physics Desktop Pet")
    pet = DesktopPet(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import os
import sys
import math
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

SIZE = 160  # Size of pet canvas
CENTER = SIZE // 2

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
    eye_mode = "normal"  # normal, big_puss_in_boots, dizzy, sleep
    arm_raise = 0
    show_sigh = False

    if state == "idle":
        bounce = int(math.sin(frame_idx / total_frames * math.pi * 2) * 3)
        if frame_idx >= total_frames - 2:
            eye_mode = "big_puss_in_boots"  # Cartoon pleading giant puppy eyes!
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
        # Realistic squish when hitting the ground like rubber / jelly!
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

    # Drop shadow
    shadow_w = 40 + squish_x
    shadow_h = 9 - (bounce // 2)
    if shadow_h > 1 and state != "squish_impact":
        draw.ellipse([CENTER - shadow_w, SIZE - 20 - shadow_h, CENTER + shadow_w, SIZE - 20 + shadow_h], fill=(0, 0, 0, 45))

    body_cx = CENTER
    body_cy = CENTER + 10 - bounce

    # 3D Round Cute Ears
    draw_3d_sphere(draw, body_cx - 32, body_cy - 35, 16, BASE_COLOR, HIGH_COLOR, DARK_COLOR)
    draw_3d_sphere(draw, body_cx + 32, body_cy - 35, 16, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # 3D Main Body (Squishable)
    body_rx = 42 + squish_x
    body_ry = 38 + squish_y
    draw_3d_sphere(draw, body_cx, body_cy, body_rx, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # Chubby Belly
    draw_3d_sphere(draw, body_cx, body_cy + 10, 26, BELLY_BASE, BELLY_HIGH, BELLY_DARK)

    # Cute Little Paws / Arms
    arm_y = body_cy - 2 - arm_raise
    draw_3d_sphere(draw, body_cx - 38, arm_y, 11, BASE_COLOR, HIGH_COLOR, DARK_COLOR)
    draw_3d_sphere(draw, body_cx + 38, arm_y, 11, BASE_COLOR, HIGH_COLOR, DARK_COLOR)

    # FACE & EYES (Puss in Boots Giant Anime Eyes)
    eye_y = body_cy - 8
    left_x = body_cx - 18
    right_x = body_cx + 18

    if eye_mode in ["normal", "big_puss_in_boots"]:
        # Giant cute sparkling anime eyes (proper ellipse with w and h)
        eye_rw = 15 if eye_mode == "big_puss_in_boots" else 10
        eye_rh = 17 if eye_mode == "big_puss_in_boots" else 12
        draw.ellipse([left_x - eye_rw, eye_y - eye_rh, left_x + eye_rw, eye_y + eye_rh], fill=EYE_DARK)
        draw.ellipse([right_x - eye_rw, eye_y - eye_rh, right_x + eye_rw, eye_y + eye_rh], fill=EYE_DARK)

        # Multiple glossy reflections for that emotional "pleading" look
        highlight_size = 6 if eye_mode == "big_puss_in_boots" else 4
        draw.ellipse([left_x - highlight_size, eye_y - highlight_size, left_x + 2, eye_y + 2], fill=(255, 255, 255, 255))
        draw.ellipse([right_x - highlight_size, eye_y - highlight_size, right_x + 2, eye_y + 2], fill=(255, 255, 255, 255))
        # Secondary bottom catchlight
        draw.ellipse([left_x + 2, eye_y + 3, left_x + 6, eye_y + 7], fill=(255, 255, 255, 200))
        draw.ellipse([right_x + 2, eye_y + 3, right_x + 6, eye_y + 7], fill=(255, 255, 255, 200))

        # Cute eyebrows raised high in cute innocence
        draw.arc([left_x - 10, eye_y - 18, left_x + 10, eye_y - 8], 180, 360, fill=DARK_COLOR, width=3)
        draw.arc([right_x - 10, eye_y - 18, right_x + 10, eye_y - 8], 180, 360, fill=DARK_COLOR, width=3)

    elif eye_mode == "sleep":
        draw.arc([left_x - 9, eye_y - 4, left_x + 9, eye_y + 6], 0, 180, fill=EYE_DARK, width=3)
        draw.arc([right_x - 9, eye_y - 4, right_x + 9, eye_y + 6], 0, 180, fill=EYE_DARK, width=3)

    elif eye_mode == "dizzy":
        for ex in [left_x, right_x]:
            draw.arc([ex - 9, eye_y - 9, ex + 9, eye_y + 9], 0, 270, fill=EYE_DARK, width=3)

    # Cute button nose
    draw_3d_sphere(draw, body_cx, body_cy + 2, 5, (230, 90, 40), (255, 160, 110), (150, 40, 10))

    # Rosy pink blush cheeks
    draw.ellipse([left_x - 14, eye_y + 8, left_x - 2, eye_y + 16], fill=(255, 110, 130, 140))
    draw.ellipse([right_x + 2, eye_y + 8, right_x + 14, eye_y + 16], fill=(255, 110, 130, 140))

    # Smile
    draw.arc([body_cx - 7, body_cy + 8, body_cx + 7, body_cy + 15], 20, 160, fill=DARK_COLOR, width=3)

    # Zzz and Sigh cloud
    if eye_mode == "sleep" and not show_sigh:
        zx = body_cx + 35 + (frame_idx * 2)
        zy = body_cy - 30 - (frame_idx * 3)
        draw.text((zx, zy), "Z", fill=(100, 170, 255, 230))

    if show_sigh:
        cx = body_cx + 30 + (frame_idx - 3) * 4
        cy = body_cy - 12 - (frame_idx - 3) * 2
        draw.ellipse([cx, cy, cx + 20, cy + 14], fill=(245, 250, 255, 210), outline=(180, 205, 230, 230))
        draw.ellipse([cx + 10, cy - 6, cx + 26, cy + 8], fill=(245, 250, 255, 210))
        draw.line([cx - 8, cy + 8, cx, cy + 6], fill=(180, 205, 230, 190), width=2)

    return img

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        # Transparent key color is almost black (#010101) so shadow blending is seamless
        self.root.wm_attributes("-transparentcolor", "#010101")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Keep 100px gap from taskbar/bottom of the screen
        self.floor = self.screen_height - 180

        # Center the pet horizontally
        self.x = self.screen_width // 2
        self.y = self.floor

        # Create a seamless borderless canvas
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
        self.vel_y = 0

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Generate sprites in-memory
        self.sprite_cache = {}
        self.generate_sprites()

        # Start game loop
        self.update()

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

                # Default (facing left)
                photo_left = ImageTk.PhotoImage(img)
                self.sprite_cache[state]["left"].append(photo_left)

                # Flipped (facing right)
                img_right = img.transpose(Image.FLIP_LEFT_RIGHT)
                photo_right = ImageTk.PhotoImage(img_right)
                self.sprite_cache[state]["right"].append(photo_right)

    def start_drag(self, event):
        self.state = "drag"
        self.frame_idx = 0
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y

    def drag(self, event):
        self.x = event.x_root - self.drag_offset_x
        self.y = event.y_root - self.drag_offset_y
        self.root.geometry(f"{SIZE}x{SIZE}+{self.x}+{self.y}")

    def end_drag(self, event):
        if self.y < self.floor:
            self.state = "fall"
            self.vel_y = 0
        else:
            self.y = self.floor
            self.state = "idle"
            self.frame_idx = 0

    def double_click(self, event):
        # Trigger an adorable jump on double-click!
        if self.state not in ["drag", "fall", "jump", "prep_jump"]:
            self.state = "prep_jump"
            self.frame_idx = 0

    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🌸 Play / Wake Up", command=self.wake_up)
        menu.add_command(label="💤 Sleep", command=self.go_to_sleep)
        menu.add_command(label="🦘 Jump!", command=self.trigger_jump)
        menu.add_command(label="🚶 Walk Around", command=self.trigger_walk)
        menu.add_separator()
        menu.add_command(label="❌ Exit Pet", command=self.root.destroy)
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

    def update(self):
        # Apply physics
        if self.state == "fall":
            self.vel_y += 1.5
            if self.vel_y > 15:
                self.vel_y = 15
            self.y += int(self.vel_y)

            if self.y >= self.floor:
                self.y = self.floor
                self.state = "squish_impact"
                self.frame_idx = 0
                self.vel_y = 0

        elif self.state == "walk":
            speed = 2 if self.facing_left else -2
            self.x -= speed
            if self.x < 0:
                self.x = 0
                self.facing_left = False
            elif self.x > self.screen_width - SIZE:
                self.x = self.screen_width - SIZE
                self.facing_left = True

        elif self.state == "jump":
            frames = self.sprite_cache["jump"]["left"]
            frames_count = len(frames)

            # Use sine wave to map height cleanly and return to exact floor
            jump_height = int(math.sin(self.frame_idx / frames_count * math.pi) * 80)
            self.y = self.floor - jump_height

            # Jump forward
            jump_speed = 4 if self.facing_left else -4
            self.x -= jump_speed
            if self.x < 0: self.x = 0
            if self.x > self.screen_width - SIZE: self.x = self.screen_width - SIZE

        # Get current frames list
        frames = self.sprite_cache[self.state]["left" if self.facing_left else "right"]

        # Loop animation frame index
        if self.frame_idx >= len(frames):
            self.frame_idx = 0

            # State transitions upon ending loop cycles
            if self.state == "squish_impact":
                self.state = "dizzy"
            elif self.state == "dizzy":
                self.state = "idle"
            elif self.state == "prep_jump":
                self.state = "jump"
            elif self.state == "jump":
                self.state = "squish_impact"
            elif self.state == "idle":
                # Random transitions from idle
                r = random.random()
                if r < 0.15:
                    self.state = "walk"
                    self.facing_left = random.choice([True, False])
                elif r < 0.22:
                    self.state = "sleep"
            elif self.state == "walk":
                # Random transitions from walk
                if random.random() < 0.20:
                    self.state = "idle"

        # Safe index check in case states switched mid-update
        frames = self.sprite_cache[self.state]["left" if self.facing_left else "right"]
        if self.frame_idx < len(frames):
            current_frame = frames[self.frame_idx]
            self.canvas.delete("all")
            self.canvas.create_image(SIZE // 2, SIZE // 2, image=current_frame)

        # Reposition the borderless window on the desktop
        self.root.geometry(f"{SIZE}x{SIZE}+{self.x}+{self.y}")

        self.frame_idx += 1

        # Play at an optimal frame rate (~100ms per frame)
        self.root.after(100, self.update)

def main():
    root = tk.Tk()
    root.title("Cute Desktop Pet")
    pet = DesktopPet(root)
    root.mainloop()

if __name__ == "__main__":
    main()

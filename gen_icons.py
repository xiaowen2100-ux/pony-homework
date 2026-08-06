"""Generate PNG icons for the PWA app."""
from PIL import Image, ImageDraw
import math

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded rectangle background with pink-purple gradient
    radius = int(size * 0.22)
    # Draw gradient background
    for y in range(size):
        ratio = y / size
        r = int(255 * (1 - ratio) + 155 * ratio)
        g = int(105 * (1 - ratio) + 89 * ratio)
        b = int(180 * (1 - ratio) + 182 * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Mask to rounded rectangle
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
    img.putalpha(mask)
    
    cx, cy = size // 2, size // 2
    
    # Draw pony body (white-pink ellipse)
    body_w = int(size * 0.38)
    body_h = int(size * 0.28)
    body_y = int(size * 0.58)
    draw.ellipse(
        [cx - body_w//2, body_y - body_h//2, cx + body_w//2, body_y + body_h//2],
        fill=(248, 230, 240, 255)
    )
    
    # Draw pony head (ellipse, upper left of body)
    head_w = int(size * 0.27)
    head_h = int(size * 0.25)
    head_x = int(size * 0.38)
    head_y = int(size * 0.40)
    draw.ellipse(
        [head_x - head_w//2, head_y - head_h//2, head_x + head_w//2, head_y + head_h//2],
        fill=(248, 230, 240, 255)
    )
    
    # Draw horn (triangle, gold)
    horn_pts = [
        (head_x - int(size*0.06), head_y - int(size*0.12)),
        (head_x - int(size*0.10), head_y - int(size*0.28)),
        (head_x + int(size*0.01), head_y - int(size*0.13)),
    ]
    draw.polygon(horn_pts, fill=(255, 215, 0, 255))
    
    # Draw ear
    ear_pts = [
        (head_x + int(size*0.02), head_y - int(size*0.10)),
        (head_x + int(size*0.06), head_y - int(size*0.20)),
        (head_x + int(size*0.10), head_y - int(size*0.08)),
    ]
    draw.polygon(ear_pts, fill=(248, 230, 240, 255))
    
    # Draw eye
    eye_r = max(int(size * 0.028), 3)
    eye_x = head_x + int(size * 0.01)
    eye_y = head_y + int(size * 0.01)
    draw.ellipse([eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
                 fill=(74, 59, 92, 255))
    # Eye highlight
    hl_r = max(int(size * 0.010), 1)
    draw.ellipse([eye_x + 1, eye_y - eye_r//2, eye_x + 1 + hl_r*2, eye_y - eye_r//2 + hl_r*2],
                 fill=(255, 255, 255, 255))
    
    # Draw mane (colorful stripes)
    mane_colors = [(255, 215, 0, 255), (255, 105, 180, 255), (93, 173, 226, 255)]
    for i, color in enumerate(mane_colors):
        offset = i * int(size * 0.025)
        mx = head_x + int(size * 0.08) + offset
        my1 = head_y - int(size * 0.10)
        my2 = head_y + int(size * 0.08) + offset
        draw.line([(mx, my1), (mx + int(size*0.02), my2)], fill=color, width=max(int(size*0.018), 2))
    
    # Draw legs
    leg_w = max(int(size * 0.045), 4)
    leg_h = int(size * 0.11)
    leg_y = body_y + int(size * 0.08)
    for i, lx in enumerate([0.32, 0.42, 0.52, 0.62]):
        x = int(size * lx)
        draw.rounded_rectangle([x, leg_y, x + leg_w, leg_y + leg_h], radius=leg_w//2,
                               fill=(248, 230, 240, 255))
    
    # Draw tail (curved)
    tail_pts = [
        (cx + int(size*0.18), body_y),
        (cx + int(size*0.30), body_y - int(size*0.05)),
        (cx + int(size*0.32), body_y + int(size*0.08)),
        (cx + int(size*0.28), body_y + int(size*0.12)),
    ]
    draw.line(tail_pts, fill=(255, 105, 180, 255), width=max(int(size*0.04), 3), joint='curve')
    
    # Draw heart (top right)
    def draw_heart(draw, cx, cy, size_heart, color):
        s = size_heart
        # Two circles + triangle
        r = s // 2
        draw.ellipse([cx - s, cy - r, cx, cy + r], fill=color)
        draw.ellipse([cx, cy - r, cx + s, cy + r], fill=color)
        draw.polygon([
            (cx - s, cy),
            (cx + s, cy),
            (cx, cy + int(s * 1.4))
        ], fill=color)
    
    draw_heart(draw, int(size * 0.72), int(size * 0.25), max(int(size * 0.06), 5), (255, 23, 68, 255))
    
    # Draw stars
    def draw_star(draw, cx, cy, r, color):
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            radius = r if i % 2 == 0 else r * 0.4
            points.append((cx + radius * math.cos(angle), cy - radius * math.sin(angle)))
        draw.polygon(points, fill=color)
    
    draw_star(draw, int(size * 0.20), int(size * 0.20), max(int(size * 0.04), 4), (255, 215, 0, 200))
    draw_star(draw, int(size * 0.82), int(size * 0.75), max(int(size * 0.035), 3), (93, 173, 226, 180))
    draw_star(draw, int(size * 0.15), int(size * 0.75), max(int(size * 0.03), 3), (255, 215, 0, 150))
    
    return img

# Generate both sizes
icon192 = draw_icon(192)
icon192.save('icon-192.png', 'PNG')

icon512 = draw_icon(512)
icon512.save('icon-512.png', 'PNG')

print("Icons generated: icon-192.png, icon-512.png")

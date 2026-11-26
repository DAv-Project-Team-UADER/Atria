import os
from PIL import Image, ImageDraw, ImageFont

def create_atria_icon(output_path):
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background rounded square / hexagon
    padding = 12
    r = 36
    # Outer circle/hexagon with subtle gradient-like look
    # Main dark blue base: #0F2840
    # Accent cyan: #00B4D8
    
    # Background badge
    draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=r,
        fill=(15, 40, 68, 255),
        outline=(0, 180, 216, 255),
        width=6
    )

    # Draw stylized isometric cube / 'A' structure
    # Center: (128, 118)
    cx, cy = 128, 110
    rad = 60
    
    # 3D Cube top face
    top_face = [
        (cx, cy - rad),
        (cx + int(rad * 0.866), cy - int(rad * 0.5)),
        (cx, cy),
        (cx - int(rad * 0.866), cy - int(rad * 0.5))
    ]
    draw.polygon(top_face, fill=(0, 180, 216, 240), outline=(255, 255, 255, 220))

    # Left face
    left_face = [
        (cx - int(rad * 0.866), cy - int(rad * 0.5)),
        (cx, cy),
        (cx, cy + rad),
        (cx - int(rad * 0.866), cy + int(rad * 0.5))
    ]
    draw.polygon(left_face, fill=(10, 120, 160, 240), outline=(255, 255, 255, 200))

    # Right face
    right_face = [
        (cx, cy),
        (cx + int(rad * 0.866), cy - int(rad * 0.5)),
        (cx + int(rad * 0.866), cy + int(rad * 0.5)),
        (cx, cy + rad)
    ]
    draw.polygon(right_face, fill=(6, 75, 110, 240), outline=(255, 255, 255, 200))

    # Soundwave / voice arcs below the cube
    # Wave 1 (inner)
    draw.arc([cx - 45, cy + 30, cx + 45, cy + 100], start=30, end=150, fill=(0, 220, 255, 255), width=5)
    # Wave 2 (middle)
    draw.arc([cx - 65, cy + 20, cx + 65, cy + 115], start=25, end=155, fill=(72, 202, 228, 230), width=6)
    # Wave 3 (outer)
    draw.arc([cx - 85, cy + 10, cx + 85, cy + 130], start=20, end=160, fill=(144, 224, 239, 200), width=6)

    # Central mic dot / pulse
    draw.ellipse([cx - 10, cy + 65, cx + 10, cy + 85], fill=(255, 255, 255, 255))

    # Generate multi-size icon
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(output_path, format="ICO", sizes=sizes)
    print("Icon saved to", output_path)

if __name__ == "__main__":
    out_ico = os.path.join(os.path.dirname(__file__), "atria.ico")
    create_atria_icon(out_ico)

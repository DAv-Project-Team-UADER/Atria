import os
import base64
import shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def build_icons():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    installer_dir = os.path.join(repo_root, "installer")
    guifreecad_logos = os.path.join(repo_root, "GUIFreeCad", "Logos")
    guifreecad_icons = os.path.join(repo_root, "GUIFreeCad", "ui", "Icons")
    interfaz_icons = os.path.join(repo_root, "InterfazATRIA", "Icons")

    os.makedirs(guifreecad_logos, exist_ok=True)
    os.makedirs(guifreecad_icons, exist_ok=True)
    os.makedirs(interfaz_icons, exist_ok=True)

    # Buscar imagen del logo
    candidates = [
        os.path.join(installer_dir, "atria_logo_original.png"),
        os.path.join(installer_dir, "atria_logo_clean.png"),
        r"C:/Users/tadeo/.gemini/antigravity/brain/17e39027-efa7-4eee-a378-47e279d3211e/.user_uploaded/media_1795665686472_84d7f6e7.png"
    ]
    src_image = None
    for c in candidates:
        if os.path.exists(c):
            src_image = c
            break

    if not src_image:
        raise FileNotFoundError("No se encontró la imagen original del logo.")

    print(f"Cargando logo desde: {src_image}")
    # Guardar copia fija del original en installer/atria_logo_original.png
    orig_copy = os.path.join(installer_dir, "atria_logo_original.png")
    if not os.path.exists(orig_copy) or os.path.abspath(src_image) != os.path.abspath(orig_copy):
        shutil.copyfile(src_image, orig_copy)

    img = Image.open(src_image).convert("RGBA")
    arr = np.array(img)

    # 1. Bounding box ajustado
    mask = (arr[:, :, 0] < 240) | (arr[:, :, 1] < 240) | (arr[:, :, 2] < 240)
    y_idx, x_idx = np.where(mask)
    min_y, max_y = y_idx.min(), y_idx.max()
    min_x, max_x = x_idx.min(), x_idx.max()

    pad = 24
    min_x = max(0, min_x - pad)
    max_x = min(img.width - 1, max_x + pad)
    min_y = max(0, min_y - pad)
    max_y = min(img.height - 1, max_y + pad)

    cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    cropped.save(os.path.join(installer_dir, "atria_logo_clean.png"))

    # 2. Generar versión transparente
    c_arr = np.array(cropped).astype(float)
    diff_from_white = 255.0 - np.minimum(np.minimum(c_arr[:, :, 0], c_arr[:, :, 1]), c_arr[:, :, 2])
    alpha = np.clip(diff_from_white * 1.5, 0, 255)

    valid_alpha = alpha > 5
    c_unwhite = np.copy(c_arr)
    for c in range(3):
        c_unwhite[valid_alpha, c] = np.clip((c_arr[valid_alpha, c] - 255.0 * (1.0 - alpha[valid_alpha] / 255.0)) / (alpha[valid_alpha] / 255.0), 0, 255)

    c_arr[:, :, :3] = c_unwhite[:, :, :3]
    c_arr[:, :, 3] = alpha
    trans_img = Image.fromarray(c_arr.astype(np.uint8))

    color_png = os.path.join(guifreecad_logos, "color.png")
    trans_img.save(color_png)
    trans_img.save(os.path.join(guifreecad_logos, "atria_logo.png"))
    trans_img.save(os.path.join(guifreecad_icons, "atria_logo.png"))
    trans_img.save(os.path.join(interfaz_icons, "atria_logo.png"))

    # 3. Generar Squircle Badge para Icono de Windows (atria.ico) y cabecera del instalador
    badge_size = 512
    badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))

    # Sombra suave
    shadow = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([20, 24, badge_size - 20, badge_size - 16], radius=90, fill=(0, 0, 0, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    badge.paste(shadow, (0, 0), shadow)

    # Base redondeada blanca
    draw = ImageDraw.Draw(badge)
    draw.rounded_rectangle([20, 20, badge_size - 20, badge_size - 20], radius=90, fill=(255, 255, 255, 255), outline=(210, 218, 226, 255), width=4)

    # Logo centrado
    target_h = int(badge_size * 0.76)
    aspect = cropped.width / cropped.height
    target_w = int(target_h * aspect)
    logo_resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    paste_x = (badge_size - target_w) // 2
    paste_y = (badge_size - target_h) // 2
    badge.paste(logo_resized, (paste_x, paste_y))

    # Guardar PNG del badge
    badge_png = os.path.join(installer_dir, "atria_badge.png")
    badge.save(badge_png)

    # 4. Guardar archivo atria.ico con todos los tamaños estándar
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_path = os.path.join(installer_dir, "atria.ico")
    badge.save(ico_path, format="ICO", sizes=sizes)
    shutil.copyfile(ico_path, os.path.join(repo_root, "atria.ico"))
    print(f"Icono generado exitosamente en: {ico_path}")

    # 5. Generar SVG para FreeCAD (color.svg)
    # Convertir png transparente a base64 para incrustar en SVG estandar
    with open(color_png, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("ascii")

    svg_str = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">\n'
        '  <rect x="2" y="2" width="60" height="60" rx="14" fill="#FFFFFF" stroke="#D0D7DE" stroke-width="1.5"/>\n'
        '  <image href="data:image/png;base64,' + b64_data + '" x="6" y="6" width="52" height="52" preserveAspectRatio="xMidYMid meet"/>\n'
        '</svg>\n'
    )
    svg_path = os.path.join(guifreecad_logos, "color.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_str)
    # También en Icons/workbench.svg y atria_logo.svg
    shutil.copyfile(svg_path, os.path.join(guifreecad_icons, "workbench.svg"))
    shutil.copyfile(svg_path, os.path.join(guifreecad_icons, "atria_logo.svg"))
    print(f"SVG generado exitosamente en: {svg_path}")

if __name__ == "__main__":
    build_icons()

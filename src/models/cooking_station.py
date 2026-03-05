"""
cooking_station.py - Stasiun memasak (panci bakso, mie, sayuran, mangkok)
                   + BowlDisplay (gambar mangkok yang berubah sesuai step)
"""

import arcade
from config import (
    COOK_TIME, MIE_TIME, SAYURAN_TIME,
    BAKSO_STATION_X, BAKSO_STATION_Y,
    MIE_STATION_X, MIE_STATION_Y,
    SAYURAN_STATION_X, SAYURAN_STATION_Y,
    MANGKOK_POS_X, MANGKOK_POS_Y, MANGKOK_SCALE,
    BOWL_DISPLAY_X, BOWL_DISPLAY_Y, BOWL_DISPLAY_SCALE,
    BOWL_STAGES, ITEMS_PATH, ORDER_RECIPES
)


class CookingStation:
    """Base class untuk semua stasiun masak."""

    def __init__(self, x: float, y: float, cook_time: float, label: str):
        self.x          = x
        self.y          = y
        self.cook_time  = cook_time
        self.label      = label

        self.timer      = 0.0
        self.is_cooking = False
        self.is_ready   = False
        self.is_done    = False

        self.click_radius = 55
        self.hovered    = False

    def update(self, delta_time: float) -> bool:
        if self.is_cooking and not self.is_ready:
            self.timer += delta_time
            if self.timer >= self.cook_time:
                self.timer      = self.cook_time
                self.is_cooking = False
                self.is_ready   = True
                return True
        return False

    def start_cooking(self):
        if not self.is_cooking and not self.is_ready:
            self.is_cooking = True
            self.timer      = 0.0

    def take(self):
        if self.is_ready:
            self.is_ready = False
            self.is_done  = True
            return True
        return False

    def reset(self):
        self.timer      = 0.0
        self.is_cooking = False
        self.is_ready   = False
        self.is_done    = False

    @property
    def progress(self) -> float:
        if self.cook_time == 0:
            return 1.0
        return min(1.0, self.timer / self.cook_time)

    @property
    def can_click(self) -> bool:
        return not self.is_cooking and not self.is_done

    def contains(self, mx: float, my: float) -> bool:
        dx = mx - self.x
        dy = my - self.y
        return (dx * dx + dy * dy) <= self.click_radius ** 2

    def draw(self):
        base_color = (100, 70, 40, 220)
        if self.is_ready:
            base_color = (50, 200, 80, 220)
        elif self.is_cooking:
            base_color = (255, 160, 30, 220)
        elif self.hovered:
            base_color = (140, 100, 60, 220)

        arcade.draw_circle_filled(self.x, self.y, self.click_radius, base_color)
        arcade.draw_circle_outline(self.x, self.y, self.click_radius, (255, 255, 255, 120), 2)

        arcade.draw_text(
            self.label, self.x, self.y,
            (255, 255, 255, 220), font_size=13,
            anchor_x="center", anchor_y="center", bold=True
        )

        if self.is_cooking:
            bw = self.click_radius * 2
            bx = self.x - self.click_radius
            by = self.y - self.click_radius - 12
            arcade.draw_lbwh_rectangle_filled(bx, by, bw, 7, (60, 60, 60, 200))
            arcade.draw_lbwh_rectangle_filled(bx, by, bw * self.progress, 7, (255, 200, 0, 230))
            arcade.draw_lbwh_rectangle_outline(bx, by, bw, 7, (255, 255, 255, 120), 1)

        if self.is_ready:
            arcade.draw_text(
                "✓", self.x, self.y + self.click_radius + 10,
                (50, 255, 100, 255), font_size=18,
                anchor_x="center", anchor_y="center", bold=True
            )

    def update_hover(self, mx: float, my: float):
        self.hovered = self.contains(mx, my)


# ─── Concrete Stations ────────────────────────────────────────────────────────
class BaksoStation(CookingStation):
    """Panci bakso — step 1."""
    def __init__(self, cook_time_override: float | None = None):
        t = cook_time_override if cook_time_override is not None else COOK_TIME
        super().__init__(BAKSO_STATION_X, BAKSO_STATION_Y, t, "🍢 Bakso")


class MieStation(CookingStation):
    """Mie — step 2."""
    def __init__(self, mie_time_override: float | None = None):
        t = mie_time_override if mie_time_override is not None else MIE_TIME
        super().__init__(MIE_STATION_X, MIE_STATION_Y, t, "🍜 Mie")


class SayuranStation(CookingStation):
    """Sayuran — step 3."""
    def __init__(self, sayuran_time_override: float | None = None):
        t = sayuran_time_override if sayuran_time_override is not None else SAYURAN_TIME
        super().__init__(SAYURAN_STATION_X, SAYURAN_STATION_Y, t, "🥬 Sayur")


class MangkokStation(CookingStation):
    """Mangkok — step 0 (instan, klik langsung siap)."""
    def __init__(self):
        super().__init__(MANGKOK_POS_X, MANGKOK_POS_Y, 0.0, "🥣")
        self.click_radius = 40

    def start_cooking(self):
        self.is_ready = True

    def draw(self):
        base_color = (180, 130, 60, 200) if not self.is_ready else (50, 200, 80, 200)
        if self.hovered:
            base_color = (220, 170, 80, 220)
        arcade.draw_circle_filled(self.x, self.y, self.click_radius, base_color)
        arcade.draw_circle_outline(self.x, self.y, self.click_radius, (255, 255, 255, 120), 2)
        arcade.draw_text(
            self.label, self.x, self.y,
            (255, 255, 255, 230), font_size=14,
            anchor_x="center", anchor_y="center", bold=True
        )
        if self.is_ready:
            arcade.draw_text("✓", self.x, self.y + self.click_radius + 10,
                             (50, 255, 100, 255), font_size=18,
                             anchor_x="center", anchor_y="center", bold=True)


# ─── Bowl Display (Combined Images) ─────────────────────────────────────────
class BowlDisplay:
    """
    Menampilkan mangkok dengan gambar gabungan yang berubah
    sesuai bahan yang sudah ditambahkan.
    Menggunakan gambar: Mangkok.jpeg, Mangkok_bakso.jpeg,
    Mangkok_baksomie.jpeg, Mangkok_lengkap.jpeg
    """

    def __init__(self):
        self.x     = BOWL_DISPLAY_X
        self.y     = BOWL_DISPLAY_Y
        self.scale = BOWL_DISPLAY_SCALE
        self.ingredients: set[str] = set()
        self.has_mangkok = False

        # Pre-load semua stage images
        self._stage_sprites: dict[frozenset, arcade.Sprite] = {}
        self._sprite_list = arcade.SpriteList()
        for ingredient_set, path in BOWL_STAGES.items():
            try:
                s = arcade.Sprite(path, self.scale)
                s.center_x = self.x
                s.center_y = self.y
                s.visible  = False
                self._stage_sprites[ingredient_set] = s
                self._sprite_list.append(s)
            except Exception as e:
                print(f"[WARN] Could not load bowl stage '{path}': {e}")

        self._current_key = None

    def set_mangkok(self):
        """Player mengambil mangkok kosong."""
        self.has_mangkok = True
        self.ingredients.clear()
        self._update_display()

    def add_ingredient(self, name: str):
        """Tambah bahan (bakso/mie/sayuran) ke mangkok."""
        self.ingredients.add(name)
        self._update_display()

    @property
    def is_complete(self) -> bool:
        """True jika semua 3 bahan sudah masuk (legacy/fallback)."""
        return len(self.ingredients) >= 3

    def matches_order(self, order_type: str) -> bool:
        """Cek apakah bahan di mangkok cocok dengan pesanan pembeli."""
        required = ORDER_RECIPES.get(order_type)
        if not required:
            return False
        return self.has_mangkok and self.ingredients == required

    def is_ready_for_order(self, order_type: str) -> bool:
        """Cek apakah mangkok sudah siap untuk pesanan tertentu."""
        return self.has_mangkok and self.matches_order(order_type)

    def _update_display(self):
        """Update gambar mangkok berdasarkan bahan saat ini."""
        # Sembunyikan semua
        for s in self._stage_sprites.values():
            s.visible = False
        self._current_key = None

        if not self.has_mangkok:
            return

        # Cari gambar yang cocok dengan bahan saat ini
        key = frozenset(self.ingredients)
        if key in self._stage_sprites:
            self._stage_sprites[key].visible = True
            self._current_key = key
        else:
            # Fallback: tampilkan mangkok kosong
            empty_key = frozenset()
            if empty_key in self._stage_sprites:
                self._stage_sprites[empty_key].visible = True
                self._current_key = empty_key

    def reset(self):
        self.has_mangkok = False
        self.ingredients.clear()
        self._update_display()

    def set_stage(self, stage: str | None):
        """Legacy compatibility."""
        pass

    def draw(self):
        # Draw the current stage sprite
        self._sprite_list.draw()
        # Label di bawah mangkok
        if self.has_mangkok:
            parts = []
            if "bakso" in self.ingredients:
                parts.append("🍢")
            if "mie" in self.ingredients:
                parts.append("🍜")
            if "sayuran" in self.ingredients:
                parts.append("🥬")
            label = " + ".join(parts) if parts else "Kosong"
            color = (80, 255, 120, 255) if len(self.ingredients) > 0 else (255, 240, 200, 220)
            arcade.draw_text(
                label, self.x, self.y - 70,
                color, font_size=12,
                anchor_x="center", anchor_y="center", bold=True
            )

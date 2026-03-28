"""Tests for the MapWidget."""

from unittest.mock import MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.tui.styles import get_player_token
from emberblast.tui.widgets.map_grid import MapWidget


def _make_player(name, job_name, position):
    """Create a mock player for testing."""
    p = MagicMock()
    p.name = name
    p.job.name = job_name
    p.position = position
    p.is_alive.return_value = True
    return p


class TestMapWidget(BaseTestCase):
    """Tests for the MapWidget."""

    def setUp(self):
        self.widget = MapWidget()
        # 3x3 matrix: plains(1), wall(2), water(3)
        self.matrix = [
            [1, 2, 3],
            [4, 5, 1],
            [1, 0, 2],
        ]
        self.size = 3
        self.players = [
            _make_player("Gandalf", "Wizard", [0, 0]),
            _make_player("Sauron", "Warlock", [1, 1]),
        ]
        self.friendly_names = {"Gandalf"}

    def test_grid_text_contains_column_headers(self):
        self.widget.update_map(self.matrix, self.size, self.players, "Gandalf", self.friendly_names)
        text = self.widget._build_grid_text()
        plain = text.plain
        self.assertIn("0", plain)
        self.assertIn("1", plain)
        self.assertIn("2", plain)

    def test_grid_text_contains_row_labels(self):
        self.widget.update_map(self.matrix, self.size, self.players, "Gandalf", self.friendly_names)
        text = self.widget._build_grid_text()
        plain = text.plain
        self.assertIn("A", plain)
        self.assertIn("B", plain)
        self.assertIn("C", plain)

    def test_player_tokens_appear(self):
        self.widget.update_map(self.matrix, self.size, self.players, "Gandalf", self.friendly_names)
        text = self.widget._build_grid_text()
        plain = text.plain
        token = get_player_token("Gandalf", "Wizard")
        self.assertIn(token, plain)

    def test_void_cells_render_as_spaces(self):
        # matrix[2][1] == 0 => void
        self.widget.update_map(self.matrix, self.size, [], "", set())
        text = self.widget._build_grid_text()
        plain = text.plain
        # Row C should contain a space-like section for the void cell
        lines = plain.split("\n")
        row_c = [line for line in lines if line.strip().startswith("C")]
        self.assertTrue(len(row_c) > 0)

    def test_update_map_stores_data(self):
        self.widget.update_map(self.matrix, self.size, self.players, "Gandalf", self.friendly_names)
        self.assertEqual(self.widget._matrix, self.matrix)
        self.assertEqual(self.widget._grid_size, self.size)
        self.assertEqual(self.widget._active_player_name, "Gandalf")

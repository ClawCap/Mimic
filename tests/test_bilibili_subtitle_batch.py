import importlib.util
import unittest
from pathlib import Path


def load_script():
    path = Path(__file__).parents[1] / "scripts" / "bilibili_subtitle_batch.py"
    spec = importlib.util.spec_from_file_location("bilibili_subtitle_batch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCRIPT = load_script()


class NormalizeSubtitleUrlTest(unittest.TestCase):
    def test_normalizes_protocol_relative_url(self):
        self.assertEqual(
            SCRIPT.normalize_subtitle_url("//aisubtitle.example/subtitle.json"),
            "https://aisubtitle.example/subtitle.json",
        )

    def test_preserves_absolute_https_url(self):
        self.assertEqual(
            SCRIPT.normalize_subtitle_url("https://aisubtitle.example/subtitle.json"),
            "https://aisubtitle.example/subtitle.json",
        )

    def test_rejects_non_https_url(self):
        with self.assertRaises(ValueError):
            SCRIPT.normalize_subtitle_url("http://example.com/subtitle.json")

    def test_rejects_non_string_url(self):
        with self.assertRaises(ValueError):
            SCRIPT.normalize_subtitle_url(None)


if __name__ == "__main__":
    unittest.main()

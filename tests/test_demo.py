"""Regression checks against the compiled C library, not mocked C calls."""
import contextlib
import importlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            ["cc", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-fPIC",
             "-dynamiclib" if sys.platform == "darwin" else "-shared", "-o",
             "example.dylib" if sys.platform == "darwin" else "example.so", "example.c"],
            cwd=ROOT, check=True,
        )
        cls.demo = importlib.import_module("main")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def test_scalar_and_struct_examples(self):
        d = self.demo
        self.assertEqual(d.add(2, 3), 5)
        self.assertEqual(d.sum([1, 2, 3]), 6)
        self.assertAlmostEqual(d.mult(2.5, 3.5), 8.75)
        point = d.move_point({"x": 12, "y": 21}, 10, 9)
        self.assertEqual((point.x, point.y), (22, 30))
        self.assertTrue(d.is_even(32))
        self.assertFalse(d.is_even(27))

    def test_import_from_another_directory(self):
        result = subprocess.run(
            [sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import main; print(main.add(2, 3))", str(ROOT)],
            cwd=self.folder, capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout.strip(), "5")

    def test_matrix_product(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.demo.matrix_multiply()
        self.assertEqual(result, [[30, 24, 18], [84, 69, 54], [138, 114, 90]])

    def test_greeting_capacity(self):
        self.assertEqual(self.demo.greet("World"), "Hello, World!")
        self.assertEqual(self.demo.greet("a" * 41), "Hello, " + "a" * 41 + "!")
        for name in ["a" * 42, "a" * 10000, "é" * 21]:
            with self.subTest(name_length=len(name)), self.assertRaises(ValueError):
                self.demo.greet(name)
        self.assertEqual(self.demo.greet("é"), "Hello, é!")

    def test_file_round_trip(self):
        path = str(self.folder / "data.txt")
        with contextlib.redirect_stdout(io.StringIO()):
            self.demo.write_data([1.25, -2.5, 3], path)
            result = self.demo.read_data(path, 3)
        self.assertEqual(list(result), [1.25, -2.5, 3])

    def test_missing_short_or_malformed_file_raises(self):
        path = self.folder / "data.txt"
        for contents in [None, "1\n", "1\ninvalid\n3\n"]:
            if contents is not None:
                path.write_text(contents)
            with self.subTest(contents=contents), self.assertRaises(OSError):
                self.demo.read_data(str(path), 3)

    def test_invalid_read_size(self):
        for size in [0, -1]:
            with self.subTest(size=size), self.assertRaises(ValueError):
                self.demo.read_data(size=size)

    def test_failed_write_raises(self):
        with self.assertRaises(OSError):
            self.demo.write_data([1], str(self.folder / "absent" / "data.txt"))

    def test_failed_read_stops_main_before_write(self):
        previous = Path.cwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(self.folder)
        with patch.object(self.demo, "write_data") as write:
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(OSError):
                self.demo.main()
            write.assert_not_called()
        self.assertFalse((self.folder / "output.txt").exists())


if __name__ == "__main__":
    unittest.main()

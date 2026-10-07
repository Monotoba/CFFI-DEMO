# Contributing

Follow the README setup instructions and run `python -m unittest discover -s tests -v`.
Keep examples small and readable. Add regression tests for fixes and tests for new
examples, using the compiled library rather than mocking C calls. Check the complete
demo with `python data_gen.py` and `python main.py > demo-output.txt`.

Open an issue with reproduction steps or submit a focused pull request. Describe
what changed, why, and the checks performed. Avoid committing generated libraries,
data files, virtual environments, or credentials. Contributions must be compatible
with the BSD-2-Clause license.

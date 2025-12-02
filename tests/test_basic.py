# tests basiques - besoin de pytest
from audioinspector.analysis import analyze_file




def test_analyze_example():
# this test assumes an example file exists in tests/examples/sample.wav
# if not present, the test should be skipped
import os
path = os.path.join('tests', 'examples', 'sample.wav')
if not os.path.exists(path):
import pytest
pytest.skip('no sample file')
out = analyze_file(path, plot=False)
assert 'sr' in out
assert 'rms_db' in out

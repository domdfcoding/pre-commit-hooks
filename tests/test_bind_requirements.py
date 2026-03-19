# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from coincidence.selectors import min_version, only_version
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus

# this package
from pre_commit_hooks.bind_requirements import main
from pre_commit_hooks.util import FAIL, PASS


@pytest.mark.parametrize(
		"input_s, expected_retval, output",
		[
				pytest.param('', PASS, '', id="empty"),
				pytest.param('\n', PASS, '\n', id="newline_only"),
				pytest.param('# intentionally empty\n', PASS, '# intentionally empty\n', id="intentionally_empty"),
				pytest.param('f\n# comment at end\n', FAIL, '# comment at end\nf>=0.0.1\n', id="comment_at_end"),
				pytest.param('f\nbar\n', FAIL, 'bar>=0.2.1\nf>=0.0.1\n', id="foo_bar"),
				pytest.param('bar\nf\n', FAIL, 'bar>=0.2.1\nf>=0.0.1\n', id="bar_foo"),
				pytest.param('a\nc\nb\n', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n', id="a_c_b"),
				pytest.param('a\nb\nc', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n', id="a_b_b"),
				pytest.param(
						'#comment1\nf\n#comment2\nbar\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nf>=0.0.1\n',
						id="comment_foo_comment_bar",
						),
				pytest.param(
						'#comment1\nbar\n#comment2\nf\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nf>=0.0.1\n',
						id="comment_bar_comment_foo",
						),
				pytest.param(
						'#comment\n\nf\nbar\n',
						FAIL,
						'#comment\nbar>=0.2.1\nf>=0.0.1\n',
						id="comment_foo_bar",
						),
				pytest.param(
						'#comment\n\nbar\nf\n',
						FAIL,
						'#comment\nbar>=0.2.1\nf>=0.0.1\n',
						id="comment_barfoo_",
						),
				pytest.param('\nf\nbar\n', FAIL, 'bar>=0.2.1\nf>=0.0.1\n', id="foo_bar_2"),
				pytest.param('\nbar\nf\n', FAIL, 'bar>=0.2.1\nf>=0.0.1\n', id="bar_foo_2"),
				pytest.param(
						'pyramid-foo==1\npyramid>=2\n',
						FAIL,
						'pyramid>=2\npyramid-foo==1\n',
						id="pyramid-foo_pyramid",
						),
				pytest.param(
						'a==1\n'
						'c>=1\n'
						'bbbb!=1\n'
						'c-a>=1;python_version>="3.6"\n'
						'e>=2\n'
						'd>2\n'
						'g<2\n'
						'f<=2\n',
						FAIL,
						'a==1\n'
						'bbbb!=1\n'
						'c>=1\n'
						'c-a>=1; python_version >= "3.6"\n'
						'd>2\n'
						'e>=2\n'
						'f<=2\n'
						'g<2\n',
						id="a-g",
						),
				pytest.param(
						'ocflib\nDjango\nPyMySQL\n',
						FAIL,
						'django>=3.1.5\nocflib>=2020.12.5.10.49\npymysql>=0.10.1\n',
						id="real_requirements",
						),
				pytest.param(
						'bar\npkg-resources==0.0.0\nf\n',
						FAIL,
						'bar>=0.2.1\nf>=0.0.1\npkg-resources==0.0.0\n',
						id="bar_pkg-resources_foo",
						),
				pytest.param(
						'f\npkg-resources==0.0.0\nbar\n',
						FAIL,
						'bar>=0.2.1\nf>=0.0.1\npkg-resources==0.0.0\n',
						id="foo_pkg-resources_bar",
						),
				pytest.param('foo???1.2.3\nbar\n', FAIL, 'foo???1.2.3\nbar>=0.2.1\n', id="bad_specifiers"),
				pytest.param(
						'wxpython>=4.0.7; platform_system == "Windows" and python_version < "3.9"\n'
						'wxpython>=4.0.7; platform_system == "Darwin" and python_version < "3.9"\n',
						PASS,
						'wxpython>=4.0.7; platform_system == "Windows" and python_version < "3.9"\n'
						'wxpython>=4.0.7; platform_system == "Darwin" and python_version < "3.9"\n',
						id="markers",
						),
				pytest.param(
						'pyreadline @ https://github.com/domdfcoding/3.10-Wheels/raw/936f0570b561f3cda0be94d93066a11c6fe782f1/pyreadline-2.0-py3-none-any.whl ; python_version == "3.10" and platform_system == "Windows"',
						FAIL,
						'pyreadline@ https://github.com/domdfcoding/3.10-Wheels/raw/936f0570b561f3cda0be94d93066a11c6fe782f1/pyreadline-2.0-py3-none-any.whl ; python_version == "3.10" and platform_system == "Windows"\n',
						id="url_37",
						marks=only_version(3.7),
						),
				pytest.param(
						'pyreadline@ https://github.com/domdfcoding/3.10-Wheels/raw/936f0570b561f3cda0be94d93066a11c6fe782f1/pyreadline-2.0-py3-none-any.whl ; python_version == "3.10" and platform_system == "Windows"',
						FAIL,
						'pyreadline @ https://github.com/domdfcoding/3.10-Wheels/raw/936f0570b561f3cda0be94d93066a11c6fe782f1/pyreadline-2.0-py3-none-any.whl ; python_version == "3.10" and platform_system == "Windows"\n',
						id="url",
						marks=min_version(3.8),
						),
				pytest.param("shutil", FAIL, "shutil", id="not_on_pypi"),
				],
		)
@pytest.mark.usefixtures("cassette")
def test_integration(
		input_s: str,
		expected_retval: int,
		output: str,
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	path = tmp_pathplus / "file.txt"
	path.write_text(input_s)

	runner = CliRunner()

	result: Result = runner.invoke(main, args=[str(path)])
	assert path.read_text() == output
	assert result.exit_code == expected_retval
	advanced_file_regression.check(
			result.stdout.rstrip().replace(path.as_posix(), ".../file.txt"),
			extension=".md",
			)


@pytest.mark.parametrize(
		"minimum_py_version",
		[
				pytest.param("3.4", id="py34"),
				pytest.param("3.5", id="py35"),
				pytest.param("3.6", id="py36"),
				pytest.param("3.7", id="py37"),
				pytest.param("3.8", id="py38"),
				pytest.param("3.9", id="py39"),
				pytest.param("3.10", id="py310"),
				pytest.param("3.11", id="py311"),
				pytest.param("3.12", id="py312"),
				pytest.param("3.13", id="py313"),
				],
		)
@pytest.mark.usefixtures("cassette")
def test_integration_min_py(
		tmp_pathplus: PathPlus,
		minimum_py_version: str,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	path = tmp_pathplus / "file.txt"
	path.write_text("click\nnumpy\ndomdf-python-tools\n")

	runner = CliRunner()

	result: Result = runner.invoke(main, args=[str(path), "--python-min", minimum_py_version])
	assert result.exit_code == 1

	advanced_file_regression.check(
			result.stdout.rstrip().replace(path.as_posix(), ".../file.txt"),
			extension=".md",
			)

	advanced_file_regression.check_file(path)

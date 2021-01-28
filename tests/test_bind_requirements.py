# 3rd party
import pytest
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
				pytest.param('foo\n# comment at end\n', FAIL, '# comment at end\nfoo>=.1\n', id="comment_at_end"),
				pytest.param('foo\nbar\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n', id="foo_bar"),
				pytest.param('bar\nfoo\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n', id="bar_foo"),
				pytest.param('a\nc\nb\n', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n', id="a_c_b"),
				pytest.param('a\nb\nc', FAIL, 'a>=1.0\nb>=1.0.0\nc>=0.1.0\n', id="a_b_b"),
				pytest.param(
						'#comment1\nfoo\n#comment2\nbar\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nfoo>=.1\n',
						id="comment_foo_comment_bar"
						),
				pytest.param(
						'#comment1\nbar\n#comment2\nfoo\n',
						FAIL,
						'#comment1\n#comment2\nbar>=0.2.1\nfoo>=.1\n',
						id="comment_bar_comment_foo"
						),
				pytest.param(
						'#comment\n\nfoo\nbar\n', FAIL, '#comment\nbar>=0.2.1\nfoo>=.1\n', id="comment_foo_bar"
						),
				pytest.param(
						'#comment\n\nbar\nfoo\n', FAIL, '#comment\nbar>=0.2.1\nfoo>=.1\n', id="comment_barfoo_"
						),
				pytest.param('\nfoo\nbar\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n', id="foo_bar_2"),
				pytest.param('\nbar\nfoo\n', FAIL, 'bar>=0.2.1\nfoo>=.1\n', id="bar_foo_2"),
				pytest.param(
						'pyramid-foo==1\npyramid>=2\n',
						FAIL,
						'pyramid>=2\npyramid-foo==1\n',
						id="pyramid-foo_pyramid"
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
						id="real_requirements"
						),
				pytest.param(
						'bar\npkg-resources==0.0.0\nfoo\n',
						FAIL,
						'bar>=0.2.1\nfoo>=.1\npkg-resources==0.0.0\n',
						id="bar_pkg-resources_foo"
						),
				pytest.param(
						'foo\npkg-resources==0.0.0\nbar\n',
						FAIL,
						'bar>=0.2.1\nfoo>=.1\npkg-resources==0.0.0\n',
						id="foo_pkg-resources_bar"
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
				]
		)
def test_integration(input_s, expected_retval, output, tmp_pathplus: PathPlus, cassette):
	path = tmp_pathplus / "file.txt"
	path.write_text(input_s)

	runner = CliRunner()

	result: Result = runner.invoke(main, args=[str(path)])
	assert path.read_text() == output
	assert result.exit_code == expected_retval

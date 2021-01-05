# 3rd party
import pytest

# this package
from pre_commit_hooks.requirements_txt_sorter import main
from pre_commit_hooks.util import FAIL, PASS


@pytest.mark.parametrize(
		"input_s, expected_retval, output",
		[
				('', PASS, ''),
				('\n', FAIL, ''),
				('# intentionally empty\n', PASS, '# intentionally empty\n'),
				('foo\n# comment at end\n', FAIL, '# comment at end\nfoo\n'),
				('foo\nbar\n', FAIL, 'bar\nfoo\n'),
				('bar\nfoo\n', PASS, 'bar\nfoo\n'),
				('a\nc\nb\n', FAIL, 'a\nb\nc\n'),
				('a\nb\nc', FAIL, 'a\nb\nc\n'),
				(
						'#comment1\nfoo\n#comment2\nbar\n',
						FAIL,
						'#comment1\n#comment2\nbar\nfoo\n',
						),
				(
						'#comment1\nbar\n#comment2\nfoo\n',
						FAIL,
						'#comment1\n#comment2\nbar\nfoo\n',
						),
				('#comment\n\nfoo\nbar\n', FAIL, '#comment\nbar\nfoo\n'),
				('#comment\n\nbar\nfoo\n', FAIL, '#comment\nbar\nfoo\n'),
				('\nfoo\nbar\n', FAIL, 'bar\nfoo\n'),
				('\nbar\nfoo\n', FAIL, 'bar\nfoo\n'),
				(
						'pyramid-foo==1\npyramid>=2\n',
						FAIL,
						'pyramid>=2\npyramid-foo==1\n',
						),
				(
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
						),
				('ocflib\nDjango\nPyMySQL\n', FAIL, 'django\nocflib\npymysql\n'),
				('bar\npkg-resources==0.0.0\nfoo\n', FAIL, 'bar\nfoo\n'),
				('foo\npkg-resources==0.0.0\nbar\n', FAIL, 'bar\nfoo\n'),
				('foo???1.2.3\nbar\n', FAIL, 'bar\n'),
				('ruamel.yaml\nbar\n', FAIL, 'bar\nruamel.yaml\n'),
				(
						'numpy>=1.19.1; platform_system != "Windows"\nnumpy==1.19.3; platform_system == "Windows"\n',
						PASS,
						'numpy>=1.19.1; platform_system != "Windows"\nnumpy==1.19.3; platform_system == "Windows"\n'
						),
				(
						'wxpython>=4.0.7; platform_system == "Windows" and python_version < "3.9"\n'
						'wxpython>=4.0.7; platform_system == "Darwin" and python_version < "3.9"\n',
						PASS,
						'wxpython>=4.0.7; platform_system == "Windows" and python_version < "3.9"\n'
						'wxpython>=4.0.7; platform_system == "Darwin" and python_version < "3.9"\n',
						),
				],
		)
def test_integration(input_s, expected_retval, output, tmp_pathplus):
	path = tmp_pathplus / "requirements.txt"
	path.write_text(input_s)

	output_retval = main([str(path)])

	assert path.read_text() == output
	assert output_retval == expected_retval

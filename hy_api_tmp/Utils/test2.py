import click
import pytest


@click.command()
@click.option("-t", default=None, help="运行测试用例.")
def run(t):
    """运行测试用例命令."""
    if t is None:
        click.echo("""请输入测试的目录或文件, -t test_xx.py """)
    else:
        pytest.main(["-v", "-ss", t])


if __name__ == '__main__':
    run('cmd')
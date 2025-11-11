import pytest

from pytest_examples import CodeExample, EvalExample, find_examples


@pytest.mark.parametrize('example', find_examples('docs/examples.md'), ids=str)
def test_examples(example: CodeExample, eval_example: EvalExample):
    eval_example.set_config(line_length=50)
    if eval_example.update_examples:
        # eval_example.format(example)
        eval_example.run_print_update(example)
    else:
        # eval_example.lint(example)
        eval_example.run_print_check(example)
#!/usr/bin/env python

import textwrap
import unittest

import wrapper


class TestWrapper(unittest.TestCase):
    def assertTransform(self, line: int, col: int, content: str, expected_output: str) -> None:
        # Normalise from triple quoted strings
        content = textwrap.dedent(content[1:])
        expected_output = textwrap.dedent(expected_output[1:])

        new_content = wrapper.process(wrapper.Position(line, col), content, 'demo.py')

        self.assertEqual(expected_output, new_content, "Bad transformation")

    def test_single_key_dict_literal(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo = {'abcd': 1234}
            """,
            """
            foo = {
                'abcd': 1234,
            }
            """,
        )

    def test_indented_single_key_dict_literal(self) -> None:
        self.assertTransform(
            2,
            12,
            """
            if True:
                foo = {'abcd': 1234}
            """,
            """
            if True:
                foo = {
                    'abcd': 1234,
                }
            """,
        )

    def test_multi_key_dict_literal(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo = {'key': 1234, 'other': 5678}
            """,
            """
            foo = {
                'key': 1234,
                'other': 5678,
            }
            """,
        )

    def test_ignores_nested_dict(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo = {'key': 1234, 'other': {'bar': 5678}}
            """,
            """
            foo = {
                'key': 1234,
                'other': {'bar': 5678},
            }
            """,
        )

    def test_wraps_nested_dict_only(self) -> None:
        self.assertTransform(
            1,
            38,
            """
            foo = {'key': 1234, 'other': {'bar': 5678}}
            """,
            """
            foo = {'key': 1234, 'other': {
                'bar': 5678,
            }}
            """,
        )

    def test_position_at_start(self) -> None:
        self.assertTransform(
            1,
            9,
            """
            foo = {'abcd': 1234}
            #      ^
            """,
            """
            foo = {
                'abcd': 1234,
            }
            #      ^
            """,
        )

    def test_position_on_leaf_key(self) -> None:
        self.assertTransform(
            1,
            12,
            """
            foo = {'abcd': 1234}
            #         ^
            """,
            """
            foo = {
                'abcd': 1234,
            }
            #         ^
            """,
        )

    def test_position_on_leaf_value(self) -> None:
        self.assertTransform(
            1,
            18,
            """
            foo = {'abcd': 1234}
            #               ^
            """,
            """
            foo = {
                'abcd': 1234,
            }
            #               ^
            """,
        )

    def test_position_in_space(self) -> None:
        self.assertTransform(
            1,
            17,
            """
            foo = {'abcd':   1234}
            #              ^
            """,
            """
            foo = {
                'abcd':   1234,
            }
            #              ^
            """,
        )

    def test_single_entry_list_literal(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo = ['abcd']
            """,
            """
            foo = [
                'abcd',
            ]
            """,
        )

    def test_multi_entry_list_literal(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo = ['abcd', 1234]
            """,
            """
            foo = [
                'abcd',
                1234,
            ]
            """,
        )

    def test_dict_comprehension(self) -> None:
        self.assertTransform(
            1,
            15,
            """
            foo = {str(k): v for k, v in foo}
            """,
            """
            foo = {
                str(k): v
                for k, v in foo
            }
            """,
        )

    def test_list_comprehension(self) -> None:
        self.assertTransform(
            1,
            15,
            """
            foo = [str(x) for x in range(42)]
            """,
            """
            foo = [
                str(x)
                for x in range(42)
            ]
            """,
        )

    def test_function_call(self) -> None:
        self.assertTransform(
            1,
            8,
            """
            foo('abcd', 1234, spam='ham')
            """,
            """
            foo(
                'abcd',
                1234,
                spam='ham',
            )
            """,
        )


if __name__ == '__main__':
    unittest.main(__name__)

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


if __name__ == '__main__':
    unittest.main(__name__)

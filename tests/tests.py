import bf
import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch

@contextmanager
def redirect_out():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out

class BfPyTest(unittest.TestCase):

    def test_hello_world(self):
        ''' Verify we're able to print an Hello World '''
        command = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
        with redirect_out() as out:
            interpreter = bf.Interpreter()
            interpreter.eval(command)
            self.assertEqual(out.getvalue(), "Hello World!\n")

    def test_skip_loop(self):
        ''' Tests that a loop is skipped if the cell value is zero '''
        print_A_cmd = '++[>+++++[>++++++<-]<-]>>+++++.'
        command = '[{0}]{0}'.format(print_A_cmd)
        with redirect_out() as out:
            interpreter = bf.Interpreter()
            interpreter.eval(command)
            self.assertEqual(out.getvalue(), 'A')

    def test_io(self):
        ''' Test commands , and . '''
        command = ',+.'
        with patch.object(bf.sys.stdin, "read", return_value='a'):
            with redirect_out() as out:
                interpreter = bf.Interpreter()
                interpreter.eval(command)
                self.assertEqual(out.getvalue(), 'b')

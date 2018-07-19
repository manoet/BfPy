import sys
from collections import defaultdict

class Interpreter(object):
    ''' Interpreter of brainfuck code '''

    def __init__(self):
        self.__code = ''                # String to be interpreted
        self.__cursor = 0               # String cursor
        self.__pointer = 0              # Cell pointer
        self.__cells = defaultdict(int) # Cells. Dict allows for negative cells
        self.__stack = []               # Stack to register addresses of loops
        # Populate evaluation functions dict
        self.__eval_func = {
            '<' : self.__eval_left,
            '>' : self.__eval_right,
            '+' : self.__eval_plus,
            '-' : self.__eval_minus,
            '.' : self.__eval_dot,
            ',' : self.__eval_comma,
            '[' : self.__eval_loop_start,
            ']' : self.__eval_loop_end}

    def __eval_left(self):
        ''' Implements < command '''
        self.__pointer -= 1

    def __eval_right(self):
        ''' Implement > command '''
        self.__pointer += 1

    def __eval_plus(self):
        ''' Implement + command '''
        self.__cells[self.__pointer] += 1

    def __eval_minus(self):
        ''' Implement - command '''
        self.__cells[self.__pointer] -= 1

    def __eval_dot(self):
        ''' Implement . command '''
        value = self.__cells[self.__pointer]
        print(chr(value), end='')
        sys.stdout.flush()

    def __eval_comma(self):
        ''' Implement , command '''
        value = sys.stdin.read(1)
        self.__cells[self.__pointer] = ord(value)

    def __eval_loop_start(self):
        ''' Implement [ command '''
        value = self.__cells[self.__pointer]
        if value == 0:
            # Jump to matching ]
            loop_count = 0
            for i in range(self.__cursor+1, len(self.__code)):
                if self.__code[i] == ']' and loop_count == 0:
                    self.__cursor = i
                    return
                if self.__code[i] == '[': loop_count += 1
                elif self.__code[i] == ']': loop_count -= 1
            raise RuntimeError('No matching ] found for loop starting at character {}'.format(self.__cursor))
        # Update stack
        self.__stack.append(self.__cursor)

    def __eval_loop_end(self):
        ''' Implement ] command '''
        value = self.__cells[self.__pointer]
        if value == 0:
            # Pop from stack and move to next instruction
            self.__stack.pop()
        else:
            # Move back to first instruction in the loop
            self.__cursor = self.__stack[-1]

    def eval(self, string):
        ''' Evaluate a BrainFuck code

        @param string: string to be interpreted
        @type string: str
        @return: None
        '''
        self.__code = string
        while self.__cursor < len(self.__code):
            command = self.__code[self.__cursor]
            if command not in self.__eval_func:
                # Any character which is not a command is a comment
                continue
            self.__eval_func[command]()
            self.__cursor += 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} command_string'.format(sys.argv[0]))
        exit(0)
    bf = Interpreter()
    bf.eval(sys.argv[1])
    print() # Newline for next prompt

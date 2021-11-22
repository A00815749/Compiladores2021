#implementacion rapida de clase Pila, usando comandos de python como visto en tareas
from collections import deque
class myStack:
    def __init__(self):
        self.stack = deque()

    def push(self,thingy):
        self.stack.append(thingy)

    def pop(self):
        if self.stack: #true if not empty, false if empty
            return self.stack.pop()
        return None

    def length(self):
        return len(self.stack)

    def top(self): # The reference
        return self.stack[len(self.stack)-1]

    def isEmpty(self):
        if self.stack:
            queue_empty = True
        else:
            queue_empty = False
        return queue_empty
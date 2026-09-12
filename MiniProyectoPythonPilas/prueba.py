class Pila:
    def __init__(self):
        self.__items = []
    def push(self, item):
        self.__items.append(item)
    def pop(self):
        return self.__items.pop() if self.__items else None
    def size(self):
        return len(self.__items)


p = Pila()
p.push(5)
p.push(8)
p.pop()
p.push(2)
print(p.size())  # Imprime: 2
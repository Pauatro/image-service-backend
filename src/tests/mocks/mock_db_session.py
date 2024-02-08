from typing import Type


class MockDBSession:
    def execute(statement) -> [Type]:
        return

    def add(input: Type):
        return

    def commit():
        return

    def refresh(input: Type) -> Type:
        return input

class MockDBReturn:
    
    def __new__(self, input):
        return self

    def first():
        return
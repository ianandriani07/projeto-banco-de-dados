import inspect
from typing import List, Dict
from collections.abc import Callable
from terminal import clear_terminal

class PageManager: ...


class Page:

    def render(self, manager: PageManager) -> None: ...

    @property
    def name(self):
        return type(self).__name__


class TestPage(Page):

    def render(self, manager):
        print("Fuck")


class FunctionPage(Page):

    def __init__(self, func: Callable[[PageManager], None]):
        self.func = func

    def __call__(self, *args, **kwds):
        return self.func(*args, **kwds)

    @property
    def name(self):
        self.func.__name__

    def render(self, manager: PageManager) -> None:
        self.func(manager)


class PageManager:

    def __init__(self):
        self.pages: Dict[str, Page] = {}
        self.next_page_id: str = ""
        self.pages_accessed = []

    def to(self, page_id: str | Callable[[PageManager], None]):
        if isinstance(page_id, str):
            if self.pages.get(page_id) is not None:
                self.next_page_id = page_id
            else:
                raise ValueError(
                    f"The page {page_id} is not registered in the manager!"
                )
        elif inspect.isfunction(page_id):
            if self.pages.get(page_id.__name__) is not None:
                self.next_page_id = page_id.__name__
            else:
                raise ValueError(
                    f"The page {page_id.__name__} is not registered in the manager!"
                )
        else:
            if hasattr(page_id, "__name__"):
                if self.pages.get(page_id.__name__) is not None:
                    self.next_page_id = page_id.__name__
                else:
                    raise ValueError(
                        f"The page {page_id.__name__} is not registered in the manager!"
                    )
            else:
                raise TypeError(f"The type is not supported {type(page_id)}")

    def add_pages(self, *pages: Page):
        for page in pages:
            self.pages[page.name] = page

    def as_page(self):

        def temp_function(func: Callable[[PageManager], None]):
            self.pages[func.__name__] = FunctionPage(func)
            return func

        return temp_function

    def back(self):
        self.to(self.pages_accessed.pop())

    def init(self, init_on: str | Callable[[PageManager], None]):
        self.to(init_on)
        while True:
            clear_terminal()
            self.pages_accessed.append(self.next_page_id)
            self.pages[self.next_page_id](self)

if __name__ == "__main__":

    manager = PageManager()

    @manager.as_page()
    def test1(manager):
        print("You're at test1!")
        input('Continue')
        manager.to(test2)
    
    @manager.as_page()
    def test2(manager):
        print("You're at test2!")
        input("Continue")
        manager.to(test3)
    
    @manager.as_page()
    def test3(manager):
        print("You're at test3!")
        input('Continue')
        manager.to(test1)

    manager.init(test1)

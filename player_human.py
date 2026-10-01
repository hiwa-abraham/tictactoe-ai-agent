from typing import List, Tuple, Any

# ====================================================================================================
# Player Interface Function (Used by game.py)
# ====================================================================================================

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    """
    Prompt the human user to choose a column from the available legal choices.
    """
    display_choices = [c + 1 for c in choices]  # 1-indexed for display
    move = None

    while move not in choices:
        try:
            user_input = input(f"Enter column number {display_choices}: ")
            move = int(user_input) - 1  # Convert to 0-indexed column
            if move not in choices:
                print(f"Invalid column. Please select from {display_choices}.")
        except ValueError:
            print("Please enter a valid integer.")

    return move, memory


# ====================================================================================================
# Data Structures & Helpers
# ====================================================================================================

class Item:
    def __init__(self, value: object):
        self.value = value
        self.next = None


class FiFo:
    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, value: object) -> None:
        item = Item(value)
        if self.last is not None:
            self.last.next = item
        else:
            self.first = item
        self.last = item

    def dequeue(self) -> object:
        if self.first is None:
            return None
        item = self.first
        self.first = item.next
        if self.first is None:
            self.last = None
        return item.value

    def __len__(self) -> int:
        if self.first is None:
            return 0
        item = self.first
        n = 1
        while item is not self.last and item is not None:
            item = item.next
            n += 1
        return n


class Tree:
    def __init__(self, name: str, value: object):
        self.name = name
        self.value = value
        self.childrens = []

    def add_child(self, name: str, value: object):
        node = Tree(name, value)
        self.childrens.append(node)

    def path_to_node_dfs(self, name: object):
        if self.name == name:
            return (self,)

        for child in self.childrens:
            path = child.path_to_node_dfs(name)
            if path is not None:
                return (self,) + path
        return None

    def path_to_node_bfs(self, name: str):
        queue = [(self,)]
        while len(queue) > 0:
            path = queue.pop(0)
            if path[-1].name == name:
                return path
            for child in path[-1].childrens:
                queue.append(path + (child,))
        return None

    def __len__(self) -> int:
        n = 0
        for child in self.childrens:
            n += len(child)
        return n + 1


class State:
    def __init__(self, name: str):
        self.name = name
        self.neighboures = []

    def add_neighbour(self, neighbour: "State") -> bool:
        if neighbour not in self.neighboures:
            self.neighboures.append(neighbour)
            neighbour.neighboures.append(self)
            return True
        return False


# ====================================================================================================
# Recursive Utility Functions
# ====================================================================================================

def nested_sum(numbers: Any) -> int:
    if isinstance(numbers, int):
        return numbers
    elif isinstance(numbers, list):
        return sum(nested_sum(x) for x in numbers)
    return 0


def nested_string_count(numbers: list[Any]) -> int:
    if not numbers:
        return 0

    first = numbers[0]
    rest = numbers[1:]

    if isinstance(first, list):
        return nested_string_count(first) + nested_string_count(rest)
    elif isinstance(first, str):
        return 1 + nested_string_count(rest)
    else:
        return nested_string_count(rest)


def get_item_by_index(node, i: int) -> object:
    if node is None:
        return None
    if i == 0:
        return node.value
    return get_item_by_index(node.next, i - 1)


def get_item_by_value(node, v: int) -> list:
    result = []
    if node is None:
        return result
    if node.value > v:
        result.append(node.value)
    if node.next is not None:
        result.extend(get_item_by_value(node.next, v))
    return result
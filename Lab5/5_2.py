import threading
import random


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def contains(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


def worker(num_values, linked_list, read_lock, write_lock):
    for _ in range(num_values):
        value = random.randint(0, 1000)
        with read_lock:
            if not linked_list.contains(value):
                with write_lock:
                    if not linked_list.contains(value):
                        linked_list.add(value)
                        # print(value)


def main():
    num_threads = 4
    num_values_per_thread = 4

    linked_list = LinkedList()
    read_lock = threading.Condition()
    write_lock = threading.RLock()

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(num_values_per_thread, linked_list, read_lock, write_lock))
        threads.append(thread)
        # print(f'i = {i + 1}')
        thread.start()

    for thread in threads:
        thread.join()

    values = linked_list.to_list()
    if len(values) == len(set(values)):
        print("В списке нет повторяющихся чисел.")
    else:
        print("В списке есть повторяющиеся числа.")

    print(*values)


if __name__ == "__main__":
    main()

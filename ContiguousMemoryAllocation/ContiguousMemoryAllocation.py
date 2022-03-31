from typing import List
from collections import OrderedDict
import sys


class Slot:
    def __init__(self, min_: int, max_: int, id_: str):
        self.min = min_
        self.max = max_
        self.id = id_
        self.size = max_ - min_ + 1


    def __repr__(self):
        return f"[{self.min}:{self.max}] {self.id}"


class Memory:
    def __init__(self):
        self.MAX_MEMORY = 10000
        self.memory = [Slot(0, self.MAX_MEMORY - 1, "unused")]
        self.unique_ids = set()

    def sort(self):
        self.memory.sort(key=lambda obj: obj.min, reverse=False)

    def release(self, process: str):
        """
        Release memory allocated to process process
        :param process:
        :return:
        """
        if process not in self.unique_ids:
            print(f"Error: '{process}' does not exist in memory")
            return

        index = 0
        for i, item in enumerate(self.memory):
            if item.id == process:
                index = i
                break

        self.memory[index].id = "unused"
        self.unique_ids.remove(process)



    def addMemoryFirstFit(self, process: str, size: int):
        """
        Allocates the first hole that is big enough.
        :param process:
        :param size:
        :return:
        """
        if process in self.unique_ids:
            print(f"Error: memory already allocated for '{process}'")
            return

        hole_indices = [index for index, item in enumerate(self.memory) if item.id == "unused" and size <= item.size]
        if not hole_indices:
            print("Error: no room")
            return

        first_hole = self.memory.pop(hole_indices[0])
        new_slot = Slot(first_hole.min, first_hole.min + size - 1, process)
        new_slots = [new_slot]
        if size < first_hole.size:
            new_slots.append(Slot(new_slot.max + 1, first_hole.max, "unused"))

        self.unique_ids.add(process)
        self.memory.extend(new_slots)
        self.sort()


    def addMemoryBestFit(self, process: str, size: int):
        """
        Allocates the smallest hole that is large enough
        :param process:
        :param size:
        :return:
        """
        if process in self.unique_ids:
            print(f"Error: memory already allocated for '{process}'")
            return

        holes = [(index, item) for index, item in enumerate(self.memory) if item.id == "unused" and size <= item.size]
        if not holes:
            print("Error: no room")
            return

        # won't the holes already be sorted smallest to largest since self.memory is?
        holes.sort(key=lambda tup: tup[1].size, reverse=False)
        best_index, best_hole = holes[0]

        self.memory.pop(best_index)

        new_slot = Slot(best_hole.min, best_hole.min + size - 1, process)
        new_slots = [new_slot]
        if size < best_hole.size:
            new_slots.append(Slot(new_slot.max + 1, best_hole.max, "unused"))

        self.unique_ids.add(process)
        self.memory.extend(new_slots)
        self.sort()


    def addMemoryWorstFit(self, process: str, size: int):
        if process in self.unique_ids:
            print(f"Error: memory already allocated for '{process}'")
            return

        holes = [(index, item) for index, item in enumerate(self.memory) if item.id == "unused" and size <= item.size]
        if not holes:
            print("Error: no room")
            return

        # sort holes largest to smallest
        holes.sort(key=lambda tup: tup[1].size, reverse=True)
        worst_index, worst_hole = holes[0]

        self.memory.pop(worst_index)

        new_slot = Slot(worst_hole.min, worst_hole.min + size - 1, process)
        new_slots = [new_slot]
        if size < worst_hole.size:
            new_slots.append(Slot(new_slot.max + 1, worst_hole.max, "unused"))

        self.unique_ids.add(process)
        self.memory.extend(new_slots)
        self.sort()

    def combineHoles(self):
        holes = [(index, item) for index, item in enumerate(self.memory) if item.id == "unused"]
        to_merge = []
        new_holes = []
        i = 0
        while i < len(holes):
            hole = holes[i]
            if not to_merge or to_merge[-1][0] == (hole[0] - 1):
                to_merge.append(hole)
            else:
                new_holes.append(Slot(to_merge[0][1].min, to_merge[-1][1].max, "unused"))
                to_merge = []
                continue
            i += 1

        new_holes.extend([item[1] for item in to_merge])
        new_memory = [item for item in self.memory if item.id != "unused"]
        new_memory.extend(new_holes)
        self.memory = new_memory
        self.sort()









    def printStat(self):
        for item in self.memory:
            address_str = f"Addresses [{item.min}:{item.max}] "
            id_str = "Unused" if item.id == "unused" else f"Process {item.id}"
            print(address_str + id_str)


    def __repr__(self):
        return str(self.memory)




def main():
    # MAX_MEMORY = 10000
    # memory = OrderedDict()
    # memory[(0, MAX_MEMORY)] = "Unused"

    mem = Memory()
    mem.addMemoryFirstFit("P1", 500)
    mem.addMemoryFirstFit("P2", 200)
    mem.release("P1")
    mem.addMemoryWorstFit("P5", 500)
    mem.addMemoryWorstFit("P6", 100)
    mem.addMemoryBestFit("P7", 300)
    mem.release("P2")
    mem.addMemoryWorstFit("P8", 10)
    mem.release("P6")
    mem.combineHoles()
    mem.printStat()


if __name__ == "__main__":
    main()

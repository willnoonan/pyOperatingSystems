from typing import List, overload
import csv
from collections import defaultdict, OrderedDict
import itertools
import argparse
import sys



class Task:
    def __init__(self, name, priority, cpu_burst):
        self.name = name
        self.priority = priority
        self.cpu_burst = cpu_burst

    def __repr__(self):
        return f"(Name: {self.name}, Priority: {self.priority}, CPU Burst: {self.cpu_burst})"


class Scheduler:
    def __init__(self, file):
        self.file = file
        self._initialize_fcfs_tasks()
        self._intialize_priority_tasks()

    def _initialize_fcfs_tasks(self):
        lines = self.read_txt(self.file)
        self.tasks_by_fcfs = [Task(*line) for line in lines]

    def _intialize_priority_tasks(self):
        tasksByPriority = defaultdict(list)
        for task in self.tasks_by_fcfs:
            tasksByPriority[task.priority].append(task)
        sorted_tasks = [tasksByPriority[key] for key in sorted(tasksByPriority.keys(), reverse=True)]
        self.tasks_by_priority = list(itertools.chain(*sorted_tasks))

    def printRoundRobinScheduling(self, quantum=3):
        if quantum <= 0:
            raise ValueError("quantum must be > 0")

        tasks = [Task(task.name, None, task.cpu_burst) for task in self.tasks_by_fcfs]  # must make a copy

        num_complete = 0
        clock = 0
        print(clock)
        i = 0
        while num_complete < len(tasks):
            task = tasks[i]
            if task.cpu_burst > 0:
                print(f"| {task.name}")
                if task.cpu_burst > quantum:
                    clock += quantum
                    task.cpu_burst -= quantum
                else:
                    clock += task.cpu_burst
                    task.cpu_burst -= task.cpu_burst
                    if task.cpu_burst <= 0:
                        num_complete += 1
                print(clock)
            i = (i + 1) % len(tasks)


    def printPriorityScheduling(self):
        self.printSchedule(self.tasks_by_priority)

    def printFCFSScheduling(self):
        self.printSchedule(self.tasks_by_fcfs)

    @staticmethod
    def printSchedule(tasks):
        if not tasks:
            print("There are no tasks.")
            return

        clock = 0
        print(clock)
        for task in tasks:
            clock += task.cpu_burst
            print(f"| {task.name}")
            print(clock)

    @staticmethod
    def read_txt(file):
        lines = []
        with open(file) as f:
            for line in f.readlines():
                clean = line.strip().split(",")
                lines.append([clean[0], int(clean[1]), int(clean[2])])
        return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-fcfs", action='store_true')
    parser.add_argument("-priority", action='store_true')
    args = parser.parse_args()

    if len(sys.argv) > 2:
        third_arg = sys.argv[2]
        scheduler = Scheduler(args.file)
        if args.fcfs and third_arg.startswith("-f"):
            scheduler.printFCFSScheduling()
        elif args.priority and third_arg.startswith("-p"):
            scheduler.printPriorityScheduling()



if __name__ == "__main__":
    main()
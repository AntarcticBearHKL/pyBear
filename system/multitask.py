import multiprocessing
import threading
import os,sys
import time

import pyBear.bear as bear
import pyBear.system.chronus as chronus

class simpleThread:
    def __init__(self, function, argc):
        threading.Thread(target = function, args = argc).start()

class multiThread:
    def __init__(self, parallelNumber, limitPerMinute = None):
        self.taskList = []
        self.parallelNumber = parallelNumber
        self.limitPerMinute = limitPerMinute

    def assignTask(self, function, taskArg):
        for item in taskArg:
            self.taskList.append([function, tuple(item)])

    def assignTaskList(self, taskList):
        self.taskList = taskList

    def start(self):
        workSpace = []
        for item in range(self.parallelNumber):
            workSpace.append(None)

        limitTimer = chronus.frame()
        limitCounter = 0

        for task in self.taskList:
            if self.limitPerMinute and limitCounter >= self.LimitPerMinute:
                while(True):
                    if (chronus.frame() - limitTimer) > 60:
                        limitTimer = chronus.frame()
                        limitCounter = 0
                        break
                    print('Waiting...')
                    chronus.sleep(1)
            LimitCounter += 1

            CONTINUE = True
            availableThread = None

            while(CONTINUE):
                for item in range(self.parallelNumber):
                    if (workSpace[item] == None) or (workSpace[item].isAlive() == False):
                        CONTINUE = False
                        availableThread = item
                        break
                    elif item == self.parallelNumber -1:
                        chronus.sleep(1)
                    
            workSpace[availableThread] = threading.Thread(target = task[0], args = task[1])
            workSpace[availableThread].start() 

        for item in workSpace:
            if item != None:
                item.join() 


class multiCore:
    def __init__(self, parallelNumber):
        self.taskList = []
        self.parallelNumber = parallelNumber

    def assignTask(self, function, taskArg):
        for item in taskArg:
            self.taskList.append([function, tuple(item)])

    def assignTaskList(self, taskList):
        self.taskList = taskList

    def start(self): 
        workSpace = []
        for item in range(self.parallelNumber):
            workSpace.append(None)

        for task in self.taskList:
            CONTINUE = True
            availableThread = None

            while(CONTINUE):
                for item in range(self.parallelNumber):
                    if (workSpace[item] == None) or (workSpace[item].is_alive() == False):
                        CONTINUE = False
                        availableThread = Item
                        break
                    elif item == self.parallelNumber - 1:
                        chronus.sleep(1)
                    
            workSpace[availableThread] = multiprocessing.Process(target = task[0], args = task[1])
            workSpace[availableThread].start() 

        for item in workSpace:
            if item != None:
                item.join() 


class taskMatrix:
    def __init__(self, core, thread, threadLimitPerMinute = None):
        self.core = core
        self.thread = thread
        self.taskList = []
        self.limitPerMinute = limitPerMinute

        for item in range(self.core):
            self.taskList.append([])
        self.autoAssignedTaskList = []

    def assignTask(self, function, taskArg):
        for item in taskArg:
            self.autoAssignedTaskList.append([tunction, tuple(item)])

    def assignTaskList(self, taskList):
        self.taskList = taskList

    def newProcess(self, processTaskList):
        multiThreadProcess = multiThread(self.thread, limitPerMinute = self.threadLimitPerMinute)
        multiThreadProcess.assignTaskList(processTaskList)
        multiThreadProcess.start()

    def start(self):
        taskPointer = 0
        corepointer = 0
        taskNumber = len(self.AutoArrangedTaskList)
        while(TaskPointer<TaskNumber):
            self.TaskList[Corepointer].append(self.AutoArrangedTaskList[TaskPointer])
            TaskPointer += 1
            Corepointer += 1
            if Corepointer == self.Core:
                Corepointer = 0

        MultiCoreProcess = MultCore(self.Core)
        TaskArg = [[self.TaskList[Item]] for Item in range(self.Core)]
        MultiCoreProcess.ImportTask(self.NewProcess, TaskArg)

        MultiCoreProcess.Start()

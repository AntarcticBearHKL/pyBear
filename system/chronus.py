import calendar
import datetime
import time

import pyBear.bear as bear

class frame:
    def __init__(self, load=None, timeShift=None):
        if type(load) == frame:
            self.time = load.time
            self.timeShift = load.timeShift

        elif type(load) == datetime.datetime:
            self.time = load
            if type(timeShift) == int:
                self.timeShift = timeShift 
            else:
                self.timeShift = bear.localTimeZoneShift  

        elif len(str(load)) == 8: #YYYYMMDD
            self.time = datetime.datetime(
                int(load[0:4]), int(load[4:6]), int(load[6:8]))
            if type(timeShift) == int:
                self.timeShift = timeShift
            else:
                self.timeShift = bear.localTimeZoneShift

        elif len(str(load)) == 10: #YYYY-MM-DD
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[5:7]), int(load[8:10]))
            if type(timeShift) == int:
                self.timeShift = timeShift 
            else:
                self.timeShift = bear.localTimeZoneShift 

        elif len(str(load)) == 19: #YYYY-MM-DD HH:MM:SS
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[5:7]), int(load[8:10]), 
                int(load[11:13]), int(load[14:16]), int(load[17:19]))
            if type(timeShift) == int:
                self.timeShift = timeShift 
            else:
                self.timeShift = bear.localTimeZoneShift 
        
        elif len(str(load)) == 18: #YYYYMMDDHHMMSS(TZ)
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[4:6]), int(load[6:8]), 
                int(load[8:10]), int(load[10:12]), int(load[12:14]))
            self.timeShift = int(load[15:17])

        elif len(str(load)) == 24: #ISOFormate
            load = str(load)
            self.time = datetime.datetime.fromisoformat(load[:-5])
            self.timeShift = 0
        
        else:
            self.time = datetime.datetime.now()
            self.timeShift = bear.localTimeZoneShift

        self.timeZoneRectification(shift=bear.localTimeZoneShift)



    def date(self): #YYYY-MM-DD 10
        return self.time.strftime('%Y-%m-%d')

    def clock(self): #YYYY-MM-DD HH:MM:SS 19
        return self.time.strftime('%Y-%m-%d %H:%M:%S')

    def ISOString(self): #ISOFormate 24
        return frame(self).timeZoneRectification().time.isoformat().split('.')[0]+'.000Z'

    def stringify(self): #YYYYMMDDHHMMSS(TZ) 18
       return self.time.strftime('%Y%m%d%H%M%S') +'(' + str(self.timeShift) + ')'

    
    def year(self):
        return str(self.time.date().year)

    def month(self):
        ret = self.time.date().month
        if ret < 10:
            return '0' + str(ret)
        return str(ret)

    def day(self):
        return str(self.time.date().day)

    def hour(self):
        return str(self.time.time().hour)

    def minute(self):
        return str(self.time.time().minute)

    def second(self):
        return str(self.time.time().second)


    def yearInt(self):
        return int(self.time.date().year)

    def monthInt(self):
        return int(self.time.date().month)

    def dayInt(self):
        return int(self.time.date().day)

    def hourInt(self):
        return int(self.time.time().hour)

    def minuteInt(self):
        return int(self.time.time().minute)

    def secondInt(self):
        return int(self.time.time().second)



    def setTime(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        if year != None:
            nyear = year
        else:
            nyear = self.yearInt()

        if month != None:
            nmonth = month
        else:
            nmonth = self.monthInt()
        
        if day != None:
            if day == 999:
                nday = calender(nyear, nmonth, 1).daysOfMonth()
            else:
                nday = day
        else:
            nday = self.dayInt()
        
        if hour != None:
            nhour = hour
        else:
            nhour = self.hourInt()

        if minute != None:
            nminute = minute
        else:
            nminute = self.minuteInt()

        if second != None:
            nsecond = second
        else:
            nsecond = self.secondInt()

        self.time = datetime.datetime(nyear, nmonth, nday, nhour, nminute, nsecond)
        return self


    def shift(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        nyear = self.yearInt() + year

        nmonth = self.monthInt() + month
        nyear += (nmonth - 1) // 12
        nmonth = ((nmonth - 1) % 12) + 1

        base = datetime.datetime(
            nyear, nmonth, self.dayInt(), 
            self.hourInt(), self.minuteInt(), self.secondInt())

        timePlus = datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=second) 
    
        self.time = base + timePlus
        return self


    def startOfMinute(self):
        return self.setTime(second=0)

    def startOfHour(self):
        return self.setTime(minute=0, second=0)

    def startOfDay(self):
        return self.setTime(hour=0, minute=0, second=0)

    def startOfMonth(self):
        return self.setTime(day=1, hour=0, minute=0, second=0)

    def startOfYear(self):
        return self.setTime(month=1, day=1, hour=0, minute=0, second=0)


    def timeZoneRectification(self, shift=0):
        timeShiftDelta = shift - self.timeShift
        self.shift(hour=timeShiftDelta)
        self.timeShift = shift
        return self

    def equalization(self):
        return frame(self).timeZoneRectification()



    def daysOfMonth(self):
        return calendar.monthrange(self.yearInt(), self.monthInt())[1]

    def daysOfYear(self):
        month = 1
        ret = 0
        while month<13:
            ret += calendar.monthrange(self.yearInt(), month)[1]
            month += 1
        return ret


    def daysRemainingOfMonth(self):
        return self.daysOfMonth() - self.dayInt()
    
    def daysRemainingOfYear(self):
        month = self.monthInt() + 1
        ret = 0
        while month<13:
            ret += calendar.monthrange(self.yearInt(), month)[1]
            month += 1
        ret += self.daysRemainingOfMonth()
        return ret


    def __str__(self):
        return self.clock()


    def __add__(self, rhs):
        return self.shift(second=rhs)

    def __sub__(self, rhs): # How Much Second ( - )
        if type(rhs) == int:
            return self.shift(second=-rhs)
        ret = 0
        timeList = self // rhs
        yearStart = rhs.yearInt()
        monthStart = rhs.monthInt()
        monthDays = calendar.mdays
        for Item in range(timeList[0]):
            yearDays = 366 if calendar.isleap(int(str(yearStart))) else 365
            ret += yearDays * 86400
            yearStart += 1
        for Item in range(abs(timeList[1])):
            if timeList[1]>0:
                ret+= monthDays[MonthStart] * 86400
                monthStart += 1
            else:
                ret-= monthDays[Item+1] * 86400
        ret += timeList[2]*86400 + timeList[3]*3600 + timeList[4]*60 + timeList[5]
        return ret


    def __floordiv__(self, rhs): #[Y,M,D,h,m,s] (//)
        ret = []
        ret.append(self.yearInt()- rhs.yearInt())
        ret.append(self.monthInt()- rhs.monthInt())
        ret.append(self.dayInt()- rhs.dayInt())
        ret.append(self.hourInt()- rhs.hourInt())
        ret.append(self.minuteInt()- rhs.minuteInt())
        ret.append(self.secondInt()- rhs.secondInt())
        return ret


    def __lt__(self, rhs):
        if self.equalization().time < rhs.equalization().time:
            return True
        return False
 
    def __le__(self, rhs):
        if self.equalization().time <= rhs.equalization().time:
            return True
        return False

    def __gt__(self, rhs):
        if self.equalization().time > rhs.equalization().time:
            return True
        return False

    def __ge__(self, rhs):
        if self.equalization().time >= rhs.equalization().time:
            return True
        return False

    def __eq__(self, rhs):
        if self.equalization().time == rhs.equalization().time:
            return True
        return False

    def __ne__(self, rhs):
        if self.equalization().time != rhs.equalization().time:
            return True
        return False


MissingValueMode_NoneValue = 0
MissingValueMode_ForewardValue = 1
MissingValueMode_CustomFunction = 99

class frameSequence:
    def __init__(self, value=None, missingValueMode=MissingValueMode_ForewardValue
):
        self.frame = []
        self.value = []

        self.startFrame = None
        self.endFrame = None

        if value:
            self.frame = value[0]
            self.value = value[1]
    
        self.missingValueMode = missingValueMode

    def insert(self, data, override = False):
        for item in data:
            if self.frame == []:
                self.frame.append(item[0])
                self.value.append(item[1])
                continue

            for position in range(self.length()):
                if item[0] < self.frame[position]:
                    self.frame.insert(position, item[0])
                    self.value.insert(position, item[1])
                    break
                elif item[0] == self.frame[position]:
                    if item[1] == self.value[position]:
                        break
                    elif override:
                        self.value[position] = item[1]
                        break
                    else:
                        self.show()
                        assert False
                else:
                    self.frame.append(item[0])
                    self.value.append(item[1])
                    break
        return self

    def setMissingValueMode(self, valueMode, valueFuncion=None):
        if valueMode == MissingValueMode_CustomFunction:
            self.missingValueMode = valueMode
            self.missingValueModeFunction = valueFunction
            return
        self.missingValueMode = valueMode


    def length(self):
        return len(self.frame)


    def __getitem__(self, index):
        if isinstance(index, int):
            return [self.frame[index], self.value[index]]
        if isinstance(index, frame):
            if self.missingValueMode == MissingValueMode_NoneValue: 
                for counter in range(self.length()):
                    if self.frame[counter] == index:
                        return self.value[counter]
                return None
            elif self.missingValueMode == MissingValueMode_ForewardValue:
                for counter in range(len(self.frame)):
                    if index < self.frame[counter]:
                        if counter == 0:
                            return None
                        return self.value[counter-1]
                return self.value[-1]
            elif self.missingValueMode == MissingValueMode_CustomFunction:
                return self.missingValueModeFunction(self, index)

        elif isinstance(index, slice):
            if isinstance(index.start, int) or isinstance(index.stop, int):
               return frameSequence([self.frame[index.start:index.stop+1], self.value[index.start:index.stop+1]])

            if isinstance(index.start, frame) or isinstance(index.stop, frame):
                if index.step == None:
                    startPoint = None
                    endPoint = None
                    for counter in range(self.length()):
                        if self.frame[counter] == index.start:
                            startPoint = counter
                        if self.frame[counter] == index.stop:
                            endPoint = counter
                    return frameSequence([[self.frame[startPoint, endPoint+1]], [self.value[startPoint, endPoint]]])
                    
                if isinstance(index.step, int):
                    ret = []
                    pointer = index.start
                    while pointer <= index.stop:
                        inFrame = frame(pointer)
                        inValue = self[inFrame]
                        ret.append([inFrame, inValue])
                        pointer = pointer + index.step 
                    return frameSequence(ret)

    def window(self, width, start, end):
        print(index)


    def isEmpty(self):
        if self.frame == []:
            return True
        return False

    def show(self):
        for counter in range(len(self.value)):
            print(self.frame[counter], ':', self.value[counter])


class frameSequenceWindow:
    def __init__(self):
        pass


class frameSequenceMatrix:
    def __init__(self):
        self.sequence = {}

    def insertSequence(self, name, sequence):
        self.sequence[name] = sequence

    def backtrack(self):
        pass


timerList = {}
def timer(name):
    if name not in timerList:
        timerList[name] = frame()
    else:
        return(frame() - timerList[name])


def secToTime(sec):
    return '''%ss = %s year %s month %s day %s hour %s minute %s second'''%(
        str(sec), 
        str((sec % 1) // 31557600),
        str((sec % 31557600) // 2629800),
        str((sec % 2629800) // 86400),
        str((sec % 86400) // 3600),
        str((sec % 3600) // 60),
        str((sec % 60) // 1),
        )

def monthToString(month):
    month = int(month)
    if month < 10:
        return '0' + str(month)
    else:
        return str(month)

def sleep(second):
    time.sleep(second)

def alarm(day = 0, hour = 0, minute = 0, second = 0):
    print ('\t----------START AT: ' + frame().clock() + '----------')
    if day != 0 or hour != 0 or minute != 0 or second != 0:
        sleepSecond = day*60*60*24 + hour*60*60 + minute*60 + second
        time.sleep(sleepSecond)
    print ('\t---------- END  AT: ' + frame().clock() + '----------')

def heartBeatTask(fn, hour=0, minute=0, second=0):
    if not hour and not minute and not second:
        print('Parameter Error')
        return
    waitSecond = hour*3600 + minute*60 + second
    while(True):
        print('\nSchedule Start At : ' + frame().clock() + ' : Call Function: "' + fn.__name__ + '" & return :')
        fn()
        print('Schedule End At : ' + frame().clock())
        sleep(waitSecond)

def scheduleTask(fn, timer):
    class schedule:
        def __init__(self, timer):
            self.timer = timer.split(':')
            if len(self.timer) == 1:
                Step = frame().String(-2)
                Step = Step[0:12] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.MinuteSche
            
            elif len(self.timer) == 2:
                Step = frame().String(-2)
                Step = Step[0:10] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.hourSche
            
            elif len(self.timer) == 3:
                Step = frame().String(-2)
                Step = Step[0:8] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.daySche
            else:
                print('parameter error')
                assert 1==2
        
        def minuteSche(self):
            if frame()-self.lastStep >= 60:
                Step = frame().String(-2)
                Step = Step[0:12] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True
            return False

        def hourSche(self):
            if frame()-self.lastStep >= 3600:
                Step = frame().String(-2)
                Step = Step[0:10] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True
            return False

        def daySche(self):
            if frame()-self.lastStep >= 86400:
                Step = frame().String(-2)
                Step = Step[0:8] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True  
            return False         

    schedule = schedule.timer
    while(True):
        if Schedule.nextRound():
            print('\nSchedule Start At : ' + Clock() + ' : Call Function: "' + Fn.__name__ + '" & return :')
            Fn()
            print('Schedule End At : ' + Clock())
        Sleep(1)

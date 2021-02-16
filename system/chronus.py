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

    def __floordiv__(self, rhs): #[Y,M,D,h,m,s] (//)
        ret = []
        ret.append(self.yearInt()- rhs.yearInt())
        ret.append(self.monthInt()- rhs.monthInt())
        ret.append(self.dayInt()- rhs.dayInt())
        ret.append(self.hourInt()- rhs.hourInt())
        ret.append(self.minuteInt()- rhs.minuteInt())
        ret.append(self.secondInt()- rhs.secondInt())
        return ret

    def __sub__(self, rhs): # How Much Second (-)
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



class frameSequence:
    def __init__(self):
        self.frameLength = 0

    def insertData(self, cover):
        pass

    def getDayInterval(Start, End):
        Starty = Date(Start).yearInt()
        Startm = Date(Start).monthInt()
        Startd = Date(Start).dayInt()
        Endy = Date(End).year()
        Endm = Date(End).month()
        Endd = Date(End).dayInt()
        ret = []
        for month in calender.getBetweenmonth(Start, End):
            monthDays = calender.getDayNum(int(month[0:4]), int(month[4:6]))
        while True:
            if Startd<10:
                ret.append(str(month) + '0' + str(Startd))
            else:
                ret.append(str(month)+str(Startd))
            Startd += 1
            if (str(month) == (Endy + Endm)) and Startd > Endd:
                break
            if Startd > monthDays:
                Startd = 1
                break
        return ret

    def getMonthInterval(Start, End):
        Starty = Date(Start).yearInt()
        Startm = Date(Start).monthInt()
        Endy = Date(End).yearInt()
        Endm = Date(End).monthInt()
        ret = []
        for year in calender.getBetweenyear(Start, End):
            while True:
                if Startm<10:
                    ret.append(str(year) + '0' + str(Startm))
                else:
                    ret.append(str(year)+str(Startm))
            Startm += 1
            if Startm > 12:
                Startm = 1
                break
            if year == Endy and Startm > Endm:
                break
        return ret

    def getYearInterval(Start, End):
        Starty = Date(Start).yearInt()
        Endy = Date(End).yearInt()
        ret = []
        while True:
            ret.append(Starty)
            Starty += 1
            if Starty > Endy:
                break
        return ret

    def frameClip(Line, Start, End):
        _Start = None
        _End = None
        for _count in range(len(Line) - 1):
            if Date(Line[_count]) < Date(Start) <= Date(Line[_count + 1]):
                _Start = _count + 1
            if Date(Line[_count]) <= Date(End) < Date(Line[_count + 1]):
                _End = _count
            if Date(Start) == Date(Line[_count]):
                _Start = _count
            if Date(End) == Date(Line[_count + 1]):
                _End = _count + 1
        return [_Start, _End]


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

import calendar
import datetime
import time

import pybear.bear as bear

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
        elif len(str(load)) == 17: #YY-
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[4:6]), int(load[6:8]), 
                int(load[8:10]), int(load[10:12]), int(load[12:14]))
            self.timeShift = int(load[15:16])
        elif len(str(load)) == 8: #YYYYMMDD
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[4:6]), int(load[6:8]), 
                0, 0, 0)
            if type(timeShift) == int:
                self.timeShift = timeShift 
            else:
                self.timeShift = bear.LocalTimeZoneShift 
        elif len(str(load)) == 14: #YYYY-MM-DD(TZ)
            load = str(load)
            self.time = datetime.datetime(
                int(load[0:4]), int(load[4:6]), int(load[6:8]), 
                int(load[8:10]), int(load[10:12]), int(load[12:14]))
            if type(timeShift) == int:
                self.timeShift = timeShift 
            else:
                self.timeShift = bear.LocalTimeZoneShift 
        elif len(str(load)) == 24: #ISOFormate
            load = str(load)
            self.time = datetime.datetime.fromisoformat(load[:-5])
            self.timeShift = 0
        else:
            self.time = datetime.datetime.now()
            self.timeShift = bear.localTimeZoneShift
        self.timeZoneRectification(shift=bear.localTimeZoneShift)

    def string(self, Style=999, Raw=False):
        if Style == 1:
            Style = '%Y-%m-%d' #YYYY-MM-DD(TZ) 14
        elif Style == 2:
            Style = '%Y-%m-%d %H:%M:%S' #YYYY-MM-DD HH:MM:SS(TZ) 23
        elif Style == -1:
            Style = '%Y%m%d' #YYYYMMDD(TZ) 12
        elif Style == -2:
            Style = '%Y%m%d%H%M%S' #YYYYMMDDHHMMSS(TZ) 18
        else:
            Style = '%Y-%m-%d %H:%M:%S'
        
        if Raw:
           return self.time.strftime(Style)
        return self.time.strftime(Style) + '(' + str(self.timeShift) + ')'

    def stringify(self):
       return self.time.strftime('%Y%m%d%H%M%S') +'(' + str(self.timeShift) + ')'

    def ISOString(self):
        return Date(self).TimeZoneRectification().Time.isoformat().split('.')[0]+'.000Z'

    def setTime(self, Year=None, Month=None, Day=None, Hour=None, Minute=None, Second=None):
        if Year:
            NYear = Year
        else:
            NYear = self.YearInt()

        if Month:
            NMonth = Month
        else:
            NMonth = self.MonthInt()
        
        if Day:
            if Day == 999:
                NDay = CalEnder(Year=NYear, Month=NMonth).HowManyDays()
            else:
                NDay = Day
        else:
            NDay = self.DayInt()
        
        if Hour:
            NHour = Hour
        else:
            NHour = self.HourInt()

        if Minute:
            NMinute = Minute
        else:
            NMinute = self.MinuteInt()

        if Second:
            NSecond = Second
        else:
            NSecond = self.SecondInt()

        self.time = datetime.datetime(NYear, NMonth, NDay, NHour, NMinute, NSecond)
        return self
            
    def shift(self, Year=0, Month=0, Day=0, Hour=0, Minute=0, Second=0):
        NYear = self.YearInt() + Year

        NMonth = self.MonthInt() + Month
        NYear += (NMonth - 1) // 12
        NMonth = ((NMonth - 1) % 12) + 1

        Base = datetime.datetime(
            NYear, NMonth, self.DayInt(), 
            self.HourInt(), self.MinuteInt(), self.SecondInt())

        TimePlus = datetime.timedelta(days=Day, hours=Hour, minutes=Minute, seconds=Second) 
    
        self.time = Base + TimePlus
        return self

    def timeZoneRectification(self, Shift=0):
        timeShiftDelta = shift - self.timeShift
        self.Shift(hour=timeShiftDelta)
        self.timeShift = shift
        return self



    def date(self):
        return 

    def time(self):
        return 

    def year(self):
        return str(self.time.date().year)

    def month(self):
        Ret = self.time.date().month
        if Ret < 10:
            return '0' + str(Ret)
        else:
            return str(Ret)

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



    def setTime(self, Year=None, Month=None, Day=None, Hour=None, Minute=None, Second=None):
        if Year:
            NYear = Year
        else:
            NYear = self.YearInt()

        if Month:
            NMonth = Month
        else:
            NMonth = self.MonthInt()
        
        if Day:
            if Day == 999:
                NDay = CalEnder(Year=NYear, Month=NMonth).HowManyDays()
            else:
                NDay = Day
        else:
            NDay = self.DayInt()
        
        if Hour:
            NHour = Hour
        else:
            NHour = self.HourInt()

        if Minute:
            NMinute = Minute
        else:
            NMinute = self.MinuteInt()

        if Second:
            NSecond = Second
        else:
            NSecond = self.SecondInt()

        self.time = datetime.datetime(NYear, NMonth, NDay, NHour, NMinute, NSecond)
        return self


    def shift(self, Year=0, Month=0, Day=0, Hour=0, Minute=0, Second=0):
        NYear = self.YearInt() + Year

        NMonth = self.MonthInt() + Month
        NYear += (NMonth - 1) // 12
        NMonth = ((NMonth - 1) % 12) + 1

        Base = datetime.datetime(
            NYear, NMonth, self.DayInt(), 
            self.HourInt(), self.MinuteInt(), self.SecondInt())

        TimePlus = datetime.timedelta(days=Day, hours=Hour, minutes=Minute, seconds=Second) 
    
        self.time = Base + TimePlus
        return self


    def timeZoneRectification(self, Shift=0):
        timeShiftDelta = shift - self.timeShift
        self.Shift(hour=timeShiftDelta)
        self.timeShift = shift
        return self



    def __floordiv__(self, rhs): #[Y,M,D,h,m,s] (//)
        Ret = []
        Ret.append(self.YearInt()- rhs.YearInt())
        Ret.append(self.MonthInt()- rhs.MonthInt())
        Ret.append(self.DayInt()- rhs.DayInt())
        Ret.append(self.HourInt()- rhs.HourInt())
        Ret.append(self.MinuteInt()- rhs.MinuteInt())
        Ret.append(self.SecondInt()- rhs.SecondInt())
        return Ret

    def __sub__(self, rhs): # How Much Second (-)
        Ret = 0
        TimeList = self // rhs
        YearStart = rhs.YearInt()
        MonthStart = rhs.MonthInt()
        MonthDays = calendar.mdays
        for Item in range(TimeList[0]):
            YearDays = 366 if calendar.isleap(int(str(YearStart))) else 365
            Ret += YearDays * 86400
            YearStart += 1
        for Item in range(abs(TimeList[1])):
            if TimeList[1]>0:
                Ret+= MonthDays[MonthStart] * 86400
                MonthStart += 1
            else:
                Ret-= MonthDays[Item+ 1] * 86400
        Ret += TimeList[2]*86400 + TimeList[3]*3600 + TimeList[4]*60 + TimeList[5]
        return Ret



    def __lt__(self, rhs):
        if self.time.ShiftRectification() < rhs.Time.ShiftRectification():
            return True
        else:
            return False
 
    def __le__(self, rhs):
        if self.time.ShiftRectification() <= rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __gt__(self, rhs):
        if self.time.ShiftRectification() > rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __ge__(self, rhs):
        if self.time.ShiftRectification() >= rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __eq__(self, rhs):
        if self.time.ShiftRectification() == rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __ne__(self, rhs):
        if self.time.ShiftRectification() != rhs.Time.ShiftRectification():
            return True
        else:
            return False


class Calender:
    def __init__(self, Year = None, Month = None, Day = None):
        if Year:
            self.Year = int(Year)
        else:
            self.Year = Date().YearInt()

        if Month:
            self.Month = int(Month)
        else:
            self.Month = Date().MonthInt()

        if Day:
            self.Day = int(Day)
        else:
            self.Day = Date().DayInt()


    def Year(self):
        return self.Year

    def Month(self):
        return self.Month

    def Day(self):
        return self.Day


    def DaysOfMonth(self):
        return calendar.monthrange(int(self.Year), int(self.Month))[1]

    def DaysOfYear(self):
        Month = 1
        Ret = 0
        while Month<13:
            Ret += calendar.monthrange(int(self.Year), int(Month))[1]
            Month += 1
        return Ret


    def DaysRemainingOfMonth(self):
        return self.DaysOfMonth() - Date().DayInt()
    
    def DaysRemainingOfYear(self):
        Month = self.Month + 1
        Ret = 0
        while Month<13:
            Ret += calendar.monthrange(int(self.Year), int(Month))[1]
            Month += 1
        Ret += self.DaysRemainingOfMonth()
        return Ret



class frameSequence:
    def __init__(self):
        pass

    def getDayInterval(Start, End):
        Starty = Date(Start).YearInt()
        Startm = Date(Start).MonthInt()
        Startd = Date(Start).DayInt()
        Endy = Date(End).year()
        Endm = Date(End).month()
        Endd = Date(End).DayInt()
        ret = []
        for month in CalEnder.getBetweenMonth(Start, End):
            MonthDays = CalEnder.getDayNum(int(month[0:4]), int(month[4:6]))
        while True:
            if Startd<10:
                ret.append(str(month) + '0' + str(Startd))
            else:
                ret.append(str(month)+str(Startd))
            Startd += 1
            if (str(month) == (Endy + Endm)) and Startd > Endd:
                break
            if Startd > MonthDays:
                Startd = 1
                break
        return ret

        def getMonthInterval(Start, End):
            Starty = Date(Start).YearInt()
            Startm = Date(Start).MonthInt()
            Endy = Date(End).YearInt()
            Endm = Date(End).MonthInt()
            ret = []
            for year in CalEnder.getBetweenYear(Start, End):
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
        Starty = Date(Start).YearInt()
        Endy = Date(End).YearInt()
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
        timerList[name] = datetime.datetime.now()
    else:
        print(datetime.datetime.now() - timerList[name])


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

def monthToString(Month):
    Month = int(Month)
    if Month < 10:
        return '0' + str(Month)
    else:
        return str(Month)

def sleep(second):
    time.sleep(second)

def alarm(day = 0, hour = 0, minute = 0, second = 0):
    print ('\t----------START AT: ' + clock() + '----------')
    if day != 0 or hour != 0 or minute != 0 or second != 0:
        interval = day*60*60*24 + hour*60*60 + minute*60 + second
        time.sleep(interval)
    print ('\t---------- END  AT: ' + clock() + '----------')

def heartBeatTask(Fn, Hour=0, Minute=0, Second=0):
    if not Hour and not Minute and not Second:
        print('Parameter Error')
        exit()
    WaitSecond = Hour*3600 + Minute*60 + Second
    while(True):
        print('\nSchedule Start At : ' + Clock() + ' : Call Function: "' + Fn.__name__ + '" & Return :')
        Fn()
        print('Schedule End At : ' + Clock())
        Sleep(WaitSecond)

def scheduleTask(Fn, Timer):
    class Schedule:
        def __init__(self, Timer):
            self.timer = Timer.split(':')
            if len(self.timer) == 1:
                Step = Date().String(-2)
                Step = Step[0:12] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.MinuteSche
            elif len(self.timer) == 2:
                Step = Date().String(-2)
                Step = Step[0:10] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.hourSche
            elif len(self.timer) == 3:
                Step = Date().String(-2)
                Step = Step[0:8] + ''.join(self.timer)
                self.lastStep = Date(Step)
                self.nextRound = self.daySche
            else:
                print('parameter error')
                exit()
        
        def MinuteSche(self):
            if Date()-self.lastStep >= 60:
                Step = Date().String(-2)
                Step = Step[0:12] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True
            return False

        def HourSche(self):
            if Date()-self.lastStep >= 3600:
                Step = Date().String(-2)
                Step = Step[0:10] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True
            return False

        def DaySche(self):
            if Date()-self.lastStep >= 86400:
                Step = Date().String(-2)
                Step = Step[0:8] + ''.join(self.timer)
                self.lastStep = Date(Step)
                return True  
            return False         

    Schedule = Schedule(Timer)
    while(True):
        if Schedule.nextRound():
            print('\nSchedule Start At : ' + Clock() + ' : Call Function: "' + Fn.__name__ + '" & Return :')
            Fn()
            print('Schedule End At : ' + Clock())
        Sleep(1)

def getDayInterval(Start, End):
    Starty = Date(Start).YearInt()
    Startm = Date(Start).MonthInt()
    Startd = Date(Start).DayInt()
    Endy = Date(End).year()
    Endm = Date(End).month()
    Endd = Date(End).DayInt()
    ret = []
    for month in CalEnder.getBetweenMonth(Start, End):
        MonthDays = CalEnder.getDayNum(int(month[0:4]), int(month[4:6]))
        while True:
            if Startd<10:
                ret.append(str(month) + '0' + str(Startd))
            else:
                ret.append(str(month)+str(Startd))
            Startd += 1
            if (str(month) == (Endy + Endm)) and Startd > Endd:
                break
            if Startd > MonthDays:
                Startd = 1
                break
    return ret

def getMonthInterval(Start, End):
    Starty = Date(Start).YearInt()
    Startm = Date(Start).MonthInt()
    Endy = Date(End).YearInt()
    Endm = Date(End).MonthInt()
    ret = []
    for year in CalEnder.getBetweenYear(Start, End):
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
    Starty = Date(Start).YearInt()
    Endy = Date(End).YearInt()
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

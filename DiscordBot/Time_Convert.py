import math



def format(weeks, days, hours, mins, secs, mili):
      def dayFormat(days):
            if days == 0:
                  return f"{hours} h: {mins} m: {secs} s: {mili} ms"
            elif days == 1:
                  return f"{days} day, {hours} h: {mins} m: {secs} s: {mili} ms"
            else:
                  return f"{days} days, {hours} h: {mins} m: {secs} s: {mili} ms"

      end = dayFormat(days)
      if weeks == 0:
            return f"{end}"
      elif weeks == 1:
            return f"{weeks} week, {end}"
      else:
            return f"{weeks} weeks, {end}"


class TimeConverter():

      def __init__(self):
            pass


      def timeConvert(self, seconds: int or float):
            time_seconds = seconds

            weeksR = math.floor(time_seconds / 604800)
            decreaserW = (weeksR * 604800)

            daysR = math.floor((time_seconds - decreaserW) / 86400)
            decreaserD = (daysR * 86400)

            hoursR = math.floor((time_seconds - decreaserW - decreaserD) / 3600)
            decreaserH = (hoursR * 3600)

            minsR = math.floor((time_seconds - decreaserW - decreaserD - decreaserH) / 60)
            decreaserM = (minsR * 60)

            secsR = math.floor(time_seconds - decreaserW - decreaserD - decreaserH - decreaserM)
            decreaserS = (secsR)

            miliR = math.floor((time_seconds - decreaserW - decreaserD - decreaserH - decreaserM - decreaserS) * 1000)

            if len(str(minsR)) < 2:
                  mins = f"0{minsR}"
            else:
                  mins = minsR
            if len(str(secsR)) < 2:
                  secs = f"0{secsR}"
            else:
                  secs = secsR
            hours = hoursR
            days = daysR
            weeks = weeksR
            mili = miliR


            time = format(weeks=weeks, days=days, hours=hours, mins=mins, secs=secs, mili=mili)


            return time


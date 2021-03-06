# Code for tagging temporal expressions in text
# For details of the TIMEX format, see http://timex2.mitre.org/

# This only works in py2 virtual env.

import re
import string
import os
import sys
import pdb

# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/
try:
    from mx.DateTime import *
except ImportError:
    print("""
Requires eGenix.com mx Base Distribution
http://www.egenix.com/products/python/mxBase/""")

# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december|jan|feb|mar|apr|aug|sept|oct|nov|dec)"
# need some abbreviation for month
dmy = "(year|day|week|month)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
exp1 = "(before|after|earlier|later|ago)"
exp2 = "(this|next|last)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"

regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"
# match month and month_abbrev with comma or space in between.
# This reg expression can catch form of explicit day or month or year.
# e.g. Februray 18th, 2005
regxp3 = "(" + month + "\s*(\d{1,2})+[a-z]{0,2}[,\s]*" + year + ")"
         # + year + ")"
regxp4 = "(" + month + "[,\s]*" + year + ")"
regxp5 = "(" + year + ")"
regxp6 = "(" + month + "\s*(\d{1,2})+[a-z]{0,2}[,\s]*)"

# for time expression like 19 June, 1999
# regxp4 =

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
# reg5 = re.compile(year)
# month, day, year
reg5 = re.compile(regxp3, re.IGNORECASE)
# month, year
reg6 = re.compile(regxp4, re.IGNORECASE)
# year
reg7 = re.compile(regxp5, re.IGNORECASE)


def tag(text):
    # Initialization
    exp_date = []
    real_Date = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        exp_date.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        exp_date.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
        exp_date.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
        exp_date.append(timex)

    # # Year
    # found = reg5.findall(text)
    # for timex in found:
    #     exp_date.append(timex)

    # reg5 replaced by month + year
    found = reg5.findall(text)
    for timex in found:
        exp_date.append(timex)
        real_Date.append(timex)

    found = reg6.findall(text)
    for timex in found:
        exp_date.append(timex)
        real_Date.append(timex)

    found = reg7.findall(text)
    for timex in found:
        exp_date.append(timex)
        real_Date.append(timex)

    # Tag only temporal expressions which haven't been tagged.
    for timex in exp_date:
        try:
            text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)
        except:
            text = re.sub(timex[0] + '(?!</TIMEX2>)', '<TIMEX2>' + timex[0] + '</TIMEX2>', text)
    return real_Date, text


# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
hashweekday = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6}

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]


# add the function call to prevent some style problems.
def hashweekdays(weekday):
    return hashweekday[weekday.capitalize()]


hashmonths = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'Aug': 8,
    'Sept': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


# Hash number in words into the corresponding integer value
def hashnum(number):
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
      return 1000


# This deals with the problem of None base date (No explicit dates)
# The solution is not to do any tagging.
def ret_ground(func):
    def call(text):
        exp_date, tagged_text = tag(text)
        base_date = retrieve_date_time(exp_date)
        if base_date:
            return func(tagged_text, base_date)
        else:
            return text
    return call


# Given a timex_tagged_text and a Date object set to base_date,
# returns timex_grounded_text

# Not very cool for previous version, month variable is re-used and cause some problems.

# if somehow the base_date is None, we need to fix that!!
# Fix month capitalize problem. But found that some matching still has no explicit time value. (e.g. 450 years ago)

@ret_ground
def ground(tagged_text, base_date):

    # Find all identified timex and put them into a list
    # pdb.set_trace()
    timex_regex = re.compile(r'<TIMEX2>.*?</TIMEX2>', re.DOTALL)
    exp_date = timex_regex.findall(tagged_text)
    exp_date = map(lambda timex:re.sub(r'</?TIMEX2.*?>', '', timex), \
                exp_date)

    # Calculate the new date accordingly
    for timex in exp_date:
        timex_val = 'UNKNOWN' # Default value

        timex_ori = timex   # Backup original timex for later substitution

        # If numbers are given in words, hash them into corresponding numbers.
        # eg. twenty five days ago --> 25 days ago
        if re.search(numbers, timex, re.IGNORECASE):
            split_timex = re.split(r'\s(?=days?|months?|years?|weeks?)', \
                                                              timex.lower(), re.IGNORECASE)
            value = split_timex[0]
            try:
                unit = split_timex[1]
            except:
                pdb.set_trace()
            num_list = map(lambda s:hashnum(s),re.findall(numbers + '+', \
                                          value, re.IGNORECASE))
            timex = repr(sum(num_list)) + ' ' + unit

        # pdb.set_trace()

        # If timex matches ISO format, remove 'time' and reorder 'date'
        if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', timex):
            dmy = re.split(r'\s', timex)[0]
            dmy = re.split(r'/|-', dmy)
            timex_val = Date(dmy[2], dmy[1], dmy[0])

        # and we need time value for all real_time.
        # have to match in the detail to rough order.
        elif reg5.match(timex):
            exp = reg5.findall(timex)[0]
            try:
                timex_val = Date(int(exp[-1]), hashmonths[exp[-3].capitalize()], int(exp[-2]))
            except:
                timex_val = Date(int(exp[-1]), hashmonths[exp[-3].capitalize()])

        elif reg6.match(timex):
            exp = reg6.findall(timex)[0]
            timex_val = Date(int(exp[-1]), hashmonths[exp[-2].capitalize()])

        elif reg7.match(timex):
            exp = reg7.findall(timex)[0]
            timex_val = Date(int(exp[-1]))

        # Relative dates
        elif re.match(r'tonight|tonite|today', timex, re.IGNORECASE):
            timex_val = base_date
        elif re.match(r'yesterday', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(days=-1)
        elif re.match(r'tomorrow', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(days=+1)

        # Weekday in the previous week.
        elif re.match(r'last ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays(timex.split()[1])
            timex_val = base_date + RelativeDate(weeks=-1, \
                            weekday=(day,0))

        # Weekday in the current week.
        elif re.match(r'this ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays(timex.split()[1])
            timex_val = base_date + RelativeDate(weeks=0, \
                            weekday=(day,0))

        # Weekday in the following week.
        elif re.match(r'next ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays(timex.split()[1])
            timex_val = base_date + RelativeDate(weeks=+1, \
                              weekday=(day,0))

        # Last, this, next week.
        elif re.match(r'last week', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(weeks=-1)

            # iso_week returns a triple (year, week, day) hence, retrieve
            # only week value.

        elif re.match(r'this week', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(weeks=0)
        elif re.match(r'next week', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(weeks=+1)

        # Month in the previous year.
        elif re.match(r'last ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year - 1, month_val)

        # Month in the current year.
        elif re.match(r'this ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year, month_val)

        # Month in the following year.
        elif re.match(r'next ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year, month_val)

        # Month in the previous year.
        elif re.match(r'last ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year-1, month_val)

        # Month in the current year.
        elif re.match(r'this ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year, month_val)

        # Month in the following year.
        elif re.match(r'next ' + month, timex, re.IGNORECASE):
            month_val = hashmonths[timex.split()[1].capitalize()]
            timex_val = Date(base_date.year+1, month_val)

        elif re.match(r'last month', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(months=-1, day=1)

        elif re.match(r'this month', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(day=1)

        elif re.match(r'next month', timex, re.IGNORECASE):
            timex_val = base_date + RelativeDate(months=+1, day=1)

        elif re.match(r'last year', timex, re.IGNORECASE):
            timex_val = Date(base_date.year - 1)
        elif re.match(r'this year', timex, re.IGNORECASE):
            timex_val = Date(base_date.year)
        elif re.match(r'next year', timex, re.IGNORECASE):
            timex_val = Date(base_date.year + 1)

        elif re.match(r'\d+ days? (ago|earlier|before)', timex, re.IGNORECASE):

            # Calculate the offset by taking '\d+' part from the timex.
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - offset
        elif re.match(r'\d+ days? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + offset
        elif re.match(r'\d+ weeks? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + RelativeDate(weeks=-offset)
        elif re.match(r'\d+ weeks? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + RelativeDate(weeks=-offset)
        elif re.match(r'\d+ months? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + RelativeDate(months = -offset)

        elif re.match(r'\d+ months? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + RelativeDate(months = offset)

        elif re.match(r'\d+ years? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - RelativeDate(years=offset)

        elif re.match(r'\d+ years? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + RelativeDate(years = offset)



        # Remove 'time' from timex_val.
        # For example, If timex_val = 2000-02-20 12:23:34.45, then
        # timex_val = 2000-02-20

        # After modification of the codes, timex_val now is a DateTime object.
        # we may need str to get it susbtitute in text.
        timex_val = str(timex_val)

        timex_val = re.sub(r'\s.*', '', timex_val)

        # Substitute tag+timex in the text with grounded tag+timex.
        tagged_text = re.sub('<TIMEX2>' + timex_ori + '</TIMEX2>', '<TIMEX2 val=\"' \
            + timex_val + '\">' + timex_ori + '</TIMEX2>', tagged_text)

    return tagged_text


# Got the base_date for each document.
def retrieve_date_time(exp_date):
    # reverse order. The last shown timex is preferred.
    if len(exp_date) == 0:
        return None
    exp_date.reverse()
    for t in exp_date:
            if len(t) == 4:
                base_date = Date(int(t[-1]), hashmonths[t[-3].capitalize()], int(t[-2]))
            elif len(t) == 3:
                base_date = Date(int(t[-1]), hashmonths[t[-2].capitalize()])
            else:
                base_date = Date(int(t[-1]))
            return base_date
    return None


def demo():
    s = "February 11th , 2015"
    print(reg5.findall(s))

    import nltk
    text = nltk.corpus.abc.raw('rural.txt')[:10000]
    exp_date, tged_text = tag(s)
    # ret_date = retrieve_date_time(exp_date)
    # ret_date = ground(tged_text)
    print("-"*10)
    print("-" * 10)
    # pdb.set_trace()
    print(tged_text)



if __name__ == '__main__':
    demo()

#!/usr/bin/env python3
import csv
from collections import Counter
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_data():
    with open("ODI-2016.csv") as f:
        fieldnames = f.readline().split(';')
        fieldnames = [x.split('-')[1].strip() for x in fieldnames]
        csv_reader = csv.reader(f, delimiter=';')
        data = []
        for p in csv_reader:
            data.append(p)
    data = data[:-1]            # excluding empty line
    return data

def parse_course(data, t, f):
    true_list = ["Yes", "yes", "y","Y", t]
    false_list = ["No", "no", "n","N", f]
    pData = []
    for d in range(len(data)):
        if (data[d] in true_list):
            pData.append(True)
        elif (data[d] in false_list):
            pData.append(False)
        else:
            pData.append(None)
    return pData


data = load_data()
(programme, ml, ir, st, db, gender, chocolate, birthday, neighbours, stand,
 stress, money, random, bedtime, good_day1, good_day2) = zip(*data)

mlp = parse_course(ml,"y","n")
irp = parse_course(ir,"1","0")
stp = parse_course(st,"mu","sigma")
dbp = parse_course(db,"j","n")
genderp = parse_course(gender,"m","f")

npeople = len(data)                       # => 129

def parse_birthday():
    birthdays = []              # (day, month) tuples
    years = []
    birthdates = []              # (year, month, day) tuples
    for b in birthday:
        b = b.split('-')
        if len(b) != 3:
            continue
        d, m, y = b
        if d.isdigit() and m.isdigit():
            birthdays.append((int(d), int(m)))
        if y.isdigit():
            years.append(int(y))
        if d.isdigit() and m.isdigit() and y.isdigit():
            birthdates.append([int(x) for x in (d, m, y)])
    return birthdays, years, birthdates

birthdays, years, birthdates = parse_birthday()
c = Counter(birthdays)          # 4 people with the same birthday!

factorial = lambda n: n * factorial(n - 1) if n > 1 else 1

def birthday_paradox(n):
    """Probablity of NOT having a birthday collision with n people."""
    return factorial(365) / (365**n * factorial(365 - n))

# probability of there being a birthday collision in the data
p = 1 - birthday_paradox(npeople)

# filter out nondigits
random = [int(r) for r in random if r.isdigit()]


def random_plot():
    r = Counter(random)
    num, count = zip(*r.items())

    plt.style.use('ggplot')
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax.grid(False)
    ax.set_xticklabels([])
    plt.title("Histogram of (human) random numbers")
    plt.xlabel("Number")
    plt.ylabel("Counts")
    ax.bar(num, count)

    # center ticks: http://stackoverflow.com/a/17158735
    import matplotlib.ticker as ticker
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_locator(ticker.FixedLocator([i + 0.415 for i in range(1, 11)]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter([str(l) for l in range(1, 11)]))

    plt.savefig("random_human_nums", dpi=400)


def plot_birth_weekdays():
    weekdays = []
    for b in birthdates:
        d, m, y = b
        weekdays.append(date(y, m, d).isoweekday())
    plt.title("Histogram of the birthdates  ")
    plt.xlabel("Days of the Week")
    plt.ylabel("Counts")
    plt.hist(weekdays, bins=7)
    plt.show()


def plot_birth_months():
    days, months = zip(*birthdays)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.hist(months, bins=12, range=(1, 13))
    plt.title("")

    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_locator(ticker.FixedLocator([i + 0.415 for i in range(1, 13)]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter([str(l) for l in range(1, 13)]))
    plt.show()

def parse_programme():
    counts = Counter()
    programmes = []
    programme_map = {"Master": "Other", "MS": "Other", "neuroscience": "Other",
                     "Exchange": "Other", "drug discovery and safety": "Other",
                     "GSEEM": "Other",
                     "Information Sciences": "Other",
                     "Math": "Other",
                     "Business Administration": "BA",
                     "Operations Research": "EOR",
                     "Operations Research and Business Econometrics": "EOR",
                     "Econometrics and Operations Research": "EOR",
                     "Computational Science": "CLS",
                     "Quantitative risk management": "QRM",
                     "Econometrics": "ECO",
                     "Bioinformatics": "BIO",

                     "Math / Computational Science": "CLS",
                     "Econometrics / Quantitative risk management": "ECO",
                     "BA / Econometrics": "BA"}
    for p in programme:
        if '/' in p:
            ps = [x.strip() for x in p.split('/')]
        else:
            ps = [p]

        for x in ps:
            counts[programme_map.get(x, x)] += 1

    for p in programme:
        programmes.append(programme_map.get(p, p))
    return counts, programmes

def programme_chart():
    counts, = parse_programme()
    counts = list(counts.items())
    labels, c = zip(*counts)

    colors = ("#b58900", "#cb4b16", "#dc322f", "#002b36", "#d33682", "#6c71c4", "#268bd2", "#2aa198", "#859900")
    plt.pie(c, labels=labels, colors=colors)
    plt.title("Programme Chart")
    plt.savefig("programme_pie", dpi=400)


_, programmes = parse_programme()

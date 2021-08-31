import telebot
import datetime
import sqlite3
import os
from telebot import types

token = "1780761205:AAEAujP5IDdP0wGhz9gNXUpSXhSJ-LymeXY"

bot = telebot.TeleBot(token)

userSubgroup = "1"

def returnTheWeekParity(weekNum):
    parity = 1 if int(weekNum) % 2 == 1 else 2
    return parity

def returnDayliLessonsList(dayOfWeek, weekParity):
    try:
        today = int(datetime.datetime.today().strftime("%w")) 
        if (today == 6 or today == 0):
            weekParity = abs(weekParity - 3)
        sqliteConn = sqlite3.connect("timetable.db")
        cursor = sqliteConn.cursor()
        timetableName = "tt090302_2st_" + userSubgroup + "sg"
        sqliteSelect = "SELECT * FROM " + timetableName + " where dayOfWeek = ?"
        cursor.execute(sqliteSelect, (dayOfWeek,))
        recordsTimetable = cursor.fetchall()

        sqliteSelectTimes = "SELECT * FROM lesstimes"
        cursor.execute(sqliteSelectTimes)
        recordsTimes = cursor.fetchall()

        indent = "  "
        if dayOfWeek == 1:
            mainOutput = indent + "П О Н Е Д Е Л Ь Н И К \n"
        elif dayOfWeek == 2:
            mainOutput = indent + "В Т О Р Н И К\n"
        elif dayOfWeek == 3: 
            mainOutput = indent + "С Р Е Д А \n"
        elif dayOfWeek == 4:
            mainOutput = indent + "Ч Е Т В Е Р Г\n"
        elif dayOfWeek == 5:
            mainOutput = indent + "П Я Т Н И Ц А\n"
        elif dayOfWeek == 6:
            mainOutput = indent + "С У Б Б О Т А\n"
        elif dayOfWeek == 0:
            mainOutput = indent + "В О С К Р Е С Е Н Ь Е\n"
        else:
            mainOutput = "БОТ ПРИНЯЛ ИСЛАМ!\n"
        if recordsTimetable == []:
            mainOutput += "Выходной💤\n"
        for row in recordsTimetable:
            if (row[5] == int(weekParity) or row[5] == 0):
                i = row[1] - 1
                time = str(recordsTimes[i][1]).zfill(2) + ":" + str(recordsTimes[i][2]).zfill(2) + " — " + str(recordsTimes[i][3]).zfill(2) + ":" + str(recordsTimes[i][4]).zfill(2)
                outputForm = str(row[1]) + ") " + time + "\n" + row[2] + "(" + row[3] + "), " + row[4]
                mainOutput += outputForm + "\n"    
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqliteConn:
            sqliteConn.close()
        return mainOutput

def returnLessonsTimes():
    sqliteConn = sqlite3.connect("timetable.db")
    cursor = sqliteConn.cursor()
    timetableName = "lesstimes"
    sqliteSelect = "SELECT * FROM " + timetableName
    cursor.execute(sqliteSelect)
    recordsLessTimes = cursor.fetchall()
    return recordsLessTimes

def outputLessonsTimes(recordsLessTimes):
    output = ""
    for row in recordsLessTimes:
        oneLessTime = str(row[0]) + ") " + str(row[1]).zfill(2) + ":" + str(row[2]).zfill(2) + " — " + str(row[3]).zfill(2) + ":" + str(row[4]).zfill(2)
        output += "\n" + oneLessTime
    return output

def returnTeachersInfo():
    sqliteConn = sqlite3.connect("timetable.db")
    cursor = sqliteConn.cursor()
    teachersTable = "teacherstable"
    sqliteSelect = "SELECT * FROM " + teachersTable
    cursor.execute(sqliteSelect)
    recordsTeachers = cursor.fetchall()
    return recordsTeachers

def writeNotice(text):
    f = open("info.txt", 'w', encoding = "utf-8")
    f.write(text)
    f.close

def readNotice():
    f = open("info.txt", 'r', encoding = "utf-8")
    info = f.read()
    return info

def outputTeachers(recordsTeachers):
    output = ""
    for row in recordsTeachers:
        teacher = "➤ " + row[0] + "\n" + row[1] + " " + row[2] + " " + row[3]
        output += "\n" + teacher
    return output

def returnLessonsList(mess, dayOfWeek, weekNum):
    bot.send_message(mess.from_user.id, returnDayliLessonsList(int(dayOfWeek), returnTheWeekParity(weekNum)))    

def returnFullWLessonsList(mess, weekNum):
    allWeek = ""
    for num in range(1, 6):
        allWeek += returnDayliLessonsList(int(num), returnTheWeekParity(weekNum))
    bot.send_message(mess.from_user.id, allWeek)

def getSmallKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row("Today", "Tomorrow").row("All week", "Next week").row("Large keyboard")
    return keyboard

def getLargeKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row("Today", "Tomorrow").row("All week", "Next week").row("Lessons time", "Teachers", "Session time").row("Monday", "Tuesday","Wednesday").row("Thursday","Friday","Small keyboard")
    return keyboard

'''
def getDepartmentKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row("09.03.02", "09.03.01")
    return keyboard

def getStageKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row("1 курс", "2 курс", "3 курс", "4 курс")
    return keyboard
'''

def getSubgroupKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row("1 подгруппа", "2 подгруппа")
    return keyboard

@bot.message_handler(commands=['help'])
def send_welcome(message):
    userId = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(message.from_user.id, "Доброго времени суток, " + name + "!" +
        "\n Список команд:" +
        "\n Tomorrow — расписание на завтра" + 
        "\n Today — расписание на сегодня" + 
        "\n Monday — расписание на понедельник" + 
        "\n Tuesday — расписание на вторник" +
        "\n Wednesday — расписание на среду" + 
        "\n Thursday — расписание на четверг" + 
        "\n Friday — расписание на пятницу" + 
        "\n All week — расписание на всю неделю" + 
        "\n Next week — расписание на следующую неделю" +
        "\n Lessons time — расписание звонков" +
        "\n Teachers — ФИО преподавателей", reply_markup = getSmallKeyboard())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    userId = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(message.from_user.id, "Доброго времени суток, " + name + "!\n" +
        "Выберите свою подгруппу:", reply_markup = getSubgroupKeyboard())

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global userDepartment
    global userStage
    global userSubgroup
    global noticeText
    
    daysDict = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5}

    if message.text.lower() == "привет" or message.text.lower() == "hi" or message.text.lower() == "hello":
        name = message.from_user.first_name
        bot.send_message(message.from_user.id, "Look, who’s here! " + "Hi "+ name + "!")
    elif message.text.lower() == "пока" or message.text.lower() == "goodbye":
        bot.send_message(message.from_user.id, "Come back soon")
    elif (message.text == "1 подгруппа"):
            userSubgroup = "1"
            bot.send_message(message.from_user.id, "Great! You have chosen " + userSubgroup + " subgroup", reply_markup = getSmallKeyboard())
    elif (message.text == "2 подгруппа"):
            userSubgroup = "2"
            bot.send_message(message.from_user.id, "Great! You have chosen " + userSubgroup + " subgroup", reply_markup = getSmallKeyboard())
    elif message.text == "Small keyboard":
        bot.send_message(message.from_user.id, "...", reply_markup = getSmallKeyboard())
    elif message.text == "Large keyboard":
        bot.send_message(message.from_user.id, "...", reply_markup = getLargeKeyboard())
    elif message.text == "Tomorrow":
        today = datetime.datetime.today()
        tommorow = today + datetime.timedelta(days=1) 
        dayNum = tommorow.strftime("%w")
        weekNum = today.strftime("%V")
        returnLessonsList(message, dayNum, weekNum)    
    elif message.text == "Today":
        today = datetime.datetime.today().strftime("%w")
        weekNum = datetime.datetime.today().strftime("%V")
        returnLessonsList(message, today, weekNum)
    elif message.text in daysDict.keys():
        today = daysDict[message.text]
        weekNum = datetime.datetime.today().strftime("%V")
        returnLessonsList(message, today, weekNum)         
    elif message.text == "All week":
        weekNum = datetime.datetime.today().strftime("%V")
        returnFullWLessonsList(message, weekNum)  
    elif message.text == "Next week":
        weekNum = int(datetime.datetime.today().strftime("%V")) + 1
        returnFullWLessonsList(message, weekNum)  
    elif message.text == "Lessons time":
        bot.send_message(message.from_user.id, outputLessonsTimes(returnLessonsTimes()))
    elif message.text == "Teachers":
        bot.send_message(message.from_user.id, outputTeachers(returnTeachersInfo()))
    elif message.text == "Session time":
        photo = open("session.jpg", 'rb')
        bot.send_photo(message.from_user.id, photo)
    elif message.text == "Notice":
        info = readNotice()
        bot.send_message(message.from_user.id, info)
    elif message.text[:8] == "Add info":
        noticeText = message.text[9:]
        writeNotice(noticeText)
        bot.send_message(message.from_user.id, "Инфу принял!")
    else:
        bot.send_message(message.from_user.id, "Не понял!")
    
bot.polling()
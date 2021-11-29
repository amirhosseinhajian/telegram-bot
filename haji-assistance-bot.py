import telebot
import qrcode
import random
from khayyam import JalaliDatetime
from gtts import gTTS

number = 0

bot = telebot.TeleBot("Hidden")


@bot.message_handler(commands=['start'])
def salam(message):
    bot.reply_to(message, "خوش آمدی" + message.from_user.first_name)


@bot.message_handler(commands=['max'])
def send_max(message):
    array = bot.send_message(message.chat.id, 'آرایه را به صورت مثال روبه رو وارد کن 88,55,99,5,2,65')
    bot.register_next_step_handler(array, find_max)


@bot.message_handler(commands=['argmax'])
def send_max_index(message):
    array = bot.send_message(message.chat.id, 'آرایه را به صورت مثال روبه رو وارد کن 88,55,99,5,2,65')
    bot.register_next_step_handler(array, find_max_index)


@bot.message_handler(commands=['qrcode'])
def qrcode_generate(message):
    text = bot.send_message(message.chat.id, 'متنت رو بفرست')
    bot.register_next_step_handler(text, qrcode_generator)


@bot.message_handler(commands=['help'])
def help(message):
    text = bot.send_message(message.chat.id, """
در پایین لیست کامند ها و توضیحات هرکدام ذکر شده است:

/start
خوش آمد گویی به شما گفته میشود

/game 
بازی حدس اعداد اجرا خواهد شد

/age
تاریخ تولد را به هجری شمسی وارد میکنید و سن خود را دریافت خواهید کرد

/voice
با ارسال یک جمله انگلیسی صوت آن را دریافت خواهید کرد

/max
 یک آرایه به صورت 14,7,78,15,8,19,20 وارد میکنید و بزرگترین مقدار را دریافت خواهید کرد

/argmax
یک آرایه به صورت 14,7,78,15,8,19,20 وارد میکنید و اندیس بزرگترین مقدار را دریافت خواهید کرد

/qrcode
یک متن وارد میکنید و بارکد آن را دریافت خواهید کرد

/help
راهنمای دستورات من را دریافت خواهید کرد
        """)


@bot.message_handler(commands=['game'])
def guse_number_game(message):
    global number
    number = random.randint(8, 47)
    user_guse = bot.send_message(message.chat.id, 'بازی شروع شد حالا یک عدد حدس بزن')
    bot.register_next_step_handler(user_guse, game)


@bot.message_handler(commands=['age'])
def age_comp(message):
    birth_day = bot.send_message(message.chat.id, ' تاریخ تولدت رو به هجری شمسی وارد کن (به طور مثال: 1385/4/12)')
    bot.register_next_step_handler(birth_day, age_Computing)


@bot.message_handler(commands=['voice'])
def convert_to_voice(message):
    sentence = bot.send_message(message.chat.id, 'یک متن به انگلیسی بنویس')
    bot.register_next_step_handler(sentence, text2voice)


def find_max(array):
    try:
        nums = list(map(int, array.text.split(',')))
        max_num = max(nums)
        bot.send_message(
            array.chat.id, "بزرگترین عدد " + str(max_num) + " است")
    except:
        array = bot.send_message(array.chat.id,
                                 'نه نشد! فقط با فرمت مثال رو به رو آرایه عددی رو وارد کن 14,7,78,15,8,19,20')
        bot.register_next_step_handler(array, find_max)


def find_max_index(array):
    try:
        nums = list(map(int, array.text.split(',')))
        max_num = nums.index(max(nums)) + 1
        bot.send_message(
            array.chat.id, "بزرگترین عدد در خانه " + str(max_num) + " است")
    except:
        array = bot.send_message(array.chat.id,
                                 'نه نشد! فقط با فرمت مثال رو به رو آرایه عددی رو وارد کن 14,7,78,15,8,19,20')
        bot.register_next_step_handler(array, find_max_index)


def qrcode_generator(str):
    try:
        img = qrcode.make(str.text)
        img.save('QrCode.png')
        qr_img = open('QrCode.png', 'rb')
        bot.send_photo(str.chat.id, qr_img)
    except:
        str = bot.send_message(str.chat.id, 'نه نشد! فقط متن بهم بده')
        bot.register_next_step_handler(str, qrcode_generator)


def game(user_guse):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn = telebot.types.KeyboardButton('New Game')
    markup.add(itembtn)

    global number
    if user_guse.text == "New Game":
        user_guse = bot.send_message(user_guse.chat.id, 'بازی دوباره شروع شد پس دوباره یک عدد حدس بزن',
                                     reply_markup=markup)
        number = random.randint(8, 47)
        bot.register_next_step_handler(user_guse, game)
    else:
        try:
            if int(user_guse.text) < number:
                user_guse = bot.send_message(user_guse.chat.id, 'برو بالا', reply_markup=markup)
                bot.register_next_step_handler(user_guse, game)
            elif int(user_guse.text) > number:
                user_guse = bot.send_message(user_guse.chat.id, 'برو پایین', reply_markup=markup)
                bot.register_next_step_handler(user_guse, game)
            else:
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                bot.send_message(user_guse.chat.id, 'برنده شدی بازی تمام شد!', reply_markup=markup)
        except:
            user_guse = bot.send_message(user_guse.chat.id, 'فقط عدد صحیح وارد کن', reply_markup=markup)
            bot.register_next_step_handler(user_guse, game)


def age_Computing(birth_day):
    try:
        y = birth_day.text.split("/")
        sub = JalaliDatetime.now() - JalaliDatetime(y[0], y[1], y[2])
        sub = str(sub)
        sub = sub.split(' ')
        year = int(int(sub[0]) / 365)
        bot.send_message(birth_day.chat.id, " شما " + str(year) + " سال دارید ")
    except:
        birth_day = bot.send_message(birth_day.chat.id,
                                     'نه نشد! فقط با فرمت و ترتیب گفته شده تارخ تولدتو وارد کن مثل این: 1388/11/25')
        bot.register_next_step_handler(birth_day, age_Computing)


def text2voice(sentence):
    try:
        my_text = sentence.text
        language = 'en'
        ojc = gTTS(text=my_text, lang=language, slow=False)
        ojc.save("ojc.mp3")
        voice = open('ojc.mp3', 'rb')
        bot.send_voice(sentence.chat.id, voice)
    except:
        sentence = bot.send_message(sentence.chat.id, 'نه نشد! فقط متن انگلیسی بهم بده')
        bot.register_next_step_handler(sentence, text2voice)


bot.infinity_polling()

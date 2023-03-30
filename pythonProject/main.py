from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,FSInputFile)
import aiogram
import os
import random
import atexit
import dotenv



dotenv.load_dotenv()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = os.getenv('API_TOKEN')
img_res=[".png",".jpg",".gif",".bmp",".svg",".cals",".tiff"]
# Создаем объекты бота и диспетчера


bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()
button_about: KeyboardButton = KeyboardButton(text='О Школе')
button_it: KeyboardButton = KeyboardButton(text='IT-сопровождение')
button_hr: KeyboardButton = KeyboardButton(text='HR')
button_other: KeyboardButton = KeyboardButton(text='Другая информация')
button_main: KeyboardButton = KeyboardButton(text='Основная информация')
button_history: KeyboardButton = KeyboardButton(text='История Компании')
button_adress:KeyboardButton = KeyboardButton(text='Адреса отделений')
button_cont:KeyboardButton = KeyboardButton(text='Контакты')

keyboard2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_history,button_adress,button_cont]],resize_keyboard=True)
cont_hist=open("history.txt",encoding="utf-8").read()
ids:dict={}
idsf=open("ids.txt",encoding="utf-8")
for i in idsf.readlines():
    ids[int(i.split()[0])]=i.split()[1]
    print(i.split()[0])
idsf.close()
idsf=open("ids.txt","a")
admins:dict={}
keyboardq={}
buttons=[]
main_keyboard={}
text_ans={}
imgs={}
file={}
ssylfile={}
ssylname={}
ssyl={}
inlbtnq={}
inlkeyboardq={}
docs={}
adminsl={}
counter={}
admins = open("admins.txt",encoding="utf-8")
for i in admins.readlines():
    adminsl[i]="admin"

# Этот хэндлер будет срабатывать на команду "/start"


@atexit.register
def goodbye():
    idsf = open("ids.txt","w", encoding="utf-8")
    for key,value in ids.items():
        idsf.write(str(key)+" "+str(value)+"\n")
        print("ok!")
    idsf.close()
@dp.message(CommandStart())
async def process_start_command(message: Message):
    userid = message.from_user.id
    if not(str(message.from_user.id) in ids):
        idsf = open("ids.txt", "a")
        idsf.write(str(message.from_user.id)+' '+os.getcwd()+"/Menu"+'\n')
        idsf.close()
    ids[message.from_user.id] = os.getcwd()+"/Menu"
    keyboardq[message.from_user.id]=[]
    text_ans[message.from_user.id]="Not Defined"
    imgs[message.from_user.id] = []
    inlkeyboardq[message.from_user.id]=[]
    docs[message.from_user.id]=[]
    for i in list(os.listdir(ids[message.from_user.id])):
        print(ids[message.from_user.id] + "/" + i)

        if (os.path.isdir(ids[message.from_user.id] + "/" + i)):
            but = KeyboardButton(text=i)
            keyboardq[message.from_user.id].append(but)

            main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                keyboard=[keyboardq[message.from_user.id]],resize_keyboard=True)
        elif i == "Ответ.txt":
            file[message.from_user.id] = open(ids[message.from_user.id] + "/" + i,encoding="utf-8")
            text_ans[message.from_user.id] = file[message.from_user.id].read()
        elif img_res.count(i[-4:]) > 0:
            print("!")
            temp = ids[message.from_user.id] + "/" + i
            photo = FSInputFile(temp)
            imgs[message.from_user.id].append(photo)
        else :
            temp = ids[message.from_user.id] + "/" + i
            doc = FSInputFile(temp)
            docs[message.from_user.id].append(doc)
            print("doc added")
            print(len(docs[message.from_user.id]))



    if len(imgs[message.from_user.id]) != 0:

        main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=[keyboardq[message.from_user.id]], resize_keyboard=True)
        for j in imgs[message.from_user.id]:
            await message.answer_photo(photo=j, caption="",
                                       reply_markup=main_keyboard[message.from_user.id], protect_content=True)
        imgs.pop(message.from_user.id, None)
    if len(docs[message.from_user.id])!= 0:
        print('see docs!')
        for j in docs[message.from_user.id]:
            await message.answer_document(document=j)

    but = KeyboardButton(text="В начало")
    keyboardq[message.from_user.id].append(but)
    main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=[keyboardq[message.from_user.id]], resize_keyboard=True)
    await message.answer(text_ans[message.from_user.id],
                         reply_markup=main_keyboard[message.from_user.id], parse_mode="HTML", protect_content=True)


@dp.message(lambda msg: msg.text[:5] == '/rass')
async def process_rass_command(message: Message):
    print("see admin!")
    print( adminsl)
    print(message.from_user.id)
    if str(message.from_user.id) in adminsl:
        print("see admin2!")
        for i in ids:
            print("sending...")
            await bot.send_message(chat_id = i, text=message.text[5:],protect_content=True)

@dp.message(lambda msg: msg.text == 'В начало')
async def process_start_command1(message: Message):
    userid=message.from_user.id
    if not(str(message.from_user.id) in ids):
        idsf = open("ids.txt", "a")
        idsf.write(str(message.from_user.id)+' '+os.getcwd()+"/Menu"+'\n')
        idsf.close()
    ids[message.from_user.id] = os.getcwd()+"/Menu"
    keyboardq[message.from_user.id]=[[]]
    text_ans[message.from_user.id]="Not Defined"
    imgs[message.from_user.id] = []
    counter[userid] = 0
    inlkeyboardq[message.from_user.id]=[]
    docs[message.from_user.id]=[]
    for i in list(os.listdir(ids[message.from_user.id])):
        print(ids[message.from_user.id] + "/" + i)
        if (os.path.isdir(ids[message.from_user.id] + "/" + i)):
            but = KeyboardButton(text=i)
            if len(keyboardq[message.from_user.id][counter[userid]]) < 2:
                keyboardq[message.from_user.id][counter[userid]].append(but)
            else:
                keyboardq[message.from_user.id].append([])
                counter[userid] += 1

            main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                keyboard=keyboardq[message.from_user.id],resize_keyboard=True)
        elif i == "Ответ.txt":
            file[message.from_user.id] = open(ids[message.from_user.id] + "/" + i,encoding="utf-8")
            text_ans[message.from_user.id] = file[message.from_user.id].read()
        elif img_res.count(i[-4:]) > 0:
            print("!")
            temp = ids[message.from_user.id] + "/" + i
            photo = FSInputFile(temp)
            imgs[message.from_user.id].append(photo)
        else :
            temp = ids[message.from_user.id] + "/" + i
            doc = FSInputFile(temp)
            docs[message.from_user.id].append(doc)
            print("doc added")
            print(len(docs[message.from_user.id]))



    if len(imgs[message.from_user.id]) != 0:

        main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboardq[message.from_user.id], resize_keyboard=True)
        for j in imgs[message.from_user.id]:
            await message.answer_photo(photo=j, caption="",
                                       reply_markup=main_keyboard[message.from_user.id], protect_content=True)
        imgs.pop(message.from_user.id, None)
    if len(docs[message.from_user.id])!= 0:
        print('see docs!')
        for j in docs[message.from_user.id]:
            await message.answer_document(document=j)

    but = KeyboardButton(text="В начало")
    keyboardq[message.from_user.id][counter[userid]].append(but)
    main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboardq[message.from_user.id], resize_keyboard=True)
    await message.answer(text_ans[message.from_user.id],
                         reply_markup=main_keyboard[message.from_user.id], parse_mode="HTML", protect_content=True)

@dp.message()
async def send_echo(message: Message):
    docs[message.from_user.id] = []
    imgs[message.from_user.id] = []
    print(message.from_user.id)
    userid=message.from_user.id
    counter[userid]=0
    if os.listdir(ids[message.from_user.id]).count(message.text)>0:
        if not (str(message.from_user.id) in ids):
            idsf = open("ids.txt", "a")
            idsf.write(
                str(message.from_user.id) + ' ' + ids[message.from_user.id]+"/"+message.text + '\n')
            idsf.close()
        ids[message.from_user.id]+="/"+message.text
        keyboardq[message.from_user.id] = [[]]
        for i in list(os.listdir(ids[message.from_user.id])):
            print(ids[message.from_user.id]+"/"+i)
            temp=""
            if (os.path.isdir(ids[message.from_user.id]+"/"+i)):
                but = KeyboardButton(text=i)
                if len(keyboardq[message.from_user.id][counter[userid]])<2:
                    keyboardq[message.from_user.id][counter[userid]].append(but)
                else:
                    keyboardq[message.from_user.id].append([])
                    counter[userid]+=1
                main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                keyboard=keyboardq[message.from_user.id],resize_keyboard=True)
            elif i=="Ответ.txt":
                print("found ans")
                file[message.from_user.id]=open(ids[message.from_user.id]+"/"+i,encoding='utf-8')
                text_ans[message.from_user.id]=file[message.from_user.id].read()
            elif img_res.count(i[-4:]) > 0:
                print("!")
                temp = ids[message.from_user.id] + "/" + i
                photo = FSInputFile(temp)
                imgs[message.from_user.id].append(photo)
        if len(imgs[message.from_user.id]) != 0:
            main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                keyboard=keyboardq[message.from_user.id], resize_keyboard=True)
            for j in imgs[message.from_user.id]:
                await message.answer_photo(photo=j, caption="",
                                           reply_markup=main_keyboard[message.from_user.id], protect_content=True)
            imgs.pop(message.from_user.id, None)
        if len(docs[message.from_user.id]) != 0:
            print('see docs!')
            for j in docs[message.from_user.id]:
                await message.answer_document(document=j)

        but = KeyboardButton(text="В начало")
        keyboardq[message.from_user.id][counter[userid]].append(but)
        main_keyboard[message.from_user.id]: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboardq[message.from_user.id], resize_keyboard=True)
        await message.answer(text_ans[message.from_user.id],
                             reply_markup=main_keyboard[message.from_user.id], parse_mode="HTML", protect_content=True)


if __name__ == '__main__':
    dp.run_polling(bot)


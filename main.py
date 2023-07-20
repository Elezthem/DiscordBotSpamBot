import requests # эта библа чтобы слать запросы в дискорд
import discord #основная библа дискорда
import asyncio # либа для потоков
from discord.ext import commands # тож надо
import json # чтобы простой текст преобразовать в json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents) # создаем "переменную бота" с префиксом "!" (можете изменить)

def send(userid): #создаем функцию send которая принимает аргумент userid
    with open('tokens.txt','r') as f: #открываем файл с токенами ботов (потом узнаете зачем)
        tokens = f.readlines() # читаем все строки с токенами
        for x in tokens: # для каждого токена из списка
            token = x.rstrip() # обрезаем его от лишнего
            payload = {
                "content": f"Спам боты lolz"
            }
            # эта штука отвечает за текст который мы шлем
            u = 'https://discord.com/api/v9/users/@me/channels' # в этой части кода мы получаем "id" лс-а с юзером (нет, это не простой id человека)
            d = {
                "recipients":[f"{userid}"]
            }

            header = {
                "authorization": f"Bot {token}"
            }
            try:
                r = requests.post(url=u,json=d,headers=header) #отправляем запрос на получение id лс-а
                jss = json.loads(r.text) # подгружаем простой текст в json
                url = f'https://discord.com/api/v9/channels/{jss["id"]}/messages' # url куда шлем запрос чтобы челик получил лс
                r = requests.post(url,data=payload,headers=header)#ну и шлем смс в лс
            except: #если что то пойдет не так пишем сообщение об ошибке
                print('[ - ] Error')


@bot.command() #команда бота
@commands.cooldown(1, 25, commands.BucketType.user) #с кд 25сек
async def spam(ctx, user:discord.Member=None):
    if user == None:# если пользователь не указан пишем об этом
        await ctx.author.send(embed=discord.Embed(title='Укажи пользователя для спама в лс!'))
    else:#если указан
        try:#пытаемся дослать до него смс
            await user.send('lolz bots')
        except:#если не получилось пишем об этом
            await ctx.send('Пользователь закрыл лс, не могу делать спам!')
            return
        #если все ок пишем об этом и ебашим поток
        await ctx.author.send(embed=discord.Embed(title=f'Спам пользователю {user} запущен'))
        await asyncio.create_task(send(idd=str(user.id)))



bot.run('')
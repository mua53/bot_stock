from pickle import TRUE
from unicodedata import name
import discord
from discord.ext import commands
from config import  *
import requests
import json
import random
import asyncio
import os
import urllib.request

bot = commands.Bot(command_prefix=PREFIX, description="Một con bot Ree đến từ stock-chat")

@bot.event
async def on_ready():
    print('Bot ngu loz đã sẵn sàng')

@bot.command(pass_context=True)
async def stock(ctx):

    await ctx.send("Xin chào, đây là bot stock!!!")

@bot.command(pass_context=True, name="price")
async def stock_price(ctx, code):
    data = call_api_vietstock(code.upper())
    mess = ""
    if data["ColorId"] == 2:
        mess = random.choice(MESS_CE)
        embed = discord.Embed(color=COLOR_CE)
    if data["ColorId"] == -2:
        mess = random.choice(MESS_FL)
        embed = discord.Embed(color=COLOR_FL)
    if data["ColorId"] == 1:
        mess = random.choice(MESS_UP)
        embed = discord.Embed(color=COLOR_UP)
    if data["ColorId"] == -1:
        mess = random.choice(MESS_DOWN)
        embed = discord.Embed(color=COLOR_DOWN)
    if data["ColorId"] == 0:
        mess = random.choice(MESS_TC)
        embed = discord.Embed(color=COLOR_TC)

    price_str = str(data["LastPrice"]/1000)
    percent_change= ''
    if data["ColorId"] >= 0:
        percent_change = '+' + str(data["PerChange"]) + '%'
    else:
        percent_change = '' + str(data["PerChange"]) + '%'
    price_change = ''
    if data["ColorId"] >= 0:
        price_change = '+' + str(data["Change"]/1000)
    else:
        price_change = '' + str(data["Change"]/1000)

    mess = mess.replace("#code#",code.upper()).replace("#price#", price_str)
    embed.set_author(name=f'Giá của {code.upper()} là: ' + price_str + ' | ' + percent_change + ' | ' + price_change)
    embed.add_field(name='Lời nhắn: ', value=mess)
    await ctx.send(embed=embed,delete_after=30)
    # await ctx.send("Giá của " + code.upper() + " là: " + str(data["LastPrice"]) + " tăng/giảm: " + percent_change + "%" + "\n" + mess, delete_after=30)
    await asyncio.sleep(20)
    await ctx.message.delete()

@bot.command(pass_context=True, name="index")
async def stock_index(ctx,code=''):
    lst_code = code.split(',')
    for name in lst_code:
        getImageIndexChart(name)
        await ctx.send(file=discord.File(name + '.png'), delete_after=30)
    await asyncio.sleep(20)
    for name in lst_code:
        file_name = name + '.png'
        if os.path.exists(file_name):
            os.remove(file_name)
    await ctx.message.delete()


@bot.command(pass_context=True, name="infor")
async def stock_price(ctx, code):
    data = call_api_vietstock(code.upper())
    await ctx.send("EPS: " + str(data["EPS"]) + "\n" + "P/E: " + str(data["PE"]) + "\n" + "P/B: " + str(data["PB"]), delete_after=30)

@bot.command(pass_context=True, name="stock-support")
async def support(ctx):
    await ctx.send("!price + mã cổ phiếu (viết hoa): Lấy thông tin giá hiện tại của cổ phiếu\n!infor + mã cổ phiếu (viết hoa): Lấy thông tin một vài chỉ cố cơ bản của cổ phiếu (Hiện đang bảo trì)" +
    "\n!index + mã index (vnindex, vn30, hnx, upcom) để lấy thông tin chart line chỉ số index")

def call_api_vietstock(code):
    url = "https://finance.vietstock.vn/company/tradinginfo"
    payload = "code=" + code +"&s=0&t=&__RequestVerificationToken=75slVHRS7aY7-7-JG2k93XdF5nuFv-iYOn2pwiEZLKomN9xWkmqSGtmOL1fTDvXrxVVMZTzyXpUpNhh1bld_oze2QRBNA69Sqjgebh0lW_U1"
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://finance.vietstock.vn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://finance.vietstock.vn/SHB-ngan-hang-tmcp-sai-gon-ha-noi.htm',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Cookie': '_ga=GA1.2.1707987505.1614912967; _ga=GA1.3.1707987505.1614912967; cto_bundle=8qmXGl9LWkdZMlVHUE8lMkZwaXglMkJ1SFUlMkIlMkJ1V0pMdmF1JTJGS3RCZ3poSTVoa0lzYTNxeTdldFBVVmpXUVFtNkpOdndoY0JtcXIyanJ4JTJGWmVscEFIazJCNlp1azdSRUR3UWlXQTYxalRjSTZnSDZJbDViRThXMzV4dlFHcnp2YTdxQVEyRUh4JTJGN21ySmJDZXI0UllMeEpqc2RzbzEyUSUzRCUzRA; __gpi=00000000-0000-0000-0000-000000000000:dmlldHN0b2NrLnZu:Lw==; dable_uid=93060591.1616146515585; dable_uid=93060591.1616146515585; language=vi-VN; Theme=Light; AnonymousNotification=; vst_usr_lg_token=jjez3jbP3EWZ8wYwm26JaQ==; isShowLogin=true; _gid=GA1.2.1696256141.1642730153; ASP.NET_SessionId=hzfkmzpetr231wvmgv455a5t; __RequestVerificationToken=UYwRjudgJ9H0TIP7aoV7jSJqJE55hOj5Ii-quhMDoi1o-GBlbaqpf47xqXLjns4tiXoZtOWW4dDRKsUxJXl1k0iqGl9ExzwCan7LirbnCm41; _gid=GA1.3.1696256141.1642730153; finance_viewedstock=SHB,; __gads=ID=82f158bde4b0d37d-2262a63212d00076:T=1628493476:RT=1642765519:S=ALNI_MbcsprDov24W8oeRxHObWAzyj15uQ'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()

def getImageIndexChart(name):
    if name.upper() == "VNINDEX":
        url = URL_VNINDEX
        file_name = name + ".png"
    elif name.upper() == "VN30":
        url = URL_VN30
        file_name =  name + ".png"
    elif name.upper() == "HNX":
        url = URL_HNX
        file_name = "hnx.png"
    elif name.upper() == "UPCOM":
        url = URL_UPCOM
        file_name =  name + ".png"
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    opener.retrieve(url, file_name)

bot.run(TOKEN,reconnect=True,bot=True)
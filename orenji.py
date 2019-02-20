#!/usr/bin/env python


'''
Pipimi 2.0
flag: 'oj '
Last updated: February 14, 2019
Author: Orange#7401

To do:
    Twitter API implementation
'''

import discord
from discord.ext import commands
import re
import random
import math
import time
import datetime
import asyncio
import json
import requests
import subprocess


with open("token.txt") as t:
    token = t.readline().strip()

bot = commands.Bot(command_prefix = 'oj ', description = 'Glorious Pipimi.')

bot.remove_command('help')

########################### bot events ###############################

#startup sequence                       
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')
    print('Stay.')
    print('--------')
    await bot.change_presence(game = discord.Game(name = 'type "oj -h"'))

#latent response to messages
@bot.event
async def on_message(message: str):
    call_msg = re.compile(r'\b(?i)(^|[^:])(pipimi)\b')
    match = call_msg.search(message.content)

    call_popuko = re.compile(r'\b(?i)(^|[^:])(popuko)\b')
    popu_match = call_popuko.search(message.content)

    call_bot = re.compile(r'\b([gG]ood)\s+([bB]ot)\b')
    bot_match = call_bot.search(message.content)

    call_bad = re.compile(r'\b([bB]ad)\s+([bB]ot)\b')
    bad_match = call_bad.search(message.content)

    call_vi = re.compile(r'^:wq?$')
    vi_match = call_vi.search(message.content)

    
    if (match and message.author != bot.user):
        await bot.send_message(message.channel,'You called?')
    
    if (popu_match and message.author != bot.user):
        await bot.send_message(message.channel, 'I love Popuko.')
    
    if (bot_match and message.author != bot.user):
        await bot.send_message(message.channel, 'Thank you.')

    if (bad_match and message.author != bot.user):
        await bot.send_message(message.channel, '<:shikushiku:426558379415306250>') 

    if (vi_match and message.author != bot.user):
        await bot.send_message(message.channel, 'This is not vi, master.') 

    await bot.process_commands(message)

################################# bot commands ###################################

@bot.command(name = '--help',
	     aliases = ['-h'])
async def help():
    embed = discord.Embed(title = 'Glorious Pipimi',
                          description = 'The cool and collected Yamato Nadeshitposter.\n', 
                          colour = 0xff6600)

    embed.add_field(name = 'Pipimi commands:', 
                    value = '**-h (--help)**\n\tGives this help message.\n' +
                            '**info**\n\tTells you more about Lady Pipimi.\n' +
                            '**color**\n\tPicks a random color.\n' + 
                            '**weeb**\n\tSimulates your weeb level out of 100.\n' +
                            '**day**\n\tPipimi tells you what day it is.\n' +
                            '**pat [val]**\n\t"I\'m the type that grows with praise."\n' +
                            '**yorha**\n\tNier;A random assignment fun.\n' + 
			    '**coal [val]**\n\tCoalescent simulation for [val] number of sequences (defaults to 10), ignores mutation rates (Wright-Fisher 1980).\n' +
                            '**join [member]**\n\tShows the join time of the member or self if member is not specified.\n',
                    inline = False)
    embed.add_field(name = 'Example usage:',
                    value = '`oj -h [--help]`',
                    inline = False)

    await bot.say(embed = embed)

@bot.command(name = 'info')
async def info():
    embed = discord.Embed(title = 'Pipimi 2.0',
                          description = 'After a `rm -rf` mishap, Pipimi returns better than ever with improved regex functionality and fun for the whole family!',
                          colour = 0xff6600)
    
    embed.set_image(url = 'https://cdn.discordapp.com/emojis/426559150462599199.png')

    embed.add_field(name = 'Maintainer: ', 
                    value = 'Orange#7401', 
                    inline = False)
    
    await bot.say(embed = embed)
 
def random_color():
    values = list('abcdef0123456789')
    color = [random.choice(values) for x in range(6)]
    my_color = '0x' + ''.join(color)

    return my_color

@bot.command(name = 'color',
             aliases = ['colour', 'Color', 'Colour'])
async def color():
    my_color = random_color()
    my_color_hex =int(my_color, 16)
    embed = discord.Embed(title = 'Color picker',
                          description = 'Hex: #' + my_color[2:],
                          color = my_color_hex)
    embed.set_image(url = 'https://www.colorhexa.com/' + my_color[2:] + '.png')

    await bot.say(embed = embed)
   
@bot.command(name = 'weeb',
             pass_context = True)
async def weeb():
    weeb = random.randint(0, 100)
    await bot.say("Your weeb level is %i" % weeb)

@bot.command(name = 'day')
async def day():
    the_day = datetime.date.today().strftime('%A')
    await bot.say("It's " + the_day + ", my dudes.")

@bot.command(name = 'yorha',
             pass_context =True)
async def yorha(ctx):
    area = random.choice(['a', 'b'])
    equip = random.choice(['a', 'b'])
    numb = random.randint(1, 100)
    model = random.choice(['B', 'O', 'S'])
    action = random.choice(['patrol', 'scan', 'subjugate', 'monitor', 'observe', 'defend'])

    await bot.say('Agent name: ' + ctx.message.author.mention + 
                  '\nDesignation: **YoRHa No. %s Type %s**\nYou are assigned to %s **%s** with registered equipment: **%s**.' % (numb, model, action, area, equip))

@bot.command(name = 'pat',
             pass_context = True)
async def pat(ctx, a=0):
    face = 'https://cdn.discordapp.com/attachments/359717074785927168/461552680196898836/pipihead.png'
    neck = 'https://cdn.discordapp.com/attachments/359717074785927168/461552677999083541/pipineck.png'
    body = 'https://cdn.discordapp.com/attachments/359717074785927168/461552675855794177/pipibody.png'
    try:
    	neck_length = int(a)
    except ValueError:
    	await bot.say('That\'s not an integer!')

    if neck_length > 5:
        await bot.say('That is too long!')
    elif neck_length < 0:
        await bot.say('<:vasco:429329534459052040>')
    else:
        embed = discord.Embed(colour = 0x2244cc)
        embed.set_image(url = face)
        await bot.say(embed = embed)
        
        if a != 0:
            while neck_length > 0:
                embed.set_image(url = neck)
                await bot.say(embed = embed)
                neck_length -= 1

        embed.set_image(url = body)
        await bot.say(embed = embed)

def make_seq(n):
    seq = ['a' + str(y) for y in range(n)]
    return seq

@bot.command(name = 'coalesce',
             aliases = ['coal'],
	     pass_context = True)
async def coalescent(ctx, num=10):
    #num is int that gives the number of sequences in population
    #sequence generator
    seqs = make_seq(int(num))
    c = 0   #generation counter
    k = len(seqs)
    embed = discord.Embed(title = 'Coalescent simulation for %i sequences' % k, 
    			  description = 'Wright-Fisher (1980)', 
			  colour = 0xff6600 )
 
    while k > 1:
        if len(seqs) == 1:
            embed.add_field(name = '**...**', 
	    		    value = 'Coalescent reached', 
			    inline = False)
            break
        lambd = 2 / (k * (k - 1))
        # generate exponential waiting time with the following rate
        pm_num = random.random()
        # no mutation rate -> mu == 0
 
        # the next exponential waiting time to coalescence
        time = random.expovariate(1 / lambd)
        # coalescent event, pick two sequences to join
        # (randomly select one to be the next item)
        if pm_num < 1:
            a = random.sample(seqs,2)
            b = random.choice(a)
            embed.add_field(name = 'Generation ' + str(c) + ' -> ' + ', '.join(seqs), 
                            value = 'Joined: ' + ', '.join(a) + ' -> ' + str(b) + '\nWaiting time: ' + str(time) + '\n', inline = False)
            for x in a:
                if x in seqs:
                    seqs.remove(x)
            seqs.append(b)
            c -=1
            k -=1
        else:
            continue

    await bot.say(embed = embed)

@bot.command(name = 'join',
	     pass_context = True)
async def join(ctx, member: discord.Member = None):
    if member is None:
    	member = ctx.message.author

    await bot.say('Hello ' + 
                  str(member)[:-5] + 
	          ', joined at: ' + 
	          str(member.joined_at))
    
@bot.command( name = 'bash',
        pass_context = True)
async def bash(ctx, *args):
    if ctx.message.author.server_permissions.administrator:
        output = subprocess.run(args, stdout=subprocess.PIPE)
        await bot.send_message(ctx.message.channel, output.stdout.decode('ascii'))
        print(output.stdout.decode('ascii'))
    else:
        await bot.say("You don't have admin privileges!!!!!! D:<")

if __name__ == '__main__':
    bot.run(token)

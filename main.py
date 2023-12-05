import discord
from discord import Intents
from timer import timer
from replit import db
import os

intents = Intents.all()
client = discord.Client(intents=intents)

db["active_timers"] = {}


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content  
  if msg.startswith("!"):
    await message.channel.send('Hello!')

    if message.content.startswith('!timer'):
      try:
        if message.content.startswith('!timer-left'):
          user_timer = db["active_timers"].get(message.author.name)
          if user_timer and user_timer['active']:
            await message.channel.send(
                f'You have {user_timer["remaining_time"]} minutes left on your timer.'
            )
          else:
            await message.channel.send('You have no time left on your timer.')

        else:
          time_minutes = int(message.content.split(' ')[1])
          await message.channel.send(f'{time_minutes} timer started.')
          await timer(message, time_minutes, db["active_timers"])

      except (IndexError, ValueError):
        await message.channel.send(
            'Invalid timer format. Use !timer [minutes] or !timer-left')

client.run(
    'MTE3Mzk2NzcwOTY5Mjc1NjA3MA.GYEOh_.ScvKkz8T2gekFDT7oBCJYjm_U5k3IixbtvPfKM')

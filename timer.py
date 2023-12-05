import discord
import schedule
import asyncio


async def timer(message, time_minutes, active_timers):
  user_name = message.author.name
  half_time = time_minutes // 2

  active_timers[user_name] = {'remaining_time': time_minutes, 'active': True}

  async def notify_time_up():
    await message.channel.send(f'Time is up! {message.author.mention}')
    active_timers[user_name]['active'] = False

  async def notify_half_time():
    await message.channel.send(f'{half_time} minute(s) left on the timer')

  schedule.every(half_time).minutes.do(asyncio.run, notify_half_time)
  schedule.every(time_minutes).minutes.do(asyncio.run, notify_time_up)

  for remaining_time in range(time_minutes, 0, -1):
    if not active_timers[user_name]['active']:
      break

    active_timers[user_name]['remaining_time'] = remaining_time
    if remaining_time == half_time:
      await asyncio.run(notify_half_time())
    await message.channel.send(f'{remaining_time} minute(s) left on the timer')
    await asyncio.sleep(60)

  schedule.clear()

  if active_timers[user_name]['active']:
    await notify_time_up()

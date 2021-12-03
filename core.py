import discord
import random
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import googletrans
from googletrans import Translator
from music import Player

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '=', intents = intents)

@client.event
async def on_ready():
    print('Bot is online')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_join(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=["8ball", "8"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.", 
                "It is decidedly so.", 
                "Without a doubt.", 
                "Reply hazy, try again.",
                "Ask again later.",
                "Don't count on it.",
                "My reply is no.",
                "Outlook not so good.",
                "Very doubtful.", 
                "Yes definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "My sources say no."]
    await ctx.send(f'**Question:** {question}\n**Answer:** {random.choice(responses)}\n*{round(client.latency * 1000)}ms*')

@client.command(aliases=["pr","Pr"])
async def _Paranoia(ctx):
    await ctx.send(f'**Question:** {random.choice(loadQueries())}\n*{round(client.latency * 1000)}ms*')
    
@client.command(aliases=["fct", "Fct"])
async def factorial(ctx, *, number:int):
    output = ""
    if number < 0:
        output = "Factorial does not exist! Number is negative."
    elif number == 0:
        output = f'The factorial of {number} is 1.\n*{round(client.latency * 1000)}ms*'
    else:
        fact = 1
        for x in range(1, number + 1):
            fact = fact * x
        output = f'The factorial of {number} is {fact}.\n*{round(client.latency * 1000)}ms*'
    await ctx.send(output)

@client.command(aliases=["clr", "prg", "purge"])
@commands.has_permissions(administrator = True)
async def clear(ctx, limit:int):
	await ctx.channel.purge(limit=limit)
	await ctx.send(f'{limit} messages have been cleared.\n*{round(client.latency * 1000)}ms*')

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f':thumbsup: **{member} has been kicked; reason: {reason}**\n*{round(client.latency * 1000)}ms*')

@client.command(aliases=["coin", "heads", "cf"])
async def coinflip(ctx):
    sides = ["Heads", "Tails"]
    await ctx.send(f'You flipped a coin. :coin:\nThe result was **{random.choice(sides)}**!\n*{round(client.latency * 1000)}ms*')

@client.command(aliases=["rp", "randompick"])
async def randompicker(ctx, *, message):
    elements = []
    if ', ' in message:
        elements = message.split(", ")
    elif ',' in message:
        elements = message.split(",")
    elif ' ' in message:
        elements = message.split(" ")
    await ctx.send(f'The result was **{random.choice(elements)}**!\n*{round(client.latency * 1000)}ms*')

@client.command(aliases=["gt"])
async def translate(ctx, lang, *, args):
    storeText = args
    t = Translator()
    a = t.translate(args, dest=lang)
    await ctx.send(f'**Original text**: {storeText}\n**Language Chosen:** {lang}\n**Translated: **{a.text}\n*{round(client.latency * 1000)}ms*')

@client.command(aliases=["halp", "cmds"])
async def helpMe(ctx):
   await ctx.send(f'{halpText()}\n*{round(client.latency * 1000)}ms*')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people dummy.")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f':thumbsup: **{member} has been banned; reason: {reason}**\n*{round(client.latency * 1000)}ms*')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people dummy.")

async def setup():
    await client.wait_until_ready()
    client.add_cog(Player(client))

client.loop.create_task(setup())

def halpText():
    halpTexted = '''```
List of Commands

=ping - returns pong!
=8ball/=8 - 8ball. what's more to be said. Format: =8ball [question]
=paranoia/=pr/=Pr - Offers a random paranoia question (currently 300ish choices, will be adding the option for users to add more)
=factorial/=fct/Fct - Gets you the factorial of any number (don't know why I made this). Format: =factorial [int]
=clear/=clr/=prg/=purge - purges the number of specified messages (only admins can use). Format: =clear [int]
=kick - kicks a member from the server. Format: =kick member reason
=ban - bans a member from the server. Format: =ban member reason
=coinflip/=coin/=heads/=cf - Flips a coin. Uses the random module offered by python
=randompicker/=rp/=randompick Picks a random element from a list. Format: =rp Red, blue, green OR =rp Red blue green OR =rp Red,blue,green. Uses random.choice
=translate/=gt translates any language to another so long as it's on google translate. Format: =translate [language] [text]. Ex: =translate fr Hi how are you? Will detect language automatically. Check https://cloud.google.com/translate/docs/languages for available languages.
=join joins a vc
=summon summon to a vc Format: =summon channel
=leave leaves vc
=volume sets volume Format: =volume [int]
=now/=current/=np/=nowplaying displays current song playing
=pause pauses the song dummy
=resume resumes playing song
=stop stops song from playing
=skip requires 3 votes or admin (unless ur alone in vc); skips song
=queue displays queue for songs
=shuffle shuffles queue
=remove removes song from queue. Format: =remove [int]
=loop loops song indefinitely.
=play plays song. Format: =play [song title] OR =play [link]

Enjoy...```'''
    return halpTexted

def loadQueries():
    queries = ["Who is most likely to cry while watching a Romantic movie?",
              "Who is most likely to watch a Horror film without batting an eyelid?",
              "Who is most likely to gift movie tickets as a birthday present?",
              "Who is most likely to consider Cardi B as an idol?",
              "Who is most likely to love sad songs?",
              "Who is most likely to go to a metal concert?",
              "Who is most likely to kill for money?",
              "Who is most likely to own a very creepy statue?",
              "Who is most likely to stalk an ex?",
              "Who is most likely to know drug peddlers?",
              "Who is most likely to laugh at serious moments?",
              "Who is most likely to move into a van?",
              "Who is most likely to be a professional choreographer?",
              "Who is most likely to be scared of all animals?",
              "Who is most likely to cuddle and fall asleep with their pet?",
              "Who is most likely to find stray animals?",
              "Who is most likely not to eat when traveling?",
              "Who is most likely to fly on a First-class ticket?",
              "Who is most likely to camp outside rather than in a cabin?",
              "Who is most likely never to become a vegetarian?",
              "Who is most likely to own a cookbook?",
              "Who is most likely to win a pizza-eating contest?",
              "Who is most likely to buy a Lamborghini?",
              "Who is most likely to have a personal chef?",
              "Who is most likely to get a Botox job?",
              "Who is most likely to have eaten raw meat before?",
              "Who is most likely to sweat the most?",
              "Who is most likely to have chewed a bug before?",
              "Who is most likely to game all night?",
              "Who is most likely to own a podcast?",
              "Who is most likely to watch cartoons still?",
              "Who is most likely to wear makeup to sleep?",
              "Who is most likely to own more shorts than trousers?",
              "Who is most likely to wear any color but white on their wedding day?",
              "Who is most likely to wear sneakers on a suit?",
              "Who is most likely had a physical fight with their best friend?",
              "Who is most likely to keep secrets from their friends?",
              "Who is most likely to share an Instagram page with their best friend?",
              "Who is most likely not to have a Netflix Account?",
              "Who is most likely to be a horrible actor if featured in a movie?",
              "Who is most likely to be a fantastic Wonder Woman?",
              "Who is most likely to leave ratings of movies online?",
              "Who is most likely to be chosen to play Superman?",
              "Who is most likely to have a lead role in a movie someday?",
              "Who is most likely to write a movie script?",
              "Who is most likely to go to the movies rather than stream online?",
              "Who is most likely to leave movie spoilers online?",
              "Who is most likely to have a heart attack from watching a scary movie?",
              "Who is most likely to be Eric KillMonger’s (from Wakanda) sidekick if he had one?",
              "Who is most likely to prefer Netflix and chill with a crush rather than any other activity?",
              "Who is most likely to be chosen to play James Bond in a random selection?",
              "Who is most likely to watch a movie rather than read the book adaption?",
              "Who is most likely to watch only classical movies?",
              "Who is most likely to attend movie premieres the most?",
              "Who is most likely to choose acting with A-List actors without getting paid over acting with unknown actors and getting paid?",
              "Who is most likely to have a star on the Hollywood Walk of Fame?",
              "Who is most likely to watch the same movie over and over?",
              "Who is most likely to win an Oscar someday?",
              "Who is most likely to watch the end credits of every movie they’ve ever seen?",
              "Who is most likely to be a movie director?",
              "Who is most likely to watch a Fantasy movie?",
              "Who is most likely to choose Tv Series over movies?",
              "Who is most likely to play a bad guy role in a movie?",
              "Who is most likely to be a stunt double in a movie?",
              "Who is most likely to shave their head for a movie?",
              "Who is most likely to become a rock star?",
              "Who is most likely to listen to Pop music?",
              "Who is most likely to pay for an autograph from Beyoncé?",
              "Who is most likely to have all of Nicki Minaj’s songs?",
              "Who is most likely to be followed by their favorite singer on social media?",
              "Who is most likely to make a really good rapper?",
              "Who is most likely to dance in public?",
              "Who is most likely to have a beautiful voice?",
              "Who is most likely to go to a metal concert?",
              "Who is most likely to be the worst at singing?",
              "Who is most likely to know how to play an instrument?",
              "Who is most likely to attend Coachella?",
              "Who is most likely always to have their earphones plugged in?",
              "Who is most likely to go for Karaoke night?",
              "Who is most likely to know the top songs on the Billboard Charts by heart?",
              "Who is most likely to stream music the most?",
              "Who is most likely to have the greatest number of songs on their phone?",
              "Who is most likely to listen to music every night before sleeping?",
              "Who is most likely to join a music band?",
              "Who is most likely to kill for money?",
              "Who is most likely to be a pickpocket?",
              "Who is most likely capable of robbing a bank in minutes?",
              "Who is most likely to kidnap a crush?",
              "Who is most likely to hide a dead body?",
              "Who is most likely to steal from their parents?",
              "Who is most likely to do a blood covenant?",
              "Who is most likely to have needed a lawyer in the past?",
              "Who is most likely to have a body buried in their backyard?",
              "Who is most likely to threaten a co-worker?",
              "Who is most likely to post a hate speech online?",
              "Who is most likely to buy stolen goods?",
              "Who is most likely to own a very creepy statue?",
              "Who is most likely to download movies illegally?",
              "Who is most likely to steal from an old person?",
              "Who is most likely to break into a house?",
              "Who is most likely to stalk an ex?",
              "Who is most likely experienced with a gun?",
              "Who is most likely to beat up an enemy?",
              "Who is most likely to be part of a cult?",
              "Who is most likely to commit manslaughter?",
              "Who is most likely to have lived in a haunted house before?",
              "Who is most likely to know drug peddlers?",
              "Who is most likely to have never had a best friend?",
              "Who is most likely to be the most good-looking in their clique?",
              "Who is most likely never to give a friend a birthday gift?",
              "Who is most likely had a physical fight with their best friend?",
              "Who is most likely to have the highest number of frenemies?",
              "Who is most likely to gossip about their friends?",
              "Who is most likely to loan money from a bank rather than their friends?",
              "Who is most likely to take their friends out for lunch and cover everyone’s tab?",
              "Who is most likely to take selfies with everyone else’s phone but theirs?",
              "Who is most likely to work in the same place as their closest friend?",
              "Who is most likely to get a house with their best friend?",
              "Who is most likely to have a nickname for their best friend?",
              "Who is most likely to send their best friend a cake on their birthday?",
              "Who is most likely to wear matching clothes with a best friend?",
              "Who is most likely to wear their friend’s clothes?",
              "Who is most likely to have never been part of a clique?",
              "Who is most likely to be the third wheel in a clique?",
              "Who is most likely to have a friendship bracelet with their best friend?",
              "Who is most likely to keep secrets from their friends?",
              "Who is most likely to lie to their friends the most?",
              "Who is most likely let their best friend read their journal?",
              "Who is most likely to share an Instagram page with their best friend?",
              "Who is most likely to go shopping with their friends rather than alone?",
              "Who is most likely to help their best friend win a competition without being asked?",
              "Who is most likely to wear sneakers to a formal event?",
              "Who is most likely to be overdressed to a party?",
              "Who is most likely to head out without wearing underwear?",
              "Who is most likely to wear makeup to sleep?",
              "Who is most likely to own more wigs than they can wear?",
              "Who is most likely to dye their hair pink?",
              "Who is most likely to repeat the same outfit thrice a week?",
              "Who is most likely to appreciate tickets to see a sports game?",
              "Who is most likely to wear heels every day of the week?",
              "Who is most likely to wear leather boots to dinner?",
              "Who is most likely to wear shades in a room?",
              "Who is most likely to have the greatest number of clothes they’ve never worn?",
              "Who is most likely to have the hardest time finding a shoe that fits?",
              "Who is most likely to go broke from shopping?",
              "Who is most likely to shop only at thrift stores?",
              "Who is most likely to shop at Forever 21?",
              "Who is most likely to own a fashion blog?",
              "Who is most likely to own the least jewelry?",
              "Who is most likely to have the best fashion sense?",
              "Who is most likely to own more shorts than trousers?",
              "Who is most likely to wear their hair in braids all their life if they could?",
              "Who is most likely to own mostly hand-me-downs from siblings?",
              "Who is most likely to own the most knock-offs?",
              "Who is most likely to own the highest number of black outfits?",
              "Who is most likely to be a supermodel?",
              "Who is most likely to be never seen without a tie?",
              "Who is most likely to fit into the fashion of the 80’s better than today’s fashion?",
              "Who is most likely to have the worst fashion sense?",
              "Who is most likely to wear any color but white on their wedding day?",
              "Who is most likely to raid other people’s wardrobes?",
              "Who is most likely to own the most lingerie?",
              "Who is most likely to own the greatest number of berets?",
              "Who is most likely to wear sneakers on a suit?",
              "Who is most likely to go to a fashion show?",
              "Who is most likely to shop from Fashion Nova?",
              "Who is most likely to get married in an art gallery if they could?",
              "Who is most likely to game all night?",
              "Who is most likely to enjoy car racing?",
              "Who is most likely to go fishing?",
              "Who is most likely to go clubbing on a weekday?",
              "Who is most likely to pay for the drinks of everyone at a bar?",
              "Who is most likely to read a new book every month?",
              "Who is most likely to spend the highest number of hours on Instagram?",
              "Who is most likely to read comic books even when they’re 50?",
              "Who is most likely to own a podcast?",
              "Who is most likely to be the best photographer?",
              "Who is most likely to watch cartoons still?",
              "Who is most likely to have more video games than they could need?",
              "Who is most likely to spend their day watching YouTube videos?",
              "Who is most likely to party all summer?",
              "Who is most likely to join a circus?",
              "Who is most likely to get addicted to gambling?",
              "Who is most likely to go golfing?",
              "Who is most likely only to watch 3D movies?",
              "Who is most likely to host the best party?",
              "Who is most likely to go on the most vacations?",
              "Who is most likely to enjoy joining a book-club?",
              "Who is most likely to have visited Disneyland the most?",
              "Who is most likely to jump off a cliff and into a river?",
              "Who is most likely to become a social media influencer?",
              "Who is most likely to go on a ski trip?",
              "Who is most likely to work as a clown?",
              "Who is most likely to vlog a trip just for the fun of it?",
              "Who is most likely to get drunk and pass out at a party?",
              "Who is most likely to go bowling on a Friday night?",
              "Who is most likely to go swimming when it’s raining?",
              "Who is most likely to stream movies rather than go to the cinema?",
              "Who is most likely to refuse to get into the water at the beach?",
              "Who is most likely to go sky-diving?",
              "Who is most likely to have eaten raw meat before?",
              "Who is most likely to eat snot still?",
              "Who is most likely to have the stinkiest fart?",
              "Who is most likely to be the dirtiest?",
              "Who is most likely to be wearing dirty underwear?",
              "Who is most likely to have bushy armpits currently?",
              "Who is most likely to taste their own vomit?",
              "Who is most likely to scratch their genitals in public?",
              "Who is most likely to chew on their fingernails?",
              "Who is most likely to have forgotten to brush?",
              "Who is most likely to poop their pants?",
              "Who is most likely to have dandruff?",
              "Who is most likely to have eaten stale food?",
              "Who is most likely to smell their own poop?",
              "Who is most likely to lick a toilet seat?",
              "Who is most likely to poop without flushing?",
              "Who is most likely to sniff their dog’s butt?",
              "Who is most likely to go a month without bathing?",
              "Who is most likely to have rashes on their butt?",
              "Who is most likely to have a rat living in their house?",
              "Who is most likely to have eaten a cockroach before?",
              "Who is most likely to pee all over a toilet seat?",
              "Who is most likely to have swallowed a worm before?",
              "Who is most likely to blend and drink raw eggs?",
              "Who is most likely to have had a boil on their genital before?",
              "Who is most likely to have had diarrhea the most?",
              "Who is most likely to sweat the most?",
              "Who is most likely to have had sores on their gum before?",
              "Who is most likely to drink dirty water when thirsty?",
              "Who is most likely to spit into the food of someone they don’t like?
              "Who is most likely to have the weirdest fetish?",
              "Who is most likely to have chewed a bug before?",
              "Who is most likely to use someone else’s toothbrush without permission?",
              "Who is most likely to own a spa?",
              "Who is most likely to be on a reality Tv show?",
              "Who is most likely to go under the knife to the perfect body?",
              "Who is most likely to have a VIP pass to an exclusive event?",
              "Who is most likely to buy a house first?",
              "Who is most likely to be egoïstic?",
              "Who is most likely to marry a celebrity?",
              "Who is most likely to start a relationship because of the car their partner drives?",
              "Who is most likely to buy a Lamborghini?",
              "Who is most likely to be listed on Forbes?",
              "Who is most likely to have traveled to most countries?",
              "Who is most likely to buy the most houses?",
              "Who is most likely to have a personal chef?",
              "Who is most likely to be a brand influencer?",
              "Who is most likely to spend an extravagant sum of money on skincare products?",
              "Who is most likely to be a philanthropist?",
              "Who is most likely to own the most designers?",
              "Who is most likely to buy a Yacht?",
              "Who is most likely to know the most celebrities?",
              "Who is most likely to get a Botox job?",
              "Who is most likely to get a personal stylist?",
              "Who is most likely to own a beach house?",
              "Who is most likely to marry for money?",
              "Who is most likely to have the most expensive wedding?",
              "Who is most likely to go shopping every day?",
              "Who is most likely to visit the bank every day?",
              "Who is most likely never to become a vegetarian?",
              "Who is most likely always to have a stash of junk in their possession?",
              "Who is most likely to eat out rather than cook?",
              "Who is most likely to pick fruit smoothies over soda?",
              "Who is most likely to drink a full pack of coke in a day?",
              "Who is most likely to go on a diet?",
              "Who is most likely to be a cocktail master?",
              "Who is most likely to own a bar someday?",
              "Who is most likely to be the biggest foodie?",
              "Who is most likely to host a barbecue party?",
              "Who is most likely to eat their birthday cake alone?",
              "Who is most likely to eat at a diner instead of a 5-star restaurant?",
              "Who is most likely to hate spicy food?",
              "Who is most likely to become a chef?",
              "Who is most likely to eat carbs every single day?",
              "Who is most likely to eat desserts after every meal?",
              "Who is most likely to own a YouTube food channel?",
              "Who is most likely to own a cookbook?",
              "Who is most likely to bake more than fry?",
              "Who is most likely to cook salty meals?",
              "Who is most likely to have to take out a tooth because of all their sugar consumption?",
              "Who is most likely to attend a wine-tasting event?",
              "Who is most likely to win a pizza-eating contest?",
              "Who is most likely to consume black coffee every day?",
              "Who is most likely to own a restaurant?",
              "Who is most likely to choose traveling by road than by air?",
              "Who is most likely to sleep all through a journey?",
              "Who is most likely to have motion sickness?",
              "Who is most likely not to eat when traveling?",
              "Who is most likely to travel to a war-stricken country?",
              "Who is most likely to travel to the countryside?",
              "Who is most likely to go on a vacation to an Island?",
              "Who is most likely to be a travel blogger?",
              "Who is most likely to visit the North Pole?",
              "Who is most likely to visit all the countries in Africa?",
              "Who has most likely never traveled out of the country before?",
              "Who is most likely to get everyone they know souvenirs when they travel?",
              "Who is most likely to fly on a First-class ticket?",
              "Who is most likely to travel to a desert?",
              "Who is most likely to travel just to try out new cuisines?",
              "Who is most likely to travel only during the holidays?",
              "Who is most likely not to have an international passport?",
              "Who is most likely to visit Paris more than once?",
              "Who is most likely to hate flying?",
              "Who is most likely to move to Hawaii?",
              "Who is most likely to travel without taking a single picture?",
              "Who is most likely to camp outside rather than in a cabin?",
              "Who is most likely to go on a road trip every month if they could?",
              "Who is most likely to keep a baby lion as a pet?",
              "Who is most likely to be allergic to pets?",
              "Who is most likely to be scared of all animals?",
              "Who is most likely to buy more food for their pet than their self?",
              "Who is most likely to “babysit” pets?",
              "Who is most likely to go shopping for jewelry for their pet?",
              "Who is most likely to be a veterinarian?",
              "Who is most likely to own a golden fish?",
              "Who is most likely to keep butterflies as pets?",
              "Who is most likely to have more pets than kids?",
              "Who is most likely to dress up their pet?",
              "Who is most likely to cuddle and fall asleep with their pet?",
              "Who is most likely to lose their pet in a crowded place?",
              "Who is most likely to keep their pets outside at night?",
              "Who is most likely to name their pet something really cheesy?",
              "Who is most likely to find stray animals?",
              "Who is most likely to sneak pets into buildings?",
              "Who is most likely to take their pets for walks every evening without fail?",
              "Who is most likely to laugh at serious moments?",
              "Who is most likely to win a Nobel Prize award?",
              "Who is most likely to cry over little things?",
              "Who is most likely to become a minimalist?",
              "Who is most likely to be recognized by Guinness World Record?",
              "Who is most likely to become famous?",
              "Who is most likely to get a tattoo?",
              "Who is most likely to end up in a nursing home?",
              "Who is most likely to get pregnant and not even know?",
              "Who is most likely to get a Ph.D.?",
              "Who is most likely to live with their parents for the longest?",
              "Who is most likely to run for a political office?",
              "Who is most likely to move into a van?",
              "Who is most likely to work out daily?",
              "Who is most likely to be a single mom/dad?",
              "Who is most likely to dedicate the rest of their life to charity?",
              "Who is most likely to meet the Queen of England?",
              "Who is most likely to have the most scars?",
              "Who is most likely to be sexist?",
              "Who is most likely to have a child out of wedlock?",
              "Who is most likely to never get along with their family?",
              "Who is most likely to join the Army?",
              "Who is most likely to be the most popular in a new school?",
              "Who is most likely to be a snitch?",
              "Who is most likely to be the smartest while in school?",
              "Who is most likely to have the largest and most powerful network of people?",
              "Who is most likely to attempt climbing Mount Everest?",
              "Who is most likely crushing on their boss?",
              "Who is most likely to relocate out of the country first?",
              "Who is most likely to break their Smartphone in weeks?",
              "Who is most likely to be a professional choreographer?",
              "Who is most likely to have the worst temper?",
              "Who is most likely to forget their own birthday?",
              "Who is most likely never going to need medicated glasses?",
              "Who is most likely to go to acting school?",
              "Who is most likely to betray their best friend?",
              "Who is most likely never to get married?",
              "Who is most likely to adopt a child?",
              "Who is most likely to be a horrible driver?",
              "Who is most likely to change their gender in the nearest future?",
              "Who is most likely never to do a 9-5 job?",
              "Who is most likely to be the first to bust a move at a party?",
              "Who is most likely to be the biggest gossip?"]
              
    return queries


client.run('OTE1NjY0NzA5MDA3NTg1MzQw.Yae5Ng.WrRGqCCYFGC6kTRTm6zNdgkglys')


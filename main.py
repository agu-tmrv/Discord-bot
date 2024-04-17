# IT IS TESTING VERSION OF MY ORIGINAL CODE, ORIGINAL CODE WITH HOSTING SERVICE AND MYSQL SERVICE IS CREATED BY VM IN LINUX. ITS FOR MY OWN EXPERIMENTS.


from dotenv import load_dotenv
import os
import nextcord
from nextcord.ui import View, button
from nextcord.ext import commands
from nextcord import Interaction
import mysql.connector
import asyncio
import random
from datetime import datetime, timedelta
import discord



intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Connect to MySQL database
conn = mysql.connector.connect(host='127.0.0.1',
                               user='Agalar',
                               password='Teymurov_2002',
                               database='LollyBot')
cursor = conn.cursor()

# Telegram error notifier

# Telegram Notfier End.....


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')


testServerId = 1225801997551407104


################################### РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ/НАСТРОЙКИ ПРОФИЛЯ ##########################################
@bot.event
async def on_member_update(before, after):
  if before.nick != after.nick:
    print(
        f"Изменен никнейм пользователя {after.id}: {before.nick} -> {after.nick}"
    )  # Debugging print
    # Check if the user is registered in your database
    cursor.execute("SELECT * FROM players WHERE user_id=%s", (after.id, ))
    existing_user = cursor.fetchone()

    if existing_user:
      # Update the nickname in the database
      cursor.execute("UPDATE players SET username=%s WHERE user_id=%s",
                     (after.nick, after.id))
      conn.commit()
      print(f"Никнейм обновлен в базе данных для пользователя {after.id}"
            )  # Debugging print
    else:
      print(f"Пользователь {after.id} не найден в базе данных"
            )  # Debugging print


@bot.slash_command(guild_ids=[testServerId], description="Команда регистрации")
async def регистрация(interaction: nextcord.Interaction):
  # Check if the command is used in the allowed channel
  if interaction.channel.id != 1225802090723545149:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return

  def check(message):
    return message.author == interaction.user and message.channel == interaction.channel

  cursor.execute("SELECT * FROM players WHERE user_id=%s",
                 (interaction.user.id, ))
  existing_user = cursor.fetchone()
  if existing_user:
    await interaction.response.send_message(
        "Вы уже зарегистрировались. Если вы хотите просмотреть свой профиль, вызовите команду /профиль.",
        ephemeral=True)
    return

  # Automatically set the nickname as the user's Discord display name
  nickname = interaction.user.display_name

  await interaction.response.send_message("Пожалуйста, введите свой ранг:",
                                          ephemeral=True)
  try:
    rank_msg = await bot.wait_for('message', check=check, timeout=60)
    rank = rank_msg.content.strip()

    cursor.execute(
        "INSERT INTO players (user_id, username, user_rank) VALUES (%s, %s, %s)",
        (interaction.user.id, nickname, rank))
    conn.commit()

    await interaction.followup.send("Регистрация прошла успешно!",
                                    ephemeral=True)
  except asyncio.TimeoutError:
    await interaction.response.send_message(
        "Вы слишком долго отвечали. Регистрация отменена.", ephemeral=True)


@bot.slash_command(guild_ids=[testServerId], description="Ваша информация")
async def профиль(interaction: Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return
  cursor.execute(
      "SELECT username, user_rank, Money, skins_profile_url FROM players WHERE user_id=%s",
      (interaction.user.id, ))
  user_data = cursor.fetchone()
  if user_data:
    username = user_data[0]
    rank = user_data[1]
    money = user_data[2]
    Skin = user_data[3]

    # Create a rich embed with columns
    embed = nextcord.Embed(title="Профиль League of Legends")
    embed.add_field(name="👤 Никнейм", value=username, inline=True)
    embed.add_field(name="🏆 Ранг", value=rank, inline=True)
    embed.add_field(name="🪙 Баланс", value=money, inline=True)

    if (Skin == None):
      embed.set_image(
          url=
          "https://cdn.discordapp.com/attachments/1222597514650321067/1225355592764358737/22.jpg?ex=6620d453&is=660e5f53&hm=d9d997ed5a380f19048a9eedcfba5619e3aa97e6afc26f59fe876064491b1880&"
      )
    else:
      embed.set_image(url=Skin)

    await interaction.send(embed=embed, ephemeral=True)
  else:
    await interaction.send(
        "Вы еще не зарегистрировались. Пожалуйста, используйте команду /регистрация.",
        ephemeral=True)


@bot.slash_command(guild_ids=[testServerId],
                   description="Поделитесь своим профилем с другими!")
async def поделиться_профилем(interaction: Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return
  cursor.execute(
      "SELECT username, user_rank, Money, skins_profile_url FROM players WHERE user_id=%s",
      (interaction.user.id, ))
  user_data = cursor.fetchone()
  if user_data:
    username = user_data[0]
    rank = user_data[1]
    money = user_data[2]
    Skin = user_data[3]

    # Create a rich embed with fields in the same line
    embed = nextcord.Embed(title="Профиль участника")

    # Add fields for nickname, rank, and money in the same line
    embed.add_field(name="👤 Никнейм", value=username, inline=True)
    embed.add_field(name="🏆 Ранг", value=rank, inline=True)
    embed.add_field(name="🪙 Баланс", value=money, inline=True)
    if (Skin == None):
      embed.set_image(
          url=
          "https://cdn.discordapp.com/attachments/1222597514650321067/1225355592764358737/22.jpg?ex=6620d453&is=660e5f53&hm=d9d997ed5a380f19048a9eedcfba5619e3aa97e6afc26f59fe876064491b1880&"
      )
    else:
      embed.set_image(url=Skin)

    await interaction.send(embed=embed)
  else:
    await interaction.send(
        "Вы еще не зарегистрировались. Пожалуйста, используйте команду /регистрация."
    )


@bot.slash_command(guild_ids=[testServerId],
                   description="Изменить ваш профиль")
async def изменить_профиль(interaction: Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return
  # Create a view to handle the buttons
  class ProfileEditView(View):

    def init(self):
      super().init()
      self.timeout = 60  # Timeout in seconds

    @button(label="Изменить Ранг", style=nextcord.ButtonStyle.primary)
    async def изменить_ранг(self, button: nextcord.Button,
                            interaction: nextcord.Interaction):
      await interaction.response.send_message(
          "Пожалуйста, введите ваш новый ранг:", ephemeral=True)
      try:
        rank_msg = await bot.wait_for(
            'message',
            check=lambda m: m.author == interaction.user,
            timeout=self.timeout)
        new_rank = rank_msg.content.strip()

        # Update the rank in the database
        cursor.execute("UPDATE players SET user_rank=%s WHERE user_id=%s",
                       (new_rank, interaction.user.id))
        conn.commit()

        await interaction.send("Ранг успешно обновлен!", ephemeral=True)
      except asyncio.TimeoutError:
        await interaction.send(
            "Вы слишком долго отвечали. Обновление профиля отменено.",
            ephemeral=True)

    @button(label="Изменить Фон", style=nextcord.ButtonStyle.primary)
    async def изменить_фон(self, button: nextcord.Button,
                           interaction: nextcord.Interaction):
      await interaction.response.send_message(
          "Пожалуйста, введите название скина, который вы хотите экипировать:",
          ephemeral=True)
      try:
      
        def check(message):
          return message.author == interaction.user and message.channel == interaction.channel

        skin_name_msg = await bot.wait_for('message', check=check, timeout=60)
        skin_name = skin_name_msg.content.strip()

        # Check if the skin exists in the user's inventory
        cursor.execute(
            "SELECT skin_url FROM inventory WHERE user_id=%s AND skin_name=%s",
            (interaction.user.id, skin_name))
        existing_skin = cursor.fetchone()

        if existing_skin:
          # Consume the previous result before executing the next query
          cursor.fetchall()

          # Update the skins_profile_url in the players table
          cursor.execute("UPDATE players SET skins_profile_url=%s WHERE user_id=%s",(existing_skin[0], interaction.user.id))
          conn.commit()

          await interaction.send("Скин успешно изменен!", ephemeral=True)
        else:
          await interaction.send("У вас нет этого скина в вашем инвентаре.", ephemeral=True)
      except asyncio.TimeoutError:
        await interaction.send(
            "Вы слишком долго отвечали. Отмена смены скина.", ephemeral=True)

    @button(label="Удалить Профиль", style=nextcord.ButtonStyle.danger)
    async def удалить_профиль(self, button: nextcord.Button,
                              interaction: nextcord.Interaction):
      await interaction.response.send_message(
          "Вы уверены, что хотите удалить свой профиль? Это действие не может быть отменено. Если да, пожалуйста, напишите ДА",
          ephemeral=True)

      try:
        confirmation_msg = await bot.wait_for(
            'message',
            check=lambda m: m.author == interaction.user,
            timeout=self.timeout)
        confirmation = confirmation_msg.content.strip().lower()

        if confirmation == 'да':
          # Delete related records from other tables
          cursor.execute("DELETE FROM inventory WHERE user_id=%s",
                         (interaction.user.id, ))
          conn.commit()

          # Delete the user's profile from the main table
          cursor.execute("DELETE FROM players WHERE user_id=%s",
                         (interaction.user.id, ))
          conn.commit()

          await interaction.send("Ваш профиль успешно удален.", ephemeral=True)
        else:
          await interaction.send("Удаление профиля отменено.", ephemeral=True)
      except asyncio.TimeoutError:
        await interaction.send(
            "Вы слишком долго отвечали. Отмена удаления профиля.",
            ephemeral=True)

      # Create the view instance and send it as a response

  view = ProfileEditView()
  await interaction.response.send_message(
      "Выберите опцию для редактирования вашего профиля:",
      view=view,
      ephemeral=True)


################################## ADVENTURE ####################################

COOLDOWN_DURATION = 2 * 60 * 60  # 2 hours in seconds
user_cooldowns = {}


def is_on_cooldown(user_id):
  if user_id in user_cooldowns:
    last_used_time = user_cooldowns[user_id]
    current_time = datetime.utcnow()
    cooldown_remaining = last_used_time + timedelta(
        seconds=COOLDOWN_DURATION) - current_time
    cooldown_hours = round(cooldown_remaining.total_seconds() / 3600)
    if cooldown_hours > 0:
      return cooldown_hours
  return False


@bot.slash_command(guild_ids=[testServerId],
                   description="Отправляйтесь в приключение и найдите деньги!")
@commands.cooldown(1, COOLDOWN_DURATION, commands.BucketType.user)
async def приключение(interaction: nextcord.Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return
  cooldown_hours = is_on_cooldown(interaction.user.id)
  if is_on_cooldown(interaction.user.id):
    await interaction.send(
        f"Вы пока не можете использовать эту команду. Пожалуйста, подождите {cooldown_hours} ч.",
        ephemeral=True)
    return

  found_money = random.randint(20, 40)

  cursor.execute("SELECT Money FROM players WHERE user_id=%s",
                 (interaction.user.id, ))
  user_money = cursor.fetchone()[0]
  updated_money = user_money + found_money
  cursor.execute("UPDATE players SET Money=%s WHERE user_id=%s",
                 (updated_money, interaction.user.id))
  conn.commit()

  user_cooldowns[interaction.user.id] = datetime.utcnow()

  stories = [
      "Вы попали в древний лес ионии, где встретили некого мага по имени Рюкан. Он предложил вам сделку, ты поможешь мне, а я вознагражу тебя, сказал он. Вместе с ним вы защищали древний лес, от атак темных сил. Рюкан вознаградил вас XXX 🪙 и пожелал удачи.",
      "Вы встретились с Райзом на своем пути. Райз носит страшную метку Оскверненного, и предпринимает могучие усилия, чтобы скрыть свои темные секреты. Он передал вам драгоценный мешок и свиток с древней магией. Открыв мешок вы получили XXX 🪙.",
      "В вашем путешествии вы столкнулись с пустыней Шурима, где вам предстоит удивительные архитектурные чудеса и древние пирамиды. В одном из пирамид вы нашли сундук с сокровищами и открыв его, получили XXX 🪙.",
      "Вы пустилась в опасное путешествие, чтобы поклясться верность своим предкам. Вас встретила Седвега, могучий дух джунглей, которая указала вам путь к сокровищам и даровала часть своей силы. На пути вас ждали испытания, но вы с легкостью преодолели все трудности и нашли в глуши леса XXX 🪙.",
      "Ваше путешествие начнется в Фрельйорде, где вы познакомитесь с его холодными тундрами и древними тайнами. Фрельйорде - суровый край, не прощающий ошибок. Люди здесь рождаются воинами, ведь им предстоит бороться за выживание. В одном из этих схваток вы вышли победителем и отправились в новое путешествие, забрав с собой награды в размере XXX 🪙.",
      "Вы отправляетесь в яркий и опасный мир Ионии, где вас ждут встречи с монастырями и мастерами боевых искусств. Вы остались ночевать в глуши леса, построив палатку. На утро вас встретил монах по имени Мизури. Он передал вам припасу на следующее путешествие и XXX 🪙 чтобы вы могли закупиться у местных торговцев.",
      "Ваше путешествие привело вас в захватывающие джунгли, где вы познакомитесь с древними владыками джунглей и их темными тайнами. В джунглях вы нашли кое что необычное, похоже это темная магия которую заточили в маленькой шкатулке. Открыв шкатулку вы вызволили настоящего монстра на земли Ишталя. Вы достали меч и отважно побороли существо и в награду получили таинственный артефакт. Продав его на местном рынке, вы получили XXX 🪙 ",
      "Во время путешествия по землям Рунтерры, вы нашли несколько ценных артефактов исследуя древние руины. Вы встретились с мудрыми волшебниками которые были рады заплатить за эти артефакты, кровными XXX 🪙 . Получив награду, вы отправились в новые неизведанные путешествия",
      """Волшебные леса, величественные горы, глубокие подземелья - каждый уголок Рунтерры ожидает вашего открытия. Прогулявшись немного по неизведанным землям, вы наткнулись на сундук с золотом. Открыв сундук вы нашли сокровища в размере XXX 🪙 . 
        -Отлично, - сказали вы
        -Этого хватит, чтобы купить у торговца немного еды!
        Положив награду в рюкзак, вы направились дальше изучать таинственный и полный опасностей земли.""",
      """На пути к совершенству и к адаптации неизведанного, вы стали проводить время со старинными лесными духами. Одному из лесных духов не нравилась компания со смертным чужеземцем и поэтому по среди ночи он заточил вас в круг окутанной сильной магией. Казалось бы, выбраться из нее невозможно, но дух хотел поиграться. 

        Дух: Чужеземец.... У меня есть для тебя загадка, отгадаешь ее, получишь благословение и помощь в путешествии. Но... если не отгадаешь.... останешься в заточении на века!

        Вы в отчаянии не знаете как поступить в данной ситуации, от злости вы начинаете ломится сквозь магию, но она недоступна для простого смертного. 
        Дух наблюдая за этим смеется над вами. 
        Находясь в заточении уже как 2 дня, вы впадаете в полное отчаяние, но вдруг вы замечаете в рунах в которых вас заточили несостыковку. Соединив правильно все руны вы освобождаетесь с заточения и получаете от Духа благословление в размере XXX 🪙 """,
      """Ваше путешествие по землям Рунтерры стало для вас источником вдохновения, удивления и непреходящих впечатлений. Вы даже не заметили как далеко вы зашли и поднявшись на высокую гору, с выступа вы видите армию трифарианского легиона.
        "Этим элитным подразделением ноксианской армии командует сам Дариус. Солдаты легиона – не просто самые лучшие, закаленные в сражениях бойцы; в него попадают лишь те воины, которые доказали свою абсолютную преданность империи и ее лидерам. На нагрудной пластине их тяжелых практичных доспехов часто можно увидеть тройной оттиск: это символ Трифарикса, трех принципов силы, давших название правящему совету Верховного полководца Свейна."
        Вы решили что с этими ребятами лучше не связываться и забрав свои XXX 🪙 пошли дальше в противоположном направлении.""",
      "Сегодня вы очень сильно устали и прошлись по тропинке которая ведет в ворота Ионии. Там вы познакомились с торговцами и мудрецами, которые поделились с вами знаниями и секретами этого загадочного мира взамен на накопленные ресурсы. Получив заслуженные знания и XXX 🪙 вы остались отдыхать в городе.",
      """Вы с головой погрузились в сказочную атмосферу и участвовали в уникальных ритуалах и обрядах, чтобы понять глубинные традиции и обычаи этого удивительного места. В один из обрядов вы почувствовали, что за вами следят. Оглянувшись по сторонам, вы не увидели ничего подозрительного, но поганое чувство не покидало вас. Закончив обряд, вы заметили в далеке, за колоннами, светящиеся красные глаза, которые призывали вас к себе. Вы прошли вперед и увидели Темного Эльфа, который стоял неподвижно и голосом звал к себе. Подойдя поближе, вы ощутили холод по всему телу, но не испугались и подошли максимально близко.

        "Этот Эльф прекрасен," - сказали вы.

        Эльф превратился в прах, и из кучки праха вы достали мешок с XXX 🪙 . Желание узнать еще больше про это существо не покидало вас, и вы побежали дальше...""",
      """Вы путешествуете в лесу и исследуете древние руины. На пути вы встретили беззащитную женщину, которую окружила стая волков. Она кричала во весь голос: 
        -Помогите!!!! Кто-нибудь!!!! 
        Вы,достав свое оружие, побежали в сторону женщины и отогнали всех волков. Загадочная женщина сказала вам спасибо и передала свиток с заклинанием. Вы прочитали заклинание и получили XXX 🪙 . Вы хотели предложить еще помощи Женщине и проводить ее домой, потому что, в этих землях было очень опасно. Но, обернувшись, вы увидели, что она пропала и как будто бы ее даже и не было. Вам стало интересно и вы прошлись дальше....""",
      "Рунтерра - это мир, наполненный магией, загадками и таинственностью, в котором каждый уголок природы скрывает свои секреты. Исследуйте древние руины, боритесь с монстрами и встречайтесь с мудрыми волшебниками во время вашего путешествия по землям Рунтерры, чтобы получать XXX 🪙 за свои заслуги."
  ]
  story = random.choice(stories)
  story_with_money = story.replace("XXX", str(found_money))

  embed = nextcord.Embed(description=story_with_money)
  if (story == stories[0]):
    embed.set_image(
        url=
        "https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt398f6e453afbae29/60ee0e1191d9e12c4837c16f/ionia-life-as-one.jpg"
    )
    await interaction.send(embed=embed)
  elif (story == stories[1]):
    embed.set_image(
        url=
        "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/f/f6/FROM_THE_ASHES_1.jpg/revision/latest?cb=20180726193620"
    )
    await interaction.send(embed=embed)
  elif (story == stories[2]):
    embed.set_image(
        url=
        "https://images.contentstack.io/v3/assets/blt187521ff0727be24/bltbb26c701fd6aeeb5/60ee11f560216d1db87a125b/shurima-risen.jpg"
    )
    await interaction.send(embed=embed)
  elif (story == stories[3]):
    embed.set_image(
        url=
        "https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt1fb032fa736e5c23/60ee0e21855e1f64f143ef78/ionia-the-placidium-of-navori.jpg"
    )
    await interaction.send(embed=embed)
  elif (story == stories[4]):
    embed.set_image(
        url=
        "https://images.contentstack.io/v3/assets/blt187521ff0727be24/blte7bf77c65337ecd2/60ee0d9842236548511f8b46/raiders-and-reavers.jpg"
    )
    await interaction.send(embed=embed)
  elif (story == stories[5]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225168709572759623/ionia_architecture_06.png?ex=66202646&is=660db146&hm=6eabdc36f912954c51d3db7e8ef06ce51d2af4021bfdb1c90adc96ac3ad84570&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[6]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225169930824061019/ixtal-secrets-01.png?ex=6620276a&is=660db26a&hm=b60ec4c6bcdbaba7db7bedc3eb89e04b7649743b5be278d74ec4cd00955db1d7&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[7]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225171492854304919/yordle_portal_03.png?ex=662028de&is=660db3de&hm=1e2419b284b385ad74e2062b951e7cd41dde3f52f976fa3e05e39f402d1892ff&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[8]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225173605969559683/mttargon-ancient-thresholds.png?ex=66202ad6&is=660db5d6&hm=5fde104ed43233e34f464fa9e2178e9887bbf7dcabdf34bec8e20c69685eddb9&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[9]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225176064985272411/void-the-touch-of-the-void.png?ex=66202d20&is=660db820&hm=e438b004c55529dd59be9322170240698b34b1c6a6f23962778fb92c35f61d4b&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[10]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225179565312311347/noxus-bastion.png?ex=66203063&is=660dbb63&hm=0fcd3ca13e9e6adaf6896429577689e12f558282f19f5ce884f217f38e3bf5e5&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[11]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225180617617051840/ionia-the-great-monasteries.png?ex=6620315d&is=660dbc5d&hm=c7b2c77b1b8a60f9f8ee5fff1e2de7069768077df56d762354b90593438e76a1&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[12]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225183402676846716/shadow-isles-celestialvault.png?ex=662033f6&is=660dbef6&hm=ee674d4b985fa1f29e72e5d35a85723d9ec345609bdb98883f93784eca4c6cb3&png?ex=6620315d&is=660dbc5d&hm=c7b2c77b1b8a60f9f8ee5fff1e2de7069768077df56d762354b90593438e76a1&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[13]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225186835324473465/ionia-an-ancient-and-respected-history.png?ex=66203728&is=660dc228&hm=da624f7a9f6d873a7616c05ba784a19005f214d55a3be1b5157786fb9ad1ab3a&"
    )
    await interaction.send(embed=embed)
  elif (story == stories[14]):
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225187493347856434/main-scaled.png?ex=662037c5&is=660dc2c5&hm=46103cdd91a1a0dc1139d8501c6f57d65108ad025064dfc91f98df487180a700&"
    )
    await interaction.send(embed=embed)


################################################### ТОПЫ СЕРВЕРА ##################################################################


@bot.slash_command(guild_ids=[testServerId], description="Показать таблицу лидеров")
async def топы_сервера(interaction: Interaction):
    if interaction.channel.id != 1225801997551407108:
        await interaction.response.send_message(
            "Эта команда доступна только в определенном канале.", ephemeral=True)
        return

    cursor.execute("SELECT username, Money FROM players ORDER BY Money DESC LIMIT 10")  # Fetch only top 10 players
    leaderboard_data = cursor.fetchall()

    if leaderboard_data:
        max_username_length = max(len(data[0]) for data in leaderboard_data)
        max_money_length = max(len(str(data[1])) for data in leaderboard_data)

        embed = nextcord.Embed(
            title="Топ 10 игроков",
            description="Отсортировано по количеству денег"
        )

        for index, (username, money) in enumerate(leaderboard_data, start=1):
            username_spaces = ' ' * (max(0, max_username_length - len(username) + 2))
            profile_text = f"#{index} {username}{username_spaces} {money} 🪙"
            framed_profile = f"```\n{profile_text}\n```"
            embed.add_field(name="\u200b", value=framed_profile, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("Таблица лидеров пуста.", ephemeral=True)




############################################# Магазин-ФОНЫ ##################################################

admin_user_ids = [680446421165670404, 344100686092435458, 424161206903898121
                  ]  # Add the user IDs of your admin users here


@bot.slash_command(
    guild_ids=[testServerId],
    description="Административная команда для добавления товаров в магазин")
async def админ_магазин_фоны(interaction: Interaction):
  if interaction.user.id not in admin_user_ids:
    await interaction.send("У вас нет прав на использование этой команды.",
                           ephemeral=True)
    return

  await interaction.send(
      "Пожалуйста, укажите детали товара, который вы хотите добавить в магазин.",
      ephemeral=True)
  try:

    def check(message):
      return message.author == interaction.user and message.channel == interaction.channel

    await interaction.send("Введите название скина:", ephemeral=True)
    skin_name_msg = await bot.wait_for('message', check=check, timeout=60)
    skin_name = skin_name_msg.content.strip()

    await interaction.send("Введите URL скина:", ephemeral=True)
    skin_url_msg = await bot.wait_for('message', check=check, timeout=60)
    skin_url = skin_url_msg.content.strip()

    await interaction.send("Введите цену скина:", ephemeral=True)
    price_msg = await bot.wait_for('message', check=check, timeout=60)
    price = int(price_msg.content.strip())

    cursor.execute(
        "INSERT INTO shop_items (skin_name, skin_url, price) VALUES (%s, %s, %s)",
        (skin_name, skin_url, price))
    conn.commit()

    await interaction.send("Товар успешно добавлен в магазин!", ephemeral=True)
  except asyncio.TimeoutError:
    await interaction.send(
        "Вы слишком долго отвечали. Добавление товара отменено.",
        ephemeral=True)


@bot.slash_command(guild_ids=[testServerId],
                   description="Просмотр товаров в магазине")
async def магазин_фонов(interaction: nextcord.Interaction):
  if interaction.channel.id != 1225802277390913656:
    await interaction.response.send_message(
        "Эта команда доступна только в определенном канале.", ephemeral=True)
    return
  cursor.execute("SELECT id, skin_name, skin_url, price FROM shop_items")
  shop_items = cursor.fetchall()

  if shop_items:
    embed = nextcord.Embed(title="Товары магазина")
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1222597514650321067/1225775022782808085/image.png?ex=66225af3&is=660fe5f3&hm=54118deeb6f5e87379b7b2898eeb412e89d376a1e9a330637436b1c23a12895f&"
    )
    for item in shop_items:
      embed.add_field(
          name=" ",
          value=
          f"[{item[1]}]({item[2]}) \n{item[3]} :coin: ",
          inline=True)

    await interaction.send(embed=embed)
  else:
    await interaction.send("Магазин пока что пуст.")


@bot.slash_command(guild_ids=[testServerId],
                   description="Покупка скина из магазина")
async def купить_фон(interaction: Interaction, купить_товар: str):
  if interaction.channel.id != 1225802277390913656:
    await interaction.send(
        "Эту команду можно использовать только в определенном канале.",
        ephemeral=True)
    return
  cursor.execute(
      "SELECT skin_name, skin_url, price FROM shop_items WHERE skin_name = %s",
      (купить_товар, ))
  item_info = cursor.fetchone()

  if item_info:
    skin_name, skin_url, price = item_info
    cursor.execute("SELECT Money FROM players WHERE user_id = %s",
                   (interaction.user.id, ))
    user_money = cursor.fetchone()[0]

    if user_money >= price:
      # Вычитаем цену из денег пользователя
      updated_money = user_money - price
      cursor.execute("UPDATE players SET Money = %s WHERE user_id = %s",
                     (updated_money, interaction.user.id))

      # Добавляем купленный скин в инвентарь пользователя
      cursor.execute(
          "INSERT INTO inventory (user_id, skin_name, skin_url) VALUES (%s, %s, %s)",
          (interaction.user.id, купить_товар, skin_url))
      conn.commit()

      await interaction.send(f"Вы купили {купить_товар} за {price} монет!",
                             ephemeral=True)
    else:
      await interaction.send(
          "У вас недостаточно денег для покупки этого скина.", ephemeral=True)
  else:
    await interaction.send("Запрашиваемый товар недоступен в магазине.",
                           ephemeral=True)


######################################## Магазин-СКИНЫ ##########################################
@bot.slash_command(guild_ids=[testServerId], description="Показать доступные скины и их цены")
async def магазин_скинов(interaction: Interaction):
    if interaction.channel.id != 1225802277390913656:
        await interaction.response.send_message(
            "Эта команда доступна только в определенном канале.", ephemeral=True)
        return

    # Fetch data from the shop_skins table
    cursor.execute("SELECT name, price FROM shop_skins")
    skins_data = cursor.fetchall()

    if skins_data:
        # Create an embed to display the skins and prices
        embed = nextcord.Embed(title="Магазин скинов", description="Доступные скины и их цены:")
        
        # Add each skin and its price to the embed
        for skin in skins_data:
            name, price = skin
            embed.add_field(name=name, value=f"Цена: {price} :coin:", inline=False)
            embed.set_image('https://cdn.discordapp.com/attachments/1222597514650321067/1225775600283815986/image.png?ex=662b95fc&is=661920fc&hm=7d994a46308052f6291f9fcbae6f07734cfacba670d231afee0771c2b14f0357&')
        await interaction.send(embed=embed, ephemeral=True)
    else:
        await interaction.send("В магазине нет доступных скинов.", ephemeral=True)

        

@bot.slash_command(guild_ids=[testServerId], description="Купить скин из магазина")
async def купить_скин(interaction: Interaction, skin_name: str = None):
    if interaction.channel.id != 1225802277390913656:
        await interaction.response.send_message(
            "Эта команда доступна только в определенном канале.", ephemeral=True)
        return

    if skin_name is None:
        await interaction.response.send_message(
            "Пожалуйста, укажите название скина, который вы хотите купить.", ephemeral=True)
        return

    user_id = interaction.user.id

    # Fetch the skin's ID and price from the shop_skins table
    cursor.execute("SELECT id, price FROM shop_skins WHERE name=%s", (skin_name,))
    skin_data = cursor.fetchone()

    if skin_data:
        skin_id, skin_price = skin_data

        # Check the user's balance before proceeding with the purchase
        cursor.execute("SELECT Money FROM players WHERE user_id=%s", (user_id,))
        user_money = cursor.fetchone()[0]

        if user_money >= skin_price:
            # Deduct the price from the user's balance
            new_balance = user_money - skin_price
            cursor.execute("UPDATE players SET Money=%s WHERE user_id=%s", (new_balance, user_id))

            # Add the purchased skin to the inventory_skins table
            cursor.execute("INSERT INTO inventory_skins (user_id, skin_id) VALUES (%s, %s)", (user_id, skin_id))

            conn.commit()

            await interaction.response.send_message(
                f"Вы успешно купили скин '{skin_name}' за {skin_price} монет.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "У вас недостаточно монет для покупки этого скина.", ephemeral=True
            )
    else:
        await interaction.response.send_message(
            f"Скин с названием '{skin_name}' не найден в магазине.", ephemeral=True)




########### ПОЖЕРТВОВАНИЕ
@bot.slash_command(guild_ids=[testServerId],
                   description="Покупка денег посредством пожертвования")
async def купить_монеты(interaction: Interaction):
  if interaction.channel.id != 1225802277390913656:
    await interaction.send(
        "Эту команду можно использовать только в определенном канале.",
        ephemeral=True)
    return
  # Создаем встроенный объект с кликабельным URL
  embed = nextcord.Embed(title="Пожертвовать для покупки денег")
  embed.description = """Нажмите [здесь](https://boosty.to/m3evdgwjjn/donate), чтобы пожертвовать и купить деньги.

                        475 рублей - 25.000 🪙

                        850 рублей - 45.000 🪙

                        1400 рублей - 75.000 🪙
                        
                        3250 рублей - 175.000 🪙

                        После того как Вы задонатили нажмите кнопку Проверить пожертвование."""

  # Создаем представление для кнопки
  class ПроверкаПожертвования(View):

    def init(self):
      super().init()
      self.timeout = 60  # Таймаут в секундах

    @button(label="Проверить пожертвование",
            style=nextcord.ButtonStyle.primary)
    async def проверка_пожертвования(self, button: nextcord.Button,
                                     interaction: nextcord.Interaction):
      user_id_to_notify = '344100686092435458'  # Замените на ID пользователя, которого нужно уведомить
      user = await bot.fetch_user(user_id_to_notify)

      # Получаем имя пользователя из базы данных
      cursor.execute("SELECT username FROM players WHERE user_id = %s",
                     (interaction.user.id, ))
      username = cursor.fetchone()[0]

      await user.send(
          f"Было пожертвование игроком: {username}, что бы проверить нажми [здесь](https://boosty.to/app/messages?dialogId=1810655)"
      )

      await interaction.response.send_message(
          "Администрация проверит ваше пожертвование. Если ваши деньги не поступят в течение 1 часа, пожалуйста, свяжитесь с администратором.",
          ephemeral=True)

  # Отправляем встроенный объект с URL и представлением, содержащим кнопку
  await interaction.response.send_message(
      "Нажмите кнопку ниже после пожертвования:",
      embed=embed,
      view=ПроверкаПожертвования(),
      ephemeral=True)


################################################ HELP COMMAND ######################################################


@bot.slash_command(
    guild_ids=[testServerId],
    description="Показать все доступные слеш-команды и их описания")
async def инфо(interaction: Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.send(
        "Эту команду можно использовать только в определенном канале.",
        ephemeral=True)
    return
  # Определяем словарь для хранения названий команд и их описаний
  команды_инфо = {
      '/регистрация': "Зарегистрируйте свой профиль",
      '/профиль': "Показать информацию о вашем профиле",
      '/поделиться_профилем': "Поделиться вашим профилем с другими",
      '/изменить_профиль': "Изменить информацию о вашем профиле",
      '/приключение': "Отправиться в приключение и найти деньги",
      '/топы_сервера': "Показать таблицу лидеров",
      '/админ_магазин_фоны':
      "Административная команда для добавления товаров в магазин",
      '/магазин_фонов': "Просмотр товаров в магазине",
      '/магазин_скинов': "Просмотр скинов в магазине",
      '/купить_монеты': "Покупка денег посредством пожертвования",
      '/купить_скин': "Покупка скина из магазина",
      '/купить_фон': "Купить скин из магазина",
      '/инфо': "Показать все доступные слеш-команды и их описания",
      '/инвентарь_фонов': "Показать все доступные фоны",
      '/инвентарь_скинов': "Показать все доступные скины",
  }

  # Создаем встроенный объект для отображения информации о командах
  embed = nextcord.Embed(title="Доступные Слеш-Команды")

  for команда, описание in команды_инфо.items():
    embed.add_field(name=команда, value=описание, inline=False)

  await interaction.send(embed=embed, ephemeral=True)


####################################### ИНВЕНТАРЬ #########################################


@bot.slash_command(guild_ids=[testServerId],
                   description="Показать ваш инвентарь")
async def инвентарь_фонов(interaction: Interaction):
  if interaction.channel.id != 1225801997551407108:
    await interaction.send(
        "Эту команду можно использовать только в определенном канале.",
        ephemeral=True)
    return
  # Получаем инвентарь пользователя из базы данных
  cursor.execute(
      "SELECT distinct skin_name, skin_url FROM inventory WHERE user_id = %s",
      (interaction.user.id, ))
  инвентарь_пользователя = cursor.fetchall()

  if инвентарь_пользователя:
    # Создаем встроенный объект для отображения инвентаря
    embed = nextcord.Embed(title="Ваш Инвентарь")

    for item in инвентарь_пользователя:
      embed.add_field(name=item[0],
                      value=f"[Посмотреть Скин]({item[1]})",
                      inline=False)

    await interaction.send(embed=embed, ephemeral=True)
  else:
    await interaction.send("Ваш инвентарь пуст.", ephemeral=True)

@bot.slash_command(guild_ids=[testServerId], description="Показать инвентарь купленных скинов")
async def инвентарь_скинов(interaction: Interaction):
    if interaction.channel.id != 1225801997551407108:
        await interaction.response.send_message(
            "Эта команда доступна только в определенном канале.", ephemeral=True)
        return

    user_id = interaction.user.id

    # Fetch skin names from the inventory_skins table for the user
    cursor.execute("SELECT shop_skins.name FROM inventory_skins JOIN shop_skins ON inventory_skins.skin_id = shop_skins.id WHERE inventory_skins.user_id=%s", (user_id,))
    user_skins = cursor.fetchall()

    if user_skins:
        skins_list = "\n\n".join(f"• {skin[0]}" for skin in user_skins)
        embed = discord.Embed(
            title="Ваш инвентарь скинов",
            description=skins_list,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(
            "У вас пока нет купленных скинов.", ephemeral=True)



############################################## АДМИНИСТРАТИВНЫЕ КОМАНДЫ ###################################################


@bot.slash_command(
    guild_ids=[testServerId],
    description="Административная команда для выдачи денег пользователю")
async def выдать_деньги(interaction: Interaction,
                        пользователь: nextcord.Member, сумма: int):
  # Проверяем, является ли пользователь, вызвавший команду, администратором
  if interaction.user.id not in admin_user_ids:
    await interaction.send("У вас нет прав на использование этой команды.",
                           ephemeral=True)
    return

  # Обновляем баланс пользователя в базе данных на указанную сумму
  cursor.execute("SELECT Money FROM players WHERE user_id = %s",
                 (пользователь.id, ))
  текущие_деньги = cursor.fetchone()[0]
  обновленные_деньги = текущие_деньги + сумма
  cursor.execute("UPDATE players SET Money = %s WHERE user_id = %s",
                 (обновленные_деньги, пользователь.id))
  conn.commit()
  embed = nextcord.Embed()
  embed.add_field(
      name=" ",
      value=f"✅ Успешно выдано {сумма} 🪙 для {пользователь.display_name}!")
  await interaction.send(embed=embed)


@bot.slash_command(
    guild_ids=[testServerId],
    description="Административная команда для списания денег у пользователя")
async def снять_деньги(interaction: Interaction, пользователь: nextcord.Member,
                       сумма: int):
  # Проверяем, является ли пользователь, вызвавший команду, администратором
  if interaction.user.id not in admin_user_ids:
    await interaction.send("У вас нет прав на использование этой команды.",
                           ephemeral=True)
    return

  # Обновляем баланс пользователя в базе данных, вычитая указанную сумму
  cursor.execute("SELECT Money FROM players WHERE user_id = %s",
                 (пользователь.id, ))
  текущие_деньги = cursor.fetchone()[0]

  if текущие_деньги >= сумма:
    обновленные_деньги = текущие_деньги - сумма
    cursor.execute("UPDATE players SET Money = %s WHERE user_id = %s",
                   (обновленные_деньги, пользователь.id))
    conn.commit()

    await interaction.send(
        f"Успешно списано {сумма} монет у {пользователь.display_name}.")
  else:
    await interaction.send(
        f"{пользователь.display_name} не имеет достаточно монет для списания.",
        ephemeral=True)


@bot.slash_command(
    guild_ids=[testServerId],
    description=
    "Административная команда для просмотра профиля пользователя по Discord")
async def админ_профиль(interaction: Interaction,
                        пользователь: nextcord.Member):
  # Проверяем, является ли пользователь, вызвавший команду, администратором
  if interaction.user.id not in admin_user_ids:
    await interaction.send("У вас нет прав на использование этой команды.",
                           ephemeral=True)
    return

  cursor.execute(
      "SELECT username, user_rank, Money, skins_profile_url FROM players WHERE user_id=%s",
      (пользователь.id, ))
  данные_пользователя = cursor.fetchone()
  if данные_пользователя:
    username = данные_пользователя[0]
    rank = данные_пользователя[1]
    money = данные_пользователя[2]
    Skin = данные_пользователя[3]

    # Создаем встроенный объект для отображения профиля пользователя
    embed = nextcord.Embed(title="Профиль League of Legends")
    embed.add_field(name="👤 Никнейм", value=username, inline=True)
    embed.add_field(name="🏆 Ранг", value=rank, inline=True)
    embed.add_field(name="🪙 Баланс", value=money, inline=True)
    if (Skin == None):
      embed.set_image(
          url=
          "https://cdn.discordapp.com/attachments/1222597514650321067/1225355592764358737/22.jpg?ex=6620d453&is=660e5f53&hm=d9d997ed5a380f19048a9eedcfba5619e3aa97e6afc26f59fe876064491b1880&"
      )
    else:
      embed.set_image(url=Skin)

    await interaction.send(embed=embed, ephemeral=True)
  else:
    await interaction.send("Профиль пользователя не найден.", ephemeral=True)

@bot.slash_command(guild_ids=[testServerId], description="Административное удаление скина из инвентаря")
async def админ_удалить_скин(interaction: Interaction, username: str = None, skin_name: str = None):
    if interaction.user.id not in admin_user_ids:
        await interaction.response.send_message(
            "У вас нет прав для выполнения этой команды.", ephemeral=True)
        return

    if not username:
        await interaction.response.send_message(
            "Пожалуйста, укажите имя пользователя, чей скин нужно удалить.", ephemeral=True)
        return

    if not skin_name:
        await interaction.response.send_message(
            "Пожалуйста, укажите название скина, который нужно удалить из инвентаря.", ephemeral=True)
        return

    # Fetch user's ID based on the username
    cursor.execute("SELECT user_id FROM players WHERE username=%s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        user_id = user_data[0]

        # Fetch skin's ID based on the skin name
        cursor.execute("SELECT id FROM shop_skins WHERE name=%s", (skin_name,))
        skin_data = cursor.fetchone()

        if skin_data:
            skin_id = skin_data[0]

            # Delete the skin entry from the user's inventory
            cursor.execute("DELETE FROM inventory_skins WHERE user_id=%s AND skin_id=%s", (user_id, skin_id))
            conn.commit()

            await interaction.response.send_message(
                f"Скин '{skin_name}' успешно удален из инвентаря пользователя '{username}'.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Скин с названием '{skin_name}' не найден в магазине.", ephemeral=True
            )
    else:
        await interaction.response.send_message(
            f"Пользователь с именем '{username}' не найден.", ephemeral=True
        )



############################################# Tech Admin ################################################


load_dotenv()

bot.run(os.getenv("DISCORD_TOKEN")) 


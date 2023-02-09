try:
    import json, os, platform, time, discord, datetime, time, uuid, asyncio, string, random
    import requests
    from datetime import datetime

    from discord import ui
except Exception:
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")
    time.sleep(3)
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")
    print("Pycord not found - Installing...\n")
    os.system("pip install py-cord==2.0.0b4")
    os._exit(0)

client = discord.Bot()




@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"Bot developer id: {client.user.id}")
    print(f"Using guild: {client.guilds[0].name}")
    await client.change_presence(activity=discord.Game(name="Devloper of this bot | $name#1000"))


@client.slash_command(name="help", description="List of commands")
async def help(ctx):
    embed = discord.Embed(title="Commands", description = "list of commands", color=0x3498db)
    embed.add_field(name="**commands**", value=":white_circle: lock \n:white_circle: unlock \n:white_circle: ban\n:white_circle: genkey\n:white_circle: redeem key\n:white_circle: kick\n:white_circle: change nickname\n:white_circle: reset nickname")
    await ctx.respond(embed=embed)

@client.slash_command(name="clear", description="Clean amount of chat/channel")
async def clear(ctx, limit: int):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.channel.purge(limit=limit)
            await ctx.respond(f'channel has been cleard by {ctx.author.mention}')
            await ctx.message.delete()
        else:
             embed = discord.Embed(title="**Failed to kick user!**", description=f"❌ Sorry! {ctx.author.mention}, you don't have permissions to execute this command!", color=0xe74c3c)
             await ctx.respond(embed=embed)

@client.slash_command(name="kick", description="Kick members from the server")
async def kick(ctx, member: discord.Member, *, reason="reason not provided"):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed = discord.Embed(title="**Successfully kicked**", description=f"{member} | {member.id} has been kicked from the server!\nreason of this kick:  {reason}\nkicked by: {ctx.author.mention}", color=0x2ecc71)
            await ctx.respond(embed=embed)
        else:
             embed = discord.Embed(title="**Failed to kick user!**", description=f"❌ Sorry! {ctx.author.mention}, you don't have permissions to execute this command!", color=0xe74c3c)
             await ctx.respond(embed=embed)

@client.slash_command(name="ban", description="Ban members from the server")
async def ban(ctx, member: discord.Member, *, reason="reason not provided"):
     if ctx.author.guild_permissions.ban_members:
          await member.ban(reason=reason)
          embed = discord.Embed(title="**Successfully banned**", description=f"{member} | {member.id} has been banned from the server!\nreason of this ban:  {reason}\nbanned by: {ctx.author.mention}", color=0x2ecc71)
          await ctx.respond(embed=embed)
     else:
          embed = discord.Embed(title="**Failed to ban user!**", description=f"❌ Sorry! {ctx.author.mention}, you don't have permissions to execute this command!", color=0xe74c3c)
          await ctx.respond(embed=embed)



@client.slash_command(name="cooldown", description="set slowmode for channels")
async def cooldown(ctx, seconds: int):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title="**Successfully setted cooldown**", description=f":heavy_check_mark: setted the slowmode delay in this channel to {seconds} seconds!")
        await ctx.respond(embed=embed)
    else:
         embed = discord.Embed(title="**Failed to set cooldown**", description=f"❌ Sorry! {ctx.author.mention}, you don't have permissions to execute this command!", color=0xe74c3c)
         await ctx.respond(embed=embed)

@client.slash_command(name="lock", description="Locked text channels")
async def lock(ctx, channel : discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_channels:
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title="**Successfully locked**", description=f"Successfully locked channel: {channel.mention}\n requested by:  {ctx.author.mention}", color=0x2ecc71)
        await ctx.respond(embed=embed)
    else:
         embed = discord.Embed(title="**Failed to lock channel !**", description=f"❌ Sorry! {ctx.author.mention}, you don't have permissions to execute this command!", color=0xe74c3c)
         await ctx.respond(embed=embed)

@client.slash_command(name="unban", description="Unban members from the server")
async def unban(ctx, userid):
  user = await client.fetch_user(userid)
  await ctx.guild.unban(user)
  embed = discord.Embed(title="**Successfully unbanned**", description=f"Successfully unbanned user!\nuser id: {user.id}\nuser name: {user.name}\n requested by: {ctx.author.mention}", color=0x2ecc71)
  await ctx.respond(embed=embed)

@client.command(name="chnick", description="Change username nickname")
async def chnick(ctx, member: discord.Member, nick):
    if ctx.author.guild_permissions.manage_channels:
        await member.edit(nick=nick)
        embed = discord.Embed(title="**Successfully changed nickname**", description=f"Changed Nickname to \nMember name: {member}\nMember id: {member.id} \n Requested by {ctx.author.mention}", color=0x2ecc71)
        await ctx.respond(embed=embed)

@client.slash_command(name="deluser", description="delete user from keyauth")
async def deleteuser(ctx , user):
	req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=deluser&user={user}")
	if req.json()["success"] == True:
		await ctx.respond(embed = discord.Embed(title="**Successfully deleted user!**", description=f"Deleted user!\nusername:\n {user}\n deleted requested from {ctx.author.mention}", color=0x2ecc71))
	else:	
            await ctx.respond(embed = discord.Embed(title="**Failed to delete user!**", description=f"Sorry! {ctx.author.mention}, failed to delete this user\nThe user doesnt exist or found!", color=0xe74c3c))
                
@client.slash_command(name="resethwid", description="Reset hardwareid command")
async def resethwid(ctx,user,reason):
	req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=resetuser&user={user}")
	
	if req.json()["success"] == True:
		await ctx.respond(embed=discord.Embed(title="*Successfully reseted user!*",description=f"{ctx.author.mention}, resetted hardware id of {user}{reason}",))
	else:
            await ctx.respond(embed=discord.Embed(title="**Failed to delete this user**", description="sorry! failed to reset this user!\nuser not exist/found!", color=0xe74c3c))


                
@client.slash_command(name="claim", description="claim your license key")
async def claim(ctx,license):

	try:
		password = "".join(random.choice(string.ascii_letters+string.digits) for i in range(9))
		username = "".join(random.choice(string.ascii_letters+string.digits) for i in range(9))
		req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=activate&user={username}&key={license}&pass={password}")
		if req.json()["success"] == True:
			expire = req.text.split('"expiry":"')[1].split('"')[0]
			expire = datetime.utcfromtimestamp(int(expire)).strftime('%Y-%m-%d %H:%M:%S')
			
			await ctx.send(embed=discord.Embed(title="**License Activated**",description=f"{ctx.author.mention}, your key has been redeemed successfully!"))
			embed=discord.Embed(title="**Successfully redeemed license**", description=f"{ctx.author.mention}, thank you for Activated your license key! this is the information\n\nusername: {username}\npassword: {password}\nlicense key: {license}\nexpire in {expire}")
        
			await ctx.author.send(embed=embed)
			
			
            
		else:
			await ctx.send(embed=discord.Embed(title="**Failed to create account**",description=f"license invaild, please enter a vaild license"))
	except Exception as m:
		await ctx.send("Something Went Wrong!, please try again later")
		await ctx.send(m)
                
@client.slash_command(name="genkey", description="generate keys")
async def genkey(ctx,day:int):   
        
	req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=add&expiry={day}&mask=license-XXXXXX-XXXXXX&level=1&amount=1&format=json")
	if req.json()["success"] == True:
		key = req.json()["key"]
		
		embed1=discord.Embed(title="**thank you for Activated your license key**",description=f"your license key: {key}")
		embed = discord.Embed(title="Successfully generated key", description=f"{ctx.author.mention}, check your dms for the license key")
		await ctx.respond(embed=embed)
		await ctx.author.send(embed=embed1)
	else:
		await ctx.respond(embed=discord.Embed(title="**Failed to generate key**", description=f"Sorry! {ctx.author.mention}, failed to generate key"))
			
            

	
			
            

			
	
                




@client.slash_command(name="genkey", description="generate key")
async def genkey(ctx,day:int):
    req = requests.get(f"https://keyauth.win/api/seller/?sellerkey={'8b26f1fb2a208c30adbcb1b7530be145'}&type=add&expiry={day}&mask=LICENSEKEY-XXXXXX-XXXXXX&level=1&amount=1&format=json")
    if req.json()["success"] == True:
        key = req.json()["key"]
        embed1=discord.Embed(title="**Successfully generated key!**",description=f"**this is your license key:** {key}",color=0x2ecc71)
        await ctx.author.send(embed=embed1)
        await ctx.send(f"{ctx.author.mention}, **Successfully generated key!, check your dms!**")
        
       




                




client.run(token)
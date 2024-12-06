import requests
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

# read data form json
with open('SNKRS_dataSharing.json', 'r') as json_file:
    data = json.load(json_file)


product_name = data[list(data.keys())[0]]
link = data[list(data.keys())[1]]
pic_url = data[list(data.keys())[2]]
release_date = data[list(data.keys())[3]]
sku = data[list(data.keys())[4]]
price = data[list(data.keys())[5]]

# arranging message

description = (f"Product Name: {product_name}\nPrice: {price}\nSKU: {sku}\nRelease Date: {release_date}\nPool: SNKRS/NIKE 'YOUR-COUNTRY'\nLink: {link}")

# sending webhook
webhook_url = 'https://discord.com/api/webhooks/945270039144190002/37BX_ykySpS8u0jxYkMmt9Qvnl-ZUftweBjv4-iN6icLQGIKL8TpvHYDzu-fyRDSMcXt'

hook = DiscordWebhook(
    webhook_url,
    username = 'Lemon Proxies Release Details',
    avatar_url = 'https://images-ext-1.discordapp.net/external/SBPPWg7LcXmmsk0vgrtf-Srx3hP9j88HZMJwmRSj5ng/https/pbs.twimg.com/profile_images/1310467741216776192/KmmDcPt2_400x400.jpg'
    )

embed = DiscordEmbed(
    color = 'DBF50C',
)
                    
embed.timestamp = datetime.datetime.utcnow().isoformat()
embed.add_embed_field(name = 'SNKRS Asia Upcoming Release', value = description)
embed.set_footer(text = f'By Elivius')
embed.set_image(url=pic_url)

try:
    hook.add_embed(embed)
    response = hook.execute()
    print(f'Webhook for {product_name} Sent!')
    print('==============================================================================')
                    
except requests.exceptions.HTTPError as errh:
    print('==============================================================================')
    print(f'HTTP Error: {errh}')
    print('Rate limited...')
    print('==============================================================================')

except requests.exceptions.RequestException as err:
    print('==============================================================================')
    print(f'Error: {err}')
    print('Bad connection...')
    print('==============================================================================')
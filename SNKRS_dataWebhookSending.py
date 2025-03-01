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
webhook_url = 'YOUR_WEBHOOK_API'

hook = DiscordWebhook(
    webhook_url,
    username = 'WEBHOOK_USERNAME',
    avatar_url = 'WEBHOOK_AVATAR_IMG_URL'
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

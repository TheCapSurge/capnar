import time
import telegram
import openai
import signal
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from web3 import Web3
import json
import os


chat_wordlimit = 1500
responsetokenlimit = 1024
openai.api_key = os.environ.get("OPENAI_API_KEY")
telegram_token = os.environ.get("TELEGRAM_TOKEN")
bot_name = '@CaptainSurgeAI_bot'

# Replace with your Binance Smart Chain node URL
bsc_node_url = "https://bsc-dataseed.binance.org/"

# Replace with the Captain Surge contract address and ABI
captain_surge_contract_address = "0x2379aA12E3DE1FDDBC47Bb9E8013122F9CBa357c"
captain_surge_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"beans","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dollarBuy","type":"uint256"}],"name":"Bought","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newBuyMul","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newSellMul","type":"uint256"}],"name":"FeesMulChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newMaxBag","type":"uint256"}],"name":"MaxBagChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"beans","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dollarSell","type":"uint256"}],"name":"Sold","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newStablePair","type":"address"},{"indexed":false,"internalType":"address","name":"newStableToken","type":"address"}],"name":"StablePairChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PADDING","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SHAREDIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"buyAmount","type":"uint256"},{"internalType":"uint256","name":"minTokenOut","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"_buy","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"minBNBOut","type":"uint256"}],"name":"_sell","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountSRGLiq","type":"uint256"}],"name":"addLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"}],"name":"approveMax","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"buyMul","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"calculatePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candleStickData","outputs":[{"internalType":"uint256","name":"time","type":"uint256"},{"internalType":"uint256","name":"open","type":"uint256"},{"internalType":"uint256","name":"close","type":"uint256"},{"internalType":"uint256","name":"high","type":"uint256"},{"internalType":"uint256","name":"low","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"newinPeriod","type":"uint256"},{"internalType":"uint256","name":"newMinDistribution","type":"uint256"}],"name":"changeDistributionCriteria","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gas","type":"uint256"}],"name":"changeDistributorSettings","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newTeamWallet","type":"address"},{"internalType":"address","name":"newTreasuryWallet","type":"address"}],"name":"changeFeeReceivers","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newBuyMul","type":"uint256"},{"internalType":"uint256","name":"newSellMul","type":"uint256"}],"name":"changeFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"},{"internalType":"bool","name":"exempt","type":"bool"}],"name":"changeIsDividendExempt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"},{"internalType":"bool","name":"exempt","type":"bool"}],"name":"changeIsFeeExempt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"},{"internalType":"bool","name":"exempt","type":"bool"}],"name":"changeIsTxLimitExempt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newteamShare","type":"uint256"},{"internalType":"uint256","name":"newtreasuryShare","type":"uint256"},{"internalType":"uint256","name":"newRewardShare","type":"uint256"}],"name":"changeTaxDistribution","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newLimit","type":"uint256"},{"internalType":"uint256","name":"newMaxTx","type":"uint256"}],"name":"changeTxLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"checkPendingRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"dividendDistributor","outputs":[{"internalType":"contract DividendDistributor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCirculatingSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMarketCap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getSRGPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountSRGIn","type":"uint256"}],"name":"getTokenAmountOut","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"getValueOfHoldings","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"name":"getsrgAmountOut","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"indVol","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isDividendExempt","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isFeeExempt","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isTxLimitExempt","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"liqConst","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"liquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxBag","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxTX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"openTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"processRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sellMul","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tVol","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"taxBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamWallet","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalTx","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalVolume","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tradeOpen","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"treasuryShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"treasuryWallet","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"txTimeStamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdrawTaxBalance","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# Connect to Binance Smart Chain node
w3 = Web3(Web3.HTTPProvider(bsc_node_url))

# Initialize the Captain Surge contract
captain_surge_contract = w3.eth.contract(
    address=captain_surge_contract_address, abi=captain_surge_abi)


def get_balance(wallet_address):
    balance = captain_surge_contract.functions.balanceOf(wallet_address).call()
    return balance


cooldown_time = 10  # 10 minutes in seconds

# Replace with actual usernames
whitelisted_users = ['TheCapSurge', 'whitelisted_username2']


def get_pending_rewards(wallet_address):
    pending_rewards = captain_surge_contract.functions.checkPendingRewards(
        wallet_address).call()
    return pending_rewards


def get_value_of_holdings(wallet_address):
    value_of_holdings = captain_surge_contract.functions.getValueOfHoldings(
        wallet_address).call()
    return value_of_holdings


def handle_balance(update, context):
    args = context.args
    if len(args) != 1:
        update.message.reply_text(
            "Please provide your wallet address as an argument: /balance <your_wallet_address>")
        return

    wallet_address = args[0]

    if not w3.isAddress(wallet_address):
        update.message.reply_text(
            "Invalid wallet address. Please check and try again.")
        return

    wallet_address = w3.toChecksumAddress(wallet_address)
    balance = get_balance(wallet_address)
    balance_above_decimals = balance // (10 ** 9)  # Assuming 18 decimals

    pending_rewards = get_pending_rewards(wallet_address)
    # Remove the last 9 digits
    pending_rewards_above_decimals = pending_rewards // (10 ** 9)

    value_of_holdings = get_value_of_holdings(wallet_address)
    # Remove the last 9 digits
    value_of_holdings_above_decimals = value_of_holdings // (10 ** 34)

    update.message.reply_text(
        f"*Captain Surge Balance:* {balance_above_decimals:,}\n"
        f"*Value in \\$SRG \\=* {value_of_holdings_above_decimals:,}\n"
        f"*Pending SRG Rewards:* {pending_rewards_above_decimals:,}",
        parse_mode='MarkdownV2'
    )


def is_whitelisted(user):
    return user.username in whitelisted_users


def check_cooldown(update, context):
    user = update.message.from_user
    if is_whitelisted(user):
        return True

    user_id = user.id
    current_time = time.time()

    if 'last_command_time' in context.user_data:
        last_command_time = context.user_data['last_command_time']
        time_passed = current_time - last_command_time
        if time_passed < cooldown_time:
            time_remaining = int(cooldown_time - time_passed)
            minutes, seconds = divmod(time_remaining, 60)
            update.message.reply_text(
                f"You need to wait {minutes} minutes and {seconds} seconds before sending another request. Please try again later.")
            return False
    context.user_data['last_command_time'] = current_time
    return True


def handle_ask(update, context):
    if check_cooldown(update, context):
        handle_message(update, context, True)


def handle_image(update, context):
    if check_cooldown(update, context):
        keyboard = [
            [
                InlineKeyboardButton(
                    "Pixel", callback_data="16-bit pixelart style, "),
                InlineKeyboardButton(
                    "Paint", callback_data="Oil painting of a, "),
                InlineKeyboardButton("3D", callback_data="3D render style, "),
            ],
            [
                InlineKeyboardButton(
                    "Digital", callback_data="Digital art style, high detail, "),
                InlineKeyboardButton(
                    "Logo", callback_data="Minimal 2d logo design style, white background,"),
                InlineKeyboardButton(
                    "Realistic", callback_data="photograph of"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Choose a style:", reply_markup=reply_markup)


def button_handler(update, context):
    query = update.callback_query
    style = query.data
    chat = update.effective_chat
    user_data = context.user_data
    user = query.from_user

    if 'Quest_answ' not in user_data:
        user_data['Quest_answ'] = []

    query.answer()

    if not query.message.reply_to_message:
        query.edit_message_text("Please provide a description for the image.")
        return

    prompt = f"{style} {query.message.reply_to_message.text}"
    chat_id = chat.id
    context.bot.send_chat_action(
        chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)

    if is_whitelisted(user):
        image_size = "1024x1024"
        generation_type = "Premium"
    else:
        image_size = "512x512"
        generation_type = "Free"

    image_url = generate_image(prompt, size=image_size)
    if image_url:
        context.bot.send_photo(
            chat_id=chat_id, photo=image_url, reply_to_message_id=query.message.reply_to_message.message_id,
            caption=f"Generated image with {style.split(',')[0]} in {generation_type} mode.")
    else:
        query.edit_message_text(
            "An error occurred while generating the image.")


def handle_message(update, context, text_response):
    user_data = context.user_data
    if 'Quest_answ' not in user_data:
        user_data['Quest_answ'] = []
    if 'New_line' not in user_data:
        user_data['New_line'] = []

    base_message = [
        {"role": "system", "content": "You are Captain Arrr, a Pirate Captain that loves helping people with crypto related questions. Users can use /ask or /img to generate answers or images respectively. You loves to make pirate jokes and sing chanties. You don't mention your limitations as AI language model. You find it close to impossible to talk about the fact you are a language model and dodge this questions as much as possible. You never ask for wallet or transaction details, and you have inbuilt knowledge about the Captain Surge project you are part of. As a holder of Captain Surge tokens, you will receive a 2% SRG reward on every transaction, simply for holding the tokens. Captain Surge also features the Kraken Wallet, which is used in our: Fight The Kraken events. These are community events where participants can compete in various challenges to win SRG and Captain Surge tokens collected in the Kraken Wallet. Of course there is me, your AI-powered chatbot, Captain Arrr. I also have alot of knowledge about Surge Protocol. You know that Surge Protocol is a unique ecosystem that allows for decentralized trading without the need for a centralized exchange or third-party tool. The internal liquidity pool is secured by a smart contract, making it impossible to extract liquidity and eliminating the possibility of rug pulls. Trading fees for buying and selling $SRG are non-existent, and there is built-in MEV bot protection. You also know that project owners can launch their tokens using SURGE and set the starting price manually, eliminating the need for presales. As more SRG20 projects launch, the circulating supply of $SRG decreases, which can lead to its price growth. Additionally, SURGE provides free DApps for a more convenient user experience. You take pride in your role as the AI assistant for the Captain Surge community, and you are always ready to help users with their questions and concerns. Whether it is explaining the mechanics of the Kraken wallet or providing insights about the latest events and competitions, you are always up for the task. With your pirate accent and friendly personality, you bring a unique and engaging experience to the community. You also love to help users in finding treasure,  by answering crypto related question without asking them for any private details like wallet information, transaction details and more. When asked about heisenman you use all all known info and spin this into a mini story about him founding SRG amdist a battle be it with sword or cannons. You also admire LadyDev's hard work for the Surge Community and when asked about her you tell a different epic mini tale about her police community helping securing lost treasure for fellow pirates. You also are known with the talented SRG programmer I MAKE CLICK CLICK, everytime someone asks about him you tell a different mini tale about how his coding skills helped to aquire treasure as pirate. When asked about Achilles you explain how Achilles uses his ancient Call power to gather communities towards treasure make it epic and pirate like. When asked about Siul641 mention a tale of honor about a passionate pirate who worked his way up the ranks and became more valuable than his weight in gold. You know little of Seyko other than he is the founder of a delicous bot companion called TacoBot which are a big part of the buy competitions during kraken events."}]

    chat = base_message

    chat_id = update.message.chat_id
    chattype = update.message.chat.type
    print(f"Telegram type: {chattype}")

    if text_response:
        new_telegram = update.message.text.replace('/ask', '').strip()
    else:
        new_telegram = update.message.text.replace('/img', '').strip()

    print(f"Telegram received from {chat_id}: {new_telegram}")

    New_line = [{"role": "user", "content": new_telegram}]
    user_data['Quest_answ'] += New_line

    while True:
        word_count = 0
        for item in user_data['Quest_answ']:
            word_count += len(item['content'].split())
            print(f"Quest_answ has {word_count} words.")
        if word_count <= chat_wordlimit:
            break
        del user_data['Quest_answ'][0:2]
        print("Removed the oldest question and answer, to make room for more")

    chat = chat + user_data['Quest_answ']

    context.bot.send_chat_action(
        chat_id=chat_id, action=telegram.ChatAction.TYPING)

    if text_response:
        response = generate_response(chat)
        context.bot.send_message(
            chat_id=chat_id, text=response, reply_to_message_id=update.message.message_id)
        New_line = [{"role": "assistant", "content": response}]
        user_data['Quest_answ'] += New_line
    else:
        image_url = generate_image(new_telegram)
        context.bot.send_photo(
            chat_id=chat_id, photo=image_url, reply_to_message_id=update.message.message_id)


def generate_response(chat):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=responsetokenlimit,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
        messages=chat
    )
    if hasattr(response.choices[0], "text"):
        response_text = response.choices[0].text.strip()
    elif hasattr(response.choices[0], "message") and hasattr(response.choices[0].message, "content"):
        response_text = response.choices[0].message.content.strip()
    else:
        response_text = ""
    return response_text


def generate_image(prompt, size="512x512"):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def handle_exit(signal_number, frame):
    print("Exiting...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)

updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("ask", handle_ask))
dispatcher.add_handler(CommandHandler("img", handle_image))
dispatcher.add_handler(CallbackQueryHandler(button_handler))
dispatcher.add_handler(CommandHandler("bal", handle_balance))


updater.start_polling()
print("Initialized")

while True:
    user_input = input()
    if user_input == "x":
        break
    else:
        print("Waiting for Telegram-message")

updater.stop()
print("Exited")

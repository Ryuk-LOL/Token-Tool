import random
import string
import base64
import os
import time
import requests
import sys

# New ASCII Art Header
def print_ascii():
    print(r"""
___________________   ____  __.___________ _______    ___________________   ________  .____     
\__    ___/\_____  \ |    |/ _|\_   _____/ \      \   \__    ___/\_____  \  \_____  \ |    |    
  |    |    /   |   \|      <   |    __)_  /   |   \    |    |    /   |   \  /   |   \|    |    
  |    |   /    |    \    |  \  |        \/    |    \   |    |   /    |    \/    |    \    |___ 
  |____|   \_______  /____|__ \/_______  /\____|__  /   |____|   \_______  /\_______  /_______ \
                   \/        \/        \/         \/                     \/         \/        \/

                    Made by Ryuk.lyy
""")

# Loading animation
def loading_animation(message, progress):
    bar_length = 30
    block = int(round(bar_length * progress))
    progress_str = "█" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r{message} |{progress_str}| {int(progress * 100)}%")
    sys.stdout.flush()

# Fake token generator function
def generate_fake_token():
    user_id = str(random.randint(100000000000000000, 999999999999999999))
    user_id_encoded = base64.b64encode(user_id.encode()).decode().replace("=", "")
    middle = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=6))
    end = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=27))
    token = f"{user_id_encoded}.{middle}.{end}"
    return token

# Token Generator
def token_generator():
    try:
        amount = int(input("\n🛠️  How many tokens to generate? "))
    except ValueError:
        print("\n❌ Invalid number. Please enter digits.")
        return

    os.makedirs('results', exist_ok=True)

    with open("results/tokens.txt", "w") as f:
        for _ in range(amount):
            token = generate_fake_token()
            f.write(token + "\n")
    
    print(f"\n✅ {amount} tokens generated and saved to results/tokens.txt!\n")

# Token Checker
def real_token_checker():
    if not os.path.exists("results/tokens.txt"):
        print("\n⚠️  No tokens found. Generate tokens first!\n")
        return

    with open("results/tokens.txt", "r") as f:
        tokens = f.read().splitlines()

    if not tokens:
        print("\n⚠️  Your tokens.txt is empty!\n")
        return

    valid = []
    invalid = []
    total = len(tokens)

    os.makedirs('results', exist_ok=True)

    print(f"\n🔍 Checking {total} tokens...\n")

    for index, token in enumerate(tokens, start=1):
        loading_animation("Checking tokens", index/total)

        headers = {'Authorization': token}
        try:
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                valid.append(token)
                print(f"\n✅ {index}/{total} - {token} [VALID]")
                print('\a', end='', flush=True)
            else:
                invalid.append(token)
                print(f"\n❌ {index}/{total} - {token} [INVALID]")
                print('\a', end='', flush=True)
        except requests.exceptions.RequestException as e:
            invalid.append(token)
            print(f"\n⚡ {index}/{total} - {token} [ERROR: {str(e)}]")

        time.sleep(0.1)  # visual smoothness

    # Saving results
    with open("results/valid.txt", "w") as f:
        for t in valid:
            f.write(t + "\n")

    with open("results/invalid.txt", "w") as f:
        for t in invalid:
            f.write(t + "\n")

    print("\n\n🎉 Checking complete!\n")
    print(f"📊 Total Tokens Checked: {total}")
    print(f"✅ Valid Tokens: {len(valid)}")
    print(f"❌ Invalid Tokens: {len(invalid)}")
    print("\n📂 Saved in results/valid.txt and results/invalid.txt\n")

# Menu
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii()
    while True:
        print("\n🌟 What would you like to do?")
        print("1️⃣  Token Checker")
        print("2️⃣  Token Generator")
        print("3️⃣  Exit")

        choice = input("\n💬 Enter your choice (1/2/3): ")

        if choice == "1":
            real_token_checker()
        elif choice == "2":
            token_generator()
        elif choice == "3":
            print("\n👋 Goodbye from Ryuk.lyy!")
            break
        else:
            print("\n❌ Invalid choice. Try again!\n")

if __name__ == "__main__":
    main()

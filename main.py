import requests
import json
import os
import time
from fake_useragent import UserAgent
import re
import uuid
from colorama import init, Fore, Style

init()

def scrap_server(server_id, proxy):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random,
        'ethod': 'GET'
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)

        if response.status_code == 200:
            server_data = response.json()
            server = str(uuid.uuid4())
            server = re.sub(r'^([0-9])', '', re.sub(r'[/:"*?<>|]', '', server_data['Data']['hostname']))[:100]

            if len(server_data['Data']['vars']['sv_projectName']) >= 10:
                server = re.sub(r'^([0-9])', '', re.sub(r'[/:"*?<>|]', '', server_data['Data']['vars']['sv_projectName']))[:100]

            if not os.path.exists('results'):
                os.makedirs('results')

            filename = f'results/{server}.txt'
            path = 'results'

            added_players = 0
            for player in server_data['Data']['players']:
                player_data = json.dumps(player, ensure_ascii=False)
                player_identifiers = player['identifiers']

                if not os.path.exists(filename) or player_identifiers not in [json.loads(line).get('identifiers') for line in open(filename, 'r', encoding='utf-8').readlines()]:
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(player_data)
                        file.write('\n')

            print(Fore.YELLOW + '(+) ' + Fore.RESET + f'Sucessfully dumped server: {server_id} ({server}) Saved in: {path}, used proxy: ' + Fore.LIGHTYELLOW_EX + f'{proxy}')
        else:
            print(Fore.YELLOW + f'(-) Failed to dump the server: Retry ({server_id}: {response.status_code})')

    except Exception as e:
        print(f'Erreur: {str(e)}')

def scrap_unique(server_id):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random,
        'ethod': 'GET'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            server_data = response.json()
            server = str(uuid.uuid4())
            server = re.sub(r'^([0-9])', '', re.sub(r'[/:"*?<>|]', '', server_data['Data']['hostname']))[:100]

            if len(server_data['Data']['vars']['sv_projectName']) >= 10:
                server = re.sub(r'^([0-9])', '', re.sub(r'[/:"*?<>|]', '', server_data['Data']['vars']['sv_projectName']))[:100]

            if not os.path.exists('results'):
                os.makedirs('results')

            filename = f'results/{server}.txt'
            path = 'results'

            added_players = 0
            for player in server_data['Data']['players']:
                player_data = json.dumps(player, ensure_ascii=False)
                player_identifiers = player['identifiers']

                if not os.path.exists(filename) or player_identifiers not in [json.loads(line).get('identifiers') for line in open(filename, 'r', encoding='utf-8').readlines()]:
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(player_data)
                        file.write('\n')

            print(Fore.YELLOW + '(+) ' + Fore.RESET + f'Sucessfully dumped server: {server_id} ({server}) Saved in: {path}')
            time.sleep(5)
            os.system('cls')
            main()
        else:
            print(Fore.YELLOW + f'(-) Failed to dump the server: Retry ({server_id}: {response.status_code})')
            time.sleep(5)
            os.system('cls')
            main()

    except Exception as e:
        print(f'Erreur: {str(e)}')

def check_id(server_id):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random,
        'ethod': 'GET'
    }

    filename = f'online_servers.txt'

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(Fore.LIGHTYELLOW_EX + f'(+) ' + Fore.WHITE + f'Server {server_id} is online, successfully added in the new list ({response.elapsed.seconds} ms)')

            with open(filename, 'w') as new_list:
                new_list.write(f'{server_id}\n')
        
            time.sleep(1)

        if response.status_code == 429:
            print(Fore.YELLOW + f'(-) Rate limit exceeded, waiting 30 seconds...')
            time.sleep(30)

        elif response.status_code == 404:
            print(Fore.YELLOW + f'(-) ' + Fore.WHITE + f'Failed to reach the server {server_id}, successfully removed from the new list ({response.status_code})')

    except Exception as e:
        print(f'Error: {e.__class__.__name__}: {e}')

def main():
    os.system('cls')
    banner = '''
               ',
            .-`-,\__
              ."`   `,
            .'_.  ._  `;.
        __ / `      `  `.\ .--.
       /--,| 0)   0)     )`_.-,)
      |    ;.-----.__ _-');   /    fivem scraper by 311 (only use uhq proxies)
       '--./         `.`/  `"`     https://github.com/311nerd   
          :   '`      |.      
          | \     /  //            @Xx_monkey.1337.311.web_xX
           \ '---'  /'        
            `------' \  
             _/       `--...                
             '''
    
    print(Fore.YELLOW + banner + Fore.RESET)
    print(Fore.YELLOW + "1." + Fore.RESET + "Dump all cfx id in servers.txt with proxies in proxy.txt")
    print(Fore.YELLOW + "2." + Fore.RESET + "Dump all cfx id in servers.txt without proxies")
    print(Fore.YELLOW + "3." + Fore.RESET + "Dump a single server without using proxies")
    print(Fore.YELLOW + "4." + Fore.RESET + "Dump cfx.re server list using Fivem API (soon)")
    print(Fore.YELLOW + "5." + Fore.RESET + "Check cfx id and remove offline servers")

    choice = input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)
    print(Fore.RESET)

    if choice == "1":
        with open('servers.txt', 'r') as server_file:
            servers = [line.strip() for line in server_file.readlines()]

        with open('proxy.txt', 'r') as proxy_file:
            proxy_list = [{'http': f'http://{proxy.strip()}'} for proxy in proxy_file]

        proxy_index = 0
        total_proxies = len(proxy_list)

        for server_id in servers:
            scrap_server(server_id, proxy_list[proxy_index % total_proxies])
            proxy_index += 1

    elif choice == "2":
        with open('servers.txt', 'r') as server_file:
            servers = [line.strip() for line in server_file.readlines()]

        for server_id in servers:
            scrap_server(server_id, {})

    elif choice == "3":
        server_id = input("Enter the server ID: ")
        scrap_unique(server_id)

    elif choice == "4":
        print("Coming soon...")
        os.system('cls')
        main()

    elif choice == "5":
        with open('servers.txt', 'r') as server_file:
            servers = [line.strip() for line in server_file.readlines()]

        for server_id in servers:
            check_id(server_id)

    else:
        print("Invalid choice, choose a valid option please.")
        time.sleep(2)
        os.system('cls')
        main()

if __name__ == "__main__":
    main()
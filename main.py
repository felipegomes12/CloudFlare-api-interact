import requests
import importlib.util
import os
from pprint import pprint

def load_settings():
    """Carrega dinamicamente o settings.py como módulo."""
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.py')
    spec = importlib.util.spec_from_file_location("settings", settings_path)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings

settings = load_settings()

def setup():
    settings = load_settings()
    print("Setup inicial deve ser concluido antes de utilizar.")
    if settings.CLOUDFLARE_API_TOKEN == 'NOT_SET':
        entrada = input("Token da API do Cloudflare: ")

        with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            conteudo = conteudo.replace(
                "CLOUDFLARE_API_TOKEN = 'NOT_SET'",
                f"CLOUDFLARE_API_TOKEN = '{entrada}'"
            )
            conteudo = conteudo.replace(
                "SETUP = False",
                f"SETUP = True"
            )

        with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print("Token salvo.")
        exit()

def change_token():
    if not settings.SETUP: setup()
    entrada = input("Token da API do Cloudflare: ")

    with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    conteudo = conteudo.replace(
        f"CLOUDFLARE_API_TOKEN = '{settings.CLOUDFLARE_API_TOKEN}'",
        f"CLOUDFLARE_API_TOKEN = '{entrada}'"
    )

    with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print("Novo token salvo.")
    
def get_domain(jump=False):
    if not settings.SETUP: setup()
    entrada = input("Digite o domínio ou deixe vazio para usar o padrão: ")
    if entrada and not jump: 
        define = input("Definir domínio como padrão? (s/n): ")
        if define.lower() == "s":
            with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                conteudo = conteudo.replace(
                    f"DEFAULT_DOMAIN = '{settings.DEFAULT_DOMAIN}'",
                    f"DEFAULT_DOMAIN = '{entrada}'"
                )

            with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
                f.write(conteudo)

            print("Domínio salvo.")
        elif define.lower() == "n": 
            pass
        else: 
            raise KeyError(f"{define} não é um valor válido") 
        return entrada
    else:
        if settings.DEFAULT_DOMAIN: return settings.DEFAULT_DOMAIN
        else:
            print("Não há um domínio padrão, defina o domínio padrão.")
            entrada = input("Domínio: ")
            with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                conteudo = conteudo.replace(
                    f"DEFAULT_DOMAIN = '{settings.DEFAULT_DOMAIN}'",
                    f"DEFAULT_DOMAIN = '{entrada}'"
                )

            with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
                f.write(conteudo)

            print("Domínio salvo.")
            return entrada

def get_zone_id(jump):
    """Pega o zone_id a partir do domínio principal."""
    if not settings.SETUP: setup()
    resp = requests.get(f'{settings.CLOUDFLARE_API_BASE}/zones', headers=settings.HEADERS, params={'name': get_domain(jump)})
    resp.raise_for_status()
    return resp.json()['result'][0]['id']

def list_dns_records():
    """Lista todos os registros DNS da zona."""
    if not settings.SETUP: setup()
    resp = requests.get(f'{settings.CLOUDFLARE_API_BASE}/zones/{get_zone_id(True)}/dns_records', headers=settings.HEADERS)
    resp.raise_for_status()
    pprint(resp.json()['result'])
    return resp.json()['result']

def get_name():
    if not settings.SETUP: setup()
    if settings.DEFAULT_SRV_NAME: return settings.DEFAULT_SRV_NAME
    else:
        print("Não há um registro A padrão, defina o registro A padrão.")
        entrada = input("Domínio: ")
        with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            conteudo = conteudo.replace(
                f"DEFAULT_SRV_NAME = '{settings.DEFAULT_SRV_NAME}'",
                f"DEFAULT_SRV_NAME = '{entrada}'"
            )

        with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print("registro A salvo.")
        return entrada

def get_public_ip():
    if not settings.SETUP: setup()
    if settings.DEFAULT_CONTENT: return settings.DEFAULT_CONTENT
    else:
        print("Não há um IP público padrão, defina o IP público.")
        entrada = input("IP público: ")
        with open(settings.SETTINGS_PATCH, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            conteudo = conteudo.replace(
                f"DEFAULT_CONTENT = '{settings.DEFAULT_CONTENT}'",
                f"DEFAULT_CONTENT = '{entrada}'"
            )

        with open(settings.SETTINGS_PATCH, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print("IP público salvo.")
        return entrada

def create_a_record():
    """Cria um registro A se ele não existir."""
    if not settings.SETUP: setup()
    zone_id = get_zone_id()
    records = list_dns_records()
    name = get_name()
    for rec in records:
        if rec['type'] == 'A' and rec['name'] == name:
            print(f"Registro A '{name}' já existe.")
            return rec

    data = {
        'type': 'A',
        'name': name,
        'content': get_public_ip(),
        'ttl': 1,
        'proxied': False
    }
    resp = requests.post(f'{settings.CLOUDFLARE_API_BASE}/zones/{zone_id}/dns_records', headers=settings.HEADERS, json=data)
    resp.raise_for_status()
    pprint(resp.json()['result'])
    return resp.json()['result']

def create_srv_record():
    """Cria um registro SRV para serviços como Minecraft."""
    if not settings.SETUP: setup()
    zone_id = get_zone_id()
    service = input("Tipo de serviço sem _ : ")
    protocol = input("Proto: ")
    name = input("Subdominio: ")
    full_name = f"_{service}._{protocol}.{name}"
    data = {
        "type": "SRV",
        "data": {
            "service": f"_{service}",
            "proto": f"_{protocol}",
            "name": name,
            "priority": 0,
            "weight": 0,
            "port": input("Porta: "),
            "target": get_name()
        },
        "ttl": 1
    }

    resp = requests.post(f'{settings.CLOUDFLARE_API_BASE}/zones/{zone_id}/dns_records', headers=settings.HEADERS, json=data)
    resp.raise_for_status()
    print(full_name)
    pprint(resp.json()['result'])
    return resp.json()['result']

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if not args:
        print("""
        Nenhuma ação fornecida.
        As ações disponíveis são:
            - setup
            - list
            - create-a
            - create-srv
            - all
              """)
        sys.exit(1)

    action = args[0]

    if action == "setup":
        setup()
    elif action == "list":
        for rec in list_dns_records():
            print(f"{rec['type']} - {rec['name']} -> {rec['content']}")
    elif action == "create-a":
        create_a_record()
    elif action == "create-srv":
        create_srv_record()
    else:
        print(f"Ação desconhecida: {action}")

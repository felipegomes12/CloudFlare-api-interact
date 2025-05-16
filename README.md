# CloudFlare api interact

nesse projeto estão disponiveis métodos para criação de multiplos Registros SRV via api do cloudflare que servem para apontar para uma porta especifíca.

## Instalação

### Dependencias (se necessário)
```shell
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
curl \
unzip \
python3 \
python3-venv \
```
### Rep
```bash
sudo curl -L https://github.com/felipegomes12/CloudFlare-api-interact/archive/refs/heads/main.zip -o /tmp/cloudflare_repo.zip
sudo unzip -o /tmp/cloudflare_repo.zip -d /opt/
sudo mv /opt/CloudFlare-api-interact-main /opt/cloudflare_dns
sudo chmod +x /opt/cloudflare_dns/cloudflare_dns.sh
echo -e '#!/bin/bash\n/opt/cloudflare_dns/cloudflare_dns.sh "$@"' | sudo tee /usr/local/bin/cloudflare_dns > /dev/null
sudo chmod +x /usr/local/bin/cloudflare_dns
```
## Uso
### cloudflare_dns
Depois da instalação, use o comando global cloudflare_dns com argumentos para executar as funcionalidades disponíveis:
```shell
cloudflare_dns setup
```
```shell
cloudflare_dns list_dns
```
```shell
cloudflare_dns create_a
```
```shell
cloudflare_dns create_srv

```
## O que cada comando faz:
setup: Realiza a configuração inicial e prepara o ambiente virtual (caso ainda não exista).

list_dns: Lista os registros DNS atuais.

create_a: Cria um registro do tipo A.

create_srv: Cria um registro do tipo SRV.
## requerimentos
- Sitema linux.
- Acesso ao root ou a senha do root.
- curl 
- unzip
- python3
- python3-venv
- pip (será instalado automaticamente no primeiro uso, junto com o ambiente virtual)
- Domínio gerenciado pelo painel da cloudflare
## Permições
Qualquer um é livre para baixar os arquivos e alterar para suprir suas necessidades. Nenhum crédito é necessário.
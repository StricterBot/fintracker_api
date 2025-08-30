import requests
import random
from faker import Faker
from rich.console import Console
from rich.progress import Progress
from collections import defaultdict

# --- CONFIGURAÇÃO ---
BASE_URL = "http://127.0.0.1:8000/api/v1"
NUM_USUARIOS = 5
MAX_CARTEIRAS_POR_USUARIO = 2
MAX_CARTOES_POR_CARTEIRA = 2
NUM_TRANSACOES = 10

# Inicializa o Faker para o Brasil e o Rich para output colorido
fake = Faker('pt_BR')
console = Console()

# --- FUNÇÕES AUXILIARES --- (as funções clear_data, create_user, create_wallet, create_card continuam iguais)

def clear_data(session):
    """Limpa todos os dados existentes na API para um novo seed."""
    console.print("[bold yellow]🗑️ Limpando dados existentes...[/bold yellow]")
    try:
        # A ordem é importante devido às Foreign Keys: cartões -> carteiras -> usuários
        cartoes = session.get(f"{BASE_URL}/cartoes/").json().get("items", [])
        for cartao in cartoes:
            session.delete(f"{BASE_URL}/cartoes/{cartao['id']}")
        
        carteiras = session.get(f"{BASE_URL}/carteiras/").json().get("items", [])
        for carteira in carteiras:
            session.delete(f"{BASE_URL}/carteiras/{carteira['id']}")
        
        usuarios = session.get(f"{BASE_URL}/usuarios/").json().get("items", [])
        for usuario in usuarios:
            session.delete(f"{BASE_URL}/usuarios/{usuario['id']}")
            
        console.print("[green]✔️ Dados limpos com sucesso![/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao limpar dados: {e}[/bold red]")

def create_user(session, progress, task_id):
    """Cria um usuário com dados do Faker."""
    user_data = {"nome": fake.name(), "cpf": fake.cpf().replace('.', '').replace('-', ''), "email": fake.email()}
    response = session.post(f"{BASE_URL}/usuarios/", json=user_data)
    progress.advance(task_id)
    if response.status_code == 201: return response.json()
    return None

def create_wallet(session, user_id, progress, task_id):
    """Cria uma carteira com moeda e saldo aleatórios."""
    moeda = random.choice(["BRL", "USD", "EUR"])
    saldo = round(random.uniform(50.0, 5000.0), 2)
    carteira_data = {"usuario_id": user_id, "moeda": moeda, "saldo_atual": str(saldo)}
    response = session.post(f"{BASE_URL}/carteiras/", json=carteira_data)
    progress.advance(task_id)
    if response.status_code == 201: return response.json()
    return None

def create_card(session, carteira_id, progress, task_id):
    """Cria um cartão com limite aleatório."""
    limite = round(random.uniform(500.0, 10000.0), 2)
    cartao_data = {"carteira_id": carteira_id, "numero": fake.credit_card_number(card_type="mastercard"), "validade": fake.credit_card_expire(), "limite": str(limite)}
    response = session.post(f"{BASE_URL}/cartoes/", json=cartao_data)
    progress.advance(task_id)
    if response.status_code == 201: return response.json()
    return None

def create_transaction(session, origem, destino, progress, task_id): # <-- MUDANÇA: Recebe origem e destino
    """Cria uma transação entre duas carteiras específicas."""
    valor_max = float(origem["saldo_atual"]) * 0.5
    if valor_max < 1.0:
        console.print(f"[yellow]Skipping transaction: Saldo insuficiente na carteira de origem {origem['id']}[/yellow]")
        progress.advance(task_id)
        return

    valor = round(random.uniform(1.0, valor_max), 2)
    
    transacao_data = {
        "carteira_origem_id": origem["id"],
        "carteira_destino_id": destino["id"],
        "valor": str(valor)
    }
    response = session.post(f"{BASE_URL}/transacoes/", json=transacao_data)
    if response.status_code == 200:
        console.print(f"  [green]✓[/green] Transação de {valor} {origem['moeda']} de C:{origem['id']} para C:{destino['id']} bem-sucedida.")
    else:
        console.print(f"  [red]✗[/red] Falha na transação de C:{origem['id']} para C:{destino['id']}: {response.text}")
    
    progress.advance(task_id)

def seed_data():
    """Função principal que orquestra o povoamento do banco."""
    try:
        with requests.Session() as session:
            clear_data(session)
            
            total_steps = NUM_USUARIOS + (NUM_USUARIOS * MAX_CARTEIRAS_POR_USUARIO) + \
                          (NUM_USUARIOS * MAX_CARTEIRAS_POR_USUARIO * MAX_CARTOES_POR_CARTEIRA) + NUM_TRANSACOES
            
            with Progress() as progress:
                task_id = progress.add_task("[cyan]Populando banco de dados...", total=total_steps)
                
                usuarios, carteiras = [], []
                for _ in range(NUM_USUARIOS):
                    user = create_user(session, progress, task_id)
                    if user:
                        usuarios.append(user)
                        for _ in range(random.randint(1, MAX_CARTEIRAS_POR_USUARIO)):
                            wallet = create_wallet(session, user["id"], progress, task_id)
                            if wallet:
                                carteiras.append(wallet)
                                for _ in range(random.randint(1, MAX_CARTOES_POR_CARTEIRA)):
                                    create_card(session, wallet["id"], progress, task_id)
                
                # --- LÓGICA DE TRANSAÇÃO APRIMORADA ---
                console.print("\n[bold cyan]🏦 Criando transações...[/bold cyan]")
                wallets_by_currency = defaultdict(list)
                for wallet in carteiras:
                    wallets_by_currency[wallet['moeda']].append(wallet)

                for _ in range(NUM_TRANSACOES):
                    # Escolhe uma moeda que tenha pelo menos 2 carteiras
                    possible_currencies = [c for c, w in wallets_by_currency.items() if len(w) >= 2]
                    if not possible_currencies:
                        console.print("[yellow]Não há carteiras suficientes para realizar mais transações.[/yellow]")
                        progress.update(task_id, advance=NUM_TRANSACOES - _) # Avança o restante
                        break
                    
                    currency = random.choice(possible_currencies)
                    origem, destino = random.sample(wallets_by_currency[currency], 2)
                    create_transaction(session, origem, destino, progress, task_id)

            console.print(f"\n[bold green]✔️ Povoamento concluído![/bold green]")
            console.print(f"   - [b]{len(usuarios)}[/b] usuários criados.")
            console.print(f"   - [b]{len(carteiras)}[/b] carteiras criadas.")

    except requests.exceptions.ConnectionError:
        console.print("\n[bold red]❌ ERRO: Não foi possível conectar à API.[/bold red]")
        console.print("   Por favor, verifique se o servidor Uvicorn está rodando em http://127.0.0.1:8000")

if __name__ == "__main__":
    seed_data()
#!/bin/bash

# Saia imediatamente se um comando falhar
set -e

# Função para verificar se o banco de dados está pronto
wait_for_db() {
  echo "Aguardando o banco de dados ficar disponível..."
  # O comando `nc` (netcat) verifica se a porta 5432 está aberta no host 'db'
  # O `until` continuará tentando até que o comando seja bem-sucedido
  until nc -z -v -w30 db 5432
  do
    echo "Aguardando conexão com o banco de dados..."
    sleep 2
  done
  echo "Banco de dados está pronto!"
}

wait_for_db
echo "Executando migrações do Alembic..."
alembic upgrade head

echo "Iniciando a aplicação..."
exec "$@"
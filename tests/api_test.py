from fastapi.testclient import TestClient # Não precisa mais do 'app'
import random

def test_create_usuario_success(client: TestClient):
    """ Teste de criação de usuário com sucesso (status 201) """
    rand_int = random.randint(1000, 9999)
    # Usamos um número aleatório para garantir que o CPF/email sejam únicos a cada teste
    
    response = client.post(
        "/api/v1/usuarios/",
        json={
            "nome": "Usuario Teste",
            "cpf": f"1234567{rand_int}",
            "email": f"teste{rand_int}@example.com"
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data["email"] == f"teste{rand_int}@example.com"
    assert "id" in data

def test_create_usuario_duplicate_cpf(client: TestClient):
    """ Teste de falha ao criar usuário com CPF duplicado (status 409) """
    # Primeiro, criamos um usuário para garantir que ele exista
    user_payload = {
        "nome": "Usuario Duplicado",
        "cpf": "98765432100",
        "email": "duplicado@example.com"
    }
    client.post("/api/v1/usuarios/", json=user_payload)
    
    # Agora, tentamos criar de novo
    response = client.post("/api/v1/usuarios/", json=user_payload)
    assert response.status_code == 409
    assert "CPF ou Email já cadastrado" in response.json()["detail"]

def test_read_usuario_not_found(client: TestClient):
    """ Teste de erro ao buscar um usuário que não existe (status 404) """
    response = client.get("/api/v1/usuarios/999999")
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]

def test_read_usuarios_paginated(client: TestClient):
    """ Teste da listagem paginada de usuários """
    # Apenas para garantir que a rota existe e retorna a estrutura correta
    response = client.get("/api/v1/usuarios/")
    data = response.json()
    assert response.status_code == 200
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
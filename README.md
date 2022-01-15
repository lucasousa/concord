# concord
Sistema web válido como trabalho final da disciplina de Projeto e Desenvolvimento de Sistemas de Informção I

## Requisitos

- Python >= 3.6

## Instalação

- Instale o <a href="https://www.docker.com/get-started"> docker</a>
- Em um terminal na pasta raiz do projeto rode o comando `docker-compose up --build`
- Em outro terminal, também na pasta raiz do projeto rode o comando `docker-compose run web python manage.py createsuperuser`
- Siga os passos para criar um usuário com privilégios de administrador
- Acesse o sistema por meio da url `localhost:8000` para uso normal
- Acesse o painel do administrador através da url `localhost:8000/admin` por aqui serão criados novos usuários
- Para criar um usuário, acesse a tabela Usuários (ou Users) na app Core e adicionar


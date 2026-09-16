# Check Point 01 - Grupo 3

**Leonardo Garroti, Aquiles Fonseca e Leandro de Souza**  
Turma: 2TDCPF. Disciplina: Cloud Security. Professor: Fabio Pires.

Estudamos quatro ferramentas indicadas na tabela do professor:

| Categoria | Ferramenta | O que ela olha |
| --- | --- | --- |
| SAST | njsscan | O código Node.js escrito pela equipe |
| SCA | npm audit | As versões das dependências |
| IaC | Datree | As configurações do Kubernetes |
| DAST | StackHawk / HawkScan | A aplicação em funcionamento |

O laboratório usa **njsscan e npm audit**, duas categorias diferentes. O alvo é uma aplicação própria, com uma versão insegura e outra corrigida.

## Resultado real do teste local

| Versão | njsscan | npm audit | Gate |
| --- | --- | --- | --- |
| Insegura | 3 ERROR | 1 pacote HIGH | Bloqueado, saída 1 |
| Corrigida | 0 alertas | 0 pacotes vulneráveis | Aprovado, saída 0 |

O njsscan usa ERROR/WARNING/INFO. Nosso gate trata ERROR como HIGH, por decisão documentada do grupo. Isso não é uma nota CVSS fornecida pelo njsscan. No npm audit, um pacote pode reunir vários avisos de segurança.

## Antes da aula

Docker 24 ou mais recente, Compose v2, Git, conexão com a internet, 4 GB de memória e cerca de 3 GB de espaço livre. Use containers Linux. A primeira preparação deve acontecer antes da apresentação.

Depois de baixar este repositório, rode:

```bash
docker pull node:24-bookworm-slim
docker compose build --pull lab
docker image inspect cp01-grupo3:1.0
```

O Dockerfile instala njsscan 1.0.0, Semgrep 1.172.0, libsast 3.1.8 e npm 11.12.0. A imagem base usa o canal Node 24, que pode receber atualização. Para congelar também a base, guarde seu digest após o teste na máquina da turma.

## Laboratório

```bash
docker compose run --rm lab inseguro
docker compose run --rm lab corrigido
```

O primeiro comando deve terminar com código 1, pois encontrou falhas. O segundo deve terminar com código 0. Leia o passo a passo e as duas perguntas em [LAB.md](LAB.md).

Não é preciso subir a aplicação para SAST e SCA. O Compose só executa os scanners, sem publicar portas. O npm audit precisa consultar o registro npm. Nenhuma varredura ativa é feita em sites de terceiros.


## GitHub Actions

O fluxo `Segurança do grupo 3` analisa a versão corrigida em push e pull request. Em **Actions > Segurança do grupo 3 > Run workflow**, escolha `inseguro` para mostrar o build vermelho e depois `corrigido` para o verde. Os relatórios ficam disponíveis como artefatos mesmo quando o gate bloqueia.

Um erro de rede, relatório ausente, JSON inválido ou erro do scanner também bloqueia a execução. O fluxo não usa `continue-on-error` para transformar falha em aprovação. Os relatórios locais incluídos não substituem os registros de duas execuções na plataforma.


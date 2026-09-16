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

Os relatórios locais foram produzidos em 16/09/2026. O Windows precisou de uma ponte de execução, explicada em `docs/VALIDACAO.md`. Os prints do relatório mostram saídas reais locais e não são telas do GitHub Actions.

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

## Material

- `docs/PESQUISA-GRUPO-3.pdf`: pesquisa com 18 páginas de conteúdo.
- `docs/APRESENTACAO-GRUPO-3.pptx`: 29 slides editáveis, com notas para a fala.
- `docs/APRESENTACAO-GRUPO-3.pdf`: cópia de segurança dos slides.
- `docs/ROTEIRO-APRESENTACAO.md`: divisão sugerida da fala e dos 30 minutos.
- `docs/ANALISE-ACHADOS.md`: três achados reais, classificação e correção.
- `reports/`: JSON, SARIF, SBOM e tempos medidos.
- `evidencias-docker/`: nove capturas reais do Docker Desktop, do relatório HTML do njsscan, do terminal e do GitHub Actions, sem caminhos de pastas.
- `USO-DE-IA.md`: como a IA ajudou e como o material foi conferido.
- `docs/ENTREGA.md`: o que está pronto e o que depende da publicação e da aula.

## GitHub Actions

O fluxo `Segurança do grupo 3` analisa a versão corrigida em push e pull request. Em **Actions > Segurança do grupo 3 > Run workflow**, escolha `inseguro` para mostrar o build vermelho e depois `corrigido` para o verde. Os relatórios ficam disponíveis como artefatos mesmo quando o gate bloqueia.

Um erro de rede, relatório ausente, JSON inválido ou erro do scanner também bloqueia a execução. O fluxo não usa `continue-on-error` para transformar falha em aprovação. Os relatórios locais incluídos não substituem os registros de duas execuções na plataforma.

## Diferenças encontradas no enunciado

O arquivo de apoio fala em três grupos, enquanto a tabela dos slides foi ajustada para cinco. Seguimos a coluna **Grupo 3** da tabela ajustada. Datree está arquivado desde 2024, e sua empresa encerrou a manutenção em 2023. StackHawk é uma plataforma comercial, mesmo tendo origem no ZAP. Mantivemos os nomes atribuídos e não fizemos substituições.

O prazo aparece como 24 horas no texto e 48 horas no checklist. Prepare a publicação com pelo menos **48 horas** de antecedência. O professor ainda precisa validar as ferramentas e a escolha das duas do laboratório.

## Referências e uso

As fontes estão em `docs/REFERENCIAS.md` e no PDF. O código de exemplo e os roteiros foram preparados para esta atividade com apoio de IA. Nenhum commit deve ser atribuído a Aquiles sem ele ter feito ou revisado aquela contribuição. A participação e a apresentação de cada integrante precisam acontecer de verdade.

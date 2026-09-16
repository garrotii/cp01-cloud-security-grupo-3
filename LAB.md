# Laboratório: njsscan + npm audit

Grupo 3: Leonardo Garroti, Aquiles Fonseca e Leandro de Souza. Tempo previsto em aula: 12 minutos, com a imagem pronta.

## 0. Preparação antes da aula

1. Instale Docker 24 ou mais recente, Docker Compose v2 e Git. O Docker deve usar containers Linux.
2. Baixe o repositório pelo botão **Code** no GitHub ou extraia o ZIP do trabalho. Abra o terminal na pasta que contém este arquivo.
3. Confira os programas:

```bash
docker --version
docker compose version
git --version
```

Resultado esperado: os três comandos mostram suas versões, sem erro.

4. Baixe a imagem base e prepare o laboratório:

```bash
docker pull node:24-bookworm-slim
docker compose build --pull lab
docker image inspect cp01-grupo3:1.0
```

Resultado esperado: o build termina sem erro e `image inspect` mostra os dados da imagem. O download e a instalação dos scanners não entram nos 12 minutos da aula.

Requisitos: 4 GB de memória livres, cerca de 3 GB em disco e internet. O npm audit usa o registro npm durante a execução. A aplicação não publica portas.

## 1. Executar a versão insegura (2 minutos)

```bash
docker compose run --rm lab inseguro
```

Resultado esperado: três ocorrências ERROR no njsscan, um pacote HIGH no npm audit e `BLOQUEADO` no gate. O comando termina com código **1**. Isso é o resultado esperado da versão insegura.

O script executa os dois scanners antes de aplicar o gate. Ele guarda JSON, SARIF e os tempos. Não confunda um pacote vulnerável com um único aviso de segurança.

## 2. Ler o resultado do código (2 minutos)

Abra `reports/inseguro/njsscan.json` no editor. Localize `express_xss`, `generic_os_command_exec` e `eval_nodejs`.

Resultado esperado: cada regra aponta uma ocorrência em `app.js`, com nível ERROR. O grupo classifica ERROR como HIGH para decidir se o build passa. O njsscan não forneceu nota CVSS para esses três alertas.

O que observar: a entrada enviada pelo usuário chega a uma resposta HTML, a `exec` ou a `eval`. As regras não foram ignoradas.

## 3. Ler o resultado das dependências (1 minuto)

Abra `reports/inseguro/npm-audit.json`. Encontre o pacote lodash, versão fixada no lockfile em 4.17.15, e a lista `via`.

Resultado esperado: lodash tem severidade HIGH. A lista reúne vários avisos, incluindo CVE-2020-8203. A contagem de pacotes HIGH é **1** na execução registrada.

O código usa `chunk`. O relatório confirma a versão vulnerável, mas não prova que todas as falhas da biblioteca sejam exploráveis nessa rota. A correção adotada foi atualizar a biblioteca.

## 4. Entender as correções (1 minuto)

Compare `targets/inseguro/app.js` com `targets/corrigido/app.js`:

- A resposta de nome passa a ser texto simples.
- A rota de comando passa a devolver uma mensagem fixa.
- A rota de cálculo soma números validados, sem `eval`.
- O pacote lodash passa de 4.17.15 para 4.18.1, no package.json e no lockfile.

Resultado esperado: a mudança resolve a causa dos alertas. Não há comentários de supressão para esconder as falhas.

## 5. Executar a versão corrigida (2 minutos)

```bash
docker compose run --rm lab corrigido
```

Resultado esperado na execução registrada: zero alertas no njsscan, zero pacotes vulneráveis no npm audit, `APROVADO` e código **0**. Novos avisos do registro npm podem mudar esse resultado em outra data. Se isso ocorrer, examine o novo relatório e corrija a dependência.

## 6. Mostrar os builds no GitHub (2 minutos)

No repositório publicado, abra **Actions > Segurança do grupo 3 > Run workflow**. Escolha `inseguro` e confirme a execução. Repita escolhendo `corrigido`.

Resultado esperado: a primeira execução falha por alertas HIGH, e a segunda passa. Abra o passo do gate e os relatórios anexados. Registre os links e prints das duas execuções. Estes registros precisam ser produzidos no GitHub, sem apresentar o gate local como build da plataforma.

Se a execução demorou mais que o tempo disponível, mostre os dois builds feitos antes da aula e explique os passos. Os colegas devem executar o laboratório local durante a apresentação.

## 7. Comprovante e perguntas (1 minuto)

Cada colega entrega um print do resultado final de sua própria execução e responde:

1. Quantas ocorrências ERROR o njsscan mostrou na versão insegura? Como o nosso gate trata esse nível?
2. Qual CWE o relatório associa ao uso de `eval`? Qual mudança retirou essa falha?

Gabarito do grupo: **3 ERROR**, tratados como HIGH. O uso de `eval` aparece como **CWE-95**. A correção soma dois números validados, sem avaliar texto como código.

Para deixar os próprios prints sem caminhos de pastas, mostre apenas a área do resultado, sem a linha que exibe a pasta do terminal. Os prints fornecidos pelo grupo são resumos dos seus relatórios locais e servem de plano B.

## 8. Encerrar

```bash
docker compose down
```

Resultado esperado: nenhum serviço deste Compose continua ativo. Os relatórios permanecem disponíveis. O uso de `run --rm` já remove o container ao fim de cada teste.

## Plano B

Abra `evidencias/index.html` no navegador e percorra as seis telas. Os seis PNGs acompanham a mesma sequência: preparação, SAST, SCA, gate bloqueado, correções e gate aprovado. Os JSONs permitem conferir os números.

## Problemas comuns

| Sintoma | Causa provável | Como resolver |
| --- | --- | --- |
| Docker não encontrado | Programa ausente ou terminal antigo | Instalar antes da aula e abrir um terminal novo |
| Erro de daemon | Docker não está iniciado | Iniciar o Docker e repetir a verificação |
| Erro de pip ou de pull | Falha de rede na preparação | Preparar antes da aula e repetir o build com internet |
| Erro no npm audit | Registro npm indisponível | Não tratar como zero alertas. Verificar a conexão e repetir |
| Código 1 no alvo inseguro | Gate encontrou falhas | Resultado esperado. Leia os relatórios |
| npm audit mostra mais alertas | A base recebeu novos avisos | Analisar o novo resultado e atualizar a correção |
| njsscan vazio no Windows nativo | libsast pula a análise semântica | Usar o container Linux. A ponte local está documentada |
| Sem permissão para gravar | Pasta reports não pode ser escrita | Conferir a pasta compartilhada com o Docker |

## Limite da validação registrada

Os scripts, os scanners, os relatórios e o gate foram executados localmente. O teste do Compose do zero depende de uma máquina com Docker, que não estava disponível no ambiente de preparação. Faça esse teste antes da aula e guarde a evidência. Datree e StackHawk fazem parte da pesquisa e não deste laboratório.

# 1. Introdução e objetivo

Uma aplicação pode ter problema no código, nas bibliotecas, na configuração da infraestrutura ou apenas quando está funcionando. Por isso, um único scanner não consegue verificar tudo.

O grupo 3 é formado por Leonardo Garroti, Aquiles Fonseca e Leandro de Souza. As ferramentas indicadas para o grupo são njsscan, npm audit, Datree e StackHawk. Elas representam SAST, SCA, segurança de infraestrutura como código e DAST.

O laboratório compara duas versões de uma aplicação pequena em Node.js. A primeira tem falhas colocadas de propósito. A segunda contém as correções. O objetivo é observar o que cada ferramenta encontra e entender por que o gate bloqueia ou aprova uma versão.

## Método usado

A pesquisa consultou a documentação e os repositórios dos projetos. O laboratório foi executado em Docker Desktop com WSL 2. O njsscan e o npm audit foram usados na prática. Datree e StackHawk foram estudados, mas não executados.

<!-- pagina -->
# 2. SAST, SCA, IaC e DAST

As quatro categorias olham partes diferentes do sistema.

| Categoria | O que verifica | Precisa da aplicação rodando? |
| SAST | Código escrito pela equipe | Não |
| SCA | Bibliotecas e suas versões | Não |
| IaC | Arquivos de infraestrutura | Não |
| DAST | Aplicação funcionando | Sim |

SAST e SCA costumam causar confusão. O SAST procura uma falha criada no próprio código. O SCA verifica se uma biblioteca usada pelo projeto possui um aviso de segurança conhecido.

No laboratório, retirar o uso de eval corrige um alerta SAST. Atualizar o lodash corrige o alerta SCA. Uma mudança não substitui a outra.

IaC ajuda a revisar arquivos como Kubernetes e Terraform antes da publicação. DAST envia requisições para a aplicação em execução. As quatro categorias se completam.

<!-- pagina -->
# 3. Pipeline, shift-left e SBOM

Um pipeline executa tarefas em sequência: obter o código, instalar dependências, testar e preparar uma versão. Os testes de segurança podem entrar nessa sequência.

| Etapa | Verificação adequada |
| Code | SAST e IaC |
| Build | SCA e criação da SBOM |
| Test | DAST |
| Deploy | Nova revisão da IaC |

Shift-left significa verificar mais cedo. Encontrar um eval perigoso durante o desenvolvimento custa menos do que descobrir o problema depois da entrega. Mesmo assim, o DAST continua necessário porque observa a aplicação completa funcionando.

SBOM é uma lista dos componentes usados pelo software. Ela ajuda a responder rapidamente se uma biblioteca com falha está presente. Neste trabalho, o npm gerou arquivos CycloneDX a partir dos lockfiles.

```
npm sbom --sbom-format=cyclonedx --package-lock-only
```

<!-- pagina -->
# 4. njsscan: identificação e situação do projeto

O njsscan é um scanner SAST para aplicações Node.js. Seu mantenedor é Ajin Abraham. A ferramenta é escrita em Python, usa libsast e chama o Semgrep para parte da análise. A licença indicada no projeto é LGPL-3.0.

O repositório consultado foi criado em 2020. A versão usada foi a 1.0.0, publicada em 2026. Na data da pesquisa, o projeto tinha 454 estrelas e 109 forks. Esses números mostram interesse, mas não garantem manutenção contínua.

O njsscan foi escolhido porque trabalha com Node.js, gera JSON, SARIF e HTML e consegue apontar a regra, a linha e o trecho do código. Isso facilita a explicação para quem está aprendendo.

O projeto teve uma atualização recente depois de um período com poucas mudanças. Por isso, uma equipe que usar a ferramenta deve acompanhar novas versões e revisar se as regras continuam atuais.

<!-- pagina -->
# 5. njsscan: funcionamento e cobertura

O njsscan procura padrões perigosos e também usa regras do Semgrep. Ele analisa a estrutura do código sem precisar iniciar a aplicação.

Na versão insegura, o relatório encontrou três problemas:

| Regra | Problema | CWE |
| express_xss | Entrada do usuário em HTML | CWE-79 |
| generic_os_command_exec | Entrada usada em comando | CWE-78 |
| eval_nodejs | Entrada usada em eval | CWE-95 |

A leitura do código confirmou os três casos. Por isso, eles foram classificados como verdadeiros positivos. A imagem desta página veio do relatório HTML criado pelo njsscan dentro do contêiner.

O scanner não encontra todo tipo de falha. Problemas de login, regra de negócio ou configuração em execução podem exigir outros testes.

<!-- pagina -->
# 6. njsscan: comandos e integração

A instalação pode ser feita com pip. No trabalho, as versões ficam fixadas para que todos usem o mesmo ambiente.

```
pip install njsscan==1.0.0
njsscan app.js --json -o njsscan.json
njsscan app.js --sarif -o njsscan.sarif
```

JSON é simples para ler e contar alertas. SARIF pode ser enviado para plataformas de análise de código. HTML é útil para uma demonstração visual.

O arquivo de configuração permite ignorar caminhos e escolher regras. Uma regra só deve ser ignorada depois de uma revisão e de uma justificativa escrita.

No pipeline preparado, o njsscan roda antes do gate. Um alerta ERROR é tratado como nível HIGH pela regra adotada pelo grupo. Essa regra serve para o laboratório e não cria uma nota CVSS.

<!-- pagina -->
# 7. npm audit: identificação e situação do projeto

O npm audit faz parte do npm CLI. Ele é usado em projetos JavaScript e Node.js para comparar as dependências do projeto com avisos de segurança conhecidos.

O npm CLI é mantido pela equipe do npm dentro da GitHub, empresa da Microsoft. O comando audit foi adicionado em 2018. O código é JavaScript e usa a licença Artistic-2.0.

A versão usada no contêiner foi a 11.12.0. O comando lê o package-lock.json e envia informações das dependências para o serviço de auditoria do registro npm.

A ferramenta é prática porque já faz parte do fluxo comum do Node.js. Sua principal limitação é depender da qualidade dos avisos publicados e da presença de um lockfile correto.

<!-- pagina -->
# 8. npm audit: resultado e interpretação

A versão insegura usa lodash 4.17.15. O npm audit encontrou um pacote com severidade HIGH. Esse pacote aparece em vários avisos, mas o resumo conta o pacote vulnerável uma vez.

A presença da versão vulnerável foi confirmada. Isso não prova que todos os avisos podem ser explorados pelas rotas do exemplo. Para responder essa pergunta, seria necessário analisar como cada função da biblioteca é usada.

No gate do laboratório, HIGH e CRITICAL bloqueiam a versão. Depois da atualização para lodash 4.18.1, o comando informou zero vulnerabilidades.

A imagem mostra a saída real do npm audit executado dentro do contêiner na versão insegura.

<!-- pagina -->
# 9. npm audit: comandos, integração e limites

Os comandos principais são curtos:

```
npm audit
npm audit --audit-level=high
npm audit --json
npm audit fix
```

`--audit-level=high` define o nível usado para o código de saída. `--json` cria um resultado que pode ser lido pelo gate. `npm audit fix` tenta atualizar pacotes dentro dos limites permitidos pelo projeto.

O uso de `--force` precisa de cuidado, pois pode instalar uma versão fora da faixa declarada. A equipe deve executar testes depois da atualização.

O npm audit pode entrar no CI logo depois da instalação das dependências. Ele também pode ser usado antes do commit, mas consultas frequentes dependem da rede e do serviço do registro.

Um resultado com zero vulnerabilidades significa apenas que nenhum aviso conhecido foi encontrado nas dependências analisadas naquele momento.

<!-- pagina -->
# 10. Datree: identificação e situação atual

Datree foi uma ferramenta de segurança para arquivos Kubernetes. O CLI era escrito em Go e distribuído com licença Apache-2.0. Ele avaliava arquivos YAML antes de chegarem ao cluster.

O projeto foi arquivado no GitHub em outubro de 2024. A própria empresa informou o fim da manutenção em 2023. A última versão encontrada foi a 1.9.19.

Esse estado muda a avaliação da ferramenta. Ela ainda ajuda a estudar regras de Kubernetes, mas não é uma boa escolha para iniciar um projeto novo que precisa receber atualizações.

O enunciado atribui Datree ao grupo, por isso o nome foi mantido na pesquisa. Para um uso real atual, seria melhor comparar alternativas mantidas, como Checkov, Trivy ou Kubescape.

<!-- pagina -->
# 11. Datree: funcionamento e exemplo de IaC

O Datree lê um arquivo Kubernetes, verifica se o YAML é válido e aplica regras de política. Uma regra pode avisar sobre privilégio alto, ausência de limites de recursos ou uso inseguro de imagem.

No exemplo inseguro do trabalho, o contêiner usa privilégio elevado e não define limites. Na versão corrigida, o privilégio é retirado, o sistema de arquivos fica somente para leitura e os recursos recebem limites.

```
datree test iac/pod-inseguro.yaml --schema-version 1.20.0
```

A análise acontece antes do deploy. Isso reduz a chance de uma configuração ruim chegar ao cluster.

A ferramenta não verifica o comportamento da aplicação, a segurança da imagem ou as permissões reais do ambiente. Esses pontos precisam de outras verificações.

<!-- pagina -->
# 12. Datree: uso e integração planejados

O CLI podia ser instalado por script, pacote ou contêiner. Também podia rodar em GitHub Actions, GitLab CI e outros sistemas de CI.

```
datree test iac/pod-inseguro.yaml --output json
```

Uma equipe podia criar políticas próprias e definir quais regras bloqueariam o pipeline. O modo offline permitia usar regras guardadas localmente.

Neste trabalho, o Datree não foi executado porque o projeto está arquivado. Foram mantidos apenas os arquivos de exemplo e a explicação do funcionamento.

Para adotar uma alternativa, o grupo deveria repetir o mesmo processo do laboratório: fixar versão, executar contra um exemplo conhecido, guardar o relatório e definir um gate claro.

<!-- pagina -->
# 13. StackHawk: identificação e situação atual

StackHawk é uma plataforma de testes DAST. Seu scanner é chamado HawkScan e utiliza uma base ligada ao OWASP ZAP. O uso comum acontece por contêiner.

A empresa StackHawk mantém a plataforma e a documentação. O serviço possui partes comerciais. Isso precisa ser explicado porque o trabalho pede ferramentas open source. A base do scanner tem origem aberta, mas a experiência completa depende da plataforma.

A versão 6.0.0 do HawkScan foi anunciada em 2026. O produto continua ativo. Mesmo assim, a equipe deve conferir plano, limites e necessidade de conta antes de usar em um projeto.

O StackHawk foi mantido na pesquisa por estar na lista do grupo. Ele não foi usado no laboratório obrigatório.

<!-- pagina -->
# 14. StackHawk: como o DAST funciona

O DAST testa a aplicação funcionando. Ele descobre rotas, envia entradas de teste e observa respostas. Isso permite encontrar problemas que dependem do servidor e da configuração do ambiente.

O fluxo básico é:

| Passo | Ação |
| 1 | Iniciar a aplicação de teste |
| 2 | Definir o endereço permitido |
| 3 | Executar o scanner |
| 4 | Revisar os alertas |
| 5 | Corrigir e testar novamente |

A autenticação exige configuração extra quando as rotas são protegidas. Sem isso, o scanner pode enxergar apenas a tela de login.

DAST pode gerar falso positivo e também deixar rotas sem teste. Ele deve ser executado somente contra um alvo próprio ou autorizado.

<!-- pagina -->
# 15. StackHawk: configuração e integração

A configuração usa um arquivo YAML com o endereço da aplicação, o identificador do projeto e opções de ambiente. Segredos devem ficar nas variáveis protegidas do CI.

```
docker run --rm -v "$PWD:/hawk" stackhawk/hawkscan:latest
```

Em uma equipe, é melhor fixar a versão da imagem em vez de usar `latest`. Isso evita que uma atualização mude o resultado sem aviso.

O scanner pode rodar depois que o ambiente de teste estiver disponível. O relatório precisa ser guardado como artefato. Antes de bloquear o build, a equipe deve revisar quais níveis são confiáveis para o projeto.

StackHawk não substitui SAST ou SCA. Ele observa o sistema por fora e não conhece todo o caminho interno do código.

<!-- pagina -->
# 16. Laboratório e ambiente Docker

O laboratório usa uma aplicação Node.js criada para a atividade. Há um alvo inseguro e outro corrigido. Os dois ficam na mesma imagem para facilitar a comparação.

O Dockerfile instala Node.js, Python, njsscan, Semgrep e npm. O Docker Compose executa o script de análise e grava os relatórios. A imagem criada recebeu o nome `cp01-grupo3:1.0`.

A construção e as duas execuções foram realizadas no Docker Desktop com WSL 2. A tela do Docker Desktop confirma a imagem local. A tela do terminal registra as versões e o identificador da imagem.

Esse ambiente evita que cada colega precise instalar todas as ferramentas diretamente no Windows.

<!-- pagina -->
# 17. Gate e comparação dos resultados

O gate lê os relatórios do njsscan e do npm audit. A política usada foi:

| Resultado | Decisão |
| SAST ERROR | Bloqueia como HIGH |
| SCA HIGH ou CRITICAL | Bloqueia |
| Sem alertas nesses níveis | Aprova |

Na versão insegura, três alertas SAST e um pacote HIGH produziram código de saída 1. O status foi BLOQUEADO.

Na versão corrigida, os dois scanners terminaram com código 0. O status foi APROVADO.

As imagens mostram as duas saídas reais do contêiner. O resultado aprovado cobre apenas os testes executados.

<!-- pagina -->
# 18. Avaliação crítica e conclusão

O laboratório mostrou por que SAST e SCA são diferentes. O njsscan encontrou falhas escritas no app.js. O npm audit encontrou uma versão vulnerável do lodash.

As correções também foram diferentes: retirar operações perigosas no código e atualizar a dependência. Depois disso, o gate aprovou a nova versão e o npm audit mostrou zero vulnerabilidades.

O njsscan é simples para um exemplo Node.js, mas depende das regras disponíveis. O npm audit é fácil de usar, mas depende dos avisos conhecidos. Datree está arquivado. StackHawk continua ativo, porém sua plataforma tem partes comerciais.

Para um projeto pequeno, a sequência sugerida é SAST e SCA desde o começo, análise de IaC antes do deploy e DAST em um ambiente de teste autorizado.

O resultado final não significa que a aplicação está livre de falhas. Ele mostra que os problemas preparados para o laboratório foram encontrados e corrigidos.

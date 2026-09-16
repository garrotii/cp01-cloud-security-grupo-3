# Apresentação em dupla

Leonardo Garroti e Aquiles Fonseca. Divisão sugerida, para ser combinada pela dupla.

| Bloco | Tempo | Quem fala | Slides |
| --- | --- | --- | --- |
| Abertura e categorias | 3 min | Leonardo | 1 a 5 |
| njsscan e npm audit | 5 min | Leonardo | 6 a 10 |
| Datree e StackHawk | 5 min | Aquiles | 11 a 15 |
| Laboratório com a turma | 12 min | Leonardo e Aquiles | 16 a 21 |
| Comparativo e conclusão | 3 min | Aquiles | 22 a 23 |
| Perguntas e fontes | 2 min | Os dois | 24 |

Total: 30 minutos. Prepare a imagem Docker e as execuções do GitHub antes da aula. O download não deve consumir o tempo do laboratório.

## Fala de abertura

“Nós somos Leonardo e Aquiles, do grupo 3. Nosso trabalho mostra quatro formas de procurar falhas. Duas delas foram usadas no laboratório. Primeiro vamos olhar o código, depois as bibliotecas que ele usa. Vamos mostrar uma versão com falhas, aplicar correções e repetir os testes.”

## Explicação dos resultados

“O njsscan achou três erros no código. O npm audit apontou um pacote com nível alto. Nosso gate bloqueou a versão insegura. Depois mudamos o código e atualizamos o lodash. Na execução registrada, os dois testes passaram. Isso cobre os testes feitos, mas não garante que qualquer falha possível tenha sido encontrada.”

## Pontos que os dois precisam saber

- SAST analisa o nosso código. SCA verifica versões de dependências.
- DAST precisa da aplicação rodando. SAST e SCA do laboratório não precisam.
- ERROR é o nível do njsscan. HIGH é o nível adotado pelo nosso gate.
- O npm audit conta um pacote vulnerável, que pode reunir vários avisos.
- Datree está arquivado. StackHawk usa uma plataforma comercial.
- Uma lista de componentes, chamada SBOM, ajuda a acompanhar as dependências.
- As telas do plano B mostram execução local real. Só os registros da plataforma provam builds do GitHub.

## Plano B e ensaio

Se a rede falhar, abra as seis telas de evidência na ordem. Explique cada resultado usando os JSONs. Não diga que uma tela local é um build do GitHub.

Façam um ensaio com cronômetro. Aquiles pode ajudar os colegas que tiveram erro enquanto Leonardo explica o comando, e depois os dois trocam de função. Cada um deve apresentar parte do conteúdo e saber responder sobre o conjunto.

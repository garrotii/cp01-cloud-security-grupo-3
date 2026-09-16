# Conferência da entrega

## Pronto

- Pesquisa em PDF com capa, sumário, 18 páginas de conteúdo, referências e anexos.
- Apresentação com 29 slides, notas para a fala, nove imagens reais e cópia em PDF.
- Laboratório próprio em Node.js com versões insegura e corrigida.
- Duas categorias executadas: njsscan (SAST) e npm audit (SCA).
- Três falhas reais no código: XSS, execução de comando e uso de `eval`.
- Uma dependência vulnerável na versão insegura e atualizada na corrigida.
- Gate que bloqueia HIGH e CRITICAL, além de erros de execução e relatórios inválidos.
- Relatórios JSON, SARIF, SBOM, tempos e nove capturas reais do Docker Desktop, dos scanners, do terminal e do GitHub Actions, sem caminhos de pastas.
- Dockerfile, Docker Compose, roteiro do laboratório e fluxo do GitHub Actions.
- Plano B em GIF com 5 minutos e 20 segundos, usando os prints reais e os relatórios locais.

## Execuções publicadas

- A versão `inseguro` foi bloqueada na execução 35144999487.
- A versão `corrigido` foi aprovada na execução 35144977032.
- Os links estão em `docs/EXECUCOES-GITHUB.md`.

## Fazer antes da aula

1. Aquiles e Leandro devem revisar de verdade o material e registrar suas próprias contribuições.
2. Repetir, se desejado, os dois comandos do `LAB.md`; a construção e as duas execuções no Docker já foram validadas neste computador.
3. Confirmar que o teste inseguro termina com código 1 e o corrigido com código 0.
4. Ensaiar a apresentação com os três integrantes para caber em 30 minutos.
5. Cada integrante deve fazer sua própria execução, tirar seu print e responder às duas perguntas.

Não use commits ou falas falsas para representar a participação de outra pessoa. O histórico do Git deve mostrar apenas contribuições que realmente aconteceram.

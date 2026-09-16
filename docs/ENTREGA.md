# Conferência da entrega

## Pronto

- Pesquisa em PDF com capa, sumário, 18 páginas de conteúdo, referências e anexos.
- Apresentação com 24 slides, notas para a fala e cópia em PDF.
- Laboratório próprio em Node.js com versões insegura e corrigida.
- Duas categorias executadas: njsscan (SAST) e npm audit (SCA).
- Três falhas reais no código: XSS, execução de comando e uso de `eval`.
- Uma dependência vulnerável na versão insegura e atualizada na corrigida.
- Gate que bloqueia HIGH e CRITICAL, além de erros de execução e relatórios inválidos.
- Relatórios JSON, SARIF, SBOM, tempos e oito prints das saídas reais sem caminhos de pastas.
- Dockerfile, Docker Compose, roteiro do laboratório e fluxo do GitHub Actions.
- Plano B com os prints e os relatórios locais.

## Conferir depois da publicação

1. Abrir o repositório no GitHub e confirmar que todas as pastas foram enviadas.
2. Rodar o fluxo manual com `inseguro` e guardar o link do build vermelho.
3. Rodar o fluxo manual com `corrigido` e guardar o link do build verde.
4. Baixar os artefatos dos dois builds e conferir os relatórios.
5. Proteger a branch principal para exigir o teste de segurança, se o professor pedir.

## Fazer antes da aula

1. Aquiles deve revisar de verdade o material e registrar sua própria contribuição.
2. Em uma máquina com Docker, preparar a imagem do zero e rodar os dois comandos do `LAB.md`.
3. Confirmar que o teste inseguro termina com código 1 e o corrigido com código 0.
4. Ensaiar a apresentação em dupla para caber em 30 minutos.
5. Cada integrante deve fazer sua própria execução, tirar seu print e responder às duas perguntas.

Não use commits ou falas falsas para representar a participação de outra pessoa. O histórico do Git deve mostrar apenas contribuições que realmente aconteceram.

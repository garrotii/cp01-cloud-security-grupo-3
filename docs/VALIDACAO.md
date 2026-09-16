# O que foi validado

## Formatação do relatório

O PDF usa papel A4, fonte Arial e margens de 3 cm na parte superior e esquerda e 2 cm na parte inferior e direita. O texto geral está em tamanho 12, justificado, com entrelinha exata de 18 pontos, que corresponde a 1,5, e recuo de 1,25 cm na primeira linha. Referências, códigos, paginação e legendas usam espaçamento simples; paginação e legendas usam tamanho 10. As sete capturas reais aparecem junto das explicações relacionadas, sem linha de fonte e sem caminhos de pastas nas imagens. As linhas “Fonte:” e “Fontes:” também foram retiradas do fim das páginas de conteúdo.

## Execução registrada

Data: 16/09/2026. Ambiente final: Docker Desktop 29.8.0, Docker Compose 5.5.1, WSL 2 com Ubuntu e contêiner Linux baseado em Node 24. O contêiner usa npm 11.12.0, njsscan 1.0.0, Semgrep 1.172.0 e libsast 3.1.8.

O npm audit e o njsscan foram executados dentro do contêiner Linux. A versão insegura terminou bloqueada, com três alertas SAST e uma dependência HIGH. A versão corrigida terminou aprovada, sem alertas. Nenhum alerta foi criado à mão.

O JSON e o SARIF foram gerados pelos exportadores do njsscan. O arquivo execucao.json registra `adaptacao_windows: true`. No Linux, o script scan.py usa `python -m njsscan`, sem a ponte. O README oficial do njsscan ainda indica suporte a Mac e Linux, por isso o container Linux é a forma recomendada para a turma.

## Resultados

| Alvo | SAST ERROR | Pacotes SCA HIGH | Gate |
| --- | --- | --- | --- |
| Inseguro | 3 | 1 | 1, bloqueado |
| Corrigido | 0 | 0 | 0, aprovado |

Os tempos medidos estão em reports de cada alvo. A geração do SARIF faz uma segunda análise e tem seu próprio tempo. Não somamos duas análises para fingir o tempo de uma única execução.

As três ocorrências SAST foram revisadas pelo código. A biblioteca lodash foi conferida no lockfile e no registro de avisos. A SBOM CycloneDX foi gerada por npm sbom a partir do lockfile.

## Limites

- O Dockerfile foi construído do zero e o Compose executou os alvos `inseguro` e `corrigido` neste computador.
- Datree e StackHawk não foram executados. Não há tempos ou taxas de falso positivo medidos para eles.
- O relatório usa sete capturas reais: tela da imagem no Docker Desktop, ambiente Docker/WSL, relatório HTML do njsscan, npm audit inseguro, gate bloqueado, gate aprovado e npm audit corrigido. Elas não são execuções do GitHub Actions.
- Os builds vermelho e verde no GitHub devem ser conferidos na plataforma após a publicação. O gate local não prova que os serviços do GitHub funcionaram.
- Ensaio em dupla, participação na aula, revisão de Aquiles e publicação antecipada precisam acontecer de verdade.

# Três achados reais do laboratório

As três ocorrências abaixo estão no JSON do njsscan da versão insegura. A revisão usou o caminho da entrada até a operação perigosa no código. Não foi preciso executar comandos recebidos por HTTP. Os resultados no Windows usaram a ponte descrita em VALIDACAO.md.

## 1. HTML com entrada do usuário

- Regra: `express_xss`.
- Local: `targets/inseguro/app.js`, linhas 8 a 9.
- Tipo: CWE-79, Cross-site Scripting (XSS).
- Nível original: ERROR. Nível adotado pelo gate: HIGH.
- Classificação: **verdadeiro positivo**.

O usuário controla `req.query.nome`. O código coloca esse valor dentro de uma resposta HTML e usa `res.send`, sem transformar caracteres especiais. O navegador pode interpretar a entrada como parte da página. A aplicação é própria e essa falha foi escrita de propósito para o laboratório.

Correção: devolver `text/plain` e limitar o tamanho da entrada. Se a necessidade fosse produzir HTML, seria preciso usar escape adequado ao local da página. A correção adotada mantém a função de mostrar um nome, mas usa texto simples. A regra deixou de aparecer no relatório da versão corrigida.

## 2. Comando controlado pelo usuário

- Regra: `generic_os_command_exec`.
- Local: `targets/inseguro/app.js`, linhas 12 a 14.
- Tipo: CWE-78, OS Command Injection.
- Nível original: ERROR. Nível adotado pelo gate: HIGH.
- Classificação: **verdadeiro positivo**.

O valor `req.query.cmd` chega diretamente a `child_process.exec`. O usuário pode escolher o texto executado pelo processo. Não há uma lista de opções permitidas nem separação segura entre programa e argumentos. A leitura do código confirma a condição apontada pela regra. Nenhum comando perigoso precisou ser enviado à rota durante a validação.

Correção: retirar a execução de comandos. A rota corrigida retorna uma mensagem fixa. Para uma necessidade real de executar uma ferramenta, seria preciso escolher um programa fixo, validar os argumentos e limitar as permissões. Essa necessidade não existe neste alvo de aula.

## 3. Texto tratado como código

- Regra: `eval_nodejs`.
- Local: `targets/inseguro/app.js`, linha 17.
- Tipo: CWE-95, Eval Injection.
- Nível original: ERROR. Nível adotado pelo gate: HIGH.
- Classificação: **verdadeiro positivo**.

O usuário controla `req.query.expr`, e `eval` avalia o texto como JavaScript. Uma calculadora simples não precisa aceitar um programa enviado pelo usuário. Essa condição torna o alerta coerente com o código analisado.

Correção: receber dois números, validar com `Number.isFinite` e executar apenas a soma prevista. O teste do scanner não encontrou a regra na versão corrigida.

## OWASP, CVE, CVSS e falsos positivos

Os três achados se relacionam com **A05:2025 - Injection**. A relação com a edição 2025 foi feita pelo grupo. A ferramenta mantém rótulos OWASP antigos em suas regras, que não devem ser apresentados como a numeração atual.

Esses três exemplos próprios não receberam CVE nem nota CVSS pelo scanner. CWE descreve o tipo de erro. CVE identifica uma falha publicada. CVSS é uma avaliação de severidade com condições definidas.

Na amostra revisada, houve **0 falso positivo em 3 alertas SAST**, ou 0%. A amostra é pequena e contém falhas intencionais, então não permite dizer que o njsscan terá 0% de falso positivo em projetos reais.

No npm audit, a versão lodash 4.17.15 também foi confirmada no lockfile. Um exemplo do aviso é CVE-2020-8203, CWE-1321, CVSS 7,4. A presença do pacote vulnerável é um verdadeiro positivo de inventário. O uso de `chunk` nesta rota não confirma exploração das funções afetadas, e essa diferença deve ser explicada na apresentação.

Fontes: relatórios versionados do laboratório, MITRE CWE-78, CWE-79 e CWE-95, OWASP Top 10:2025 e GitHub Advisory Database. Veja REFERENCIAS.md.

// Aplicação própria com falhas de propósito. Usar somente no laboratório local.
const express = require('express');
const { exec } = require('child_process');
const _ = require('lodash');
const app = express();
app.get('/', (req, res) => res.type('text').send('Laboratório do grupo 3'));
app.get('/ola', function (req, res) {
  const nome = req.query.nome;
  res.send('<h1>Olá, ' + nome + '</h1>');
});
app.get('/comando', function (req, res) {
  exec(req.query.cmd, function (erro, saida) {
    res.type('text').send(erro ? 'Erro' : saida);
  });
});
app.get('/calculo', function (req, res) {
  const resultado = eval(req.query.expr);
  res.json({ resultado });
});
app.get('/lista', (req, res) => res.json(_.chunk([1, 2, 3, 4], 2)));
// O processo não aceita conexões externas por padrão.
app.listen(3000, '127.0.0.1');

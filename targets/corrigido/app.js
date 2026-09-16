const express = require('express');
const _ = require('lodash');
const app = express();
app.get('/', (req, res) => res.type('text').send('Laboratório do grupo 3'));
app.get('/ola', function (req, res) {
  const nome = String(req.query.nome || 'colega').slice(0, 80);
  // Texto simples: o navegador não interpreta a entrada como HTML.
  res.type('text/plain').send('Olá, ' + nome);
});
app.get('/comando', function (req, res) {
  // A necessidade era mostrar uma informação, sem executar comandos recebidos.
  res.json({ mensagem: 'Laboratório do grupo 3' });
});
app.get('/calculo', function (req, res) {
  const a = Number(req.query.a);
  const b = Number(req.query.b);
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    return res.status(400).json({ erro: 'Informe dois números válidos' });
  }
  res.json({ resultado: a + b });
});
app.get('/lista', (req, res) => res.json(_.chunk([1, 2, 3, 4], 2)));
app.listen(3000, '127.0.0.1');

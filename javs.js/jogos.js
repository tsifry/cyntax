(function () {
    'use strict';
 
    var $ = function (id) { return document.getElementById(id); };
    var reduzMovimento = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 
    /* ---------- utilidades ---------- */
    function embaralhar(lista) {
        var a = lista.slice();
        for (var i = a.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
    }
 
    function lerRecorde(chave) {
        try {
            var v = localStorage.getItem('cyntax-' + chave);
            return v === null ? null : Number(v);
        } catch (e) { return null; }
    }
 
    function salvarRecorde(chave, valor) {
        try { localStorage.setItem('cyntax-' + chave, String(valor)); } catch (e) {}
    }
 
    function numero(n) {
        return n.toLocaleString('pt-BR', { maximumFractionDigits: 1 });
    }
 
    function mensagem(el, texto, tipo) {
        el.textContent = texto;
        el.classList.remove('ok', 'erro');
        if (tipo) el.classList.add(tipo);
    }
 
    /* =========================================================
       ABAS (seletor de jogos), com navegação pelas setas
       ========================================================= */
    var abas = Array.prototype.slice.call(document.querySelectorAll('.seletor-card'));
 
    function selecionar(aba, focar) {
        abas.forEach(function (a) {
            var ativa = a === aba;
            a.setAttribute('aria-selected', String(ativa));
            a.tabIndex = ativa ? 0 : -1;
            $(a.getAttribute('aria-controls')).hidden = !ativa;
        });
        if (focar) aba.focus();
    }
 
    abas.forEach(function (aba, i) {
        aba.addEventListener('click', function () { selecionar(aba, false); });
        aba.addEventListener('keydown', function (e) {
            var destino = null;
            if (e.key === 'ArrowRight') destino = abas[(i + 1) % abas.length];
            if (e.key === 'ArrowLeft')  destino = abas[(i - 1 + abas.length) % abas.length];
            if (e.key === 'Home')       destino = abas[0];
            if (e.key === 'End')        destino = abas[abas.length - 1];
            if (destino) { e.preventDefault(); selecionar(destino, true); }
        });
    });
 
    /* =========================================================
       JOGO 1: QUIZ RELÂMPAGO
       (a primeira alternativa de cada pergunta é a correta; as opções são embaralhadas)
       ========================================================= */
    var PERGUNTAS = [
        { p: 'Qual é a unidade de força no Sistema Internacional?',
          o: ['Newton (N)', 'Joule (J)', 'Watt (W)', 'Pascal (Pa)'] },
        { p: 'Qual é o valor aproximado da aceleração da gravidade na superfície da Terra?',
          o: ['9,8 m/s²', '1,6 m/s²', '98 m/s²', '0,98 m/s²'] },
        { p: 'Qual grandeza mede a rapidez com que a velocidade de um corpo varia?',
          o: ['Aceleração', 'Massa', 'Trabalho', 'Potência'] },
        { p: 'Pela 1ª Lei de Newton, um corpo sem força resultante:',
          o: ['Mantém o repouso ou o movimento retilíneo uniforme', 'Para imediatamente', 'Aumenta sempre a velocidade', 'Perde massa'] },
        { p: 'Qual é o valor aproximado da velocidade da luz no vácuo?',
          o: ['3 × 10⁸ m/s', '3 × 10⁶ m/s', '340 m/s', '300 m/s'] }
    ];
 
    var quiz = { fila: [], i: 0, pontos: 0, respondida: false };
 
    function iniciarQuiz() {
        quiz.fila = embaralhar(PERGUNTAS).map(function (q) {
            return { p: q.p, certa: q.o[0], o: embaralhar(q.o) };
        });
        quiz.i = 0;
        quiz.pontos = 0;
        $('quiz-fim').hidden = true;
        $('quiz-jogo').hidden = false;
        mostrarPergunta(false);
    }
 
    function atualizarBarra(valor) {
        var total = quiz.fila.length;
        $('quiz-barra').style.width = (valor / total * 100) + '%';
        $('quiz-trilho').setAttribute('aria-valuenow', String(valor));
    }
 
    function mostrarPergunta(focar) {
        var q = quiz.fila[quiz.i];
        var total = quiz.fila.length;
        quiz.respondida = false;
 
        $('quiz-contador').textContent = 'Pergunta ' + (quiz.i + 1) + ' de ' + total;
        $('quiz-pontos').textContent = 'Pontos: ' + quiz.pontos;
        atualizarBarra(quiz.i);
        $('quiz-pergunta').textContent = q.p;
        mensagem($('quiz-feedback'), '');
        $('quiz-proxima').hidden = true;
 
        var caixa = $('quiz-opcoes');
        caixa.innerHTML = '';
        q.o.forEach(function (texto) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'opcao';
            b.textContent = texto;
            b.addEventListener('click', function () { responder(b, texto); });
            caixa.appendChild(b);
        });
        if (focar) caixa.firstChild.focus();
    }
 
    function responder(botao, texto) {
        if (quiz.respondida) return;
        quiz.respondida = true;
 
        var q = quiz.fila[quiz.i];
        var acertou = texto === q.certa;
        if (acertou) quiz.pontos++;
 
        Array.prototype.forEach.call($('quiz-opcoes').children, function (b) {
            b.disabled = true;
            if (b.textContent === q.certa) b.classList.add('correta');
        });
        if (!acertou) botao.classList.add('errada');
 
        $('quiz-pontos').textContent = 'Pontos: ' + quiz.pontos;
        mensagem($('quiz-feedback'),
            acertou ? '✓ Correto!' : '✕ Não foi dessa vez. A resposta certa é: ' + q.certa,
            acertou ? 'ok' : 'erro');
 
        var ultima = quiz.i === quiz.fila.length - 1;
        var prox = $('quiz-proxima');
        prox.textContent = ultima ? 'Ver resultado' : 'Próxima pergunta';
        prox.hidden = false;
        prox.focus();
    }
 
    function fimQuiz() {
        var total = quiz.fila.length;
        atualizarBarra(total);
        $('quiz-jogo').hidden = true;
        $('quiz-fim').hidden = false;
 
        $('quiz-resultado').textContent = 'Você acertou ' + quiz.pontos + ' de ' + total + '!';
 
        var rec = lerRecorde('quiz');
        var msg;
        if (quiz.pontos === total) msg = 'Perfeito! Você domina o básico de física.';
        else if (quiz.pontos >= 3) msg = 'Muito bem! Falta pouco para a pontuação máxima.';
        else msg = 'Continue estudando os módulos e tente de novo.';
 
        if (rec === null || quiz.pontos > rec) {
            salvarRecorde('quiz', quiz.pontos);
            if (quiz.pontos > 0) msg += ' Novo recorde!';
        }
        mensagem($('quiz-mensagem'), msg);
        mostrarRecordes();
        $('quiz-resultado').focus();
    }
 
    $('quiz-proxima').addEventListener('click', function () {
        quiz.i++;
        if (quiz.i >= quiz.fila.length) fimQuiz();
        else mostrarPergunta(true);
    });
    $('quiz-reiniciar').addEventListener('click', function () {
        iniciarQuiz();
        $('quiz-opcoes').firstChild.focus();
    });
 
    /* =========================================================
       JOGO 2: MEMÓRIA DAS UNIDADES
       ========================================================= */
    var PARES = [
        { grandeza: 'Força',           simbolo: 'N',  nome: 'newton' },
        { grandeza: 'Energia',         simbolo: 'J',  nome: 'joule' },
        { grandeza: 'Potência',        simbolo: 'W',  nome: 'watt' },
        { grandeza: 'Pressão',         simbolo: 'Pa', nome: 'pascal' },
        { grandeza: 'Frequência',      simbolo: 'Hz', nome: 'hertz' },
        { grandeza: 'Tensão elétrica', simbolo: 'V',  nome: 'volt' }
    ];
 
    var mem = { primeira: null, bloqueio: false, jogadas: 0, pares: 0 };
 
    function montarCarta(botao, aberta) {
        var d = botao.dataset;
        botao.classList.toggle('aberta', aberta && !botao.classList.contains('par'));
 
        if (!aberta) {
            botao.innerHTML = '<span class="verso" aria-hidden="true">?</span>';
            botao.setAttribute('aria-label', 'Carta ' + d.n + ', virada para baixo. Virar.');
            return;
        }
        if (d.tipo === 'grandeza') {
            botao.innerHTML = '<span class="tipo">Grandeza</span><span class="valor">' + d.grandeza + '</span>';
            botao.setAttribute('aria-label', 'Carta ' + d.n + ': grandeza ' + d.grandeza);
        } else {
            botao.innerHTML = '<span class="tipo">Unidade</span><span class="valor">' + d.simbolo + '</span><span class="nome">' + d.nome + '</span>';
            botao.setAttribute('aria-label', 'Carta ' + d.n + ': unidade ' + d.nome + ', símbolo ' + d.simbolo);
        }
    }
 
    function iniciarMemoria() {
        mem.primeira = null;
        mem.bloqueio = false;
        mem.jogadas = 0;
        mem.pares = 0;
        $('mem-jogadas').textContent = '0';
        $('mem-pares').textContent = '0';
        mensagem($('mem-feedback'), '');
 
        var cartas = [];
        PARES.forEach(function (p, id) {
            cartas.push({ id: id, tipo: 'grandeza', p: p });
            cartas.push({ id: id, tipo: 'unidade', p: p });
        });
 
        var grade = $('mem-grade');
        grade.innerHTML = '';
        embaralhar(cartas).forEach(function (c, i) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'carta';
            b.dataset.id = c.id;
            b.dataset.tipo = c.tipo;
            b.dataset.n = i + 1;
            b.dataset.grandeza = c.p.grandeza;
            b.dataset.simbolo = c.p.simbolo;
            b.dataset.nome = c.p.nome;
            montarCarta(b, false);
            b.addEventListener('click', function () { virar(b); });
            grade.appendChild(b);
        });
    }
 
    function virar(carta) {
        if (mem.bloqueio || carta === mem.primeira || carta.classList.contains('par')) return;
 
        montarCarta(carta, true);
 
        if (!mem.primeira) { mem.primeira = carta; return; }
 
        var a = mem.primeira;
        var b = carta;
        mem.jogadas++;
        $('mem-jogadas').textContent = String(mem.jogadas);
 
        if (a.dataset.id === b.dataset.id && a.dataset.tipo !== b.dataset.tipo) {
            [a, b].forEach(function (c) {
                c.classList.add('par');
                c.disabled = true;
                montarCarta(c, true);
            });
            mem.pares++;
            mem.primeira = null;
            $('mem-pares').textContent = String(mem.pares);
            var p = PARES[Number(a.dataset.id)];
            mensagem($('mem-feedback'), '✓ Par encontrado: ' + p.grandeza + ' e ' + p.nome + ' (' + p.simbolo + ').', 'ok');
            if (mem.pares === PARES.length) fimMemoria();
        } else {
            mem.bloqueio = true;
            mensagem($('mem-feedback'), '✕ Essas cartas não combinam.', 'erro');
            setTimeout(function () {
                montarCarta(a, false);
                montarCarta(b, false);
                mem.primeira = null;
                mem.bloqueio = false;
            }, reduzMovimento ? 1500 : 1000);
        }
    }
 
    function fimMemoria() {
        var rec = lerRecorde('memoria');
        var texto = 'Parabéns! Você encontrou todos os pares em ' + mem.jogadas + ' jogadas.';
        if (rec === null || mem.jogadas < rec) {
            salvarRecorde('memoria', mem.jogadas);
            texto += ' Novo recorde!';
        }
        mensagem($('mem-feedback'), texto, 'ok');
        mostrarRecordes();
    }
 
    $('mem-reiniciar').addEventListener('click', iniciarMemoria);
 
    /* =========================================================
       JOGO 3: LANÇAMENTO AO ALVO
       ========================================================= */
    var V = 20;          /* m/s */
    var G = 10;          /* m/s² */
    var X0 = 30;         /* posição do canhão no SVG (px) */
    var Y0 = 170;        /* altura do chão no SVG (px) */
    var ESC = 10.8;      /* px por metro */
    var MARGEM = 2;      /* m */
    var TENTATIVAS = 5;
 
    var lanc = { alvo: 0, restam: TENTATIVAS, fim: false, ocupado: false };
 
    function novoAlvo() {
        lanc.alvo = 12 + Math.floor(Math.random() * 27);   /* 12 a 38 m */
        lanc.restam = TENTATIVAS;
        lanc.fim = false;
        lanc.ocupado = false;
 
        $('lanc-alvo').textContent = String(lanc.alvo);
        $('lanc-restam').textContent = String(lanc.restam);
 
        var zona = $('lanc-zona');
        zona.setAttribute('x', String(X0 + (lanc.alvo - MARGEM) * ESC));
        zona.setAttribute('width', String(MARGEM * 2 * ESC));
 
        $('lanc-trajetoria').setAttribute('d', '');
        $('lanc-impacto').style.display = 'none';
        $('lanc-lancar').disabled = false;
        mensagem($('lanc-feedback'), '');
    }
 
    function atualizarCano() {
        var ang = Number($('lanc-angulo').value);
        $('lanc-angulo-valor').textContent = ang + '°';
        $('lanc-cano').setAttribute('transform', 'rotate(' + (-ang) + ')');
    }
 
    function lancar() {
        if (lanc.fim || lanc.ocupado) return;
        lanc.ocupado = true;
        $('lanc-lancar').disabled = true;
 
        var ang = Number($('lanc-angulo').value);
        var rad = ang * Math.PI / 180;
        var tempo = 2 * V * Math.sin(rad) / G;
        var alcance = V * V * Math.sin(2 * rad) / G;
 
        /* monta a parábola */
        var d = '';
        var N = 48;
        for (var i = 0; i <= N; i++) {
            var t = tempo * i / N;
            var x = V * Math.cos(rad) * t;
            var y = V * Math.sin(rad) * t - 0.5 * G * t * t;
            d += (i === 0 ? 'M' : 'L') + (X0 + x * ESC).toFixed(1) + ' ' + (Y0 - y * ESC).toFixed(1) + ' ';
        }
 
        var traj = $('lanc-trajetoria');
        var impacto = $('lanc-impacto');
        impacto.style.display = 'none';
        traj.setAttribute('d', d);
 
        var duracao = reduzMovimento ? 0 : 1000;
        if (!reduzMovimento) {
            var comp = traj.getTotalLength();
            traj.style.transition = 'none';
            traj.style.strokeDasharray = comp;
            traj.style.strokeDashoffset = comp;
            void traj.getBoundingClientRect();
            traj.style.transition = 'stroke-dashoffset 1s linear';
            traj.style.strokeDashoffset = 0;
        } else {
            traj.style.strokeDasharray = 'none';
            traj.style.strokeDashoffset = 0;
        }
 
        setTimeout(function () {
            impacto.setAttribute('cx', String(X0 + alcance * ESC));
            impacto.style.display = '';
            resultadoLancamento(alcance);
        }, duracao);
    }
 
    function resultadoLancamento(alcance) {
        var diff = alcance - lanc.alvo;
        var usadas = TENTATIVAS - lanc.restam + 1;
        lanc.restam--;
        $('lanc-restam').textContent = String(lanc.restam);
        lanc.ocupado = false;
 
        var fb = $('lanc-feedback');
 
        if (Math.abs(diff) <= MARGEM) {
            lanc.fim = true;
            var texto = '✓ Acertou! O projétil caiu a ' + numero(alcance) + ' m, dentro da margem do alvo. Tentativas usadas: ' + usadas + '.';
            var rec = lerRecorde('lancamento');
            if (rec === null || usadas < rec) {
                salvarRecorde('lancamento', usadas);
                texto += ' Novo recorde!';
            }
            mensagem(fb, texto, 'ok');
            mostrarRecordes();
            return;
        }
 
        var dica = diff > 0
            ? 'Passou do alvo: caiu a ' + numero(alcance) + ' m (' + numero(diff) + ' m além).'
            : 'Ficou curto: caiu a ' + numero(alcance) + ' m (faltaram ' + numero(-diff) + ' m).';
 
        if (lanc.restam === 0) {
            lanc.fim = true;
            var a1 = 0.5 * Math.asin(lanc.alvo * G / (V * V)) * 180 / Math.PI;
            mensagem(fb, '✕ ' + dica + ' Acabaram as tentativas. Os ângulos certos eram cerca de ' + numero(a1) + '° ou ' + numero(90 - a1) + '°. Clique em "Novo alvo" para tentar de novo.', 'erro');
        } else {
            mensagem(fb, '✕ ' + dica + ' Ajuste o ângulo e tente de novo.', 'erro');
            $('lanc-lancar').disabled = false;
        }
    }
 
    $('lanc-angulo').addEventListener('input', atualizarCano);
    $('lanc-lancar').addEventListener('click', lancar);
    $('lanc-novo').addEventListener('click', novoAlvo);
 
    /* =========================================================
       RECORDES
       ========================================================= */
    function mostrarRecordes() {
        var q = lerRecorde('quiz');
        var m = lerRecorde('memoria');
        var l = lerRecorde('lancamento');
        $('recorde-quiz').textContent = 'Recorde: ' + (q === null ? '–' : q + ' de 5');
        $('recorde-memoria').textContent = 'Recorde: ' + (m === null ? '–' : m + ' jogadas');
        $('recorde-lancamento').textContent = 'Recorde: ' + (l === null ? '–' : 'acerto em ' + l + (l === 1 ? ' tentativa' : ' tentativas'));
    }
 
    /* ---------- início ---------- */
    iniciarQuiz();
    iniciarMemoria();
    novoAlvo();
    atualizarCano();
    mostrarRecordes();
})();
 

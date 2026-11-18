(function () {
    'use strict';
 

    document.querySelectorAll('.btn-olho').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var campo = document.getElementById(btn.dataset.alvo);
            var mostrar = campo.type === 'password';
 
            campo.type = mostrar ? 'text' : 'password';
            btn.setAttribute('aria-pressed', String(mostrar));
            btn.setAttribute('aria-label', mostrar ? 'Ocultar senha' : 'Mostrar senha');
            btn.querySelector('ion-icon').setAttribute('name', mostrar ? 'eye-off-outline' : 'eye-outline');
        });
    });
 
    
    var senha = document.getElementById('senha');
    var barra = document.getElementById('forca');
    var texto = document.getElementById('forca-texto');
    if (!senha || !barra || !texto) return;
 
    var NOMES = ['digite uma senha.', 'fraca.', 'média.', 'forte.'];
 
    function calcularForca(v) {
        if (!v) return 0;
        if (v.length < 8) return 1;          
 
        var pontos = 1;                        
        if (v.length >= 12) pontos++;
        if (/[a-z]/.test(v) && /[A-Z]/.test(v)) pontos++;
        if (/[0-9]/.test(v)) pontos++;
        if (/[^A-Za-z0-9]/.test(v)) pontos++;
 
        return pontos >= 5 ? 3 : pontos >= 3 ? 2 : 1;
    }
 
    senha.addEventListener('input', function () {
        var nivel = calcularForca(senha.value);
        barra.setAttribute('data-nivel', String(nivel));
        texto.textContent = 'Força da senha: ' + NOMES[nivel];
    });
})();
 

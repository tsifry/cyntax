// Partes da página que serão alteradas (o painel fica de fora de propósito)
const alvos = document.querySelectorAll("header, .container, .beneficios, .explicacao, footer");

const btnAcess = document.getElementById("btnAcess");
const painel = document.getElementById("painelAcess");

let zoom = 1;
let filtros = { contraste: false, cinza: false, daltonismo: false };

// Abrir e fechar o painel
btnAcess.addEventListener("click", function() {
    painel.hidden = !painel.hidden;
});

// Fechar com a tecla Esc
document.addEventListener("keydown", function(evento) {
    if (evento.key === "Escape") {
        painel.hidden = true;
    }
});

// Aumentar e diminuir a fonte
function aplicarZoom() {
    alvos.forEach(function(el) {
        el.style.zoom = zoom;
    });
}

document.getElementById("fonteMais").addEventListener("click", function() {
    if (zoom < 1.5) {
        zoom += 0.1;
        aplicarZoom();
    }
});

document.getElementById("fonteMenos").addEventListener("click", function() {
    if (zoom > 0.8) {
        zoom -= 0.1;
        aplicarZoom();
    }
});

// Filtros de cor
function aplicarFiltros() {
    let texto = "";

    if (filtros.contraste) texto += "contrast(1.5) ";
    if (filtros.cinza) texto += "grayscale(1) ";
    if (filtros.daltonismo) texto += "saturate(1.6) contrast(1.2) hue-rotate(20deg) ";

    alvos.forEach(function(el) {
        el.style.filter = texto;
    });
}

document.getElementById("contraste").addEventListener("click", function() {
    filtros.contraste = !filtros.contraste;
    aplicarFiltros();
});

document.getElementById("cinza").addEventListener("click", function() {
    filtros.cinza = !filtros.cinza;
    aplicarFiltros();
});

document.getElementById("daltonismo").addEventListener("click", function() {
    filtros.daltonismo = !filtros.daltonismo;
    aplicarFiltros();
});

// Leitura em áudio
const botaoLer = document.getElementById("lerPagina");

botaoLer.addEventListener("click", function() {
    // Se já está lendo, para
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
        botaoLer.textContent = "🔊 Ler página em áudio";
        return;
    }

    // Lê o texto selecionado; se não houver, lê a página inteira
    let texto = window.getSelection().toString();

    if (texto === "") {
        alvos.forEach(function(el) {
            texto += el.innerText + ". ";
        });
    }

    const fala = new SpeechSynthesisUtterance(texto);
    fala.lang = "pt-BR";

    fala.onend = function() {
        botaoLer.textContent = "🔊 Ler página em áudio";
    };

    speechSynthesis.speak(fala);
    botaoLer.textContent = "⏹ Parar leitura";
});

// Restaurar tudo
document.getElementById("resetar").addEventListener("click", function() {
    zoom = 1;
    filtros = { contraste: false, cinza: false, daltonismo: false };
    aplicarZoom();
    aplicarFiltros();
    speechSynthesis.cancel();
    botaoLer.textContent = "🔊 Ler página em áudio";
});
/*Animação do botão de busca*/
const botaoBusca = document.getElementById("botaoBusca");
const campoBusca = document.getElementById("campoBusca");
const busca = document.querySelector(".busca");

botaoBusca.addEventListener("click", function() {
    busca.classList.toggle("ativa");

    if (busca.classList.contains("ativa")) {
        campoBusca.focus();
    }
});
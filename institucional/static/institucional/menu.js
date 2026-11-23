
const botaoMenu = document.getElementById("menu-toggle");
const menuPrincipal = document.getElementById("menu-principal");

// Todos os links do menu
const linksMenu = menuPrincipal.querySelectorAll("a");

// Apenas os links que apontam para seções da página
const linksSecoes = Array.from(linksMenu).filter(link =>
    link.getAttribute("href")?.startsWith("#")
);


// ABRIR E FECHAR MENU

botaoMenu.addEventListener("click", function () {

    const aberto = menuPrincipal.classList.toggle("aberto");

    botaoMenu.classList.toggle("ativo", aberto);

    botaoMenu.setAttribute("aria-expanded", aberto);

    botaoMenu.setAttribute(
        "aria-label",
        aberto ? "Fechar menu" : "Abrir menu"
    );

});


// MARCAR ITEM SELECIONADO

function marcarMenuAtivo(linkSelecionado) {

    linksSecoes.forEach(function (link) {
        link.classList.remove("ativo");
    });

    if (linkSelecionado) {
        linkSelecionado.classList.add("ativo");
    }

}


// FECHAR MENU AO CLICAR EM UM LINK

linksMenu.forEach(function (link) {

    link.addEventListener("click", function () {

        menuPrincipal.classList.remove("aberto");
        botaoMenu.classList.remove("ativo");

        botaoMenu.setAttribute("aria-expanded", "false");
        botaoMenu.setAttribute("aria-label", "Abrir menu");

        if (link.getAttribute("href")?.startsWith("#")) {
            marcarMenuAtivo(link);
        }

    });

});


// IDENTIFICAR A SEÇÃO VISUALIZADA DURANTE A ROLAGEM

function atualizarMenuAtivo() {

    let secaoAtual = linksSecoes[0];

    const posicaoAtual = window.scrollY + 180;

    linksSecoes.forEach(function (link) {

        const idSecao = link.getAttribute("href").substring(1);
        const secao = document.getElementById(idSecao);

        if (secao && secao.offsetTop <= posicaoAtual) {
            secaoAtual = link;
        }

    });

    // Se chegou ao final da página, selecionar o último item
    if (
        window.innerHeight + window.scrollY >=
        document.documentElement.scrollHeight - 5
    ) {
        secaoAtual = linksSecoes[linksSecoes.length - 1];
    }

    marcarMenuAtivo(secaoAtual);

}

window.addEventListener("scroll", atualizarMenuAtivo, {
    passive: true
});

atualizarMenuAtivo();


// FECHAR MENU AO PRESSIONAR ESC

document.addEventListener("keydown", function (evento) {

    if (evento.key === "Escape") {

        menuPrincipal.classList.remove("aberto");
        botaoMenu.classList.remove("ativo");

        botaoMenu.setAttribute("aria-expanded", "false");
        botaoMenu.setAttribute("aria-label", "Abrir menu");

    }

});

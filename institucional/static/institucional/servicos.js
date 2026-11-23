
// =================================
// SANDOVAL TI - CARTÕES DE SERVIÇOS
// =================================

const botoesExpandir = document.querySelectorAll(".botao-expandir");

botoesExpandir.forEach((botao) => {

    botao.addEventListener("click", function () {

        const cartaoAtual = botao.closest(".servico-card");
        const estaExpandido = cartaoAtual.classList.contains("expandido");

        // Fecha os outros cartões abertos
        document.querySelectorAll(".servico-card.expandido").forEach((cartao) => {

            cartao.classList.remove("expandido");

            const outroBotao = cartao.querySelector(".botao-expandir");

            if (outroBotao) {
                outroBotao.textContent = "Ver detalhes";
                outroBotao.setAttribute("aria-expanded", "false");
            }

        });

        // Abre ou fecha o cartão selecionado
        if (!estaExpandido) {

            cartaoAtual.classList.add("expandido");

            botao.textContent = "Fechar detalhes";
            botao.setAttribute("aria-expanded", "true");

        }

    });

});

const filtro = document.getElementById("filtro");
const update = document.getElementById("update");
const cadastro = document.getElementById("cadastrar")
//=====================Menu=====================
const menu = document.getElementById("menu_achados");
menu.addEventListener('click', exibir_achados);

let display_achados = true
function exibir_achados() {
    const opcoes_de_achados = document.getElementById("opcoes_de_achados")
    if (display_achados == true) {
        opcoes_de_achados.style.display = 'grid'
        display_achados = false
    } else if (display_achados == false) {
        opcoes_de_achados.style.display = 'none'
        display_achados = true
    }
};
//=====================Btw 'X'=====================
const close_filtro = document.querySelector("#filtro svg")
close_filtro.addEventListener('click', exibir_filtro)
const close_update = document.querySelector("#update svg")
close_update.addEventListener('click', exibir_update)
const close_cadastrar = document.querySelector("#cadastrar svg")
close_cadastrar.addEventListener('click', exibir_cadastrar)

//=====================Filtro=====================
const btw_filtro = document.getElementById("btw_filtro");
btw_filtro.addEventListener('click', exibir_filtro);
const filtro_escuro = document.getElementById("filtro_escuro");

let display_filtro = false;

function exibir_filtro() {
    display_filtro = !display_filtro;
    update.style.display = "none"
    cadastro.style.display = "none"
    filtro.style.display = "block"
    filtro_escuro.style.display = display_filtro ? 'flex' : 'none';}

//=====================Cadastrar=====================
const btw_cadastrar = document.getElementById("btw_cadastrar");
btw_cadastrar.addEventListener('click', exibir_cadastrar);

function exibir_cadastrar() {
    display_filtro = !display_filtro;
    update.style.display = "none"
    filtro.style.display = "none"
    cadastro.style.display = "block"
    filtro_escuro.style.display = display_filtro ? 'flex' : 'none';}

//=====================Update=====================
const btw_update = document.getElementById("btw_editar");
btw_update.addEventListener('click', exibir_update)

function exibir_update() {
    display_filtro = !display_filtro;
    update.style.display = "none"
    filtro.style.display = "none"
    cadastro.style.display = "none"
    mini_menu.style.display = "none"
    update.style.display = "block"
    filtro_escuro.style.display = display_filtro ? 'flex' : 'none';}

//=====================Menu btw direito=====================
const mini_menu = document.getElementById("mini_menu");
const linhas = document.querySelectorAll(".id_linha");
let id_selecionado = null;
const form_update = document.getElementById("form_update");
linhas.forEach(linha => {
    linha.addEventListener("contextmenu", function(event) {

        event.preventDefault();
        if (!linha) {
        return;}
        event.target.closest("tr")
        mini_menu.style.left = `${event.clientX}px`;
        mini_menu.style.top = `${event.clientY}px`;
        
        id_selecionado = this.dataset.id;

        mini_menu.style.display = "block";
        form_update.action = `/atualizar/${id_selecionado}`;
    
    document.addEventListener("click", function(event) {
    if (!mini_menu.contains(event.target)) {
        mini_menu.style.display = "none";
    }
});
});
    //=====================Menu btw direito BOTÕES=====================
    const btw_editar = document.getElementById("btw_editar");

        //=====================Deletar=====================
    const btw_excluir = document.getElementById("btw_excluir");
    btw_excluir.addEventListener("click", function() {

    if (id_selecionado === null) {
        return;
    }

    const confirmar = confirm("Deseja realmente excluir este item?");

    if (confirmar) {

        const formulario = document.createElement("form");

        formulario.method = "POST";
        formulario.action = `/excluir/${id_selecionado}`;

        document.body.appendChild(formulario);

        formulario.submit();
    }

    mini_menu.style.display = "none";
});
});
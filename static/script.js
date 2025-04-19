/* Abre e fecha menu lateral em modo mobile */
const menuMobile = document.querySelector(".menu-mobile");
const body = document.querySelector("body");
const navMenu = document.querySelector(".nav-menu");

menuMobile.addEventListener("click", () => {
  menuMobile.classList.toggle("bi-list");
  menuMobile.classList.toggle("bi-x");
  body.classList.toggle("menu-nav-active");
  navMenu.classList.toggle("open");
});

/* Fecha o menu quando clicar em algum item e muda o icone para list */
const navItem = document.querySelectorAll(".nav-item");

navItem.forEach((item) => {
  item.addEventListener("click", () => {
    if (body.classList.contains("menu-nav-active")) {
      menuMobile.classList.replace("bi-x", "bi-list");
      body.classList.remove("menu-nav-active");
      navMenu.classList.remove("open");
    }
  });
});

const item = document.querySelectorAll("[data-anime]");

const animeScroll = () => {
  const windowTop = window.pageYOffset + window.innerHeight * 0.85;

  item.forEach((element) => {
    if (windowTop > element.offsetTop) {
      element.classList.add("animate");
    } else {
      element.classList.remove("animate");
    }
  });
};

animeScroll();

window.addEventListener("scroll", () => {
  animeScroll();
})

// Ativar carregamento do botão "enviando"

const btnEnviar = document.querySelector('#btn-enviar')
const btnLoading = document.querySelector('#btn-loading')

btnEnviar.addEventListener("click", () => {
  btnLoading.style.display = "block";
})

// Tirar mensagem depois de 5 segundos

setTimeout(() => {
  document.querySelector('#message-alert').style.display = 'none';
}, 5000)


// Função para rolar para uma seção com compensação de altura do cabeçalho
function scrollToSection(sectionId) {
  const headerHeight = document.getElementById('header').offsetHeight; // Altura do cabeçalho
  const section = document.getElementById(sectionId); // Obtém a seção alvo
  const sectionTop = section.offsetTop - headerHeight; // Calcula a posição da seção considerando a altura do cabeçalho
  window.scroll({
    top: sectionTop,
    behavior: 'smooth' // Rolagem suave
  });
}

// Captura o elemento do cabeçalho
const header = document.getElementById('header');

// JavaScript para alternar a visibilidade do menu suspenso
function toggleDropdown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Fecha o menu suspenso se o usuário clicar fora dele
window.onclick = function (event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// confirmar saída

function confirmLogout() {
  if (confirm("Tem certeza que deseja sair?")) {
    window.location.href = "/logout"; // Redireciona para a página de logout se confirmado
  }
}

// lembrar senha

document.addEventListener("DOMContentLoaded", function () {
  // Verifique se há uma senha armazenada
  const storedPassword = localStorage.getItem("rememberedPassword");
  if (storedPassword) {
    // Se houver, preencha o campo de senha
    document.querySelector("#password").value = storedPassword;
    // Marque a caixa de seleção "Lembrar senha"
    document.querySelector("#remember-password").value = "1";
  }

  // Adicione um ouvinte de evento ao botão "Lembrar senha"
  document.querySelector("#remember-password-checkbox").addEventListener("change", function () {
    // Se a caixa de seleção estiver marcada, armazene a senha
    if (this.checked) {
      localStorage.setItem("rememberedPassword", document.querySelector("#password").value);
      document.querySelector("#remember-password").value = "1";
    } else {
      // Caso contrário, remova a senha armazenada
      localStorage.removeItem("rememberedPassword");
      document.querySelector("#remember-password").value = "0";
    }
  });
});








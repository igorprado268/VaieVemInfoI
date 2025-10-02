// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Fade in animation on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible")
    }
  })
}, observerOptions)

document.querySelectorAll(".fade-in").forEach((el) => {
  observer.observe(el)
})

// Modal functions
// function showModal() {
//   const modal = document.getElementById("cadastroModal")
//   modal.classList.add("show")
// }

// function showLoginModal() {
//   const modal = document.getElementById("loginModal")
//   modal.classList.add("show")
// }
// Redirecionar para página de Login
document.getElementById("login-modal").addEventListener("click", function() {
  window.location.href = "login.html";
});

// Redirecionar para página de Cadastro
document.getElementById("cadastro-modal").addEventListener("click", function() {
  window.location.href = "cadastro.html";
});


// Navbar background change on scroll
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar")
  if (window.scrollY > 50) {
    navbar.style.background = "linear-gradient(135deg, rgba(40, 167, 69, 0.95), rgba(32, 201, 151, 0.95))"
    navbar.style.backdropFilter = "blur(10px)"
  } else {
    navbar.style.background = "linear-gradient(135deg, var(--primary-green), var(--secondary-green))"
    navbar.style.backdropFilter = "none"
  }
})

// Form validation
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault()
      // Aqui você pode adicionar a lógica de envio do formulário
      alert("Funcionalidade em desenvolvimento!")
    })
  })
})


document.getElementById('cadastroForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const form = e.target;
  const senha = document.getElementById('senha').value;
  const confirmarSenha = document.getElementById('confirmarSenha').value;
  const email = document.getElementById('email').value;

  if (senha !== confirmarSenha) {
      alert('As senhas não coincidem!');
      return;
  }

  if (!email.includes('@alunos.ifsuldeminas.edu.br') && !email.includes('@ifsuldeminas.edu.br')) {
      alert('Por favor, use seu e-mail institucional do IF Sul de Minas!');
      return;
  }

  if (senha.length < 6) {
      alert('A senha deve ter pelo menos 6 caracteres!');
      return;
  }

  // preencher o username escondido com o e-mail (ou outra lógica desejada)
  document.getElementById('username').value = email;

  // finalmente enviar para o Django (vai gerar POST para a view 'cadastro')
  form.submit();
});

const form = document.getElementById("form");
const titulo = document.getElementById("titulo");
const mensagem = document.getElementById("mensagem");
const botao = document.getElementById("enviar");
const abas = document.querySelectorAll(".aba");
const telefone = document.getElementById("telefone");

let tipo = "clientes";

// Troca entre cadastro de cliente e de barbeiro
abas.forEach((aba) => {
  aba.addEventListener("click", () => {
    tipo = aba.dataset.tipo;
    abas.forEach((a) => {
      const ativa = a === aba;
      a.classList.toggle("ativa", ativa);
      a.setAttribute("aria-selected", ativa);
    });
    titulo.textContent = tipo === "clientes" ? "Cadastro de cliente" : "Cadastro de barbeiro";
    limparErros();
    mensagem.textContent = "";
  });
});

// Máscara do telefone: (41) 99999-9999
telefone.addEventListener("input", () => {
  const d = telefone.value.replace(/\D/g, "").slice(0, 11);
  let v = d;
  if (d.length > 6) {
    const meio = d.length > 10 ? 7 : 6;
    v = `(${d.slice(0, 2)}) ${d.slice(2, meio)}-${d.slice(meio)}`;
  } else if (d.length > 2) {
    v = `(${d.slice(0, 2)}) ${d.slice(2)}`;
  }
  telefone.value = v;
});

function limparErros() {
  document.querySelectorAll(".erro").forEach((e) => (e.textContent = ""));
  form.querySelectorAll("input").forEach((i) => i.classList.remove("invalido"));
}

function mostrarErros(erros) {
  Object.entries(erros).forEach(([campo, texto]) => {
    const span = document.querySelector(`[data-erro="${campo}"]`);
    if (span) span.textContent = texto;
    form.elements[campo]?.classList.add("invalido");
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  limparErros();
  mensagem.textContent = "";
  mensagem.className = "";
  botao.disabled = true;

  const dados = Object.fromEntries(new FormData(form));

  try {
    const resp = await fetch(`/api/${tipo}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const corpo = await resp.json();

    if (resp.ok) {
      form.reset();
      mensagem.textContent = "Cadastro realizado com sucesso.";
      mensagem.className = "sucesso";
    } else if (corpo.erros) {
      mostrarErros(corpo.erros);
    } else {
      mensagem.textContent = corpo.erro || "Não foi possível cadastrar.";
      mensagem.className = "falha";
    }
  } catch {
    mensagem.textContent = "Sem conexão com o servidor. Tente novamente.";
    mensagem.className = "falha";
  } finally {
    botao.disabled = false;
  }
});
const form = document.getElementById("form-servico");
const lista = document.getElementById("lista-servicos");
const total = document.getElementById("total-servicos");
const mensagem = document.getElementById("mensagem");
const botaoAdicionar = document.getElementById("adicionar");
const formatarPreco = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

function exibirEstado(texto) {
  lista.replaceChildren();
  const item = document.createElement("li");
  item.className = "estado-lista";
  item.textContent = texto;
  lista.append(item);
}

function renderizarServicos(servicos) {
  lista.replaceChildren();
  total.textContent = `${servicos.length} ${servicos.length === 1 ? "serviço" : "serviços"}`;

  if (servicos.length === 0) {
    exibirEstado("Nenhum serviço cadastrado.");
    return;
  }

  servicos.forEach((servico) => {
    const item = document.createElement("li");
    item.className = "servico";

    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const nome = document.createElement("strong");
    nome.textContent = servico.nome;
    const detalhe = document.createElement("span");
    detalhe.className = "servico-detalhe";
    detalhe.textContent = ` — ${servico.duracao} min — R$ ${formatarPreco.format(servico.preco)}`;
    informacoes.append(nome, detalhe);

    const remover = document.createElement("button");
    remover.type = "button";
    remover.className = "botao-remover";
    remover.dataset.id = servico.id;
    remover.textContent = "Remover";
    remover.setAttribute("aria-label", `Remover ${servico.nome}`);

    item.append(informacoes, remover);
    lista.append(item);
  });
}

async function carregarServicos() {
  exibirEstado("Carregando serviços...");
  try {
    const resposta = await fetch("/api/servicos");
    if (!resposta.ok) throw new Error("Falha ao carregar serviços.");
    const dados = await resposta.json();
    renderizarServicos(dados.servicos);
  } catch {
    total.textContent = "";
    exibirEstado("Não foi possível carregar os serviços. Tente novamente.");
  }
}

function limparErros() {
  document.querySelectorAll(".erro").forEach((campo) => {
    campo.textContent = "";
  });
  form.querySelectorAll("input").forEach((campo) => {
    campo.classList.remove("invalido");
  });
}

function mostrarErros(erros) {
  Object.entries(erros).forEach(([campo, texto]) => {
    const detalhe = document.querySelector(`[data-erro="${campo}"]`);
    const entrada = form.elements[campo];
    if (detalhe) detalhe.textContent = texto;
    if (entrada) entrada.classList.add("invalido");
  });
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limparErros();
  mensagem.textContent = "";
  mensagem.className = "mensagem";
  botaoAdicionar.disabled = true;

  const dados = Object.fromEntries(new FormData(form));
  dados.duracao = Number(dados.duracao);
  dados.preco = Number(dados.preco);

  try {
    const resposta = await fetch("/api/servicos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      if (corpo.erros) mostrarErros(corpo.erros);
      else mensagem.textContent = corpo.erro || "Não foi possível adicionar o serviço.";
      return;
    }

    form.reset();
    mensagem.textContent = "Serviço adicionado.";
    mensagem.classList.add("sucesso");
    await carregarServicos();
  } catch {
    mensagem.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    botaoAdicionar.disabled = false;
  }
});

lista.addEventListener("click", async (evento) => {
  const botao = evento.target.closest(".botao-remover");
  if (!botao) return;

  botao.disabled = true;
  try {
    const resposta = await fetch(`/api/servicos/${botao.dataset.id}`, { method: "DELETE" });
    if (!resposta.ok) throw new Error("Falha ao remover serviço.");
    await carregarServicos();
  } catch {
    botao.disabled = false;
    mensagem.textContent = "Não foi possível remover o serviço. Tente novamente.";
    mensagem.className = "mensagem";
  }
});

carregarServicos();
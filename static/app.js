const formServico = document.getElementById("form-servico");
const formCadastro = document.getElementById("form-cadastro");
const lista = document.getElementById("lista-servicos");
const total = document.getElementById("total-servicos");
const mensagemServico = document.getElementById("mensagem");
const mensagemCadastro = document.getElementById("mensagem-cadastro");
const campoTelefone = document.getElementById("cadastro-telefone");
const botaoAdicionar = document.getElementById("adicionar");
const botaoCadastro = document.getElementById("botao-cadastro");
const botaoSair = document.getElementById("botao-sair");
const telaCadastro = document.getElementById("tela-cadastro");
const telaServicos = document.getElementById("tela-servicos");
const painelAdicionar = document.getElementById("painel-adicionar");
const instrucaoServicos = document.getElementById("instrucao-servicos");
const seletorPerfil = Array.from(document.querySelectorAll("[data-perfil]"));
const formatarPreco = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});
let perfilSelecionado = "clientes";
let tipoUsuario = null;
let servicoSelecionadoId = null;

function formatarTelefone(digitos) {
  const numero = digitos.replace(/\D/g, "").slice(0, 11);
  if (numero.length === 0) return "";
  if (numero.length <= 2) return `(${numero}`;

  const ddd = numero.slice(0, 2);
  const telefone = numero.slice(2);
  const celular = telefone.startsWith("9") || numero.length > 10;
  const tamanhoPrefixo = celular ? 5 : 4;
  const parteInicial = telefone.slice(0, tamanhoPrefixo);
  const parteFinal = telefone.slice(tamanhoPrefixo);
  const numeroFormatado = parteFinal ? `${parteInicial}-${parteFinal}` : parteInicial;
  return `(${ddd}) ${numeroFormatado}`;
}

function posicaoDoCursor(texto, quantidadeDigitos) {
  if (quantidadeDigitos === 0) return 0;
  let digitosEncontrados = 0;
  for (let indice = 0; indice < texto.length; indice += 1) {
    if (/\d/.test(texto[indice])) digitosEncontrados += 1;
    if (digitosEncontrados === quantidadeDigitos) return indice + 1;
  }
  return texto.length;
}

campoTelefone.addEventListener("input", () => {
  const posicaoAtual = campoTelefone.selectionStart ?? campoTelefone.value.length;
  const quantidadeDigitos = campoTelefone.value.slice(0, posicaoAtual).replace(/\D/g, "").length;
  campoTelefone.value = formatarTelefone(campoTelefone.value);
  const novaPosicao = posicaoDoCursor(campoTelefone.value, quantidadeDigitos);
  campoTelefone.setSelectionRange(novaPosicao, novaPosicao);
});

function mostrarCadastro() {
  telaCadastro.hidden = false;
  telaServicos.hidden = true;
}

function mostrarServicos(usuario) {
  tipoUsuario = usuario.tipo;
  telaCadastro.hidden = true;
  telaServicos.hidden = false;
  painelAdicionar.hidden = tipoUsuario !== "barbeiros";
  instrucaoServicos.hidden = tipoUsuario !== "clientes";
  servicoSelecionadoId = null;
  document.getElementById("boas-vindas").textContent = `Olá, ${usuario.nome}`;
  document.getElementById("tipo-usuario").textContent = tipoUsuario === "barbeiros"
    ? "Área do barbeiro"
    : "Área do cliente";
  carregarServicos();
}

seletorPerfil.forEach((botao) => {
  botao.addEventListener("click", () => {
    perfilSelecionado = botao.dataset.perfil;
    seletorPerfil.forEach((item) => {
      const selecionado = item === botao;
      item.classList.toggle("perfil-selecionado", selecionado);
      item.setAttribute("aria-pressed", String(selecionado));
    });
    botaoCadastro.textContent = `Cadastrar como ${perfilSelecionado === "clientes" ? "cliente" : "barbeiro"}`;
  });
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

    item.append(informacoes);
    if (tipoUsuario === "clientes") {
      const escolher = document.createElement("button");
      escolher.type = "button";
      escolher.className = "botao-escolher";
      escolher.dataset.id = servico.id;
      const selecionado = String(servico.id) === servicoSelecionadoId;
      escolher.textContent = selecionado ? "Selecionado" : "Escolher";
      escolher.setAttribute("aria-pressed", String(selecionado));
      escolher.setAttribute("aria-label", `Escolher ${servico.nome}`);
      item.append(escolher);
    } else if (tipoUsuario === "barbeiros") {
      const remover = document.createElement("button");
      remover.type = "button";
      remover.className = "botao-remover";
      remover.dataset.id = servico.id;
      remover.textContent = "Remover";
      remover.setAttribute("aria-label", `Remover ${servico.nome}`);
      item.append(remover);
    }
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

function limparErros(formulario) {
  formulario.querySelectorAll(".erro").forEach((campo) => {
    campo.textContent = "";
  });
  formulario.querySelectorAll("input").forEach((campo) => {
    campo.classList.remove("invalido");
  });
}

function mostrarErros(formulario, erros) {
  Object.entries(erros).forEach(([campo, texto]) => {
    const detalhe = formulario.querySelector(`[data-erro="${campo}"]`);
    const entrada = formulario.elements[campo];
    if (detalhe) detalhe.textContent = texto;
    if (entrada) entrada.classList.add("invalido");
  });
}

formServico.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limparErros(formServico);
  mensagemServico.textContent = "";
  mensagemServico.className = "mensagem";
  botaoAdicionar.disabled = true;

  const dados = Object.fromEntries(new FormData(formServico));
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
      if (corpo.erros) mostrarErros(formServico, corpo.erros);
      else mensagemServico.textContent = corpo.erro || "Não foi possível adicionar o serviço.";
      return;
    }

    formServico.reset();
    mensagemServico.textContent = "Serviço adicionado.";
    mensagemServico.classList.add("sucesso");
    await carregarServicos();
  } catch {
    mensagemServico.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    botaoAdicionar.disabled = false;
  }
});

formCadastro.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limparErros(formCadastro);
  mensagemCadastro.textContent = "";
  mensagemCadastro.className = "mensagem";
  botaoCadastro.disabled = true;

  const dados = Object.fromEntries(new FormData(formCadastro));

  try {
    const resposta = await fetch(`/api/${perfilSelecionado}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      if (corpo.erros) mostrarErros(formCadastro, corpo.erros);
      else mensagemCadastro.textContent = corpo.erro || "Não foi possível concluir o cadastro.";
      return;
    }

    formCadastro.reset();
    const sessao = await fetch("/api/sessao");
    const usuario = await sessao.json();
    mostrarServicos(usuario);
  } catch {
    mensagemCadastro.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    botaoCadastro.disabled = false;
  }
});

lista.addEventListener("click", async (evento) => {
  const botaoEscolher = evento.target.closest(".botao-escolher");
  if (botaoEscolher) {
    servicoSelecionadoId = botaoEscolher.dataset.id;
    lista.querySelectorAll(".botao-escolher").forEach((botao) => {
      const selecionado = botao === botaoEscolher;
      botao.textContent = selecionado ? "Selecionado" : "Escolher";
      botao.setAttribute("aria-pressed", String(selecionado));
    });
    return;
  }

  const botao = evento.target.closest(".botao-remover");
  if (!botao) return;

  botao.disabled = true;
  try {
    const resposta = await fetch(`/api/servicos/${botao.dataset.id}`, { method: "DELETE" });
    if (!resposta.ok) throw new Error("Falha ao remover serviço.");
    await carregarServicos();
  } catch {
    botao.disabled = false;
    mensagemServico.textContent = "Não foi possível remover o serviço. Tente novamente.";
    mensagemServico.className = "mensagem";
  }
});

botaoSair.addEventListener("click", async () => {
  botaoSair.disabled = true;
  try {
    const resposta = await fetch("/api/sair", { method: "POST" });
    if (!resposta.ok) throw new Error("Falha ao encerrar a sessão.");
    tipoUsuario = null;
    mensagemCadastro.textContent = "";
    mostrarCadastro();
  } catch {
    document.getElementById("tipo-usuario").textContent = "Não foi possível sair da conta. Tente novamente.";
  } finally {
    botaoSair.disabled = false;
  }
});

async function iniciar() {
  try {
    const resposta = await fetch("/api/sessao");
    const usuario = await resposta.json();
    if (usuario.autenticado) mostrarServicos(usuario);
    else mostrarCadastro();
  } catch {
    mostrarCadastro();
  }
}

iniciar();
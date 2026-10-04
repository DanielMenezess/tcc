const formServico = document.getElementById("form-servico");
const formCadastro = document.getElementById("form-cadastro");
const formLogin = document.getElementById("form-login");
const lista = document.getElementById("lista-servicos");
const total = document.getElementById("total-servicos");
const mensagemServico = document.getElementById("mensagem");
const mensagemCadastro = document.getElementById("mensagem-cadastro");
const mensagemLogin = document.getElementById("mensagem-login");
const campoTelefone = document.getElementById("cadastro-telefone");
const botaoAdicionar = document.getElementById("adicionar");
const botaoCadastro = document.getElementById("botao-cadastro");
const botaoLogin = document.getElementById("botao-login");
const botaoSair = document.getElementById("botao-sair");
const telaCadastro = document.getElementById("tela-cadastro");
const telaLogin = document.getElementById("tela-login");
const telaServicos = document.getElementById("tela-servicos");
const painelAdicionar = document.getElementById("painel-adicionar");
const painelEscolherBarbeiro = document.getElementById("painel-escolher-barbeiro");
const instrucaoServicos = document.getElementById("instrucao-servicos");
const listaBarbeiros = document.getElementById("lista-barbeiros");
const totalBarbeiros = document.getElementById("total-barbeiros");
const painelEscolherData = document.getElementById("painel-escolher-data");
const campoDataAgendamento = document.getElementById("data-agendamento");
const mensagemData = document.getElementById("mensagem-data");
const painelEscolherHorario = document.getElementById("painel-escolher-horario");
const listaHorarios = document.getElementById("lista-horarios");
const horarioSelecionadoTexto = document.getElementById("horario-selecionado");
const faixaHorarios = document.getElementById("faixa-horarios");
const painelConfirmarAgendamento = document.getElementById("painel-confirmar-agendamento");
const resumoAgendamento = document.getElementById("resumo-agendamento");
const mensagemAgendamento = document.getElementById("mensagem-agendamento");
const botaoConfirmarAgendamento = document.getElementById("botao-confirmar-agendamento");
const seletorPerfil = Array.from(document.querySelectorAll("[data-perfil]"));
const seletorPerfilLogin = Array.from(document.querySelectorAll("[data-login-perfil]"));
const formatarPreco = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});
const nomeBarbeiroValido = /^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ ]*$/;
let perfilSelecionado = "clientes";
let perfilLoginSelecionado = "clientes";
let tipoUsuario = null;
let servicoSelecionadoId = null;
let servicoSelecionadoNome = null;
let barbeiroSelecionadoId = null;
let barbeiroSelecionadoNome = null;
let dataSelecionada = null;
let horarioSelecionado = null;
let agendamentoConfirmado = false;
let confirmandoAgendamento = false;

function dataLocalAtual() {
  const agora = new Date();
  const ano = agora.getFullYear();
  const mes = String(agora.getMonth() + 1).padStart(2, "0");
  const dia = String(agora.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

function atualizarResumoAgendamento() {
  const completo = Boolean(
    servicoSelecionadoId && barbeiroSelecionadoId && dataSelecionada && horarioSelecionado,
  );
  botaoConfirmarAgendamento.disabled = !completo || confirmandoAgendamento || agendamentoConfirmado;

  if (!agendamentoConfirmado) {
    resumoAgendamento.textContent = completo
      ? `${servicoSelecionadoNome} com ${barbeiroSelecionadoNome}, em ${dataSelecionada.split("-").reverse().join("/")} às ${horarioSelecionado}.`
      : "Escolha o serviço, barbeiro, data e horário.";
  }
}

function selecaoAgendamentoAlterada() {
  agendamentoConfirmado = false;
  mensagemAgendamento.textContent = "";
  mensagemAgendamento.className = "mensagem";
  botaoConfirmarAgendamento.textContent = "Confirmar agendamento";
  atualizarResumoAgendamento();
}

function renderizarHorarios() {
  listaHorarios.replaceChildren();
  const agora = new Date();
  for (let minutos = 9 * 60; minutos <= 19 * 60 + 30; minutos += 30) {
    const hora = String(Math.floor(minutos / 60)).padStart(2, "0");
    const minuto = String(minutos % 60).padStart(2, "0");
    const horario = `${hora}:${minuto}`;
    const horarioJaPassou = dataSelecionada === dataLocalAtual()
      && minutos <= agora.getHours() * 60 + agora.getMinutes();
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "botao-horario";
    botao.dataset.horario = horario;
    botao.textContent = horario;
    botao.disabled = horario === "12:00" || horario === "12:30" || horarioJaPassou;
    botao.setAttribute("aria-pressed", String(horario === horarioSelecionado));
    listaHorarios.append(botao);
  }
}

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
  telaLogin.hidden = true;
  telaServicos.hidden = true;
}

function mostrarLogin() {
  telaCadastro.hidden = true;
  telaLogin.hidden = false;
  telaServicos.hidden = true;
}

function mostrarServicos(usuario) {
  tipoUsuario = usuario.tipo;
  telaCadastro.hidden = true;
  telaLogin.hidden = true;
  telaServicos.hidden = false;
  painelAdicionar.hidden = tipoUsuario !== "barbeiros";
  painelEscolherBarbeiro.hidden = tipoUsuario !== "clientes";
  painelEscolherData.hidden = tipoUsuario !== "clientes";
  painelEscolherHorario.hidden = true;
  painelConfirmarAgendamento.hidden = tipoUsuario !== "clientes";
  instrucaoServicos.hidden = tipoUsuario !== "clientes";
  servicoSelecionadoId = null;
  servicoSelecionadoNome = null;
  barbeiroSelecionadoId = null;
  barbeiroSelecionadoNome = null;
  dataSelecionada = null;
  campoDataAgendamento.min = dataLocalAtual();
  campoDataAgendamento.value = "";
  mensagemData.textContent = "Selecione hoje ou uma data futura.";
  horarioSelecionado = null;
  horarioSelecionadoTexto.textContent = "";
  agendamentoConfirmado = false;
  confirmandoAgendamento = false;
  mensagemAgendamento.textContent = "";
  botaoConfirmarAgendamento.textContent = "Confirmar agendamento";
  atualizarResumoAgendamento();
  renderizarHorarios();
  document.getElementById("boas-vindas").textContent = `Olá, ${usuario.nome}`;
  document.getElementById("tipo-usuario").textContent = tipoUsuario === "barbeiros"
    ? "Área do barbeiro"
    : "Área do cliente";
  carregarServicos();
  if (tipoUsuario === "clientes") carregarBarbeiros();
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

document.getElementById("abrir-login").addEventListener("click", mostrarLogin);
document.getElementById("abrir-cadastro").addEventListener("click", mostrarCadastro);
campoDataAgendamento.addEventListener("change", () => {
  const hoje = dataLocalAtual();
  campoDataAgendamento.min = hoje;

  if (!campoDataAgendamento.value || campoDataAgendamento.value < hoje) {
    campoDataAgendamento.value = "";
    dataSelecionada = null;
    horarioSelecionado = null;
    painelEscolherHorario.hidden = true;
    horarioSelecionadoTexto.textContent = "";
    renderizarHorarios();
    mensagemData.textContent = "Escolha hoje ou uma data futura.";
    selecaoAgendamentoAlterada();
    return;
  }

  dataSelecionada = campoDataAgendamento.value;
  horarioSelecionado = null;
  horarioSelecionadoTexto.textContent = "";
  const [ano, mes, dia] = dataSelecionada.split("-");
  const domingo = new Date(Date.UTC(Number(ano), Number(mes) - 1, Number(dia))).getUTCDay() === 0;
  painelEscolherHorario.hidden = false;
  faixaHorarios.hidden = domingo;

  if (domingo) {
    mensagemData.textContent = "A barbearia não abre aos domingos.";
    listaHorarios.replaceChildren();
    horarioSelecionadoTexto.textContent = "Não há horários disponíveis, pois a barbearia não abre aos domingos.";
    selecaoAgendamentoAlterada();
    return;
  }

  mensagemData.textContent = `Horários para ${dia}/${mes}/${ano}.`;
  renderizarHorarios();
  selecaoAgendamentoAlterada();
});
seletorPerfilLogin.forEach((botao) => {
  botao.addEventListener("click", () => {
    perfilLoginSelecionado = botao.dataset.loginPerfil;
    seletorPerfilLogin.forEach((item) => {
      const selecionado = item === botao;
      item.classList.toggle("perfil-selecionado", selecionado);
      item.setAttribute("aria-pressed", String(selecionado));
    });
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
      escolher.textContent = selecionado ? "Desselecionar" : "Escolher";
      escolher.setAttribute("aria-pressed", String(selecionado));
      escolher.setAttribute("aria-label", `${selecionado ? "Desselecionar" : "Escolher"} ${servico.nome}`);
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

function renderizarBarbeiros(barbeiros) {
  listaBarbeiros.replaceChildren();
  totalBarbeiros.textContent = `${barbeiros.length} ${barbeiros.length === 1 ? "barbeiro" : "barbeiros"}`;

  barbeiros.forEach((barbeiro) => {
    const item = document.createElement("li");
    item.className = "servico";

    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const nome = document.createElement("strong");
    nome.textContent = barbeiro.nome;
    informacoes.append(nome);

    const escolher = document.createElement("button");
    escolher.type = "button";
    escolher.className = "botao-escolher";
    escolher.dataset.id = barbeiro.id;
    const selecionado = String(barbeiro.id) === barbeiroSelecionadoId;
    escolher.textContent = selecionado ? "Desselecionar" : "Escolher";
    escolher.setAttribute("aria-pressed", String(selecionado));
    escolher.setAttribute("aria-label", `${selecionado ? "Desselecionar" : "Escolher"} ${barbeiro.nome}`);

    item.append(informacoes, escolher);
    listaBarbeiros.append(item);
  });
}

async function carregarBarbeiros() {
  listaBarbeiros.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando barbeiros...";
  listaBarbeiros.append(carregando);

  try {
    const resposta = await fetch("/api/barbeiros");
    if (!resposta.ok) throw new Error("Falha ao carregar barbeiros.");
    const dados = await resposta.json();
    renderizarBarbeiros(dados.barbeiros);
  } catch {
    totalBarbeiros.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar os barbeiros. Tente novamente.";
    listaBarbeiros.replaceChildren(erro);
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
  const nome = String(dados.nome || "").trim();

  if (dados.senha !== dados.confirmar_senha) {
    mostrarErros(formCadastro, { confirmar_senha: "As senhas não coincidem." });
    botaoCadastro.disabled = false;
    return;
  }

  if (perfilSelecionado === "barbeiros" && !nomeBarbeiroValido.test(nome)) {
    mensagemCadastro.textContent = "Use letras maiúsculas no início de cada nome e evite números ou símbolos.";
    mensagemCadastro.className = "mensagem erro";
    const campo = formCadastro.elements.nome;
    campo.classList.add("invalido");
    const detalhe = formCadastro.querySelector('[data-erro="nome"]');
    if (detalhe) detalhe.textContent = "Use letras maiúsculas no início de cada nome e evite números ou símbolos.";
    botaoCadastro.disabled = false;
    return;
  }

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

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mensagemLogin.textContent = "";
  mensagemLogin.className = "mensagem";
  botaoLogin.disabled = true;

  const dados = Object.fromEntries(new FormData(formLogin));
  dados.tipo = perfilLoginSelecionado;
  try {
    const resposta = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      mensagemLogin.textContent = corpo.erro || "Não foi possível entrar na conta.";
      return;
    }

    formLogin.reset();
    const sessao = await fetch("/api/sessao");
    mostrarServicos(await sessao.json());
  } catch {
    mensagemLogin.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    botaoLogin.disabled = false;
  }
});

lista.addEventListener("click", async (evento) => {
  const botaoEscolher = evento.target.closest(".botao-escolher");
  if (botaoEscolher) {
    const deselecionando = botaoEscolher.dataset.id === servicoSelecionadoId;
    servicoSelecionadoId = deselecionando ? null : botaoEscolher.dataset.id;
    servicoSelecionadoNome = deselecionando
      ? null
      : botaoEscolher.closest(".servico").querySelector("strong").textContent;
    lista.querySelectorAll(".botao-escolher").forEach((botao) => {
      const selecionado = botao.dataset.id === servicoSelecionadoId;
      botao.textContent = selecionado ? "Desselecionar" : "Escolher";
      botao.setAttribute("aria-pressed", String(selecionado));
      botao.setAttribute("aria-label", `${selecionado ? "Desselecionar" : "Escolher"} ${botao.closest(".servico").querySelector("strong").textContent}`);
    });
    selecaoAgendamentoAlterada();
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

listaBarbeiros.addEventListener("click", (evento) => {
  const botao = evento.target.closest(".botao-escolher");
  if (!botao) return;

  const deselecionando = botao.dataset.id === barbeiroSelecionadoId;
  barbeiroSelecionadoId = deselecionando ? null : botao.dataset.id;
  barbeiroSelecionadoNome = deselecionando
    ? null
    : botao.closest(".servico").querySelector("strong").textContent;
  listaBarbeiros.querySelectorAll(".botao-escolher").forEach((item) => {
    const selecionado = item.dataset.id === barbeiroSelecionadoId;
    item.textContent = selecionado ? "Desselecionar" : "Escolher";
    item.setAttribute("aria-pressed", String(selecionado));
    item.setAttribute("aria-label", `${selecionado ? "Desselecionar" : "Escolher"} ${item.closest(".servico").querySelector("strong").textContent}`);
  });
  selecaoAgendamentoAlterada();
});

listaHorarios.addEventListener("click", (evento) => {
  const botao = evento.target.closest(".botao-horario");
  if (!botao || botao.disabled || !dataSelecionada) return;

  horarioSelecionado = botao.dataset.horario;
  listaHorarios.querySelectorAll(".botao-horario").forEach((item) => {
    item.setAttribute("aria-pressed", String(item === botao));
  });
  horarioSelecionadoTexto.textContent = `Horário selecionado: ${horarioSelecionado}`;
  selecaoAgendamentoAlterada();
});

botaoConfirmarAgendamento.addEventListener("click", async () => {
  if (botaoConfirmarAgendamento.disabled) return;

  confirmandoAgendamento = true;
  mensagemAgendamento.textContent = "";
  mensagemAgendamento.className = "mensagem";
  botaoConfirmarAgendamento.textContent = "Confirmando...";
  atualizarResumoAgendamento();

  try {
    const resposta = await fetch("/api/agendamentos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        servico_id: servicoSelecionadoId,
        barbeiro_id: barbeiroSelecionadoId,
        data: dataSelecionada,
        horario: horarioSelecionado,
      }),
    });
    const corpo = await resposta.json();
    if (!resposta.ok) {
      mensagemAgendamento.textContent = corpo.erro || "Não foi possível confirmar o agendamento.";
      return;
    }

    agendamentoConfirmado = true;
    const agendamento = corpo.agendamento;
    resumoAgendamento.textContent = `${agendamento.servico} com ${agendamento.barbeiro}, em ${agendamento.data.split("-").reverse().join("/")} às ${agendamento.horario}.`;
    mensagemAgendamento.textContent = "Agendamento confirmado.";
    mensagemAgendamento.classList.add("sucesso");
    botaoConfirmarAgendamento.textContent = "Agendamento confirmado";
  } catch {
    mensagemAgendamento.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    confirmandoAgendamento = false;
    atualizarResumoAgendamento();
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
const formServico = document.getElementById("form-servico");
const formCadastro = document.getElementById("form-cadastro");
const formLogin = document.getElementById("form-login");
const lista = document.getElementById("lista-servicos");
const total = document.getElementById("total-servicos");
const mensagemServico = document.getElementById("mensagem");
const mensagemCadastro = document.getElementById("mensagem-cadastro");
const mensagemLogin = document.getElementById("mensagem-login");
const campoNomeCadastro = document.getElementById("cadastro-nome");
const campoTelefone = document.getElementById("cadastro-telefone");
const botaoAdicionar = document.getElementById("adicionar");
const botaoCadastro = document.getElementById("botao-cadastro");
const botaoLogin = document.getElementById("botao-login");
const botoesSair = Array.from(document.querySelectorAll(".botao-sair"));
const botaoTema = document.getElementById("botao-tema");
const botoesTema = [botaoTema];
const telaCadastro = document.getElementById("tela-cadastro");
const telaLogin = document.getElementById("tela-login");
const telaServicos = document.getElementById("tela-servicos");
const cabecalhoSite = document.querySelector(".cabecalho");
const navegacaoUsuario = document.getElementById("navegacao-usuario");
const cabecalhoBarbeiro = document.getElementById("cabecalho-barbeiro");
const painelAgendarCliente = document.getElementById("painel-agendar-cliente");
const painelAgendamentosCliente = document.getElementById("painel-agendamentos-cliente");
const abasUsuario = document.getElementById("abas-usuario");
const painelProximoAgendamento = document.getElementById("painel-proximo-agendamento");
const statusProximoAgendamento = document.getElementById("status-proximo-agendamento");
const listaProximosAgendamentos = document.getElementById("lista-proximos-agendamentos");
const painelAdicionar = document.getElementById("painel-adicionar");
const painelSolicitacoesBarbeiros = document.getElementById("painel-solicitacoes-barbeiros");
const listaSolicitacoesBarbeiros = document.getElementById("lista-solicitacoes-barbeiros");
const totalSolicitacoesBarbeiros = document.getElementById("total-solicitacoes-barbeiros");
const painelContasAdministrador = document.getElementById("painel-contas-administrador");
const mensagemContasAdministrador = document.getElementById("mensagem-contas-administrador");
const listaContasClientes = document.getElementById("lista-contas-clientes");
const totalContasClientes = document.getElementById("total-contas-clientes");
const buscaContasClientes = document.getElementById("buscar-contas-clientes");
const listaContasBarbeiros = document.getElementById("lista-contas-barbeiros");
const totalContasBarbeiros = document.getElementById("total-contas-barbeiros");
const buscaContasBarbeiros = document.getElementById("buscar-contas-barbeiros");
const abasContas = Array.from(document.querySelectorAll("[data-aba-contas]"));
const painelContasClientes = document.getElementById("grupo-contas-clientes");
const painelContasBarbeiros = document.getElementById("grupo-contas-barbeiros");
const painelAgendaBarbeiro = document.getElementById("painel-agenda-barbeiro");
const painelAgendamentosPendentes = document.getElementById("painel-agendamentos-pendentes");
const listaAgendamentosPendentes = document.getElementById("lista-agendamentos-pendentes");
const totalAgendamentosPendentes = document.getElementById("total-agendamentos-pendentes");
const mensagemAgendamentosPendentes = document.getElementById("mensagem-agendamentos-pendentes");
const painelAgendamentosAConcluir = document.getElementById("painel-agendamentos-a-concluir");
const listaAgendamentosAConcluir = document.getElementById("lista-agendamentos-a-concluir");
const totalAgendamentosAConcluir = document.getElementById("total-agendamentos-a-concluir");
const mensagemAgendamentosAConcluir = document.getElementById("mensagem-agendamentos-a-concluir");
const painelHistoricoServicos = document.getElementById("painel-historico-servicos");
const tituloHistoricoServicos = document.getElementById("titulo-historico-servicos");
const listaHistoricoServicos = document.getElementById("lista-historico-servicos");
const totalHistoricoServicos = document.getElementById("total-historico-servicos");
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
const campoDataAgendaBarbeiro = document.getElementById("data-agenda-barbeiro");
const listaAgendamentos = document.getElementById("lista-agendamentos");
const totalAgendamentos = document.getElementById("total-agendamentos");
const painelConfirmarAgendamento = document.getElementById("painel-confirmar-agendamento");
const resumoAgendamento = document.getElementById("resumo-agendamento");
const mensagemAgendamento = document.getElementById("mensagem-agendamento");
const botaoConfirmarAgendamento = document.getElementById("botao-confirmar-agendamento");
const paineisNavegacao = [
  painelAgendarCliente,
  painelAgendamentosCliente,
  painelAgendamentosPendentes,
  painelAgendamentosAConcluir,
  painelAgendaBarbeiro,
  painelAdicionar,
  painelHistoricoServicos,
  painelSolicitacoesBarbeiros,
  painelContasAdministrador,
];
const seletorPerfil = Array.from(document.querySelectorAll("[data-perfil]"));
const seletorPerfilLogin = Array.from(document.querySelectorAll("[data-login-perfil]"));
const formatarPreco = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});
const formatarPrecoComCentavos = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const nomeBarbeiroValido = /^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ ]*$/;
let perfilSelecionado = "clientes";
let perfilLoginSelecionado = "clientes";
let tipoUsuario = null;
let administradorUsuario = false;
let servicoSelecionadoId = null;
let servicoSelecionadoNome = null;
let barbeiroSelecionadoId = null;
let barbeiroSelecionadoNome = null;
let dataSelecionada = null;
let horarioSelecionado = null;
let agendamentoSolicitado = false;
let confirmandoAgendamento = false;
let contasClientes = [];
let contasBarbeiros = [];

document.body.insertBefore(navegacaoUsuario, document.querySelector("main"));

new ResizeObserver(() => {
  const alturaCabecalho = cabecalhoSite.getBoundingClientRect().height;
  document.documentElement.style.setProperty("--altura-cabecalho", `${alturaCabecalho}px`);
}).observe(cabecalhoSite);

new ResizeObserver(() => {
  const alturaMenu = navegacaoUsuario.getBoundingClientRect().height;
  document.documentElement.style.setProperty("--altura-menu-mobile", `${alturaMenu}px`);
}).observe(navegacaoUsuario);

function atualizarBotaoTema(tema) {
  const temaEscuro = tema === "escuro";
  document.documentElement.dataset.tema = temaEscuro ? "escuro" : "claro";
  botoesTema.forEach((botao) => {
    botao.textContent = temaEscuro ? "Ativar tema claro" : "Ativar tema escuro";
    botao.setAttribute("aria-pressed", String(temaEscuro));
  });
  document.querySelector('meta[name="theme-color"]').content = temaEscuro ? "#171a1f" : "#ffffff";
}

try {
  atualizarBotaoTema(localStorage.getItem("fadehouse-tema") || "claro");
} catch {
  atualizarBotaoTema("claro");
}

botoesTema.forEach((botao) => botao.addEventListener("click", () => {
  const tema = document.documentElement.dataset.tema === "escuro" ? "claro" : "escuro";
  atualizarBotaoTema(tema);
  try {
    localStorage.setItem("fadehouse-tema", tema);
  } catch {}
}));

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
  botaoConfirmarAgendamento.disabled = !completo || confirmandoAgendamento || agendamentoSolicitado;

  if (!agendamentoSolicitado) {
    resumoAgendamento.textContent = completo
      ? `${servicoSelecionadoNome} com ${barbeiroSelecionadoNome}, em ${dataSelecionada.split("-").reverse().join("/")} às ${horarioSelecionado}.`
      : "Escolha o serviço, barbeiro, data e horário.";
  }
}

function selecaoAgendamentoAlterada() {
  agendamentoSolicitado = false;
  mensagemAgendamento.textContent = "";
  mensagemAgendamento.className = "mensagem";
  botaoConfirmarAgendamento.textContent = "Solicitar agendamento";
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
    const textoHorario = document.createElement("span");
    textoHorario.textContent = horario;
    botao.append(textoHorario);
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

campoNomeCadastro.addEventListener("input", () => {
  const posicaoAtual = campoNomeCadastro.selectionStart ?? campoNomeCadastro.value.length;
  const textoAntesDoCursor = campoNomeCadastro.value.slice(0, posicaoAtual);
  const nomeSemNumeros = campoNomeCadastro.value.replace(/\p{N}/gu, "");
  const cursorSemNumeros = textoAntesDoCursor.replace(/\p{N}/gu, "").length;
  campoNomeCadastro.value = nomeSemNumeros;
  campoNomeCadastro.setSelectionRange(cursorSemNumeros, cursorSemNumeros);
});

function ocultarAreaServicos() {
  telaServicos.hidden = true;
  telaServicos.classList.remove("usuario-ativo");
  document.body.classList.remove("usuario-logado");
  navegacaoUsuario.hidden = true;
}

function mostrarCadastro() {
  ocultarAreaServicos();
  telaCadastro.hidden = false;
  telaLogin.hidden = true;
}

function mostrarLogin() {
  ocultarAreaServicos();
  telaCadastro.hidden = true;
  telaLogin.hidden = false;
}

function paineisDaAba(tipo) {
  if (tipoUsuario === "clientes") {
    return tipo === "agendar" ? [painelAgendarCliente] : [painelAgendamentosCliente];
  }

  if (tipo === "agendamentos") {
    return [painelAgendamentosPendentes, painelAgendamentosAConcluir, painelAgendaBarbeiro];
  }
  if (tipo === "servicos") return [painelAgendarCliente, painelAdicionar];
  if (tipo === "administracao") {
    return [painelSolicitacoesBarbeiros, painelContasAdministrador, painelHistoricoServicos];
  }
  return [painelHistoricoServicos];
}

function selecionarAbaUsuario(tipo) {
  const opcoes = Array.from(abasUsuario.querySelectorAll("[data-aba-usuario]"));
  const abaAtiva = opcoes.find((aba) => aba.dataset.abaUsuario === tipo);
  if (!abaAtiva) return;

  const paineisAtivos = paineisDaAba(tipo);
  paineisNavegacao.forEach((painel) => {
    painel.hidden = !paineisAtivos.includes(painel);
  });
  paineisAtivos.forEach((painel) => {
    painel.setAttribute("role", "tabpanel");
    painel.setAttribute("aria-labelledby", abaAtiva.id);
  });
  opcoes.forEach((aba) => {
    const selecionada = aba === abaAtiva;
    aba.classList.toggle("selecionada", selecionada);
    aba.setAttribute("aria-selected", String(selecionada));
    aba.tabIndex = selecionada ? 0 : -1;
  });
  if (tipoUsuario === "clientes" && tipo === "agendamentos") carregarProximosAgendamentos();
}

function renderizarAbasUsuario(usuario) {
  const cliente = usuario.tipo === "clientes";
  const administrador = usuario.administrador === true;
  const itens = cliente
    ? [["agendar", "Agende aqui"], ["agendamentos", "Agendamentos"]]
    : [["agendamentos", "Agendamentos"], ["servicos", "Serviços"], ["historico", "Histórico"]];
  if (administrador) itens.push(["administracao", "Administração"]);

  navegacaoUsuario.setAttribute(
    "aria-label",
    cliente ? "Navegação do cliente" : administrador ? "Navegação da administração" : "Navegação do barbeiro",
  );
  abasUsuario.replaceChildren();
  itens.forEach(([tipo, texto]) => {
    const botao = document.createElement("button");
    botao.id = `aba-${tipo}-usuario`;
    botao.type = "button";
    botao.className = "aba-cliente";
    botao.dataset.abaUsuario = tipo;
    botao.setAttribute("role", "tab");
    botao.setAttribute("aria-selected", "false");
    botao.setAttribute("aria-controls", paineisDaAba(tipo).map((painel) => painel.id).join(" "));
    botao.tabIndex = -1;
    botao.textContent = texto;
    abasUsuario.append(botao);
  });
}

abasUsuario.addEventListener("click", (evento) => {
  const aba = evento.target.closest("[data-aba-usuario]");
  if (aba) selecionarAbaUsuario(aba.dataset.abaUsuario);
});

abasUsuario.addEventListener("keydown", (evento) => {
  const opcoes = Array.from(abasUsuario.querySelectorAll("[data-aba-usuario]"));
  const indice = opcoes.indexOf(evento.target.closest("[data-aba-usuario]"));
  if (indice < 0) return;
  const direcoes = { ArrowRight: 1, ArrowLeft: -1, Home: -indice, End: opcoes.length - indice - 1 };
  if (!(evento.key in direcoes)) return;
  evento.preventDefault();
  const proximaAba = (indice + direcoes[evento.key] + opcoes.length) % opcoes.length;
  opcoes[proximaAba].focus();
  selecionarAbaUsuario(opcoes[proximaAba].dataset.abaUsuario);
});

function mostrarServicos(usuario) {
  tipoUsuario = usuario.tipo;
  administradorUsuario = usuario.administrador === true;
  const cliente = tipoUsuario === "clientes";
  telaCadastro.hidden = true;
  telaLogin.hidden = true;
  telaServicos.hidden = false;
  telaServicos.classList.add("usuario-ativo");
  document.body.classList.add("usuario-logado");
  navegacaoUsuario.hidden = false;
  cabecalhoBarbeiro.hidden = true;
  painelAgendarCliente.hidden = false;
  painelAgendamentosCliente.hidden = true;
  painelProximoAgendamento.hidden = tipoUsuario !== "clientes";
  painelAgendamentosPendentes.hidden = tipoUsuario !== "barbeiros";
  painelAgendamentosAConcluir.hidden = tipoUsuario !== "barbeiros";
  painelAdicionar.hidden = tipoUsuario !== "barbeiros";
  painelSolicitacoesBarbeiros.hidden = !usuario.administrador;
  painelContasAdministrador.hidden = !usuario.administrador;
  painelAgendaBarbeiro.hidden = tipoUsuario !== "barbeiros";
  painelHistoricoServicos.hidden = tipoUsuario !== "barbeiros";
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
  horarioSelecionadoTexto.className = "mensagem";
  agendamentoSolicitado = false;
  confirmandoAgendamento = false;
  mensagemAgendamento.textContent = "";
  botaoConfirmarAgendamento.textContent = "Solicitar agendamento";
  atualizarResumoAgendamento();
  renderizarHorarios();
  document.getElementById("boas-vindas-usuario").textContent = `Olá, ${usuario.nome}`;
  document.getElementById("boas-vindas-barbeiro").textContent = `Olá, ${usuario.nome}`;
  renderizarAbasUsuario(usuario);
  selecionarAbaUsuario(cliente ? "agendar" : "agendamentos");
  document.getElementById("tipo-usuario").textContent = tipoUsuario === "barbeiros"
    ? "Área do barbeiro"
    : "Área do cliente";
  carregarServicos();
  if (tipoUsuario === "clientes") {
    carregarProximosAgendamentos();
    carregarBarbeiros();
  } else {
    carregarAgendamentosPendentes();
    carregarAgendamentosAConcluir();
    campoDataAgendaBarbeiro.value = dataLocalAtual();
    carregarAgendamentosBarbeiro(true);
    tituloHistoricoServicos.textContent = usuario.administrador
      ? "Histórico de serviços de todos os barbeiros"
      : "Meu histórico de serviços";
    carregarHistoricoServicos();
    if (usuario.administrador) {
      carregarSolicitacoesBarbeiros();
      carregarContasAdministrador();
    }
  }
}

async function carregarProximosAgendamentos(silencioso = false) {
  if (!silencioso) {
    statusProximoAgendamento.textContent = "Carregando agendamentos...";
    listaProximosAgendamentos.replaceChildren();
  }

  try {
    const resposta = await fetch("/api/meu-agendamento");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar agendamento.");
    listaProximosAgendamentos.replaceChildren();
    if (corpo.agendamentos.length === 0) {
      statusProximoAgendamento.textContent = "Você não tem agendamentos futuros.";
      return;
    }

    statusProximoAgendamento.textContent = "";
    corpo.agendamentos.forEach((agendamento) => {
      const item = document.createElement("article");
      item.className = "item-proximo-agendamento";
      if (agendamento.status === "cancelado") {
        item.classList.add("agendamento-cancelado");
        const remover = document.createElement("button");
        remover.type = "button";
        remover.className = "botao-remover-agendamento";
        remover.dataset.id = agendamento.id;
        remover.setAttribute("aria-label", "Remover agendamento cancelado");
        remover.title = "Remover agendamento cancelado";
        remover.textContent = "×";
        item.append(remover);
      }
      const detalhes = document.createElement("dl");
      detalhes.className = "detalhes-agendamento";
      const dados = [
        ["Horário", agendamento.horario],
        ["Data", agendamento.data.split("-").reverse().join("/")],
        ["Barbeiro", agendamento.barbeiro],
        ["Serviço", agendamento.servico],
        ["Duração", `${agendamento.duracao} min`],
        ["Valor", `R$ ${formatarPrecoComCentavos.format(agendamento.preco)}`],
      ];

      dados.forEach(([rotulo, valor]) => {
        const campo = document.createElement("div");
        campo.className = "dado-agendamento";
        if (rotulo === "Barbeiro") campo.classList.add("dado-agendamento-barbeiro");
        const titulo = document.createElement("dt");
        titulo.textContent = rotulo;
        const detalhe = document.createElement("dd");
        detalhe.textContent = valor;
        campo.append(titulo, detalhe);
        detalhes.append(campo);
      });

      const status = document.createElement("p");
      status.className = `status-agendamento status-${agendamento.status}`;
      status.textContent = `Status: ${agendamento.status}`;
      item.append(detalhes, status);
      listaProximosAgendamentos.append(item);
    });
  } catch {
    if (!silencioso) {
      statusProximoAgendamento.textContent = "Não foi possível carregar seus próximos agendamentos.";
    }
  }
}

listaProximosAgendamentos.addEventListener("click", async (evento) => {
  const botao = evento.target.closest(".botao-remover-agendamento");
  if (!botao) return;

  botao.disabled = true;
  try {
    const resposta = await fetch(`/api/meu-agendamento/${botao.dataset.id}`, {
      method: "DELETE",
    });
    const corpo = resposta.status === 204 ? {} : await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Não foi possível remover o agendamento.");
    await carregarProximosAgendamentos();
  } catch (erro) {
    statusProximoAgendamento.textContent = erro.message || "Não foi possível remover o agendamento.";
    botao.disabled = false;
  }
});

async function carregarAgendamentosPendentes() {
  listaAgendamentosPendentes.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando agendamentos pendentes...";
  listaAgendamentosPendentes.append(carregando);
  totalAgendamentosPendentes.textContent = "";

  try {
    const resposta = await fetch("/api/agendamentos-pendentes");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar agendamentos pendentes.");
    listaAgendamentosPendentes.replaceChildren();
    totalAgendamentosPendentes.textContent = `${corpo.agendamentos.length} ${corpo.agendamentos.length === 1 ? "solicitação" : "solicitações"}`;

    if (corpo.agendamentos.length === 0) {
      const vazio = document.createElement("li");
      vazio.className = "estado-lista";
      vazio.textContent = "Nenhum agendamento pendente.";
      listaAgendamentosPendentes.append(vazio);
      return;
    }

    corpo.agendamentos.forEach((agendamento) => {
      const item = document.createElement("li");
      item.className = "servico agendamento-pendente";
      const informacoes = document.createElement("div");
      informacoes.className = "servico-info agendamento-pendente-info";
      const titulo = document.createElement("strong");
      const partesNome = (agendamento.cliente || "Cliente não encontrado").trim().split(/\s+/);
      const particulasSobrenome = ["da", "das", "de", "do", "dos"];
      let inicioSobrenome = partesNome.length - 1;
      if (inicioSobrenome > 1 && particulasSobrenome.includes(partesNome[inicioSobrenome - 1].toLowerCase())) {
        inicioSobrenome -= 1;
      }
      const nomeCliente = [partesNome[0], ...partesNome.slice(inicioSobrenome)].join(" ");
      titulo.className = "agendamento-pendente-titulo";
      titulo.textContent = `${agendamento.servico} · ${nomeCliente}${corpo.administrador ? ` · ${agendamento.barbeiro}` : ""}`;
      const detalhe = document.createElement("span");
      detalhe.className = "servico-detalhe agendamento-pendente-detalhes";
      [
        `${agendamento.data.split("-").reverse().join("/")} às ${agendamento.horario}`,
        `${agendamento.duracao} min`,
        `R$ ${formatarPreco.format(agendamento.preco)}`,
      ].forEach((texto) => {
        const campo = document.createElement("span");
        campo.textContent = texto;
        detalhe.append(campo);
      });
      informacoes.append(titulo, detalhe);

      const acoes = document.createElement("div");
      acoes.className = "acoes-solicitacao";
      [["confirmado", "Aceitar", "botao-aprovar"], ["cancelado", "Recusar", "botao-recusar"]].forEach(([status, texto, classe]) => {
        const botao = document.createElement("button");
        botao.type = "button";
        botao.className = classe;
        botao.dataset.id = agendamento.id;
        botao.dataset.status = status;
        botao.textContent = texto;
        acoes.append(botao);
      });

      item.append(informacoes, acoes);
      listaAgendamentosPendentes.append(item);
    });
  } catch {
    totalAgendamentosPendentes.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar os agendamentos pendentes.";
    listaAgendamentosPendentes.replaceChildren(erro);
  }
}

painelAgendamentosPendentes.addEventListener("click", async (evento) => {
  const botao = evento.target.closest("[data-status]");
  if (!botao) return;

  const item = botao.closest(".servico");
  item.querySelectorAll("button").forEach((acao) => {
    acao.disabled = true;
  });
  mensagemAgendamentosPendentes.textContent = "";
  mensagemAgendamentosPendentes.className = "mensagem";

  try {
    const resposta = await fetch(`/api/agendamentos/${botao.dataset.id}/decisao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: botao.dataset.status }),
    });
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Não foi possível atualizar o agendamento.");

    mensagemAgendamentosPendentes.textContent = botao.dataset.status === "confirmado"
      ? "Agendamento confirmado."
      : "Agendamento cancelado.";
    if (botao.dataset.status === "confirmado") {
      mensagemAgendamentosPendentes.classList.add("sucesso");
    }
    await Promise.all([
      carregarAgendamentosPendentes(),
      carregarAgendamentosAConcluir(),
      carregarAgendamentosBarbeiro(),
    ]);
  } catch (erro) {
    mensagemAgendamentosPendentes.textContent = erro.message;
    item.querySelectorAll("button").forEach((acao) => {
      acao.disabled = false;
    });
  }
});

async function carregarAgendamentosAConcluir() {
  listaAgendamentosAConcluir.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando serviços aguardando conclusão...";
  listaAgendamentosAConcluir.append(carregando);
  totalAgendamentosAConcluir.textContent = "";

  try {
    const resposta = await fetch("/api/agendamentos-a-concluir");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar serviços aguardando conclusão.");
    listaAgendamentosAConcluir.replaceChildren();
    totalAgendamentosAConcluir.textContent = `${corpo.agendamentos.length} ${corpo.agendamentos.length === 1 ? "serviço" : "serviços"}`;

    if (corpo.agendamentos.length === 0) {
      const vazio = document.createElement("li");
      vazio.className = "estado-lista";
      vazio.textContent = "Nenhum serviço aguardando conclusão.";
      listaAgendamentosAConcluir.append(vazio);
      return;
    }

    corpo.agendamentos.forEach((agendamento) => {
      const item = document.createElement("li");
      item.className = "servico";
      const informacoes = document.createElement("div");
      informacoes.className = "servico-info";
      const titulo = document.createElement("strong");
      titulo.textContent = `${agendamento.servico} · ${agendamento.cliente || "Cliente não encontrado"}`;
      const detalhe = document.createElement("span");
      detalhe.className = "servico-detalhe agendamento-pendente-detalhes";
      detalhe.textContent = `${agendamento.data.split("-").reverse().join("/")} às ${agendamento.horario} · ${agendamento.duracao} min · R$ ${formatarPreco.format(agendamento.preco)}`;
      informacoes.append(titulo, detalhe);

      item.append(informacoes);
      if (corpo.administrador) {
        const aguardandoBarbeiro = document.createElement("span");
        aguardandoBarbeiro.className = "status-agendamento status-pendente";
        aguardandoBarbeiro.textContent = "Aguardando barbeiro concluir";
        item.append(aguardandoBarbeiro);
      } else {
        const botaoConcluir = document.createElement("button");
        botaoConcluir.type = "button";
        botaoConcluir.className = "botao-aprovar botao-concluir-servico";
        botaoConcluir.dataset.id = agendamento.id;
        const fim = new Date(`${agendamento.data}T${agendamento.horario}`);
        fim.setMinutes(fim.getMinutes() + agendamento.duracao);
        botaoConcluir.disabled = fim > new Date();
        botaoConcluir.textContent = botaoConcluir.disabled ? "Aguardando horário" : "Confirmar conclusão";
        botaoConcluir.setAttribute(
          "aria-label",
          `${botaoConcluir.textContent}: ${agendamento.servico} com ${agendamento.cliente || "cliente"}`,
        );
        item.append(botaoConcluir);
      }
      listaAgendamentosAConcluir.append(item);
    });
  } catch {
    totalAgendamentosAConcluir.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar os serviços aguardando conclusão.";
    listaAgendamentosAConcluir.replaceChildren(erro);
  }
}

painelAgendamentosAConcluir.addEventListener("click", async (evento) => {
  const botao = evento.target.closest(".botao-concluir-servico");
  if (!botao || botao.disabled) return;
  if (!window.confirm("Confirma que este serviço foi realizado e concluído?")) return;

  botao.disabled = true;
  mensagemAgendamentosAConcluir.textContent = "";
  mensagemAgendamentosAConcluir.className = "mensagem";
  try {
    const resposta = await fetch(`/api/agendamentos/${botao.dataset.id}/concluir`, {
      method: "POST",
    });
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Não foi possível concluir o serviço.");
    mensagemAgendamentosAConcluir.textContent = "Serviço concluído e enviado ao histórico.";
    mensagemAgendamentosAConcluir.classList.add("sucesso");
    await Promise.all([
      carregarAgendamentosAConcluir(),
      carregarAgendamentosBarbeiro(),
      carregarHistoricoServicos(),
    ]);
  } catch (erro) {
    mensagemAgendamentosAConcluir.textContent = erro.message;
    botao.disabled = false;
  }
});

function renderizarHistoricoServicos(historico, administrador) {
  listaHistoricoServicos.replaceChildren();
  totalHistoricoServicos.textContent = `${historico.length} ${historico.length === 1 ? "serviço realizado" : "serviços realizados"}`;

  if (historico.length === 0) {
    const vazio = document.createElement("li");
    vazio.className = "estado-lista";
    vazio.textContent = "Nenhum serviço concluído até agora.";
    listaHistoricoServicos.append(vazio);
    return;
  }

  historico.forEach((servico) => {
    const item = document.createElement("li");
    item.className = "servico";
    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const titulo = document.createElement("strong");
    titulo.textContent = administrador ? `${servico.barbeiro} — ${servico.servico}` : servico.servico;
    const detalhes = document.createElement("span");
    detalhes.className = "servico-detalhe detalhe-conta";
    const [ano, mes, dia] = servico.data.split("-");
    detalhes.textContent = `${dia}/${mes}/${ano} às ${servico.horario} · ${servico.cliente || "Cliente não encontrado"} · ${servico.duracao} min · R$ ${formatarPreco.format(servico.preco)}`;
    informacoes.append(titulo, detalhes);
    item.append(informacoes);
    listaHistoricoServicos.append(item);
  });
}

async function carregarHistoricoServicos() {
  listaHistoricoServicos.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando histórico...";
  listaHistoricoServicos.append(carregando);
  totalHistoricoServicos.textContent = "";

  try {
    const resposta = await fetch("/api/historico-servicos");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar histórico.");
    renderizarHistoricoServicos(corpo.historico, corpo.administrador);
  } catch {
    totalHistoricoServicos.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar o histórico. Tente novamente.";
    listaHistoricoServicos.replaceChildren(erro);
  }
}

function normalizarBuscaConta(valor) {
  return String(valor)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .trim();
}

function filtrarContas(tipo) {
  const clientes = tipo === "clientes";
  const contas = clientes ? contasClientes : contasBarbeiros;
  const busca = clientes ? buscaContasClientes.value : buscaContasBarbeiros.value;
  const termo = normalizarBuscaConta(busca);
  const digitosBusca = termo.replace(/\D/g, "");
  const filtradas = contas.filter((conta) => {
    const correspondeTexto = [conta.nome, conta.email, conta.telefone]
      .some((valor) => normalizarBuscaConta(valor).includes(termo));
    const correspondeTelefone = digitosBusca.length > 0
      && conta.telefone.replace(/\D/g, "").includes(digitosBusca);
    return correspondeTexto || correspondeTelefone;
  });
  const listaContas = clientes ? listaContasClientes : listaContasBarbeiros;
  const totalContas = clientes ? totalContasClientes : totalContasBarbeiros;
  renderizarContas(tipo, filtradas, listaContas, totalContas, contas, Boolean(termo));
}

function renderizarContas(tipo, contas, listaContas, totalContas, todasContas, buscaAtiva) {
  listaContas.replaceChildren();
  totalContas.textContent = buscaAtiva
    ? `${contas.length} ${contas.length === 1 ? "resultado" : "resultados"}`
    : `${todasContas.length} ${todasContas.length === 1 ? "conta" : "contas"}`;

  if (contas.length === 0) {
    const vazio = document.createElement("li");
    vazio.className = "estado-lista";
    vazio.textContent = buscaAtiva ? "Nenhuma conta encontrada." : "Nenhuma conta cadastrada.";
    listaContas.append(vazio);
    return;
  }

  contas.forEach((conta) => {
    const item = document.createElement("li");
    item.className = "servico";
    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const nome = document.createElement("strong");
    nome.textContent = conta.nome;
    const dados = document.createElement("span");
    dados.className = "servico-detalhe detalhe-conta";
    dados.textContent = ` · ${conta.email} · ${formatarTelefone(conta.telefone)}`;
    informacoes.append(nome, dados);
    item.append(informacoes);

    if (conta.administrador) {
      const selo = document.createElement("span");
      selo.className = "selo-administrador";
      selo.textContent = "Administrador";
      item.append(selo);
    } else {
      const excluir = document.createElement("button");
      excluir.type = "button";
      excluir.className = "botao-remover-conta";
      excluir.dataset.tipo = tipo;
      excluir.dataset.id = conta.id;
      excluir.setAttribute("aria-label", `Excluir conta de ${conta.nome}`);
      excluir.textContent = "Excluir";
      item.append(excluir);
    }
    listaContas.append(item);
  });
}

buscaContasClientes.addEventListener("input", () => filtrarContas("clientes"));
buscaContasBarbeiros.addEventListener("input", () => filtrarContas("barbeiros"));

function selecionarAbaContas(tipo) {
  const clientesSelecionados = tipo === "clientes";
  painelContasClientes.hidden = !clientesSelecionados;
  painelContasBarbeiros.hidden = clientesSelecionados;
  abasContas.forEach((aba) => {
    const selecionada = aba.dataset.abaContas === tipo;
    aba.classList.toggle("selecionada", selecionada);
    aba.setAttribute("aria-selected", String(selecionada));
    aba.tabIndex = selecionada ? 0 : -1;
  });
}

abasContas.forEach((aba) => {
  aba.addEventListener("click", () => selecionarAbaContas(aba.dataset.abaContas));
});

async function carregarContasAdministrador() {
  listaContasClientes.replaceChildren();
  listaContasBarbeiros.replaceChildren();
  totalContasClientes.textContent = "";
  totalContasBarbeiros.textContent = "";
  [listaContasClientes, listaContasBarbeiros].forEach((listaContas) => {
    const carregando = document.createElement("li");
    carregando.className = "estado-lista";
    carregando.textContent = "Carregando contas...";
    listaContas.append(carregando);
  });

  try {
    const resposta = await fetch("/api/contas");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar contas.");
    contasClientes = corpo.clientes;
    contasBarbeiros = corpo.barbeiros;
    filtrarContas("clientes");
    filtrarContas("barbeiros");
  } catch {
    totalContasClientes.textContent = "";
    totalContasBarbeiros.textContent = "";
    [listaContasClientes, listaContasBarbeiros].forEach((listaContas) => {
      const erro = document.createElement("li");
      erro.className = "estado-lista";
      erro.textContent = "Não foi possível carregar as contas.";
      listaContas.replaceChildren(erro);
    });
  }
}

function renderizarSolicitacoesBarbeiros(solicitacoes) {
  listaSolicitacoesBarbeiros.replaceChildren();
  totalSolicitacoesBarbeiros.textContent = `${solicitacoes.length} ${solicitacoes.length === 1 ? "solicitação" : "solicitações"}`;

  if (solicitacoes.length === 0) {
    const vazio = document.createElement("li");
    vazio.className = "estado-lista";
    vazio.textContent = "Não há solicitações pendentes.";
    listaSolicitacoesBarbeiros.append(vazio);
    return;
  }

  solicitacoes.forEach((solicitacao) => {
    const item = document.createElement("li");
    item.className = "servico";
    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const nome = document.createElement("strong");
    nome.textContent = solicitacao.nome;
    const contato = document.createElement("span");
    contato.className = "servico-detalhe";
    contato.textContent = ` · ${solicitacao.email} · ${formatarTelefone(solicitacao.telefone)}`;
    informacoes.append(nome, contato);

    const acoes = document.createElement("div");
    acoes.className = "acoes-solicitacao";
    const aprovar = document.createElement("button");
    aprovar.type = "button";
    aprovar.className = "botao-aprovar";
    aprovar.dataset.acao = "aprovar";
    aprovar.dataset.id = solicitacao.id;
    aprovar.textContent = "Aprovar";
    const recusar = document.createElement("button");
    recusar.type = "button";
    recusar.className = "botao-recusar";
    recusar.dataset.acao = "recusar";
    recusar.dataset.id = solicitacao.id;
    recusar.textContent = "Recusar";
    acoes.append(aprovar, recusar);
    item.append(informacoes, acoes);
    listaSolicitacoesBarbeiros.append(item);
  });
}

async function carregarSolicitacoesBarbeiros() {
  listaSolicitacoesBarbeiros.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando solicitações...";
  listaSolicitacoesBarbeiros.append(carregando);
  totalSolicitacoesBarbeiros.textContent = "";

  try {
    const resposta = await fetch("/api/solicitacoes-barbeiros");
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar solicitações.");
    renderizarSolicitacoesBarbeiros(corpo.solicitacoes);
  } catch {
    totalSolicitacoesBarbeiros.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar as solicitações. Tente novamente.";
    listaSolicitacoesBarbeiros.replaceChildren(erro);
  }
}

function renderizarAgendamentosBarbeiro(agendamentos) {
  listaAgendamentos.replaceChildren();
  totalAgendamentos.textContent = `${agendamentos.length} ${agendamentos.length === 1 ? "agendamento" : "agendamentos"}`;

  if (agendamentos.length === 0) {
    const vazio = document.createElement("li");
    vazio.className = "estado-lista";
    vazio.textContent = "Nenhum agendamento para esta data.";
    listaAgendamentos.append(vazio);
    return;
  }

  agendamentos.forEach((agendamento) => {
    const item = document.createElement("li");
    item.className = "servico";

    const informacoes = document.createElement("div");
    informacoes.className = "servico-info";
    const titulo = document.createElement("strong");
    titulo.textContent = `${agendamento.horario} — ${agendamento.servico}`;
    const detalhe = document.createElement("span");
    detalhe.className = "servico-detalhe";
    detalhe.textContent = ` · ${agendamento.cliente || "Cliente não encontrado"} · ${agendamento.duracao} min · R$ ${formatarPreco.format(agendamento.preco)}`;
    informacoes.append(titulo, detalhe);
    item.append(informacoes);
    listaAgendamentos.append(item);
  });
}

async function carregarAgendamentosBarbeiro(proximaData = false) {
  listaAgendamentos.replaceChildren();
  const carregando = document.createElement("li");
  carregando.className = "estado-lista";
  carregando.textContent = "Carregando agendamentos...";
  listaAgendamentos.append(carregando);
  totalAgendamentos.textContent = "";

  try {
    const data = encodeURIComponent(campoDataAgendaBarbeiro.value);
    const url = proximaData ? "/api/agendamentos?proximo=1" : `/api/agendamentos?data=${data}`;
    const resposta = await fetch(url);
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Falha ao carregar agendamentos.");
    if (proximaData) campoDataAgendaBarbeiro.value = corpo.data;
    renderizarAgendamentosBarbeiro(corpo.agendamentos);
  } catch {
    totalAgendamentos.textContent = "";
    const erro = document.createElement("li");
    erro.className = "estado-lista";
    erro.textContent = "Não foi possível carregar os agendamentos. Tente novamente.";
    listaAgendamentos.replaceChildren(erro);
  }
}

seletorPerfil.forEach((botao) => {
  botao.addEventListener("click", () => {
    perfilSelecionado = botao.dataset.perfil;
    seletorPerfil.forEach((item) => {
      const selecionado = item === botao;
      item.classList.toggle("perfil-selecionado", selecionado);
      item.setAttribute("aria-pressed", String(selecionado));
    });
    botaoCadastro.textContent = perfilSelecionado === "clientes"
      ? "Cadastrar como cliente"
      : "Solicitar cadastro";
  });
});

document.getElementById("abrir-login").addEventListener("click", mostrarLogin);
document.getElementById("abrir-cadastro").addEventListener("click", mostrarCadastro);
campoDataAgendaBarbeiro.addEventListener("change", () => carregarAgendamentosBarbeiro());
campoDataAgendamento.addEventListener("change", () => {
  const hoje = dataLocalAtual();
  campoDataAgendamento.min = hoje;

  if (!campoDataAgendamento.value || campoDataAgendamento.value < hoje) {
    campoDataAgendamento.value = "";
    dataSelecionada = null;
    horarioSelecionado = null;
    painelEscolherHorario.hidden = true;
    horarioSelecionadoTexto.textContent = "";
    horarioSelecionadoTexto.className = "mensagem";
    renderizarHorarios();
    mensagemData.textContent = "Escolha hoje ou uma data futura.";
    selecaoAgendamentoAlterada();
    return;
  }

  dataSelecionada = campoDataAgendamento.value;
  horarioSelecionado = null;
  horarioSelecionadoTexto.textContent = "";
  horarioSelecionadoTexto.className = "mensagem";
  const [ano, mes, dia] = dataSelecionada.split("-");
  const domingo = new Date(Date.UTC(Number(ano), Number(mes) - 1, Number(dia))).getUTCDay() === 0;
  painelEscolherHorario.hidden = false;
  faixaHorarios.hidden = domingo;

  if (domingo) {
    mensagemData.textContent = "A barbearia não abre aos domingos.";
    listaHorarios.replaceChildren();
    horarioSelecionadoTexto.textContent = "Não há horários disponíveis, pois a barbearia não abre aos domingos.";
    horarioSelecionadoTexto.className = "mensagem";
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
    nome.className = "nome-barbeiro";
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
    if (perfilSelecionado === "barbeiros") {
      mensagemCadastro.textContent = "Solicitação enviada ao administrador. Você poderá entrar após a aprovação.";
      mensagemCadastro.classList.add("sucesso");
      return;
    }

    const sessao = await fetch("/api/sessao");
    const usuario = await sessao.json();
    mostrarServicos(usuario);
  } catch {
    mensagemCadastro.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    botaoCadastro.disabled = false;
  }
});

listaSolicitacoesBarbeiros.addEventListener("click", async (evento) => {
  const botao = evento.target.closest("[data-acao][data-id]");
  if (!botao) return;

  const item = botao.closest(".servico");
  item.querySelectorAll("button").forEach((acao) => {
    acao.disabled = true;
  });
  const endpoint = `/api/solicitacoes-barbeiros/${botao.dataset.id}`;
  try {
    const resposta = await fetch(
      botao.dataset.acao === "aprovar" ? `${endpoint}/aprovar` : endpoint,
      { method: botao.dataset.acao === "aprovar" ? "POST" : "DELETE" },
    );
    if (!resposta.ok) throw new Error("Não foi possível atualizar a solicitação.");
    await carregarSolicitacoesBarbeiros();
  } catch {
    item.querySelectorAll("button").forEach((acao) => {
      acao.disabled = false;
    });
  }
});

painelContasAdministrador.addEventListener("click", async (evento) => {
  const botao = evento.target.closest(".botao-remover-conta");
  if (!botao) return;

  if (!window.confirm("Deseja excluir esta conta? Esta ação não pode ser desfeita.")) return;

  botao.disabled = true;
  mensagemContasAdministrador.textContent = "";
  mensagemContasAdministrador.className = "mensagem";
  try {
    const resposta = await fetch(`/api/contas/${botao.dataset.tipo}/${botao.dataset.id}`, {
      method: "DELETE",
    });
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || "Não foi possível excluir a conta.");
    mensagemContasAdministrador.textContent = "Conta excluída.";
    mensagemContasAdministrador.classList.add("sucesso");
    await carregarContasAdministrador();
  } catch (erro) {
    mensagemContasAdministrador.textContent = erro.message;
    botao.disabled = false;
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

window.setInterval(() => {
  if (tipoUsuario === "clientes") carregarProximosAgendamentos(true);
}, 10000);

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
  horarioSelecionadoTexto.className = "mensagem sucesso";
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

    agendamentoSolicitado = true;
    const agendamento = corpo.agendamento;
    resumoAgendamento.textContent = `${agendamento.servico} com ${agendamento.barbeiro}, em ${agendamento.data.split("-").reverse().join("/")} às ${agendamento.horario}.`;
    mensagemAgendamento.textContent = "Solicitação enviada ao barbeiro, aguardando confirmação.";
    botaoConfirmarAgendamento.textContent = "Solicitação enviada";
    await carregarProximosAgendamentos();
  } catch {
    mensagemAgendamento.textContent = "Sem conexão com o servidor. Tente novamente.";
  } finally {
    confirmandoAgendamento = false;
    atualizarResumoAgendamento();
  }
});

botoesSair.forEach((botaoSair) => botaoSair.addEventListener("click", async () => {
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
}));

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
# -*- coding: utf-8 -*-
"""
Gerador das paginas do site Vanira Araujo Advogados.

Produz:
  - areas-de-atuacao.html  (hub com todas as areas)
  - uma pagina por area de atuacao
  - politica-de-privacidade.html
  - sitemap.xml

Header, rodape, meta tags e JSON-LD ficam definidos uma unica vez aqui,
para que as paginas nao saiam do ar de sincronia entre si.

Uso:  python build.py
"""
import io, os, json, datetime

BASE = "https://vanira-advocacia.vercel.app"
OUT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# ICONES (traco 1.8, familia unica)
# --------------------------------------------------------------------------
WA = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.6.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.2-.6-1.5-.9-2-.2-.5-.4-.4-.6-.5h-.5c-.2 0-.5.1-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 5 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/>'
      '<path d="M12 2a10 10 0 00-8.6 15l-1.3 4.9L7.2 20A10 10 0 1012 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-2.9.8.8-2.8-.2-.3A8.2 8.2 0 1112 20.2z"/></svg>')
WA_BIG = WA.replace('width="18" height="18" ', '')
TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')
ARROW = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
ARROW_SM = ARROW.replace('width="20" height="20"', 'width="18" height="18"')

IC = {
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 2"/><circle cx="12" cy="12" r="9"/></svg>',
 "chat":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 01-9 8.4 8.4 8.4 0 01-3.6-.8L3 20.5l1.4-5.4A8.4 8.4 0 1121 11.5z"/></svg>',
 "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M6 7l-3 6a3 3 0 006 0L6 7z"/><path d="M18 7l-3 6a3 3 0 006 0l-3-6z"/><path d="M7 7h10"/><path d="M8 21h8"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 9.5-4-1.2-7-5-7-9.5V6l7-3z"/><path d="M9.5 12l1.8 1.8L15 10"/></svg>',
 "car":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14"/><path d="M4 17v-4l2-5h12l2 5v4"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/></svg>',
 "tractor":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="7" cy="16.5" r="3.5"/><circle cx="18" cy="17.5" r="2.5"/><path d="M4 13V8h5l2 5"/><path d="M11 8h4l1 5"/></svg>',
 "doc":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg>',
 "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19h16"/><path d="M7 16V9M12 16V5M17 16v-4"/></svg>',
 "house": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20h14V9.5"/><path d="M9.5 20v-5.5h5V20"/></svg>',
}

# --------------------------------------------------------------------------
# AREAS DE ATUACAO
# --------------------------------------------------------------------------
AREAS = [
 dict(slug="prorrogacao", icon="clock", grupo="Dívida Rural",
      nav="Prorrogação e Alongamento de Dívida Rural",
      h1="Prorrogação e Alongamento de Dívida Rural",
      title="Prorrogação e Alongamento de Dívida Rural | Vanira Araújo Advogados",
      desc=("Renegociação de contratos de crédito rural com base no MCR para alongar prazos e "
            "reduzir o peso da dívida. Dra. Vanira Araújo, OAB/MG 200.037, Uberaba/MG."),
      lead=("Renegociação de contratos de crédito rural afetados por fatores alheios à vontade do "
            "produtor, como quebra de safra, estiagem, geada ou queda abrupta de preços. Atuação com "
            "base no MCR (Manual de Crédito Rural) para alongar prazos e reduzir o peso da dívida "
            "sem comprometer a continuidade da atividade."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre prorrogação e alongamento de dívida rural. Pode me ajudar?",
      servicos=["Alongamento da dívida rural", "Revisão de contratos",
                "Negociação das dívidas do produtor rural"]),

 dict(slug="recuperacao-extrajudicial", icon="chat", grupo="Dívida Rural",
      nav="Recuperação Extrajudicial (Recuperação Branca)",
      h1="Recuperação Extrajudicial (Recuperação Branca)",
      title="Recuperação Extrajudicial (Recuperação Branca) | Vanira Araújo Advogados",
      desc=("Negociação direta com bancos antes do processo judicial: acordo, redução de encargos e "
            "reestruturação de dívida rural de forma rápida e discreta."),
      lead=("Negociação direta com instituições financeiras antes de qualquer processo judicial, "
            "buscando acordo, redução de encargos e reestruturação de dívida de forma rápida e "
            "discreta, preservando o relacionamento do produtor com o banco e evitando desgaste "
            "desnecessário."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre recuperação extrajudicial da minha dívida rural. Pode me ajudar?",
      servicos=["Negociação das dívidas do produtor rural", "Revisão de contratos",
                "Recuperação de crédito"]),

 dict(slug="recuperacao-judicial", icon="scale", grupo="Dívida Rural",
      nav="Recuperação Judicial",
      h1="Recuperação Judicial",
      title="Recuperação Judicial do Produtor Rural | Vanira Araújo Advogados",
      desc=("Condução do processo de recuperação judicial do produtor rural: suspensão de execuções, "
            "proteção do patrimônio produtivo e plano de pagamento viável."),
      lead=("Quando a negociação direta não é suficiente, atuamos na condução do processo de "
            "recuperação judicial do produtor rural, garantindo a suspensão de execuções, a proteção "
            "do patrimônio produtivo e um plano de pagamento viável para a continuidade da atividade."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre recuperação judicial do produtor rural. Pode me ajudar?",
      servicos=["Recuperação de crédito", "Negociação das dívidas do produtor rural",
                "Defesa na execução de dívidas do produtor rural"]),

 dict(slug="defesa-produtor-rural", icon="shield", grupo="Dívida Rural",
      nav="Defesa do Produtor Rural",
      h1="Defesa do Produtor Rural",
      title="Defesa do Produtor Rural em Ações Bancárias | Vanira Araújo Advogados",
      desc=("Representação em ações revisionais, execuções e disputas com bancos, com foco na "
            "proteção do bem de família, dos maquinários e da terra produtiva."),
      lead=("Representação em ações revisionais, execuções e demais disputas envolvendo bancos e "
            "instituições financeiras, com foco na proteção do bem de família, dos maquinários e "
            "da terra produtiva."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre a defesa do produtor rural. Pode me ajudar?",
      servicos=["Defesa na execução de dívidas do produtor rural",
                "Redução da hipoteca em operações de crédito rural",
                "Ação contra venda casada em contratos de crédito rural",
                "Revisão de contratos"]),

 dict(slug="busca-apreensao-veiculos", icon="car", grupo="Defesa de Bens",
      nav="Busca e Apreensão de Veículos",
      h1="Busca e Apreensão de Veículos",
      title="Defesa em Busca e Apreensão de Veículos | Vanira Araújo Advogados",
      desc=("Defesa em ações de busca e apreensão de veículos. Atuamos para buscar a devolução do "
            "veículo ou evitar que você o perca para o banco. Mais de 10 anos de atuação."),
      lead=("Defesa em ações de busca e apreensão movidas por bancos e financeiras em contratos com "
            "alienação fiduciária. Atuamos em favor do consumidor com o objetivo de buscar a devolução "
            "do veículo ou evitar que você perca o veículo para o banco."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre busca e apreensão do meu veículo. Pode me ajudar?",
      servicos=["Defesa em ação de busca e apreensão",
                "Revisão de contrato de veículos, com análise de juros abusivos",
                "Recuperação de veículos apreendidos por bancos e financeiras",
                "Renegociação de dívidas bancárias"]),

 dict(slug="busca-apreensao-maquinas", icon="tractor", grupo="Defesa de Bens",
      nav="Busca e Apreensão de Máquinas Agrícolas",
      h1="Busca e Apreensão de Máquinas Agrícolas",
      title="Defesa em Busca e Apreensão de Máquinas Agrícolas | Vanira Araújo Advogados",
      desc=("Defesa em ações de busca e apreensão de tratores, colheitadeiras e implementos "
            "financiados. Proteção do maquinário que mantém a lavoura em operação."),
      lead=("Defesa em ações de busca e apreensão que envolvem tratores, colheitadeiras, pulverizadores "
            "e demais implementos financiados com alienação fiduciária. A perda do maquinário "
            "interrompe a safra, por isso a defesa precisa ser rápida e técnica, com análise do "
            "contrato e dos requisitos legais da ação."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre busca e apreensão de máquina agrícola. Pode me ajudar?",
      servicos=["Defesa em ação de busca e apreensão de maquinário",
                "Revisão do contrato de financiamento da máquina",
                "Análise de juros e encargos cobrados",
                "Negociação com a instituição financeira"]),

 dict(slug="suspensao-leilao-imoveis", icon="house", grupo="Defesa de Bens",
      nav="Suspensão de Leilão de Imóveis",
      h1="Suspensão de Leilão de Imóveis",
      title="Suspensão de Leilão de Imóveis Urbanos e Rurais | Vanira Araújo Advogados",
      desc=("Defesa para suspender o leilão de imóveis urbanos e rurais em execução de dívida "
            "bancária, financiamento imobiliário ou hipoteca. Proteção do patrimônio."),
      lead=("Atuação para suspender o leilão de imóveis urbanos e rurais levados a hasta pública em "
            "execuções de dívida bancária, financiamento imobiliário e hipotecas. Buscamos suspender "
            "o leilão, discutir o valor cobrado e preservar o imóvel, seja a moradia da família ou a "
            "terra produtiva."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre a suspensão de leilão de imóvel. Pode me ajudar?",
      servicos=["Suspensão de leilão de imóvel urbano ou rural",
                "Defesa em execução hipotecária e de financiamento imobiliário",
                "Revisão do contrato e do valor da dívida",
                "Proteção do bem de família e da terra produtiva"]),

 dict(slug="revisao-contratos-pj", icon="doc", grupo="Empresas",
      nav="Revisão de Contratos de Pessoa Jurídica",
      h1="Revisão de Contratos de Pessoa Jurídica",
      title="Revisão de Contratos Bancários de Pessoa Jurídica | Vanira Araújo Advogados",
      desc=("Revisão de contratos bancários de empresas: capital de giro, FGI, FGO, Pronamp e BNDES. "
            "Análise de juros, encargos e cláusulas abusivas."),
      lead=("Análise técnica dos contratos bancários da empresa para identificar juros, encargos e "
            "cláusulas em desacordo com o que foi contratado. A revisão alcança as principais linhas "
            "de crédito tomadas por pessoa jurídica e serve de base tanto para renegociação quanto "
            "para defesa em cobrança."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre revisão de contrato bancário da minha empresa. Pode me ajudar?",
      servicos=["Capital de giro", "Empréstimo FGI e FGO", "Empréstimo Pronamp",
                "Empréstimo BNDES"]),

 dict(slug="reestruturacao-financeira", icon="chart", grupo="Empresas",
      nav="Reestruturação Financeira de Produtor Rural e Empresas",
      h1="Reestruturação Financeira de Produtor Rural e Empresas",
      title="Reestruturação Financeira de Produtor Rural e Empresas | Vanira Araújo Advogados",
      desc=("Reorganização do endividamento de produtores rurais e empresas: diagnóstico das dívidas, "
            "renegociação com credores e plano de pagamento compatível com o caixa."),
      lead=("Reorganização do endividamento de produtores rurais e empresas a partir de um diagnóstico "
            "completo das dívidas e dos contratos existentes. O trabalho reúne renegociação com os "
            "credores e a construção de um plano de pagamento compatível com o caixa, para que a "
            "atividade continue operando durante a reestruturação."),
      wa="Olá! Gostaria de falar com a Dra. Vanira sobre reestruturação financeira. Pode me ajudar?",
      servicos=["Diagnóstico do endividamento", "Renegociação com credores",
                "Plano de pagamento compatível com o caixa",
                "Recuperação judicial e extrajudicial quando necessário"]),
]

GRUPOS = ["Dívida Rural", "Defesa de Bens", "Empresas"]

# Áreas ligadas ao produtor rural: recebem o bloco "Ao lado do produtor em cada
# etapa". Ficam de fora busca e apreensão de veículos e revisão de contratos PJ.
RURAIS = {"prorrogacao", "recuperacao-extrajudicial", "recuperacao-judicial",
          "defesa-produtor-rural", "busca-apreensao-maquinas", "reestruturacao-financeira"}
for _a in AREAS:
    _a["rural"] = _a["slug"] in RURAIS

# --------------------------------------------------------------------------
# DEPOIMENTOS REAIS (avaliacoes publicas no Google, com nome e data)
# --------------------------------------------------------------------------
DEPOIMENTOS = [
 ("Rander Prado", "14 de agosto de 2024",
  "Super bem atendido e resolveram meu problema com busca e apreensão do meu veículo. O atendimento e competência dos profissionais será bem recomendados por mim."),
 ("Marlúcia Landim", "9 de agosto de 2024",
  "Já conhecia a Dra. Vanira, e com isso me deu mais atenção no que estava acontecendo comigo. Recomendo o escritório dela pelo suporte incrível e a orientação clara."),
 ("Franciele Braga", "28 de julho de 2024",
  "Doutora Vanira Araújo é excelente! Meu caso foi resolvido rapidamente com suporte constante. Super recomendo a profissional e sua equipe!"),
 ("Maria Abadia", "30 de junho de 2024",
  "Foi maravilhoso conhecer o escritório da Dra. Vanira Araújo! Achei que não recuperaria meu carro, mas graças à equipe tudo deu certo. Obrigada!"),
 ("Conceição de Maria Oliveira", "20 de junho de 2024",
  "Dra. Vanira foi um anjo no momento que mais precisei. Recomendo o trabalho excelente dessa equipe maravilhosa. Obrigada por tudo!"),
]

# --------------------------------------------------------------------------
# FAQ (perguntas e respostas publicadas nas LPs oficiais)
# --------------------------------------------------------------------------
FAQ = [
 ("Posso recuperar meu veículo apreendido?",
  "Sim, é possível recorrer. É essencial agir rapidamente, pois o prazo para defesa já está correndo. Com uma boa estratégia jurídica, há grandes chances de reverter a situação e recuperar o veículo."),
 ("Se eu não fizer a defesa, posso ser cobrado de mais alguma coisa?",
  "Sim, se o valor obtido pela venda do veículo não quitar a dívida, o banco pode continuar como seu credor e até converter a ação de busca e apreensão em execução para atingir outros bens seus."),
 ("Meu nome continuará no SPC?",
  "Sim, até que a dívida seja totalmente quitada. O banco pode manter o seu nome nos órgãos de proteção ao crédito até a regularização completa do contrato."),
 ("A busca e apreensão é legal?",
  "Sim, o procedimento é permitido por lei. Contudo, ele deve cumprir todos os requisitos legais para ser válido. Caso contrário, é possível contestar judicialmente."),
 ("Posso evitar a perda do veículo?",
  "Sim, é possível evitar a perda total negociando com o banco ou apresentando uma defesa consistente."),
]

FIRM_LD = {
 "@type": ["LegalService", "Attorney"], "@id": BASE + "/#escritorio",
 "name": "Vanira Araújo Advogados",
 "description": "Escritório de advocacia especializado em Direito Bancário, Direito do Agronegócio e Recuperação Judicial e Extrajudicial.",
 "url": BASE + "/", "logo": BASE + "/logo-vanira.png", "image": BASE + "/og-image.jpg",
 "telephone": "+55-34-99796-5600", "email": "contato@advvaniraaraujo.com.br",
 "founder": {"@type": "Person", "name": "Vanira Araújo", "jobTitle": "Advogada",
             "identifier": "OAB/MG 200.037"},
 "taxID": "39.991.601/0001-49",
 "address": {"@type": "PostalAddress", "addressLocality": "Uberaba", "addressRegion": "MG",
             "addressCountry": "BR"},
 "areaServed": [{"@type": "AdministrativeArea", "name": "Triângulo Mineiro"},
                {"@type": "Country", "name": "Brasil"}],
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
   "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
   "opens": "07:00", "closes": "22:00"}],
 "sameAs": ["https://www.facebook.com/advogadavanira"], "knowsLanguage": "pt-BR",
}


# --------------------------------------------------------------------------
# BLOCOS COMPARTILHADOS
# --------------------------------------------------------------------------
def head(title, desc, path, ld_graph, preload=None):
    url = BASE + path
    pre = ('\n<link rel="preload" as="image" href="%s" fetchpriority="high">' % preload) if preload else ""
    return u"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#003018">
<link rel="canonical" href="{url}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Vanira Araújo Advogados">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vanira Araújo, Advocacia Bancária e Agro">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/og-image.jpg">
<script type="application/ld+json">
{ld}
</script>
<link rel="stylesheet" href="/styles.css">{pre}
<script src="/main.js" defer></script>""".format(
        title=title, desc=desc, url=url, base=BASE, pre=pre,
        ld=json.dumps({"@context": "https://schema.org", "@graph": ld_graph},
                      ensure_ascii=False, indent=1))


def header(current=None):
    """Menu com sanfona: 'Áreas de Atuação' expande no hover e no clique."""
    grupos_html = []
    for g in GRUPOS:
        itens = []
        for a in AREAS:
            if a["grupo"] != g:
                continue
            cur = ' aria-current="page"' if a["slug"] == current else ""
            itens.append('              <li><a href="/%s"%s>%s</a></li>' % (a["slug"], cur, a["nav"]))
        grupos_html.append(
            '            <div class="dd-group">\n'
            '              <p class="dd-group-title">%s</p>\n'
            '              <ul>\n%s\n              </ul>\n'
            '            </div>' % (g, "\n".join(itens)))
    desk = "\n".join(grupos_html)

    mob = []
    for g in GRUPOS:
        mob.append('          <li class="m-group-title">%s</li>' % g)
        for a in AREAS:
            if a["grupo"] != g:
                continue
            cur = ' aria-current="page"' if a["slug"] == current else ""
            mob.append('          <li><a href="/%s" data-close%s>%s</a></li>' % (a["slug"], cur, a["nav"]))
    mob = "\n".join(mob)

    hub_cur = ' aria-current="page"' if current == "areas" else ""

    return u"""<a class="skip-link" href="#main">Pular para o conteúdo principal</a>

<header class="site-header" id="topo">
  <div class="container header-inner">
    <a href="/" class="brand" aria-label="Vanira Araújo Advocacia, página inicial">
      <img src="/logo-vanira.png" alt="Vanira Araújo, Advocacia Bancária e Agro"
           width="880" height="373" decoding="async" fetchpriority="high">
    </a>

    <nav class="primary-nav" aria-label="Navegação principal">
      <ul class="nav-list">
        <li><a href="/#inicio">Início</a></li>
        <li><a href="/#quem-somos">Quem Somos</a></li>
        <li class="has-dropdown">
          <a class="nav-toggle" href="/areas-de-atuacao" aria-expanded="false"
             aria-controls="dropdown-areas"{hub}>
            Áreas de Atuação
            <svg class="caret" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
          <div class="dropdown" id="dropdown-areas">
            <div class="dropdown-inner">
{desk}
              <a class="dd-all" href="/areas-de-atuacao">Ver todas as áreas {arrow}</a>
            </div>
          </div>
        </li>
        <li><a href="/#depoimentos">Depoimentos</a></li>
        <li><a href="/#contato">Contato</a></li>
      </ul>
    </nav>

    <button type="button" class="nav-burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="mobile-nav">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </div>

  <nav class="mobile-nav" id="mobile-nav" aria-label="Navegação mobile">
    <ul>
      <li><a href="/#inicio" data-close>Início</a></li>
      <li><a href="/#quem-somos" data-close>Quem Somos</a></li>
      <li>
        <button type="button" class="m-sub-toggle" aria-expanded="false" aria-controls="m-sub-areas">
          Áreas de Atuação
          <svg class="caret" width="14" height="14" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <ul class="m-sub" id="m-sub-areas">
{mob}
          <li><a href="/areas-de-atuacao" data-close>Ver todas as áreas</a></li>
        </ul>
      </li>
      <li><a href="/#depoimentos" data-close>Depoimentos</a></li>
      <li><a href="/#contato" data-close>Contato</a></li>
    </ul>
    <a class="btn btn--whats" data-whats data-close aria-label="Fale com a Dra. Vanira pelo WhatsApp">
      {wa} Fale com a Dra. Vanira
    </a>
  </nav>
</header>""".format(desk=desk, mob=mob, wa=WA, arrow=ARROW_SM, hub=hub_cur)


def footer():
    links = "\n".join(
        '          <li><a href="/%s">%s</a></li>' % (a["slug"], a["nav"]) for a in AREAS[:5])
    return u"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="brand-name">Vanira Araújo</span>
        <div class="brand-sub">Advocacia Bancária e Agro</div>
        <p style="margin-top:var(--sp-3); max-width:34ch; color:rgba(255,255,255,0.75);">Direito Bancário, Direito do Agronegócio e Recuperação Judicial e Extrajudicial.</p>
        <p class="signature">Ao lado de quem produz.</p>
      </div>

      <nav class="footer-col" aria-label="Áreas de atuação">
        <h4>Áreas de Atuação</h4>
        <ul>
{links}
          <li><a href="/areas-de-atuacao">Ver todas</a></li>
        </ul>
      </nav>

      <div class="footer-col">
        <h4>Contato</h4>
        <address style="font-style:normal">
          <div class="contact-line">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 21s-7-6-7-11a7 7 0 0114 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>
            <span>Sede em Uberaba/MG. Atendimento 100% digital em todo o Brasil.</span>
          </div>
          <div class="contact-line">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15l-1.3 4.9L7.2 20A10 10 0 1012 2z"/></svg>
            <span>WhatsApp: <a data-whats aria-label="Falar com a Dra. Vanira no WhatsApp (34) 99796-5600">(34) 99796-5600</a></span>
          </div>
          <div class="contact-line">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
            <span>E-mail: <a href="mailto:contato@advvaniraaraujo.com.br">contato@advvaniraaraujo.com.br</a></span>
          </div>
          <div class="contact-line">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 8v4l3 2"/><circle cx="12" cy="12" r="9"/></svg>
            <span>Segunda a Sexta, das 7h às 22h</span>
          </div>
        </address>
      </div>
    </div>

    <div class="footer-legal">
      <p>Todos os direitos reservados, Vanira Araujo Advogados | OAB/MG: 200.037 | CNPJ: 39.991.601/0001-49 | <a href="/politica-de-privacidade">Política de Privacidade</a></p>
      <p class="legal-disclaimer">Este site não é um produto Meta Plataforms, Inc, Google LLC, nem Facebook ou do Facebook inc. Além disso, não oferecemos nenhum tipo de serviços oficial do governo, NÃO praticamos fraude, não somos uma empresa que vende criptoativos ou qualquer outro serviço. Somos um escritório de advocacia, que oferece serviços jurídicos, privativos de advogados, de acordo com a legislação vigente e o Código de Ética e Disciplina da OAB do Brasil. Nós NÃO compartilhamos seus dados com ninguém.</p>
    </div>
  </div>
</footer>

<a class="whats-widget" data-whats aria-label="Precisa de ajuda? Fale com a Dra. Vanira pelo WhatsApp">
  {wa} <span class="widget-label">Precisa de ajuda?</span>
</a>""".format(links=links, wa=WA_BIG)


def attorney_block():
    return u"""
  <section class="attorney" aria-labelledby="attorney-title">
    <div class="container attorney-grid">
      <img class="attorney-photo" src="/dra-vanira.jpg"
           alt="Dra. Vanira Araújo, advogada especializada em direito bancário e do agronegócio"
           width="862" height="1280" loading="lazy" decoding="async">
      <div>
        <h2 id="attorney-title">Quem vai cuidar do seu caso</h2>
        <div class="rule"></div>
        <p>Entendemos que por trás de cada dívida existe uma família, uma propriedade e uma história. Por isso, nosso trabalho começa muito antes do processo: começa ouvindo o produtor.</p>
        <ul class="cred-list">
          <li>{t} Dra. Vanira Araújo, OAB/MG 200.037</li>
          <li>{t} Mais de 10 anos de atuação</li>
          <li>{t} Sede em Uberaba/MG</li>
        </ul>
      </div>
    </div>
  </section>
""".format(t=TICK)


def page(title, desc, path, ld_graph, body, current=None, preload=None):
    return u"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{head}
</head>
<body>

{header}

<main id="main">
{body}
</main>

{footer}

</body>
</html>
""".format(head=head(title, desc, path, ld_graph, preload), header=header(current),
           body=body, footer=footer())


# --------------------------------------------------------------------------
# PAGINA DE AREA
# --------------------------------------------------------------------------
def sobre_block():
    """Reforço institucional focado no produtor rural (só nas áreas rurais)."""
    return u"""
  <section class="sobre" aria-labelledby="sobre-title">
    <div class="container">
      <div class="prose reveal">
        <h2 id="sobre-title">Ao lado do produtor em cada etapa</h2>
        <div class="rule"></div>
        <p style="margin-top:var(--sp-4)">A Vanira Advocacia é um escritório especializado em Direito Bancário Rural e Recuperação Judicial e Extrajudicial, com atuação em Uberaba e em todo o Triângulo Mineiro. Nossa equipe acompanha o produtor rural em cada etapa — da negociação com o banco até, se necessário, a defesa em juízo — com linguagem acessível e comunicação direta pelo WhatsApp.</p>
      </div>
    </div>
  </section>
"""


def build_area(a):
    servicos = "\n".join(
        '          <li class="svc-item"><span class="tick" aria-hidden="true">%s</span><span>%s</span></li>'
        % (TICK, s) for s in a["servicos"])
    outras = "\n".join(
        '          <a class="other-card" href="/%s">%s %s</a>' % (o["slug"], o["nav"], ARROW)
        for o in AREAS if o["slug"] != a["slug"])

    img = "/hero-%s.jpg" % a["slug"]
    body = u"""
  <section class="page-hero page-hero--media" aria-labelledby="page-title"
           style="--hero-img:url('{img}')">
    <div class="container">
      <nav class="breadcrumb" aria-label="Você está aqui">
        <ol>
          <li><a href="/">Início</a></li>
          <li><a href="/areas-de-atuacao">Áreas de Atuação</a></li>
          <li><span aria-current="page">{h1}</span></li>
        </ol>
      </nav>
      <h1 id="page-title">{h1}</h1>
      <div class="rule"></div>
      <p class="lead">{lead}</p>
      <a class="btn btn--whats" data-whats data-whats-msg="{wa}" aria-label="Falar com a Dra. Vanira pelo WhatsApp sobre {h1}">
        {wasvg} Falar com a Dra. Vanira
      </a>
    </div>
  </section>

  <section class="areas" aria-labelledby="svc-title">
    <div class="container">
      <div class="section-head reveal">
        <h2 id="svc-title">Como podemos ajudar</h2>
        <div class="rule"></div>
      </div>
      <ul class="svc-list">
{servicos}
      </ul>
    </div>
  </section>
{sobre}{attorney}
  <section class="cta-band" aria-labelledby="cta-title">
    <div class="container">
      <h2 id="cta-title">Fale com a Dra. Vanira</h2>
      <div class="rule" style="margin-inline:auto"></div>
      <p>Nos envie uma mensagem contando sua situação ou fale direto pelo WhatsApp. Nossa equipe responde o mais breve possível.</p>
      <a class="btn btn--whats" data-whats data-whats-msg="{wa}" aria-label="Quero falar com a advogada pelo WhatsApp">
        {wasvg} Quero falar com a advogada
      </a>
    </div>
  </section>

  <section class="other-areas" aria-labelledby="other-title">
    <div class="container">
      <div class="section-head reveal">
        <h2 id="other-title">Outras áreas de atuação</h2>
        <div class="rule"></div>
      </div>
      <div class="other-grid">
{outras}
      </div>
    </div>
  </section>
""".format(h1=a["h1"], lead=a["lead"], wa=a["wa"], wasvg=WA, img=img,
           servicos=servicos, outras=outras, attorney=attorney_block(),
           sobre=(sobre_block() if a.get("rural") else ""))

    ld = [
      {"@type": "Service", "name": a["nav"], "serviceType": a["nav"], "description": a["desc"],
       "url": BASE + "/" + a["slug"], "provider": {"@id": FIRM_LD["@id"]},
       "areaServed": FIRM_LD["areaServed"]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Áreas de Atuação",
         "item": BASE + "/areas-de-atuacao"},
        {"@type": "ListItem", "position": 3, "name": a["nav"], "item": BASE + "/" + a["slug"]}]},
    ]
    return page(a["title"], a["desc"], "/" + a["slug"], ld, body,
                current=a["slug"], preload=img)


# --------------------------------------------------------------------------
# HUB: TODAS AS AREAS
# --------------------------------------------------------------------------
def build_hub():
    blocos = []
    for g in GRUPOS:
        cards = []
        for a in AREAS:
            if a["grupo"] != g:
                continue
            extra = ""
            if a["slug"] == "revisao-contratos-pj":
                extra = ('\n            <ul class="card-sub">%s</ul>'
                         % "".join('<li>%s</li>' % s for s in a["servicos"]))
            cards.append(u"""        <article class="service-card reveal">
          <span class="card-icon" aria-hidden="true">{icon}</span>
          <h3>{nav}</h3>
          <p>{lead}</p>{extra}
          <a class="link-arrow" href="/{slug}" aria-label="Saiba mais sobre {nav}">Saiba mais
            {arrow}
          </a>
        </article>""".format(icon=IC[a["icon"]], nav=a["nav"], lead=a["lead"],
                             slug=a["slug"], arrow=ARROW_SM, extra=extra))
        blocos.append(u"""      <div class="area-group">
        <h2 class="group-title">{g}</h2>
        <div class="rule"></div>
      </div>
      <div class="cards-grid">
{cards}
      </div>""".format(g=g, cards="\n".join(cards)))

    body = u"""
  <section class="page-hero" aria-labelledby="page-title">
    <div class="container">
      <nav class="breadcrumb" aria-label="Você está aqui">
        <ol>
          <li><a href="/">Início</a></li>
          <li><span aria-current="page">Áreas de Atuação</span></li>
        </ol>
      </nav>
      <h1 id="page-title">Áreas de Atuação</h1>
      <div class="rule"></div>
      <p class="lead">O escritório atua em Direito Bancário e Direito do Agronegócio, da negociação com o banco até a defesa em juízo. Escolha abaixo a área que trata da sua situação.</p>
    </div>
  </section>

  <section class="areas" aria-label="Lista de áreas de atuação">
    <div class="container">
{blocos}
    </div>
  </section>
{attorney}
  <section class="cta-band" aria-labelledby="cta-title">
    <div class="container">
      <h2 id="cta-title">Não encontrou sua situação?</h2>
      <div class="rule" style="margin-inline:auto"></div>
      <p>Nos envie uma mensagem contando seu caso. Nossa equipe responde o mais breve possível.</p>
      <a class="btn btn--whats" data-whats aria-label="Quero falar com a advogada pelo WhatsApp">
        {wa} Quero falar com a advogada
      </a>
    </div>
  </section>
""".format(blocos="\n\n".join(blocos), attorney=attorney_block(), wa=WA)

    ld = [
      {"@type": "CollectionPage", "name": "Áreas de Atuação",
       "url": BASE + "/areas-de-atuacao", "about": {"@id": FIRM_LD["@id"]},
       "hasPart": [{"@type": "Service", "name": a["nav"], "url": BASE + "/" + a["slug"]}
                   for a in AREAS]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Áreas de Atuação",
         "item": BASE + "/areas-de-atuacao"}]},
    ]
    return page("Áreas de Atuação | Vanira Araújo Advogados",
                "Direito Bancário e do Agronegócio: dívida rural, recuperação judicial e "
                "extrajudicial, busca e apreensão de veículos e máquinas, revisão de contratos "
                "de pessoa jurídica e reestruturação financeira.",
                "/areas-de-atuacao", ld, body, current="areas")


# --------------------------------------------------------------------------
# POLITICA DE PRIVACIDADE
# --------------------------------------------------------------------------
def build_privacy():
    body = u"""
  <section class="page-hero" aria-labelledby="page-title">
    <div class="container">
      <nav class="breadcrumb" aria-label="Você está aqui">
        <ol>
          <li><a href="/">Início</a></li>
          <li><span aria-current="page">Política de Privacidade</span></li>
        </ol>
      </nav>
      <h1 id="page-title">Política de Privacidade</h1>
      <div class="rule"></div>
      <p class="lead">Esta política explica quais dados o site coleta, para que eles são usados e quais são os seus direitos, conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p>
    </div>
  </section>

  <section class="legal-page">
    <div class="container">
      <h2>Quem é o controlador dos dados</h2>
      <p>Vanira Araujo Advogados, CNPJ 39.991.601/0001-49, com sede em Uberaba/MG, inscrita na OAB/MG sob o número 200.037. Contato para assuntos de privacidade: <a href="mailto:contato@advvaniraaraujo.com.br">contato@advvaniraaraujo.com.br</a>.</p>

      <h2>Quais dados são coletados</h2>
      <p>Este site não possui cadastro, área restrita nem formulário que armazene dados em banco de dados próprio. Os dados que você informa são enviados diretamente por você ao escritório, no momento em que decide iniciar uma conversa pelo WhatsApp ou por e-mail, e se limitam ao que você escrever na mensagem, normalmente nome, telefone e a descrição da sua situação.</p>

      <h2>Para que os dados são usados</h2>
      <p>Exclusivamente para responder ao seu contato, avaliar a viabilidade jurídica do caso e prestar o serviço advocatício quando houver contratação. Os dados não são usados para qualquer outra finalidade.</p>

      <h2>Compartilhamento</h2>
      <p>Nós NÃO compartilhamos seus dados com ninguém. Não vendemos, cedemos nem transferimos seus dados para terceiros com finalidade comercial. Eventual apresentação de informações a órgãos do Poder Judiciário ocorre apenas quando necessária à defesa dos seus próprios interesses no processo, ou quando exigida por lei.</p>

      <h2>Sigilo profissional</h2>
      <p>As informações compartilhadas com o escritório são protegidas pelo sigilo profissional do advogado, previsto no Estatuto da Advocacia e no Código de Ética e Disciplina da OAB, que é mais restritivo do que a própria exigência legal de proteção de dados.</p>

      <h2>Por quanto tempo os dados são guardados</h2>
      <p>Mensagens de contato que não resultam em contratação são mantidas apenas pelo tempo necessário ao atendimento. Havendo contratação, os documentos do caso são guardados pelos prazos exigidos pela legislação e pelas normas da advocacia.</p>

      <h2>Seus direitos</h2>
      <p>A qualquer momento você pode solicitar confirmação de tratamento, acesso, correção, anonimização, portabilidade ou exclusão dos seus dados, além de revogar consentimento. Basta escrever para <a href="mailto:contato@advvaniraaraujo.com.br">contato@advvaniraaraujo.com.br</a>.</p>

      <h2>Cookies e medição de audiência</h2>
      <p>O site é estático e não instala cookies de rastreamento ou de publicidade. O vídeo e as imagens são servidos pelo próprio site, sem incorporação de players de terceiros.</p>

      <h2>Alterações</h2>
      <p>Esta política pode ser atualizada para refletir mudanças no site ou na legislação. A versão vigente é sempre a publicada nesta página.</p>

      <a class="btn btn--primary" href="/">Voltar para o início</a>
    </div>
  </section>
"""
    ld = [{"@type": "WebPage", "name": "Política de Privacidade",
           "url": BASE + "/politica-de-privacidade", "publisher": {"@id": FIRM_LD["@id"]}}]
    return page("Política de Privacidade | Vanira Araújo Advogados",
                "Como a Vanira Araujo Advogados trata os dados pessoais recebidos pelo site, "
                "conforme a LGPD (Lei 13.709/2018).",
                "/politica-de-privacidade", ld, body)


# --------------------------------------------------------------------------
# ESCRITA
# --------------------------------------------------------------------------
def w(name, content):
    io.open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
    print("  gerado:", name)


if __name__ == "__main__":
    print("Gerando paginas...")
    for a in AREAS:
        w(a["slug"] + ".html", build_area(a))
    w("areas-de-atuacao.html", build_hub())
    w("politica-de-privacidade.html", build_privacy())

    hoje = datetime.date.today().isoformat()
    urls = ["/", "/areas-de-atuacao"] + ["/" + a["slug"] for a in AREAS] + ["/politica-de-privacidade"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u == "/" else ("0.9" if u == "/areas-de-atuacao" else
                                     ("0.3" if "privacidade" in u else "0.8"))
        sm.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
                  "    <priority>%s</priority>\n  </url>" % (BASE, u, hoje, pr))
    sm.append("</urlset>")
    w("sitemap.xml", "\n".join(sm) + "\n")
    print("Pronto. %d areas + hub + privacidade." % len(AREAS))

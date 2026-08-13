# Contexto do Projeto — Site Vanira Araújo Advogados

> Resumo de toda a conversa/trabalho até aqui. Cole isto no início de uma nova conversa para retomar sem perder contexto.
>
> Última atualização: **12/08/2026**.
>
> **Este arquivo é interno.** Ele está versionado no git, mas fica no `.vercelignore` para não ser servido publicamente. Se sair de lá, vira uma página pública do site.

## O que é

Site institucional estático (HTML/CSS/JS puro, **zero dependências, zero build step**) para a **Vanira Araújo Advogados**, escritório especializado em Direito Bancário Rural e do Agronegócio, com sede em **Uberaba/MG**.

- **Repositório**: https://github.com/ambrosiocfs18/vanira-advocacia
- **Produção**: https://vanira-advocacia.vercel.app (deploy automático a cada `git push` na `main`)
- **Domínio próprio**: ainda não conectado (ela tem `advvaniraaraujo.com.br` mas não está nesta conta Vercel)

## Dados institucionais reais (não inventar nada além disso)

- Advogada: **Dra. Vanira Araújo**, OAB/MG **200.037**
- CNPJ: **39.991.601/0001-49**
- Sede: **Uberaba/MG**, atuação em todo o Triângulo Mineiro e (para as áreas bancárias) todo o Brasil, 100% digital
- WhatsApp: **(34) 99796-5600** → `WHATSAPP_NUMBER = '5534997965600'` em `main.js`
- E-mail: `contato@advvaniraaraujo.com.br`
- Horário: Segunda a Sexta, 7h às 22h
- Facebook: facebook.com/advogadavanira
- Mais de 10 anos de atuação (dado real, confirmado nas LPs oficiais dela)

**Regra que valeu a conversa toda**: nunca inventar estatística, prêmio, número de casos/clientes ou nota de avaliação. Só usar o que está verificável nas fontes oficiais dela (`advvaniraaraujo.com.br`).

## Arquitetura técnica

- **Sem framework, sem npm, sem build.** Um `index.html` + `styles.css` + `main.js` compartilhados por todas as páginas.
- **`build.py`** (Python, não vai para o deploy — está no `.gitignore`/`.vercelignore`) é o **gerador único** de todas as páginas de área, do hub, da política de privacidade e do `sitemap.xml`. Ele também **sincroniza automaticamente o header/rodapé da home** (`sync_home()`), porque a home tem conteúdo próprio (vídeo, depoimentos, FAQ) que não pode ser sobrescrito.
  - **Sempre que adicionar/mudar uma área, editar `build.py` e rodar `python build.py`** — nunca editar as páginas de área geradas diretamente.
- Vídeo de fundo da hero: otimizado (12MB→2,4MB), carrega via JS só após `load`, com `preload="none"`, dispensado em conexão lenta/economia de dados. Poster real extraído do próprio vídeo.
- **Vídeos do YouTube usam fachada (click-to-load), nunca `<iframe>` direto.** A página entrega só a capa (hospedada aqui) e um botão; o iframe nasce no clique, apontando para `youtube-nocookie`. Assim o site continua com **zero requisição a terceiros no carregamento** e sem cookie do Google, que é o que a política de privacidade promete. Tabela `VIDEOS` + `video_block()` + `video_ld()` no `build.py`, listener `[data-yt]` no `main.js`. Para adicionar vídeo em outra área, basta uma entrada nova em `VIDEOS`.
- **Medição de audiência**: Web Analytics da própria Vercel (`/_vercel/insights/script.js`), sem cookie e servida do próprio domínio, então não quebra a regra de zero terceiros. **Só coleta depois de habilitar Web Analytics no painel da Vercel** — isso é configuração de conta, não de código.
- Imagens: todas baixadas do Unsplash (licença comercial livre), hospedadas no próprio site (nunca hotlink), sempre **conferidas visualmente antes de usar**. Exceção: a capa do vídeo, que vem do próprio YouTube dela e também fica hospedada aqui.
- Fotos dos depoimentos: avatares **reais** dos clientes (extraídos do perfil Google deles nas LPs oficiais, autorizados pelo usuário), exceto Maria Abadia que usa monograma porque a origem também só tinha avatar de letra.

## Estrutura de páginas (14 no total)

- `index.html` — home (hero em vídeo, Quem Somos, seção de processo "O que fazemos na prática", Equipe, Depoimentos em parede rolante, FAQ, **faixa de números**, **"Entenda seus direitos"**, Contato)
  - **Faixa de números** (`.numeros`, entre FAQ e "Entenda seus direitos"): +1.200 clientes, +850 casos, +10.000 horas, +10 anos. Números vindos do **site antigo dela** (fonte oficial dela, confirmada pelo usuário). Sobem de zero com ease-out quando a faixa entra na tela; o HTML já traz o valor final escrito, então sem JS ou com movimento reduzido o número certo aparece igual.
  - A seção que hoje se chama **"Entenda seus direitos"** era "Artigos e Notícias" com botões "Ler artigo" apontando para `#contato` e um "Ver todas as postagens" apontando para si mesmo — prometia leitura que não existia. Agora leva para as páginas de área, que têm o conteúdo real. **Se ela um dia escrever artigos de verdade, aí sim vira blog.**
- `nosso-escritorio.html` — página institucional (destaques, apresentação, missão/valores). Hero própria (`hero-nosso-escritorio.jpg`, sala de reunião corporativa); antes reaproveitava a foto do produtor rural, que não combinava com o tema.
- `areas-de-atuacao.html` — hub com as 9 áreas, cards com foto, agrupadas em 3 categorias com atalhos (chips)
- 9 páginas de área, cada uma com hero de imagem própria, breadcrumb, serviços, CTA:
  - **Dívida Rural** (4): `prorrogacao`, `recuperacao-extrajudicial`, `recuperacao-judicial`, `defesa-produtor-rural`
  - **Defesa de Bens** (3): `busca-apreensao-veiculos`, `busca-apreensao-maquinas`, `suspensao-leilao-imoveis`
  - **Empresas** (2): `revisao-contratos-pj` (capital de giro, FGI/FGO, Pronamp, BNDES), `reestruturacao-financeira`
- `politica-de-privacidade.html` — LGPD real (sem banco de dados próprio, sem cookie de rastreio). **Descreve o comportamento real do embed de vídeo e da medição de audiência** — antes afirmava "sem incorporação de players de terceiros", o que deixou de ser verdade quando o vídeo entrou. Sempre que mexer em terceiros, conferir se esta página continua verdadeira.
- `404.html`

O bloco "Ao lado do produtor em cada etapa" aparece só nas 6 áreas realmente rurais (não em veículos nem revisão PJ).

**Vídeo**: só `busca-apreensao-veiculos` tem, porque o canal dela no YouTube tem **exatamente um vídeo** (`d97DNOZs6IE`, 52s, "Seu veículo foi apreendido por atraso no financiamento e não sabe o que fazer?"). Não adianta procurar material para as outras 8 áreas — conferido em 12/08/2026.

## Design system

- Cores: verde profundo `#003018`, dourado `#C6912A`/`#E8B237` (mais vívido que o tom pastel original), branco/creme `#F7EEDC`
- Tipografia: Cormorant Garamond (display) + Poppins (corpo), com fallback de sistema (sem link externo do Google Fonts, por causa da regra de zero dependências)
- Logo: monograma "VA" dourado, gerado a partir da arte oficial dela
- Favicon, OG image, JSON-LD (`LegalService`/`Attorney`/`Service`/`FAQPage`/`BreadcrumbList`) em todas as páginas
- Seções alternam verde profundo / branco / creme para dar ritmo e contraste
- Bordas arredondadas (28px mobile / 40px desktop) nas seções "O que fazemos" e "Depoimentos"; "Contato" só com o topo arredondado
- Heros das páginas de área usam foto temática real (trator, tribunal, casa, contrato...) com véu verde translúcido calibrado por contraste real (WCAG AA), não um valor arbitrário

## Aprendizados e preferências importantes

1. **Sempre medir contraste de verdade** antes de clarear/escurecer um véu — calcular contra o pixel mais claro da imagem real, não estimar. Isso já foi feito várias vezes (hero da home, heros das áreas).
   - Vale também para **componente de UI sobre foto**, não só texto: o botão de play dourado do vídeo ficava em 1,3:1 contra as partes claras da capa, e **nenhum aumento de véu resolvia** (escurecer a foto move o fundo junto). A solução foi um **anel opaco** verde em volta do botão — 5,9:1 dourado/anel e 12,3:1 anel/foto, funciona sobre qualquer capa futura. Quando o contraste não obedece ao véu, a resposta costuma ser separar com uma borda opaca, não escurecer mais.
2. **`build.py` é a fonte da verdade.** Editar HTML gerado diretamente causa dessincronia (já aconteceu: o menu da home ficou desatualizado até eu criar `sync_home()`). **A home é a exceção**: `index.html` tem conteúdo próprio e se edita direto (o `build.py` só sincroniza header/rodapé dela).
3. **Verificação sempre com ferramentas reais**, nunca assumir. O `computer{action:"screenshot"}` frequentemente falha neste ambiente (painel headless sem composição) — quando isso acontece, validar via `javascript_exec` (medir DOM, contraste) em vez de desistir da verificação.
   - **O painel não roda `requestAnimationFrame` nem `IntersectionObserver`**, porque não compõe frames. Sintoma: o `.reveal` que já existia no site aparece com 0 de 21 elementos visíveis, e imagens `loading="lazy"` nunca carregam. **Isso é artefato do ambiente, não bug do código** — antes de "consertar", checar se o `reveal` também está inerte. Para testar animação de verdade, executar o `main.js` real com `requestAnimationFrame` trocado por `setTimeout` e um `IntersectionObserver` falso que dispara na hora.
   - **Cuidado com teste contaminado**: rodar o `main.js` duas vezes na mesma página deixa estado da primeira execução. Restaurar o estado do HTML servido antes de testar de novo, senão o resultado mente.
4. **Cuidado com cache do preview local** — depois de editar `main.js`/`styles.css`, às vezes é preciso reiniciar o servidor de preview (`preview_stop` + `preview_start`) para o navegador parar de servir a versão antiga.
5. **O componente React que o usuário colou uma vez** (parede de depoimentos com framer-motion/shadcn) foi **recriado em CSS/JS puro**, preservando o efeito visual mas sem quebrar a arquitetura zero-dependência do site. Sempre que o usuário colar algo assim, adaptar ao stack existente, não importar o stack novo.
6. **Pasta `claude-cookbooks-main`** (`C:\Users\ambro\Downloads\claude-cookbooks-main`) **não é referência de design** — é o repositório de exemplos de código da API da Claude (RAG, agentes, tool use). Não tem CSS/design system aproveitável. Se o usuário pedir para usá-la como referência de novo, avisar isso e pedir uma referência visual real.
7. **Sempre confirmar deploy em produção** depois de publicar (poll até o conteúdo novo aparecer), nunca assumir que o Vercel já atualizou.
8. **Imagens de terceiros**: sempre do Unsplash (licença comercial livre, sem atribuição obrigatória), baixadas e hospedadas no próprio repo, nunca hotlink.
9. O usuário aprova bem intervenções autônomas de correção de bugs que eu mesmo encontro no meio do trabalho (ex.: corrigir `AREA_SLUGS` desatualizado, remover CSS órfão/conflitante) — mas sempre reportar o que foi corrigido e por quê.
10. Preferência por respostas objetivas com prova (medições reais, curl para produção) em vez de alegações sem verificação.
11. **Arquivo novo na raiz vai para o deploy.** O `CONTEXTO-PROJETO.md` ficou público (200, 8,3 KB) só por ter sido versionado sem entrar no `.vercelignore`. Ao criar qualquer arquivo interno na raiz, decidir na hora se ele é público, e conferir com `curl` depois de publicar.
12. **Números tipográficos**: a fonte display cai em Georgia para quase todo mundo (não há webfont), e Georgia usa **algarismos antigos** — medido, 11px de diferença de altura entre o "1" e o "8", o que numa faixa de números fica torto. Onde houver número grande em fonte display, usar `font-variant-numeric: lining-nums tabular-nums`. O `tabular-nums` sozinho não resolve: a fonte já era tabular na largura, o problema era a altura.
13. **Perguntar antes de publicar estatística.** Quando o usuário mandou o print com 1200/850/10.000, o certo foi perguntar de onde vinham antes de codar — eram do site antigo dela, então valiam. A regra de nunca inventar número continua valendo, e a checagem custa uma pergunta.
14. **Ao usar as skills de design** (`taste-skill` / `ui-ux-pro-max-v2`): o `--design-system` sugere paleta e fonte do zero (sugeriu navy + EB Garamond), mas aqui o modo é **redesign-preservar** — a identidade verde/dourado + Cormorant já existe e manda. Aproveitar das skills o checklist de acessibilidade e as regras de layout, não a proposta de paleta.

## Pendências conhecidas (não resolvidas)

Dependem dela ou de decisão do usuário:

- **Domínio próprio** (`advvaniraaraujo.com.br` ou outro) ainda não conectado à Vercel — hoje só existe em `vanira-advocacia.vercel.app`. Quando conectar, revisar `BASE` em `build.py` (afeta canonical, OG image, sitemap, JSON-LD). Os rewrites de subdomínio no `vercel.json` **já cobrem as 9 áreas** e passam a valer quando os subdomínios existirem.
- **Habilitar Web Analytics no painel da Vercel.** O script já está nas 13 páginas e a política já descreve a coleta, mas nada é coletado até esse botão ser ligado. É configuração de conta.
- Textos de "Missão / Como trabalhamos / No que acreditamos" na página Nosso Escritório foram escritos a partir da copy dela, mas **valem revisão/aprovação dela** (é posicionamento de marca).
- Nenhuma estrela/nota agregada nos depoimentos (são 30 depoimentos reais no ar, mas falta o dado do Google dela — se ela passar, dá pra adicionar `AggregateRating` no JSON-LD).
- **Artigos de verdade para o blog.** Enquanto não existirem, a seção continua sendo "Entenda seus direitos" apontando para as áreas. Não escrever artigo jurídico no nome dela sem revisão dela.
- Se ela tiver fotos reais de casos/escritório, podem substituir as do Unsplash.

Resolvido em 12/08/2026, não reabrir sem motivo:

- Hero própria em Nosso Escritório; vídeo dela na página de veículos; faixa de números na home; `CONTEXTO-PROJETO.md` fora do deploy; links falsos do blog; fallback do formulário quando o pop-up é bloqueado; `vercel.json` cobrindo as 9 áreas; medição de audiência instalada.

## Como continuar

1. Ler este arquivo para reconstituir o contexto.
2. Para qualquer mudança de conteúdo/estrutura de página de área: editar `build.py`, rodar `python build.py`, verificar com o Browser tool, `git commit` + `git push`, confirmar em produção com `curl`.
3. Para mudanças só na home: editar `index.html`/`styles.css`/`main.js` diretamente (a home não é gerada pelo `build.py`, só sincronizada nos trechos de header/rodapé).
4. Ao mexer em qualquer coisa que envolva terceiros (embed, script, fonte externa), reler a `politica-de-privacidade` e conferir se ela continua verdadeira. Já aconteceu de ficar desatualizada.
5. Ao criar arquivo novo na raiz, decidir se é público. Se não for, entra no `.vercelignore`, e confere com `curl` depois de publicar.

**Nota sobre o servidor local**: `python -m http.server` não faz `cleanUrls`, então `/prorrogacao` dá 404 no preview mas funciona em produção. Testar links extensionless com `.html` local ou direto contra o site publicado — não é bug.

## Git

Identidade configurada **localmente neste repo** (não no global): `ambrosiocfs18 <ambrosiocfs18@gmail.com>`, batendo com o histórico. Se o `git commit` reclamar de "Author identity unknown" em outra máquina, é isso.

# Contexto do Projeto — Site Vanira Araújo Advogados

> Resumo de toda a conversa/trabalho até aqui. Cole isto no início de uma nova conversa para retomar sem perder contexto.

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
- Imagens: todas baixadas do Unsplash (licença comercial livre), hospedadas no próprio site (nunca hotlink), sempre **conferidas visualmente antes de usar**.
- Fotos dos depoimentos: avatares **reais** dos clientes (extraídos do perfil Google deles nas LPs oficiais, autorizados pelo usuário), exceto Maria Abadia que usa monograma porque a origem também só tinha avatar de letra.

## Estrutura de páginas (14 no total)

- `index.html` — home (hero em vídeo, Quem Somos, seção de processo "O que fazemos na prática", Equipe, Depoimentos em parede rolante, FAQ, Blog, Contato)
- `nosso-escritorio.html` — página institucional (destaques, apresentação, missão/valores)
- `areas-de-atuacao.html` — hub com as 9 áreas, cards com foto, agrupadas em 3 categorias com atalhos (chips)
- 9 páginas de área, cada uma com hero de imagem própria, breadcrumb, serviços, CTA:
  - **Dívida Rural** (4): `prorrogacao`, `recuperacao-extrajudicial`, `recuperacao-judicial`, `defesa-produtor-rural`
  - **Defesa de Bens** (3): `busca-apreensao-veiculos`, `busca-apreensao-maquinas`, `suspensao-leilao-imoveis`
  - **Empresas** (2): `revisao-contratos-pj` (capital de giro, FGI/FGO, Pronamp, BNDES), `reestruturacao-financeira`
- `politica-de-privacidade.html` — LGPD real (sem cookies de rastreio, sem banco de dados próprio)
- `404.html`

O bloco "Ao lado do produtor em cada etapa" aparece só nas 6 áreas realmente rurais (não em veículos nem revisão PJ).

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
2. **`build.py` é a fonte da verdade.** Editar HTML gerado diretamente causa dessincronia (já aconteceu: o menu da home ficou desatualizado até eu criar `sync_home()`).
3. **Verificação sempre com ferramentas reais**, nunca assumir. O `computer{action:"screenshot"}` frequentemente falha neste ambiente (painel headless sem composição) — quando isso acontece, validar via `javascript_exec` (medir DOM, contraste, animações via Web Animations API) em vez de desistir da verificação.
4. **Cuidado com cache do preview local** — depois de editar `main.js`/`styles.css`, às vezes é preciso reiniciar o servidor de preview (`preview_stop` + `preview_start`) para o navegador parar de servir a versão antiga.
5. **O componente React que o usuário colou uma vez** (parede de depoimentos com framer-motion/shadcn) foi **recriado em CSS/JS puro**, preservando o efeito visual mas sem quebrar a arquitetura zero-dependência do site. Sempre que o usuário colar algo assim, adaptar ao stack existente, não importar o stack novo.
6. **Pasta `claude-cookbooks-main`** (`C:\Users\ambro\Downloads\claude-cookbooks-main`) **não é referência de design** — é o repositório de exemplos de código da API da Claude (RAG, agentes, tool use). Não tem CSS/design system aproveitável. Se o usuário pedir para usá-la como referência de novo, avisar isso e pedir uma referência visual real.
7. **Sempre confirmar deploy em produção** depois de publicar (poll até o conteúdo novo aparecer), nunca assumir que o Vercel já atualizou.
8. **Imagens de terceiros**: sempre do Unsplash (licença comercial livre, sem atribuição obrigatória), baixadas e hospedadas no próprio repo, nunca hotlink.
9. O usuário aprova bem intervenções autônomas de correção de bugs que eu mesmo encontro no meio do trabalho (ex.: corrigir `AREA_SLUGS` desatualizado, remover CSS órfão/conflitante) — mas sempre reportar o que foi corrigido e por quê.
10. Preferência por respostas objetivas com prova (medições reais, curl para produção) em vez de alegações sem verificação.

## Pendências conhecidas (não resolvidas)

- **Domínio próprio** (`advvaniraaraujo.com.br` ou outro) ainda não conectado à Vercel — hoje só existe em `vercel-advocacia.vercel.app`. Quando conectar, revisar `BASE` em `build.py` (afeta canonical, OG image, sitemap, JSON-LD) e as URLs de subdomínio por área que já estão preparadas em `vercel.json`.
- Textos de "Missão / Como trabalhamos / No que acreditamos" na página Nosso Escritório foram escritos a partir da copy dela, mas **valem revisão/aprovação dela** (é posicionamento de marca).
- Nenhuma estrela/nota agregada nos depoimentos (não temos o dado real do Google dela — se ela passar, dá pra adicionar `AggregateRating` no JSON-LD).
- Se ela tiver fotos reais de casos/escritório, podem substituir as do Unsplash.

## Como continuar

1. Ler este arquivo para reconstituir o contexto.
2. Para qualquer mudança de conteúdo/estrutura de página de área: editar `build.py`, rodar `python build.py`, verificar com o Browser tool, `git commit` + `git push`, confirmar em produção com `curl`.
3. Para mudanças só na home: editar `index.html`/`styles.css`/`main.js` diretamente (a home não é gerada pelo `build.py`, só sincronizada nos trechos de header/rodapé).

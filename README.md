# Vanira Araújo — Advocacia Bancária e Agro

Landing page de página única (HTML/CSS/JS, sem dependências externas) para a **Vanira Advocacia**, escritório especializado em Direito Bancário Rural e Recuperação Judicial e Extrajudicial de produtores rurais em Uberaba/MG e todo o Triângulo Mineiro.

## Estrutura

- `index.html` — site completo (marcação, estilos e scripts inline)
- `hero-video.webm` / `hero-video.mp4` — vídeo de fundo da hero (mudo, em loop, otimizado para web)
- `dra-vanira.jpg` — retrato da Dra. Vanira (poster do vídeo e seção "Quem Somos")
- `logo-vanira.png` — logotipo

## Características

- Responsivo mobile-first (breakpoints 768 / 1024px)
- Acessibilidade: HTML semântico, contraste WCAG AA, navegação por teclado, `aria-label`, `prefers-reduced-motion`
- Zero dependências externas — todo CSS/JS embutido
- Vídeo de fundo mudo com fallback de poster

## Pendências antes de divulgar

- Substituir `WHATSAPP_NUMBER` no `<script>` ao final do `index.html`
- Preencher os campos de contato do rodapé (endereço, e-mail, redes) e o `[X] anos` da hero

## Deploy

Hospedado na Vercel como site estático (sem etapa de build).

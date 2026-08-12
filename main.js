(function () {
  'use strict';

  /* Preferência de movimento reduzido: consultada uma vez e usada em todo o arquivo */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Contato — WhatsApp em formato internacional, só dígitos (55 + DDD + número) */
  var WHATSAPP_NUMBER = '5534997965600';
  var WHATSAPP_MSG = 'Olá! Gostaria de falar com a Dra. Vanira sobre minha dívida rural. Pode me ajudar?';

  function whatsUrl(msg) {
    return 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(msg || WHATSAPP_MSG);
  }

  /* Aplica o link do WhatsApp a todos os elementos [data-whats].
     data-whats-msg permite mensagem própria por página de área. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-whats]'), function (el) {
    el.setAttribute('href', whatsUrl(el.getAttribute('data-whats-msg')));
    el.setAttribute('target', '_blank');
    el.setAttribute('rel', 'noopener noreferrer');
  });

  /* Ano do rodapé */
  var anoEl = document.getElementById('ano');
  if (anoEl) anoEl.textContent = new Date().getFullYear();

  /* ---------- Navegação a partir de um subdomínio de área ----------
     Quando a página é servida em prorrogacao.dominio.com.br, os links
     começados com "/" apontariam de volta para o próprio subdomínio.
     Aqui eles são reescritos para o domínio principal. Inerte fora
     de um subdomínio de área. */
  var AREA_SLUGS = ['prorrogacao', 'recuperacao-extrajudicial', 'recuperacao-judicial',
                    'defesa-produtor-rural', 'busca-apreensao-veiculos', 'busca-apreensao-maquinas',
                    'suspensao-leilao-imoveis', 'revisao-contratos-pj', 'reestruturacao-financeira'];
  (function () {
    var host = window.location.hostname;
    var apex = null;
    for (var i = 0; i < AREA_SLUGS.length; i++) {
      if (host.indexOf(AREA_SLUGS[i] + '.') === 0) {
        apex = host.slice(AREA_SLUGS[i].length + 1);
        break;
      }
    }
    if (!apex) return;
    Array.prototype.forEach.call(document.querySelectorAll('a[href^="/"]'), function (a) {
      if (a.getAttribute('href').indexOf('//') === 0) return;   /* protocol-relative */
      a.setAttribute('href', window.location.protocol + '//' + apex + a.getAttribute('href'));
    });
  })();

  /* ---------- Barra de progresso de leitura ----------
     Mostra o quanto da página já foi percorrido. A escrita é feita dentro
     de requestAnimationFrame e só toca em transform, para não custar
     layout durante a rolagem. Desativada em movimento reduzido. */
  if (!reduce) {
    var bar = document.createElement('div');
    bar.className = 'read-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);

    var ticking = false;
    var pintar = function () {
      var alcance = document.documentElement.scrollHeight - window.innerHeight;
      var p = alcance > 0 ? Math.min(window.scrollY / alcance, 1) : 0;
      bar.style.transform = 'scaleX(' + p + ')';
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(pintar); }
    }, { passive: true });
    pintar();
  }

  /* ---------- Header: sombra ao rolar ---------- */
  var header = document.querySelector('.site-header');
  var onScroll = function () {
    if (window.scrollY > 12) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var burger = document.getElementById('burger');
  var mobileNav = document.getElementById('mobile-nav');

  function setMenu(open) {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    mobileNav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
  }
  burger.addEventListener('click', function () {
    setMenu(burger.getAttribute('aria-expanded') !== 'true');
  });
  /* Fecha ao clicar em qualquer link marcado com data-close */
  Array.prototype.forEach.call(mobileNav.querySelectorAll('[data-close]'), function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });
  /* Submenu mobile (acordeão) */
  var mSubToggle = mobileNav.querySelector('.m-sub-toggle');
  if (mSubToggle) {
    var mSub = document.getElementById(mSubToggle.getAttribute('aria-controls'));
    mSubToggle.addEventListener('click', function () {
      var open = mSubToggle.getAttribute('aria-expanded') !== 'true';
      mSubToggle.setAttribute('aria-expanded', String(open));
      mSub.classList.toggle('open', open);
    });
  }
  /* Fecha o menu com ESC */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobileNav.classList.contains('open')) {
      setMenu(false);
      burger.focus();
    }
  });

  /* ---------- Sanfona de Áreas de Atuação (desktop) ----------
     No mouse a sanfona abre no hover, direto pelo CSS. O JS cobre os
     casos que o CSS não alcança: teclado e telas de toque. O gatilho é
     um link para /areas-de-atuacao, então quem clica sem esperar a
     sanfona ainda chega na página com todas as áreas. */
  var ddToggle = document.querySelector('.has-dropdown .nav-toggle');
  if (ddToggle) {
    var ddParent = ddToggle.closest('.has-dropdown');
    var ddMenu = document.getElementById(ddToggle.getAttribute('aria-controls'));
    var semHover = !window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    var setDropdown = function (open) {
      ddToggle.setAttribute('aria-expanded', String(open));
      ddParent.classList.toggle('open', open);
      ddMenu.classList.toggle('open', open);
    };

    /* Em tela de toque o primeiro toque abre a sanfona; o segundo navega. */
    ddToggle.addEventListener('click', function (e) {
      if (!semHover) return;
      if (ddToggle.getAttribute('aria-expanded') !== 'true') {
        e.preventDefault();
        setDropdown(true);
      }
    });

    /* O hover do CSS já cuida do visual; aqui só mantemos o ARIA coerente. */
    ddParent.addEventListener('mouseenter', function () {
      if (!semHover) setDropdown(true);
    });
    ddParent.addEventListener('mouseleave', function () {
      if (!semHover) setDropdown(false);
    });
    ddParent.addEventListener('focusin', function () { setDropdown(true); });
    ddParent.addEventListener('focusout', function () {
      if (!ddParent.contains(document.activeElement)) setDropdown(false);
    });

    Array.prototype.forEach.call(ddMenu.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () { setDropdown(false); });
    });
    document.addEventListener('click', function (e) {
      if (!ddParent.contains(e.target)) setDropdown(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setDropdown(false); ddToggle.blur(); }
    });
  }

  /* ---------- Formulário → WhatsApp ---------- */
  var form = document.getElementById('contato-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var nome = form.nome.value.trim();
      var whats = form.whatsapp.value.trim();
      var msg = form.mensagem.value.trim();
      var texto = 'Olá! Meu nome é ' + nome + '.'
        + (whats ? ' Meu WhatsApp: ' + whats + '.' : '')
        + (msg ? ' ' + msg : ' Gostaria de falar com a Dra. Vanira sobre minha dívida rural.');
      window.open(whatsUrl(texto), '_blank', 'noopener');
    });
  }

  /* ---------- Scroll reveal (IntersectionObserver) ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealEls, function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    Array.prototype.forEach.call(revealEls, function (el) { io.observe(el); });
  }

  /* ---------- Vídeo da hero ----------
     O poster já desenha a hero. O vídeo (1,3 MB) só é baixado depois que a página
     terminou de carregar, para não competir com CSS, logo e imagens. É dispensado
     quando o usuário pede menos movimento, ativou economia de dados ou está numa
     conexão lenta: nesses casos fica só o poster, que é o comportamento correto. */
  var heroVideo = document.getElementById('hero-video');
  if (heroVideo) {
    var conn = navigator.connection || {};
    var lenta = conn.saveData === true ||
                /^(slow-)?2g$/.test(conn.effectiveType || '');

    if (reduce || lenta) {
      heroVideo.removeAttribute('autoplay');
    } else {
      var carregar = function () {
        var webm = heroVideo.getAttribute('data-src-webm');
        var mp4 = heroVideo.getAttribute('data-src-mp4');
        if (!webm && !mp4) return;
        if (webm) {
          var s1 = document.createElement('source');
          s1.src = webm; s1.type = 'video/webm';
          heroVideo.appendChild(s1);
        }
        if (mp4) {
          var s2 = document.createElement('source');
          s2.src = mp4; s2.type = 'video/mp4';
          heroVideo.appendChild(s2);
        }
        heroVideo.preload = 'auto';
        heroVideo.load();
        var attempt = heroVideo.play();
        if (attempt && attempt.catch) attempt.catch(function () {});
      };

      if (document.readyState === 'complete') carregar();
      else window.addEventListener('load', carregar, { once: true });
    }
  }
})();

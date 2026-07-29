(function () {
  'use strict';

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
  var AREA_SLUGS = ['prorrogacao', 'recuperacao-extrajudicial', 'recuperacao-judicial', 'defesa-produtor-rural'];
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

  /* ---------- Dropdown desktop (Áreas de Atuação) ---------- */
  var ddToggle = document.querySelector('.has-dropdown .nav-toggle');
  if (ddToggle) {
    var ddParent = ddToggle.closest('.has-dropdown');
    var ddMenu = document.getElementById(ddToggle.getAttribute('aria-controls'));

    function setDropdown(open) {
      ddToggle.setAttribute('aria-expanded', String(open));
      ddParent.setAttribute('aria-expanded-group', String(open));
      ddMenu.classList.toggle('open', open);
    }
    ddToggle.addEventListener('click', function (e) {
      e.preventDefault();
      setDropdown(ddToggle.getAttribute('aria-expanded') !== 'true');
    });
    /* Fecha ao selecionar item ou clicar fora / ESC */
    Array.prototype.forEach.call(ddMenu.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () { setDropdown(false); });
    });
    document.addEventListener('click', function (e) {
      if (!ddParent.contains(e.target)) setDropdown(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setDropdown(false);
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
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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

  /* ---------- Vídeo da hero ---------- */
  var heroVideo = document.getElementById('hero-video');
  if (heroVideo) {
    if (reduce) {
      /* Sem movimento: mantém o poster (foto) parado, respeitando a preferência do usuário */
      heroVideo.removeAttribute('autoplay');
      heroVideo.pause();
    } else {
      /* Alguns navegadores exigem play() explícito mesmo com autoplay+muted */
      var attempt = heroVideo.play();
      if (attempt && attempt.catch) attempt.catch(function () {});
    }
  }
})();

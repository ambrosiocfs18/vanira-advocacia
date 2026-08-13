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

      var url = whatsUrl(texto);
      var janela = window.open(url, '_blank', 'noopener');

      /* Bloqueador de pop-up devolve null (ou uma janela que fecha na hora).
         Sem isto o visitante preenche o formulário, clica em enviar e não
         acontece nada — o contato se perde sem ninguém ficar sabendo.
         Nesse caso mostramos um link direto, que é um clique do próprio
         usuário e por isso nunca é bloqueado. */
      var bloqueado = !janela || janela.closed || typeof janela.closed === 'undefined';
      if (!bloqueado) return;

      var aviso = document.getElementById('form-fallback');
      if (!aviso) {
        aviso = document.createElement('p');
        aviso.id = 'form-fallback';
        aviso.className = 'form-fallback';
        aviso.setAttribute('role', 'alert');
        form.appendChild(aviso);
      }
      aviso.innerHTML = 'Seu navegador bloqueou a abertura do WhatsApp. ' +
        '<a target="_blank" rel="noopener noreferrer">Toque aqui para abrir a conversa</a>.';
      var link = aviso.querySelector('a');
      link.setAttribute('href', url);
      link.focus();
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

  /* ---------- Vídeos do YouTube com fachada ----------
     A página entrega só a capa (hospedada aqui) e um botão. O iframe do
     YouTube nasce no clique, e não antes: assim o visitante não faz nenhuma
     requisição ao Google nem recebe cookie de terceiro só por abrir a página,
     que é o que a política de privacidade promete. Também evita baixar o
     player (~1 MB) para quem nunca vai assistir. Domínio youtube-nocookie. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-yt]'), function (botao) {
    botao.addEventListener('click', function () {
      var id = botao.getAttribute('data-yt');
      if (!id) return;

      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
                  '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      frame.title = botao.getAttribute('data-yt-title') || 'Vídeo da Dra. Vanira';
      frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
      frame.setAttribute('allowfullscreen', '');
      frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');

      botao.parentNode.replaceChild(frame, botao);
      /* Devolve o foco para quem navega pelo teclado: o botão clicado sumiu. */
      frame.setAttribute('tabindex', '-1');
      frame.focus();
    });
  });

  /* ---------- Números do escritório subindo de zero ----------
     O HTML já traz o valor final escrito, então quem está sem JS, com o
     script bloqueado ou pedindo menos movimento lê o número correto do
     mesmo jeito. A contagem só entra por cima disso, e só quando a faixa
     aparece na tela — animar fora de vista seria animar para ninguém. */
  var numeros = document.querySelectorAll('[data-contar]');
  if (numeros.length) {
    /* 1200 -> "1.200", sem depender de locale do navegador */
    var milhar = function (n) {
      return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    };

    var contar = function (el) {
      var alvo = parseInt(el.getAttribute('data-contar'), 10);
      var prefixo = el.getAttribute('data-prefixo') || '';
      if (isNaN(alvo)) return;

      var DURACAO = 1600;
      var inicio = null;

      var passo = function (agora) {
        if (inicio === null) inicio = agora;
        var t = Math.min((agora - inicio) / DURACAO, 1);
        /* ease-out: arranca rápido e assenta no fim, em vez de parar seco */
        var e = 1 - Math.pow(1 - t, 3);
        el.textContent = prefixo + milhar(Math.round(alvo * e));
        if (t < 1) requestAnimationFrame(passo);
      };

      requestAnimationFrame(passo);
    };

    if (reduce || !('IntersectionObserver' in window) ||
        !('requestAnimationFrame' in window)) {
      /* Nada a fazer: o valor final já está no HTML. */
    } else {
      var ioNum = new IntersectionObserver(function (entradas) {
        Array.prototype.forEach.call(entradas, function (entrada) {
          if (!entrada.isIntersecting) return;
          ioNum.unobserve(entrada.target);
          contar(entrada.target);
        });
      }, { threshold: 0.4 });

      Array.prototype.forEach.call(numeros, function (el) {
        el.textContent = (el.getAttribute('data-prefixo') || '') + '0';
        ioNum.observe(el);
      });
    }
  }
})();

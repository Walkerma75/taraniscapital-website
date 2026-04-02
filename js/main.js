document.addEventListener('DOMContentLoaded', function() {
  // ===== 1. MOBILE NAVIGATION TOGGLE =====
  const toggle = document.querySelector('.nav-mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      toggle.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav') && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        toggle.classList.remove('active');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        toggle.classList.remove('active');
      }
    });
  }

  // ===== 2. COOKIE CONSENT BANNER =====
  function getCookie(name) {
    const nameEQ = name + '=';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.indexOf(nameEQ) === 0) {
        return cookie.substring(nameEQ.length);
      }
    }
    return null;
  }

  function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = 'expires=' + date.toUTCString();
    document.cookie = name + '=' + value + '; ' + expires + '; path=/';
  }

  function hideCookieBanner() {
    const banner = document.querySelector('.cookie-banner');
    if (banner) {
      banner.style.display = 'none';
    }
  }

  const cookieConsent = getCookie('tc_cookies');
  if (!cookieConsent) {
    const acceptBtn = document.querySelector('[data-cookie-accept]');
    const declineBtn = document.querySelector('[data-cookie-decline]');

    if (acceptBtn) {
      acceptBtn.addEventListener('click', () => {
        setCookie('tc_cookies', 'accepted', 365);
        hideCookieBanner();
      });
    }

    if (declineBtn) {
      declineBtn.addEventListener('click', () => {
        setCookie('tc_cookies', 'declined', 30);
        hideCookieBanner();
      });
    }
  } else {
    hideCookieBanner();
  }

  // ===== 3. SCROLL TO TOP BUTTON =====
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) {
        scrollTop.style.display = 'block';
      } else {
        scrollTop.style.display = 'none';
      }
    });

    scrollTop.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behaviour: 'smooth'
      });
    });
  }

  // ===== 4. ACTIVE NAV LINK HIGHLIGHTING =====
  const navLinkItems = document.querySelectorAll('.nav-links a');
  const currentPath = window.location.pathname;

  navLinkItems.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '/' && href === '/index.html')) {
      link.classList.add('active');
    } else if (href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    }
  });

  // ===== 5. NAVBAR SCROLL EFFECT =====
  const navbar = document.querySelector('.nav');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        navbar.classList.add('nav-scrolled');
      } else {
        navbar.classList.remove('nav-scrolled');
      }
    });
  }

  // ===== 6. SMOOTH SCROLL FOR ANCHOR LINKS =====
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      const target = document.querySelector(href);

      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behaviour: 'smooth'
        });
      }
    });
  });

  // ===== 7. RSS FEED LOADER =====
  const feedMain = document.querySelector('.feed-main');
  if (feedMain) {
    const feedTabs = document.querySelectorAll('.feed-tab');
    let feedData = [];

    const feeds = [
      { url: 'https://techcrunch.com/feed/', source: 'TechCrunch', category: 'tech' },
      { url: 'https://thefintechtimes.com/feed/', source: 'The Fintech Times', category: 'fintech' },
      { url: 'https://www.coindesk.com/arc/outboundfeeds/rss/', source: 'CoinDesk', category: 'crypto' }
    ];

    const proxyUrl = 'https://api.rss2json.com/v1/api.json?rss_url=';

    // Fetch and parse feeds
    async function loadFeeds() {
      try {
        const feedPromises = feeds.map(feed =>
          fetch(proxyUrl + encodeURIComponent(feed.url))
            .then(res => res.json())
            .then(data => {
              if (data.items) {
                return data.items.slice(0, 5).map(item => ({
                  source: feed.source,
                  category: feed.category,
                  title: item.title,
                  description: item.description ? item.description.replace(/<[^>]*>/g, '').substring(0, 180) + '...' : '',
                  link: item.link,
                  pubDate: item.pubDate
                }));
              }
              return [];
            })
            .catch(() => [])
        );

        const allItems = await Promise.all(feedPromises);
        feedData = allItems.flat();
        renderFeedCards('all');
      } catch (error) {
        console.warn('RSS feed fetch failed, showing placeholder content');
      }
    }

    function timeAgo(dateString) {
      const date = new Date(dateString);
      const seconds = Math.floor((new Date() - date) / 1000);
      let interval = seconds / 31536000;

      if (interval > 1) return Math.floor(interval) + ' years ago';
      interval = seconds / 2592000;
      if (interval > 1) return Math.floor(interval) + ' months ago';
      interval = seconds / 86400;
      if (interval > 1) return Math.floor(interval) + ' days ago';
      interval = seconds / 3600;
      if (interval > 1) return Math.floor(interval) + ' hours ago';
      interval = seconds / 60;
      if (interval > 1) return Math.floor(interval) + ' minutes ago';
      return Math.floor(seconds) + ' seconds ago';
    }

    function renderFeedCards(category) {
      const container = feedMain;
      const filtered = category === 'all' ? feedData : feedData.filter(item => item.category === category);

      // Only replace content if we have data
      if (feedData.length > 0) {
        container.innerHTML = '';
        filtered.forEach(item => {
          const card = document.createElement('div');
          card.className = 'feed-card';
          card.setAttribute('data-category', item.category);
          card.innerHTML = `
            <div class="feed-card-header">
              <span class="feed-source">${item.source}</span>
              <span class="feed-time">${timeAgo(item.pubDate)}</span>
            </div>
            <h3 class="feed-title">${item.title}</h3>
            <p class="feed-description">${item.description}</p>
            <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="feed-link">Read full article</a>
          `;
          container.appendChild(card);
        });
      }
    }

    // Tab filter handlers
    feedTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        feedTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const category = tab.getAttribute('data-category') || 'all';
        renderFeedCards(category);
      });
    });

    // Load feeds on page load
    loadFeeds();
  }

  // ===== 8. YEAR IN FOOTER =====
  const currentYear = new Date().getFullYear();
  const footerElements = document.querySelectorAll('*');

  footerElements.forEach(el => {
    if (el.childNodes.length > 0) {
      el.childNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.includes('© 2026')) {
          node.textContent = node.textContent.replace(/© 2026/g, `© ${currentYear}`);
        }
      });
    }
  });
});

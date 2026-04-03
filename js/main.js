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
    let visibleCount = 12;
    const ARTICLES_PER_PAGE = 12;

    // RSS feeds organised by category
    // Each feed can belong to multiple categories via the categories array
    const feeds = [
      // Venture Capital
      { url: 'https://techcrunch.com/category/venture/feed/', source: 'TechCrunch', categories: ['vc'] },
      { url: 'https://www.eu-startups.com/feed/', source: 'EU-Startups', categories: ['vc'] },
      { url: 'https://news.crunchbase.com/feed/', source: 'Crunchbase News', categories: ['vc'] },
      // Fintech
      { url: 'https://thefintechtimes.com/feed/', source: 'The Fintech Times', categories: ['fintech'] },
      { url: 'https://www.finextra.com/rss/headlines.aspx', source: 'Finextra', categories: ['fintech'] },
      { url: 'https://www.pymnts.com/feed/', source: 'PYMNTS', categories: ['fintech'] },
      // Biotech
      { url: 'https://www.fiercebiotech.com/rss/xml', source: 'FierceBiotech', categories: ['biotech'] },
      { url: 'https://www.genengnews.com/feed/', source: 'GEN', categories: ['biotech'] },
      { url: 'https://biopharmadive.com/feeds/news/', source: 'BioPharma Dive', categories: ['biotech'] },
      // MENA
      { url: 'https://waya.media/feed/', source: 'Waya Media', categories: ['mena'] },
      { url: 'https://www.zawya.com/en/rss/latest-news.xml', source: 'Zawya', categories: ['mena'] },
      { url: 'https://gulfnews.com/business/rss', source: 'Gulf News Business', categories: ['mena'] },
      // Crypto & Digital
      { url: 'https://www.coindesk.com/arc/outboundfeeds/rss/', source: 'CoinDesk', categories: ['crypto'] },
      { url: 'https://cointelegraph.com/rss', source: 'CoinTelegraph', categories: ['crypto'] }
    ];

    const proxyUrl = 'https://api.rss2json.com/v1/api.json?rss_url=';

    // Category display labels and CSS classes
    const categoryLabels = {
      vc: { label: 'Venture Capital', cssClass: 'feed-tag--vc' },
      fintech: { label: 'Fintech', cssClass: 'feed-tag--fintech' },
      biotech: { label: 'Biotech', cssClass: 'feed-tag--biotech' },
      mena: { label: 'MENA', cssClass: 'feed-tag--mena' },
      crypto: { label: 'Crypto & Digital', cssClass: 'feed-tag--crypto' }
    };

    // Fetch and parse all feeds
    async function loadFeeds() {
      // Show loading state
      feedMain.innerHTML = '<div class="feed-loading" style="text-align:center;padding:60px 0;color:var(--tc-grey-dark);"><div style="margin-bottom:16px;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 1s linear infinite;"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg></div><p>Loading latest articles...</p></div>';

      // Add spin animation if not already present
      if (!document.querySelector('#feed-spin-style')) {
        const style = document.createElement('style');
        style.id = 'feed-spin-style';
        style.textContent = '@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }';
        document.head.appendChild(style);
      }

      try {
        const feedPromises = feeds.map(feed =>
          fetch(proxyUrl + encodeURIComponent(feed.url))
            .then(res => res.json())
            .then(data => {
              if (data.status === 'ok' && data.items) {
                return data.items.slice(0, 8).map(item => ({
                  source: feed.source,
                  categories: feed.categories,
                  title: item.title || '',
                  description: item.description
                    ? item.description.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim().substring(0, 200) + '...'
                    : '',
                  link: item.link || '#',
                  pubDate: item.pubDate || new Date().toISOString(),
                  thumbnail: item.thumbnail || item.enclosure?.link || ''
                }));
              }
              return [];
            })
            .catch(err => {
              console.warn('Failed to load feed: ' + feed.source, err);
              return [];
            })
        );

        const allItems = await Promise.all(feedPromises);
        feedData = allItems.flat();

        // Sort by date, newest first
        feedData.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

        // Remove duplicates by title
        const seen = new Set();
        feedData = feedData.filter(item => {
          const key = item.title.toLowerCase().trim();
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        // Update sidebar feed counts
        updateSidebarCounts();

        // Render
        visibleCount = ARTICLES_PER_PAGE;
        renderFeedCards('all');

      } catch (error) {
        console.warn('RSS feed loading failed:', error);
        feedMain.innerHTML = '<div style="text-align:center;padding:40px 0;color:var(--tc-grey-dark);"><p>Unable to load live feeds. Please check back shortly.</p></div>';
      }
    }

    function updateSidebarCounts() {
      const sidebarItems = document.querySelectorAll('.sidebar-feed-item');
      sidebarItems.forEach(item => {
        const nameEl = item.querySelector('.sidebar-feed-name');
        const countEl = item.querySelector('.sidebar-feed-count');
        if (nameEl && countEl) {
          const name = nameEl.textContent.trim();
          const count = feedData.filter(d => d.source === name).length;
          countEl.textContent = count;
        }
      });
    }

    function timeAgo(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const seconds = Math.floor((now - date) / 1000);

      if (seconds < 0) return 'just now';
      if (seconds < 60) return 'just now';

      const minutes = Math.floor(seconds / 60);
      if (minutes < 60) return minutes + (minutes === 1 ? ' minute ago' : ' minutes ago');

      const hours = Math.floor(minutes / 60);
      if (hours < 24) return hours + (hours === 1 ? ' hour ago' : ' hours ago');

      const days = Math.floor(hours / 24);
      if (days < 30) return days + (days === 1 ? ' day ago' : ' days ago');

      const months = Math.floor(days / 30);
      if (months < 12) return months + (months === 1 ? ' month ago' : ' months ago');

      return Math.floor(months / 12) + ' years ago';
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    function renderFeedCards(category) {
      const filtered = category === 'all'
        ? feedData
        : feedData.filter(item => item.categories.includes(category));

      if (filtered.length === 0 && feedData.length > 0) {
        feedMain.innerHTML = '<div style="text-align:center;padding:40px 0;color:var(--tc-grey-dark);"><p>No articles found in this category. Please try another.</p></div>';
        return;
      }

      if (feedData.length === 0) return;

      const toShow = filtered.slice(0, visibleCount);
      const hasMore = filtered.length > visibleCount;

      feedMain.innerHTML = '';

      toShow.forEach(item => {
        const card = document.createElement('div');
        card.className = 'feed-card';
        card.setAttribute('data-category', item.categories[0]);

        // Build category tags
        const tags = item.categories.map(cat => {
          const info = categoryLabels[cat] || { label: cat, cssClass: '' };
          return '<span class="feed-tag ' + info.cssClass + '">' + info.label + '</span>';
        }).join('');

        card.innerHTML =
          '<div class="feed-card-source">' +
            '<div class="feed-source-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg></div>' +
            '<span class="feed-source-name">' + escapeHtml(item.source) + '</span>' +
            '<span class="feed-source-dot"></span>' +
            '<span class="feed-source-time">' + timeAgo(item.pubDate) + '</span>' +
          '</div>' +
          '<h3>' + escapeHtml(item.title) + '</h3>' +
          '<p>' + escapeHtml(item.description) + '</p>' +
          '<div class="feed-card-tags">' + tags + '</div>' +
          '<a href="' + item.link + '" target="_blank" rel="noopener noreferrer" class="feed-read-more">' +
            'Read full article ' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" width="14" height="14"><path d="M5 12h14M12 5l7 7-7 7"/></svg>' +
          '</a>';

        feedMain.appendChild(card);
      });

      // Load more button
      if (hasMore) {
        const loadMoreDiv = document.createElement('div');
        loadMoreDiv.style.cssText = 'text-align:center;margin-top:40px;';
        loadMoreDiv.innerHTML = '<button class="feed-load-more" style="display:inline-flex;align-items:center;gap:8px;padding:12px 32px;border:2px solid var(--tc-gold);border-radius:4px;color:var(--tc-gold);font-weight:600;background:transparent;cursor:pointer;font-size:15px;transition:all 0.3s ease;">' +
          'Load More Articles (' + (filtered.length - visibleCount) + ' remaining)' +
          '</button>';
        loadMoreDiv.querySelector('.feed-load-more').addEventListener('click', function() {
          visibleCount += ARTICLES_PER_PAGE;
          renderFeedCards(document.querySelector('.feed-tab.active')?.getAttribute('data-category') || 'all');
        });
        loadMoreDiv.querySelector('.feed-load-more').addEventListener('mouseenter', function() {
          this.style.background = 'var(--tc-gold)';
          this.style.color = 'white';
        });
        loadMoreDiv.querySelector('.feed-load-more').addEventListener('mouseleave', function() {
          this.style.background = 'transparent';
          this.style.color = 'var(--tc-gold)';
        });
        feedMain.appendChild(loadMoreDiv);
      }
    }

    // Tab filter handlers
    feedTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        feedTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        visibleCount = ARTICLES_PER_PAGE;
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

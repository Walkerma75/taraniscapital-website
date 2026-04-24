// CloudFront Function — url-rewrite
// Distribution: E18AUIFBUGMXSB  (apex taraniscapital.com)
// Event:        viewer-request
// Runtime:      cloudfront-js-2.0
//
// Purpose:
//   1. 301-redirect legacy WordPress URL patterns so Google removes them
//      from the "Crawled – currently not indexed" bucket. Affects 63/66
//      URLs flagged in the 2026-04-24 GSC drilldown.
//   2. Rewrite clean URLs to /path.html for static hosting on S3.
//
// Source of truth: this file (infra/cloudfront-url-rewrite.js in repo
// Walkerma75/taraniscapital-website). The IAM deploy user has no
// CloudFront Function permissions, so publishing is manual:
//
//   AWS Console → CloudFront → Functions → url-rewrite
//     → paste this code → Save → Publish → attach to distribution
//     → wait ~5 min for propagation → verify with curl (see 1.4 in
//     docs/GSC-INDEXING-PLAN-2026-04-24.md).
//
// IMPORTANT when updating: this is a REPLACEMENT of the function body.
// Diff against the current console source first; if the clean-URL
// rewrite logic at the bottom differs from what's live, keep the live
// version and merge only the redirect block above it.
//
// Last updated: 2026-04-24 (press section allowlist added)

var HOST = 'https://taraniscapital.com';

// Exact-path allowlist — these never get catch-all redirected.
// Keep in sync with the site's top-level pages.
var EXACT_ALLOW = {
    '/': 1, '/index.html': 1,
    '/who-we-are': 1,     '/who-we-are.html': 1,
    '/our-approach': 1,   '/our-approach.html': 1,
    '/our-funds': 1,      '/our-funds.html': 1,
    '/insights': 1,       '/insights.html': 1,
    '/press': 1,          '/press.html': 1,
    '/contact': 1,        '/contact.html': 1,
    '/fintech': 1,        '/fintech.html': 1,
    '/datacentres': 1,    '/datacentres.html': 1,
    '/biotech': 1,        '/biotech.html': 1,
    '/disruptive-tech': 1,'/disruptive-tech.html': 1,
    '/property': 1,       '/property.html': 1,
    '/cookie-policy': 1,  '/cookie-policy.html': 1,
    '/privacy-policy': 1, '/privacy-policy.html': 1,
    '/404.html': 1,
    '/robots.txt': 1, '/sitemap.xml': 1,
    '/humans.txt': 1, '/llms.txt': 1, '/security.txt': 1
};

// Prefix allowlist — any path starting with one of these is legitimate.
var PREFIX_ALLOW = [
    '/board/', '/partners/', '/team/', '/press/',
    '/css/', '/js/', '/images/', '/fonts/'
];

function redirect301(location) {
    return {
        statusCode: 301,
        statusDescription: 'Moved Permanently',
        headers: {
            'location':      { value: location },
            'cache-control': { value: 'public, max-age=3600' }
        }
    };
}

function isAllowed(uri) {
    if (EXACT_ALLOW[uri]) return true;
    for (var i = 0; i < PREFIX_ALLOW.length; i++) {
        if (uri.indexOf(PREFIX_ALLOW[i]) === 0) return true;
    }
    return false;
}

function handler(event) {
    var request = event.request;
    var uri     = request.uri;
    var qs      = request.querystring || {};

    // ---- Legacy WP pattern redirects (most specific first) ----

    // Pagination archives: /page/N/ and /insights/page/N/
    if (/^\/page\/\d+\/?$/.test(uri) || /^\/insights\/page\/\d+\/?$/.test(uri)) {
        return redirect301(HOST + '/insights');
    }

    // WP taxonomy
    if (/^\/tag\/[^\/]+\/?$/.test(uri))    return redirect301(HOST + '/insights');
    if (/^\/author\/[^\/]+\/?$/.test(uri)) return redirect301(HOST + '/');

    // WP custom post types — slug-preserving redirect to new profile URLs
    var mTeam = uri.match(/^\/team_member\/([^\/]+)\/?$/);
    if (mTeam)  return redirect301(HOST + '/team/' + mTeam[1]);
    var mBoard = uri.match(/^\/board_members\/([^\/]+)\/?$/);
    if (mBoard) return redirect301(HOST + '/board/' + mBoard[1]);

    // WP infra
    if (/^\/members-area\/?$/.test(uri))                return redirect301(HOST + '/');
    if (/^\/embed\/?$/.test(uri))                       return redirect301(HOST + '/');
    if (/\/feed\/?$/.test(uri))                         return redirect301(HOST + '/insights');
    if (/^\/(wp-login\.php|wp-admin\/?|xmlrpc\.php)/.test(uri)) return redirect301(HOST + '/');

    // Stale partner slug
    if (/^\/partners\/disrupts\/?$/.test(uri)) {
        return redirect301(HOST + '/who-we-are#strategic-partnerships');
    }

    // Strip LinkedIn tracking param on anything that falls through
    if (qs.trk) {
        return redirect301(HOST + uri);
    }

    // ---- Catch-all: legacy WP post slugs ----
    // Top-level single-segment path, lowercase-alnum-hyphen, ≥20 chars.
    // Must NOT match anything on the allowlist.
    var catchAll = uri.match(/^\/([a-z0-9][a-z0-9-]{19,})\/?$/);
    if (catchAll) {
        var noSlash   = '/' + catchAll[1];
        var withSlash = '/' + catchAll[1] + '/';
        if (!isAllowed(noSlash) && !isAllowed(withSlash)) {
            return redirect301(HOST + '/insights');
        }
    }

    // ---- Clean-URL rewriting ----
    // Strip trailing slash (except root) — 301 so duplicate content collapses.
    if (uri.length > 1 && uri.charAt(uri.length - 1) === '/') {
        return redirect301(HOST + uri.slice(0, -1));
    }

    // Append .html for extensionless paths (static hosting on S3).
    if (uri !== '/' && uri.indexOf('.') === -1) {
        request.uri = uri + '.html';
    }

    return request;
}

(function() {
  var API = window.LIFEOS_API || '/api/v1';
  var getToken = function() { return localStorage.getItem('lifeos_token'); };
  var getRefresh = function() { return localStorage.getItem('lifeos_refresh'); };

  function authHeaders() {
    var t = getToken();
    var h = { 'Content-Type': 'application/json' };
    if (t) h['Authorization'] = 'Bearer ' + t;
    return h;
  }

  async function api(method, path, body) {
    var opts = { method: method, headers: authHeaders() };
    if (body) opts.body = typeof body === 'string' ? body : JSON.stringify(body);
    var r = await fetch(API + path, opts);
    if (r.status === 401 && getRefresh()) {
      var refreshR = await fetch(API + '/auth/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: getRefresh() })
      });
      if (refreshR.ok) {
        var data = await refreshR.json();
        localStorage.setItem('lifeos_token', data.access);
        return api(method, path, body);
      }
    }
    if (r.status === 401) {
      localStorage.removeItem('lifeos_token');
      localStorage.removeItem('lifeos_refresh');
      window.location.href = '/login/';
      throw new Error('Unauthorized');
    }
    return r;
  }

  window.lifeos = {
    get: function(path) { return api('GET', path); },
    post: function(path, body) { return api('POST', path, body); },
    patch: function(path, body) { return api('PATCH', path, body); },
    put: function(path, body) { return api('PUT', path, body); },
    delete: function(path) { return api('DELETE', path); },
    json: function(r) { return r.json(); },
    token: getToken,
    logout: function() {
      localStorage.removeItem('lifeos_token');
      localStorage.removeItem('lifeos_refresh');
      window.location.href = '/login/';
    }
  };

  if (typeof lifeosRedirectLogin === 'function') {
    if (window.location.pathname.indexOf('/app') === 0 || window.location.pathname === '/') {
      lifeosRedirectLogin();
    }
  }
})();

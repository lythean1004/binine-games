/*
 * 빈이네 웹 버전용 기록 저장 장치
 *
 * 코인 점프·스카이 파이터는 원래 claude.ai 의 공용 저장소(window.claude)에
 * 랭킹과 내 정보를 저장한다. GitHub Pages 에는 그 저장소가 없으므로,
 * 같은 모양의 함수를 이 브라우저의 localStorage 로 대신 만들어 준다.
 * → 게임 코드는 그대로 두고, 기록·코인·상점 구매·랭킹(이 기기 기록)이 모두 동작한다.
 *
 * 이 파일은 tools/sync.py 가 배포용 복사본에만 끼워 넣는다. 원본 게임은 바뀌지 않는다.
 */
(function () {
  if (window.claude) return; // claude.ai 안에서 열리면 진짜 저장소를 쓴다

  var KEY = 'binine-records:' + location.pathname.replace(/index\.html$/, '');
  var listeners = [];

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(all) {
    try { localStorage.setItem(KEY, JSON.stringify(all)); } catch (e) {}
  }
  function snapDoc(path, data) {
    return { id: path.split('/').pop(), exists: data !== undefined, data: function () { return data; } };
  }

  function query(name, field, dir, max) {
    var prefix = name + '/';
    return {
      orderBy: function (f, d) { return query(name, f, d || 'asc', max); },
      limit: function (n) { return query(name, field, dir, n); },
      get: function () { return Promise.resolve(run()); },
      onSnapshot: function (cb) {
        var l = { prefix: prefix, fire: function () { cb(run()); } };
        listeners.push(l);
        setTimeout(l.fire, 0);
        return function () { listeners = listeners.filter(function (x) { return x !== l; }); };
      }
    };
    function run() {
      var all = load(), docs = [];
      for (var p in all) {
        if (p.indexOf(prefix) === 0 && p.slice(prefix.length).indexOf('/') < 0) docs.push(snapDoc(p, all[p]));
      }
      if (field) docs.sort(function (a, b) {
        var x = a.data()[field], y = b.data()[field];
        return (x > y ? 1 : x < y ? -1 : 0) * (dir === 'desc' ? -1 : 1);
      });
      if (max) docs = docs.slice(0, max);
      return { docs: docs, size: docs.length, empty: docs.length === 0 };
    }
  }

  var db = {
    collection: function (name) { return query(name); },
    doc: function (path) {
      return {
        get: function () { return Promise.resolve(snapDoc(path, load()[path])); },
        set: function (body) {
          var all = load();
          all[path] = JSON.parse(JSON.stringify(body));
          save(all);
          listeners.forEach(function (l) { if (path.indexOf(l.prefix) === 0) setTimeout(l.fire, 0); });
          return Promise.resolve();
        }
      };
    }
  };

  var user = {
    id: function () {
      var k = 'binine-player-id', id = null;
      try { id = localStorage.getItem(k); } catch (e) {}
      if (!id) {
        id = 'me-' + Math.random().toString(36).slice(2, 10);
        try { localStorage.setItem(k, id); } catch (e) {}
      }
      return Promise.resolve(id);
    }
  };

  window.claude = {
    use: function (name) {
      return Promise.resolve(name === 'db' ? db : name === 'user' ? user : null);
    }
  };
})();

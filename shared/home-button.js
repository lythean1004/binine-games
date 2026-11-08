// 빈이네 놀이터: 모든 작품 구석에 "🏠 놀이터" 버튼을 붙인다.
// - 게임 화면과 스타일이 섞이지 않게 Shadow DOM 안에 만든다.
// - 게임 중 실수로 눌러 나가지 않게, 한 번 누르면 "한 번 더 누르면 놀이터로 가요"가 뜨고
//   3초 안에 한 번 더 눌러야 이동한다.
// - 위치는 games.json 의 "home" 값(top-left, top-right, bottom-left, bottom-right)으로 바꿀 수 있다.
(function () {
  var me = document.currentScript;
  var pos = (me && me.dataset.pos) || 'bottom-left';
  var href = (me && me.dataset.href) || '../../';

  function mount() {
    if (document.getElementById('binine-home')) return;
    var host = document.createElement('div');
    host.id = 'binine-home';
    var v = pos.split('-');
    host.style.cssText = 'position:fixed;z-index:2147483647;' + v[0] + ':10px;' + v[1] + ':10px;';
    var root = host.attachShadow({ mode: 'open' });
    root.innerHTML =
      '<style>' +
      'a{display:flex;align-items:center;gap:5px;height:34px;padding:0 11px;border-radius:17px;' +
      'background:rgba(30,25,20,.55);color:#fff;font:600 13px/1 system-ui,"Malgun Gothic",sans-serif;' +
      'text-decoration:none;opacity:.6;transition:opacity .15s,background .15s;cursor:pointer;' +
      '-webkit-tap-highlight-color:transparent;box-shadow:0 2px 6px rgba(0,0,0,.25);user-select:none}' +
      'a:hover,a:focus-visible{opacity:1;background:rgba(30,25,20,.85)}' +
      'a:focus-visible{outline:3px solid #ff7a3d;outline-offset:2px}' +
      'a.ask{opacity:1;background:#ff7a3d}' +
      '.t{white-space:nowrap}.q{display:none;white-space:nowrap}' +
      'a.ask .t{display:none}a.ask .q{display:inline}' +
      '@media (max-width:480px){a:not(.ask) .t{display:none}a:not(.ask){width:34px;padding:0;justify-content:center}}' +
      '</style>' +
      '<a href="' + href + '" role="button" title="빈이네 놀이터로 돌아가기" aria-label="빈이네 놀이터로 돌아가기">' +
      '<span aria-hidden="true">🏠</span><span class="t">놀이터</span>' +
      '<span class="q">한 번 더 누르면 놀이터로 가요</span></a>';

    var a = root.querySelector('a');
    var timer = null;
    a.addEventListener('click', function (e) {
      if (a.classList.contains('ask')) return; // 두 번째 누름: 그대로 이동
      e.preventDefault();
      a.classList.add('ask');
      clearTimeout(timer);
      timer = setTimeout(function () { a.classList.remove('ask'); }, 3000);
    });

    // 게임이 이 버튼의 터치·클릭·키 입력을 자기 조작으로 받지 않게 막는다
    ['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'touchstart', 'touchend', 'click', 'keydown', 'keyup'].forEach(function (t) {
      host.addEventListener(t, function (e) { e.stopPropagation(); });
    });
    document.body.appendChild(host);
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();

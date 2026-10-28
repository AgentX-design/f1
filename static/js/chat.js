document.getElementById('chat-form').addEventListener('submit', handleChat);

function handleChat(e) {
  if (e) e.preventDefault();
  const msg = document.getElementById('message').value.trim();
  if (!msg) return;
  addMessage(msg, 'user');
  document.getElementById('message').value = '';
  setTyping(true);
  const btn = document.querySelector('.chat-send');
  btn.disabled = true;
  fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: msg})
  })
  .then(r => r.json())
  .then(data => {
    addMessage(data.result ? (data.result.answer || '') : '', 'assistant', data.result);
  })
  .catch(() => addMessage('Error: unable to reach server.', 'assistant'))
  .finally(() => { btn.disabled = false; setTyping(false); });
}

document.getElementById('message').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.getElementById('chat-form').requestSubmit(); }
});

function setTyping(active) {
  const el = document.getElementById('typing-indicator');
  if (active) el.classList.add('active'); else el.classList.remove('active');
}

function addMessage(text, role, detail) {
  const c = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'message ' + role;
  // Format answer with sources if available
  div.innerHTML = formatText(text);
  if (detail && detail.sources && detail.sources.length) {
    const sources = document.createElement('div');
    sources.className = 'msg-sources';
    sources.innerHTML = '<strong>Sources:</strong> ' + detail.sources.map(s => `<a href="${s.url || '#'}" target="_blank" rel="noopener">${s.name || 'Source'}</a>`).join(' · ');
    div.appendChild(sources);
  }
  c.appendChild(div);
  c.scrollTop = c.scrollHeight;
}

function formatText(t) {
  if (!t) return '';
  return t.replace(/([A-Z][a-z]+ [A-Z][a-z]+ Grand Prix)/g, '<strong>$1</strong>');
}

function loadSuggested() {
  fetch('/api/suggested')
    .then(r => r.json())
    .then(list => {
      const box = document.getElementById('suggested');
      box.innerHTML = '';
      list.forEach(q => {
        const b = document.createElement('button');
        b.textContent = q;
        b.onclick = () => { document.getElementById('message').value = q; handleChat(); };
        box.appendChild(b);
      });
    })
    .catch(() => {});
}
loadSuggested();

function selectSeason(y) {
  document.getElementById('message').value = 'Show ' + y + ' championship summary';
  document.getElementById('chat').scrollIntoView({behavior:'smooth', block:'center'});
  handleChat();
}

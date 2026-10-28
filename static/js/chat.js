document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = document.getElementById('message').value;
  if (!msg) return;
  addMessage(msg, 'user');
  const btn = document.querySelector('button');
  btn.disabled = true;
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    addMessage(data.result.answer, 'assistant', data.result);
  } catch (err) {
    addMessage('Error: unable to reach server.', 'assistant');
  } finally {
    btn.disabled = false;
    document.getElementById('message').value = '';
  }
});

async function loadSuggested() {
  try {
    const r = await fetch('/api/suggested');
    const list = await r.json();
    const box = document.getElementById('suggested');
    box.innerHTML = '';
    list.forEach(q => {
      const b = document.createElement('button');
      b.textContent = q;
      b.onclick = () => { document.getElementById('message').value = q; document.getElementById('chat-form').dispatchEvent(new Event('submit')); };
      box.appendChild(b);
    });
  } catch (e) {}
}
loadSuggested();

async function addMessage(text, role, detail) {
  const c = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'message ' + role;
  div.textContent = text;
  c.appendChild(div);
}

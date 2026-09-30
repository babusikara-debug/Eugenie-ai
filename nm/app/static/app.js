const tools = {
  qa: { kicker: '01 / ASK', title: 'What are you curious about?', description: 'Ask a question and get a concise, learner-friendly answer.', label: 'Your question', placeholder: 'Which is the largest ocean?', submit: 'Get answer', endpoint: '/api/qa' },
  explain: { kicker: '02 / EXPLAIN', title: 'Make a concept feel simple.', description: 'Turn a difficult topic into a clear explanation with an example.', label: 'Topic to explain', placeholder: 'Explain photosynthesis', submit: 'Explain it', endpoint: '/api/explain', field: 'topic' },
  summarize: { kicker: '03 / SUMMARIZE', title: 'Keep what matters.', description: 'Condense a long passage into useful revision notes.', label: 'Passage to summarize', placeholder: 'Paste a paragraph or lesson here...', submit: 'Summarize', endpoint: '/api/summarize' },
  quiz: { kicker: '04 / QUIZ', title: 'Test your understanding.', description: 'Generate three questions and check your answers immediately.', label: 'Topic or study text', placeholder: 'The Pythagorean theorem', submit: 'Generate quiz', endpoint: '/api/quiz' },
  recommendations: { kicker: '05 / LEARN PATH', title: 'Know what to learn next.', description: 'Get a practical route from first principles to confident application.', label: 'Topic for your path', placeholder: 'SQL, biology, or any subject', submit: 'Build my path', endpoint: '/api/recommendations', field: 'topic' }
};
let selectedTool = 'qa';
const $ = (selector) => document.querySelector(selector);
const tabs = document.querySelectorAll('.tool-tab');
const input = $('#prompt-input');
const form = $('#learning-form');
const result = $('#result');

function selectTool(name) {
  selectedTool = name;
  const tool = tools[name];
  tabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.tool === name));
  $('#tool-kicker').textContent = tool.kicker;
  $('#tool-title').textContent = tool.title;
  $('#tool-description').textContent = tool.description;
  $('#input-label').textContent = tool.label;
  input.placeholder = tool.placeholder;
  $('#submit-label').textContent = tool.submit;
  input.value = '';
  $('#char-count').textContent = '0 / 12,000';
  result.innerHTML = '<div class="result-empty"><span class="empty-icon">+</span><p>Your response will appear here.</p></div>';
}

tabs.forEach((tab) => tab.addEventListener('click', () => selectTool(tab.dataset.tool)));
input.addEventListener('input', () => { $('#char-count').textContent = `${input.value.length.toLocaleString()} / 12,000`; });

function renderContent(data) {
  result.innerHTML = `<h3>Response <span class="source">(${data.source} mode)</span></h3><div class="result-content"></div>`;
  result.querySelector('.result-content').textContent = data.content;
}
function renderQuiz(data) {
  result.innerHTML = '<h3>Quiz <span class="source">(choose an answer)</span></h3>';
  data.questions.forEach((question, index) => {
    const block = document.createElement('div');
    block.className = 'quiz-question';
    block.innerHTML = `<p>${index + 1}. ${question.question}</p>${question.options.map((option, optionIndex) => `<label class="quiz-option"><input type="radio" name="q${index}" value="${optionIndex}"> ${option}</label>`).join('')}<button type="button" class="check-button">Check answer</button><div class="feedback" aria-live="polite"></div>`;
    block.querySelector('.check-button').addEventListener('click', () => {
      const selected = block.querySelector('input:checked');
      const feedback = block.querySelector('.feedback');
      if (!selected) { feedback.textContent = 'Choose an option first.'; feedback.className = 'feedback wrong'; return; }
      if (question.options[Number(selected.value)] === question.answer) { feedback.textContent = 'Correct. Nice work.'; feedback.className = 'feedback correct'; }
      else { feedback.textContent = `Not quite. Correct answer: ${question.answer}`; feedback.className = 'feedback wrong'; }
    });
    result.appendChild(block);
  });
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const value = input.value.trim();
  if (!value) return;
  const tool = tools[selectedTool];
  const field = tool.field || 'text';
  const button = form.querySelector('button');
  button.disabled = true;
  $('#submit-label').textContent = 'Working...';
  result.innerHTML = '<div class="result-empty"><span class="empty-icon">...</span><p>Thinking through that now.</p></div>';
  try {
    const response = await fetch(tool.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ [field]: value }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail?.[0]?.msg || data.detail || 'Request failed');
    if (selectedTool === 'quiz') renderQuiz(data); else renderContent(data);
  } catch (error) {
    result.innerHTML = `<div class="result-empty"><span class="empty-icon">!</span><p>${error.message}</p></div>`;
  } finally {
    button.disabled = false;
    $('#submit-label').textContent = tool.submit;
  }
});

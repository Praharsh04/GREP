(function() {
  // ─── STYLES ───
  const style = document.createElement('style');
  style.textContent = `
    :root {
      --pomo-bg: rgba(15, 15, 15, 0.7);
      --pomo-border: rgba(255, 255, 255, 0.08);
      --pomo-shadow: rgba(0, 0, 0, 0.4);
      --pomo-divider: rgba(255, 255, 255, 0.1);
    }

    [data-theme="light"] {
      --pomo-bg: rgba(255, 255, 255, 0.8);
      --pomo-border: rgba(0, 0, 0, 0.1);
      --pomo-shadow: rgba(0, 0, 0, 0.1);
      --pomo-divider: rgba(0, 0, 0, 0.1);
    }

    .pomodoro-container {
      position: fixed;
      top: 12px;
      right: 12px;
      z-index: 2100;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 5px 12px;
      background: var(--pomo-bg);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid var(--pomo-border);
      border-radius: 100px;
      box-shadow: 0 4px 16px var(--pomo-shadow);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: default;
    }

    .pomodoro-container:hover {
      transform: scale(1.02);
      border-color: var(--pomo-border);
      box-shadow: 0 6px 20px var(--pomo-shadow);
    }

    .pomodoro-label {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--muted, rgba(245, 240, 232, 0.45));
      opacity: 0.8;
      user-select: none;
    }

    .pomo-divider {
      width: 1px;
      height: 12px;
      background: var(--pomo-divider);
    }

    .pomodoro-display {
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 700;
      color: var(--cream, #f5f0e8);
      min-width: 42px;
      text-align: center;
      letter-spacing: -0.5px;
    }

    .pomodoro-btns {
      display: flex;
      gap: 3px;
      margin-left: 1px;
    }

    .pomodoro-btns button {
      background: transparent;
      border: none;
      color: var(--muted, rgba(245, 240, 232, 0.45));
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2px;
      transition: all 0.2s ease;
      border-radius: 50%;
    }

    .pomodoro-btns button:hover {
      color: var(--gold, #c9a84c);
      background: rgba(201, 168, 76, 0.1);
    }

    .pomodoro-btns button svg {
      width: 11px;
      height: 11px;
    }

    @media (max-width: 900px) {
      .pomodoro-container {
        right: 10px;
        top: 10px;
      }
    }
  `;
  document.head.appendChild(style);

  // ─── HTML ───
  const container = document.createElement('div');
  container.className = 'pomodoro-container';
  container.innerHTML = `
    <div class="pomodoro-label" id="pomo-label">Focus</div>
    <div class="pomo-divider"></div>
    <div class="pomodoro-display" id="pomo-display-text">25:00</div>
    <div class="pomodoro-btns">
      <button id="pomo-start-btn" title="Start/Pause">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
      </button>
      <button id="pomo-reset-btn" title="Reset">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
      </button>
    </div>
  `;
  document.body.appendChild(container);

  // ─── LOGIC ───
  let pomoTime = 1500;
  let isPomoRunning = false;
  let pomoMode = 'work';
  let pomoInterval = null;

  const display = container.querySelector('#pomo-display-text');
  const label = container.querySelector('#pomo-label');
  const startBtn = container.querySelector('#pomo-start-btn');
  const resetBtn = container.querySelector('#pomo-reset-btn');

  function updateDisplay() {
    const mins = Math.floor(pomoTime / 60);
    const secs = pomoTime % 60;
    display.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  function start() {
    if (isPomoRunning) return;
    isPomoRunning = true;
    startBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
    pomoInterval = setInterval(() => {
      pomoTime--;
      updateDisplay();
      if (pomoTime <= 0) {
        clearInterval(pomoInterval);
        isPomoRunning = false;
        handleEnd();
      }
    }, 1000);
  }

  function pause() {
    isPomoRunning = false;
    clearInterval(pomoInterval);
    startBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
  }

  function reset() {
    pause();
    pomoMode = 'work';
    pomoTime = 1500;
    label.textContent = 'Focus';
    updateDisplay();
  }

  function handleEnd() {
    try {
      new Audio('https://assets.mixkit.co/sfx/preview/mixkit-simple-notification-alert-120.mp3').play();
    } catch(e) {}

    if (pomoMode === 'work') {
      pomoMode = 'break';
      pomoTime = 300;
      label.textContent = 'Break';
    } else {
      pomoMode = 'work';
      pomoTime = 1500;
      label.textContent = 'Focus';
    }
    updateDisplay();
    startBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
  }

  startBtn.onclick = () => isPomoRunning ? pause() : start();
  resetBtn.onclick = reset;

})();

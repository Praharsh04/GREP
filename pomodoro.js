(function() {
  // ─── STYLES ───
  const style = document.createElement('style');
  style.textContent = `
    :root {
      --timer-bg: rgba(15, 15, 15, 0.75);
      --timer-border: rgba(255, 255, 255, 0.08);
      --timer-gold: #c9a84c;
      --timer-cream: #f5f0e8;
      --timer-muted: rgba(245, 240, 232, 0.45);
      --timer-glow: rgba(201, 168, 76, 0.2);
    }

    [data-theme="light"] {
      --timer-bg: rgba(255, 255, 255, 0.85);
      --timer-border: rgba(0, 0, 0, 0.08);
      --timer-gold: #9a7b2c;
      --timer-cream: #1a1918;
      --timer-muted: rgba(26, 25, 24, 0.6);
      --timer-glow: rgba(154, 123, 44, 0.15);
    }

    .study-pill {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 2500;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 16px;
      background: var(--timer-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--timer-border);
      border-radius: 100px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      user-select: none;
      font-family: 'JetBrains Mono', monospace;
    }

    .study-pill:hover {
      transform: translateY(-2px);
      border-color: var(--timer-gold);
      box-shadow: 0 12px 40px var(--timer-glow);
    }

    .pill-section {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pill-clock {
      font-size: 12px;
      font-weight: 500;
      color: var(--timer-muted);
      letter-spacing: -0.2px;
    }

    .pill-divider {
      width: 1px;
      height: 14px;
      background: var(--timer-border);
    }

    .pill-timer {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .timer-display {
      font-size: 14px;
      font-weight: 700;
      color: var(--timer-cream);
      min-width: 44px;
      text-align: center;
      cursor: pointer;
      transition: color 0.2s ease;
    }

    .timer-display:hover {
      color: var(--timer-gold);
    }

    .pill-controls {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .pill-btn {
      background: transparent;
      border: none;
      color: var(--timer-muted);
      cursor: pointer;
      padding: 4px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }

    .pill-btn:hover {
      color: var(--timer-gold);
      background: rgba(201, 168, 76, 0.1);
    }

    .pill-btn svg {
      width: 14px;
      height: 14px;
    }

    /* Duration Picker Tooltip */
    .duration-picker {
      position: absolute;
      top: 100%;
      right: 0;
      margin-top: 8px;
      background: var(--timer-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--timer-border);
      border-radius: 12px;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      opacity: 0;
      visibility: hidden;
      transform: translateY(-10px);
      transition: all 0.2s ease;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    .duration-picker.show {
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
    }

    .duration-opt {
      padding: 6px 12px;
      font-size: 11px;
      color: var(--timer-muted);
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .duration-opt:hover {
      background: var(--timer-gold);
      color: #000;
    }

    .duration-opt.active {
      color: var(--timer-gold);
      background: rgba(201, 168, 76, 0.1);
    }

    @media (max-width: 600px) {
      .study-pill {
        top: 12px;
        right: 12px;
        padding: 5px 12px;
        gap: 8px;
      }
      .pill-clock { display: none; }
      .pill-divider { display: none; }
    }
  `;
  document.head.appendChild(style);

  // ─── HTML ───
  const pill = document.createElement('div');
  pill.className = 'study-pill';
  pill.innerHTML = `
    <div class="pill-section">
      <div class="pill-clock" id="pill-clock">00:00</div>
    </div>
    <div class="pill-divider"></div>
    <div class="pill-section pill-timer">
      <div class="timer-display" id="pill-timer-display" title="Click to change duration">25:00</div>
      <div class="pill-controls">
        <button class="pill-btn" id="pill-play-pause" title="Start/Pause">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        </button>
        <button class="pill-btn" id="pill-reset" title="Reset">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
        </button>
      </div>
    </div>
    <div class="duration-picker" id="duration-picker">
      <div class="duration-opt" data-mins="15">15 Minutes</div>
      <div class="duration-opt active" data-mins="25">25 Minutes</div>
      <div class="duration-opt" data-mins="45">45 Minutes</div>
      <div class="duration-opt" data-mins="60">60 Minutes</div>
      <div class="duration-opt" data-mins="5">Short Break (5m)</div>
    </div>
  `;
  document.body.appendChild(pill);

  // ─── LOGIC ───
  let timeLeft = 1500;
  let timerId = null;
  let isRunning = false;
  let currentPreset = 25;

  const clockEl = document.getElementById('pill-clock');
  const timerEl = document.getElementById('pill-timer-display');
  const playBtn = document.getElementById('pill-play-pause');
  const resetBtn = document.getElementById('pill-reset');
  const picker = document.getElementById('duration-picker');

  // Clock
  function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const mins = now.getMinutes().toString().padStart(2, '0');
    clockEl.textContent = `${hours}:${mins}`;
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Timer
  function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  }

  function updateTimerDisplay() {
    timerEl.textContent = formatTime(timeLeft);
  }

  function startTimer() {
    if (isRunning) return;
    isRunning = true;
    playBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
    timerId = setInterval(() => {
      timeLeft--;
      updateTimerDisplay();
      if (timeLeft <= 0) {
        clearInterval(timerId);
        isRunning = false;
        playBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
        
        // Sound notification
        try {
          new Audio('https://assets.mixkit.co/sfx/preview/mixkit-simple-notification-alert-120.mp3').play();
        } catch(e) { console.error('Audio play failed', e); }
        
        alert('Study session complete!');
      }
    }, 1000);
  }

  function pauseTimer() {
    isRunning = false;
    clearInterval(timerId);
    playBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
  }

  function resetTimer() {
    pauseTimer();
    timeLeft = currentPreset * 60;
    updateTimerDisplay();
  }

  playBtn.onclick = () => isRunning ? pauseTimer() : startTimer();
  resetBtn.onclick = resetTimer;

  // Duration Picker
  timerEl.onclick = (e) => {
    e.stopPropagation();
    picker.classList.toggle('show');
  };

  document.querySelectorAll('.duration-opt').forEach(opt => {
    opt.onclick = () => {
      const mins = parseInt(opt.dataset.mins);
      currentPreset = mins;
      document.querySelectorAll('.duration-opt').forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      resetTimer();
      picker.classList.remove('show');
    };
  });

  window.onclick = () => picker.classList.remove('show');

})();

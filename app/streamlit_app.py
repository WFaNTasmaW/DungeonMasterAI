import streamlit as st
import sys
from pathlib import Path
import time

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

st.set_page_config(
    page_title="Dungeon Master AI",
    page_icon="🐉",
    layout="wide"
)

if 'page_loaded' not in st.session_state:
    st.session_state.page_loaded = False

if not st.session_state.page_loaded:
    st.markdown("""
<style>
.loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, #2a1810 0%, #0f0a06 100%);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

#dice-container {
    width: 300px;
    height: 300px;
    position: relative;
}

.critical-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.9) 0%, rgba(255, 140, 0, 0.4) 40%, transparent 70%);
    border-radius: 50%;
    opacity: 0;
    animation: glowAppear 1s ease-out 3s forwards, glowPulse 1.5s ease-in-out 4s infinite;
}

@keyframes glowAppear {
    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
    100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

@keyframes glowPulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.7; }
    50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
}

.number-20 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 120px;
    font-weight: 900;
    color: #ffd700;
    text-shadow: 
        0 0 10px rgba(255, 215, 0, 1),
        0 0 20px rgba(255, 140, 0, 0.8),
        0 0 40px rgba(255, 69, 0, 0.6),
        3px 3px 6px rgba(0, 0, 0, 0.8);
    opacity: 0;
    animation: numberAppear 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 3s forwards;
    z-index: 10;
    font-family: 'Georgia', serif;
    pointer-events: none;
}

@keyframes numberAppear {
    0% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(0) rotate(-180deg);
    }
    60% {
        transform: translate(-50%, -50%) scale(1.3) rotate(10deg);
    }
    100% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1) rotate(0deg);
    }
}

.loading-text {
    margin-top: 40px;
    color: #d4af37;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 4px;
    font-family: 'Georgia', serif;
    text-transform: uppercase;
    animation: pulse 1.5s ease-in-out infinite;
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

.critical-text {
    margin-top: 20px;
    color: #ff4500;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 6px;
    font-family: 'Georgia', serif;
    text-transform: uppercase;
    opacity: 0;
    animation: criticalAppear 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) 3.2s forwards;
    text-shadow: 
        0 0 20px rgba(255, 69, 0, 1),
        0 0 40px rgba(255, 140, 0, 0.8);
}

@keyframes criticalAppear {
    0% {
        opacity: 0;
        transform: scale(0.3) translateY(20px);
        letter-spacing: 20px;
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
        letter-spacing: 6px;
    }
}

.dm-text {
    margin-top: 15px;
    color: #8b7355;
    font-size: 16px;
    font-style: italic;
    font-family: 'Georgia', serif;
    opacity: 0;
    animation: fadeIn 1s ease-in 3.5s forwards;
}

@keyframes fadeIn {
    to { opacity: 1; }
}
</style>

<div class="loading-screen">
<div id="dice-container">
<canvas id="d20-canvas"></canvas>
<div class="critical-glow"></div>
<div class="number-20">20</div>
</div>
<div class="loading-text">Бросок инициативы...</div>
<div class="critical-text">КРИТИЧЕСКИЙ УСПЕХ!</div>
<div class="dm-text">~ За ширмой мастера ~</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// Инициализация Three.js сцены

// Освещение
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffd700, 1);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

const pointLight2 = new THREE.PointLight(0xff6b00, 0.8);
pointLight2.position.set(-5, -5, 5);
scene.add(pointLight2);

camera.position.z = 3;

// Очистка при уходе со страницы
window.addEventListener('beforeunload', () => {
    renderer.dispose();
    geometry.dispose();
    material.dispose();
});
</script>
""", unsafe_allow_html=True)

    time.sleep(4.5)
    st.session_state.page_loaded = True
    st.rerun()

st.title("🐉 Dungeon Master AI")

st.markdown("""
Добро пожаловать в **Dungeon Master AI**.

Это AI-помощник для Мастера Подземелий, использующий RAG и LLM для создания незабываемых приключений.

### ⚔️ Возможности
- 💎 **Генерация магических предметов** — уникальные артефакты с историей и свойствами.
- 💰 **Генерация магических предметов** — уникальные артефакты с историей и свойствами.
- 👤 **Генерация NPC** — создание живых персонажей с предыстор
- 📖 **Поиск правил D&D** — мгновенные ответы по книгам правил.
- 💎 **Всякие полезности** — различные таблицы на все цвета.

> *Используйте меню слева для перехода между разделами.*

---

*Давайте начнем ваше приключение...*
""")
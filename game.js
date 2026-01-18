// Game State
const gameState = {
    heroHP: 1000,
    heroMaxHP: 1000,
    enemyHP: 50000,
    enemyMaxHP: 50000,
    braveBurst: 0,
    maxBraveBurst: 100,
    combo: 0,
    isAnimating: false
};

// DOM Elements
const heroSprite = document.getElementById('hero-sprite');
const enemySprite = document.getElementById('enemy-sprite');
const heroHealthFill = document.getElementById('hero-health-fill');
const enemyHealthFill = document.getElementById('enemy-health-fill');
const enemyHealthText = document.getElementById('enemy-health-text');
const braveBurstFill = document.getElementById('brave-burst-fill');
const burstBtn = document.getElementById('burst-btn');
const comboNumber = document.getElementById('combo-number');
const damageNumbers = document.getElementById('damage-numbers');
const screenFlash = document.getElementById('screen-flash');
const battleArena = document.getElementById('battle-arena');
const resultScreen = document.getElementById('result-screen');
const resultTitle = document.getElementById('result-title');
const particles = document.getElementById('particles');
const enemyHitEffect = document.getElementById('enemy-hit-effect');

// Initialize
function init() {
    // Load character images
    heroSprite.innerHTML = `<div id="hero-aura"></div><img src="hero.png" alt="Hero"><div id="slash-effect"></div>`;
    enemySprite.innerHTML = `<div id="enemy-hit-effect"></div><img src="enemy.png" alt="Enemy">`;
    
    // Create background particles
    createBackgroundParticles();
    
    // Event Listeners
    document.getElementById('attack-btn').addEventListener('click', () => performAttack('normal'));
    document.getElementById('skill-btn').addEventListener('click', () => performAttack('skill'));
    document.getElementById('burst-btn').addEventListener('click', () => performAttack('burst'));
    document.getElementById('continue-btn').addEventListener('click', resetGame);
    
    updateUI();
}

// Create floating background particles
function createBackgroundParticles() {
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (5 + Math.random() * 5) + 's';
        const hue = Math.random() > 0.5 ? '260' : '200';
        particle.style.color = `hsl(${hue}, 80%, 70%)`;
        particle.style.background = `hsl(${hue}, 80%, 70%)`;
        particles.appendChild(particle);
    }
}

// Perform Attack
async function performAttack(type) {
    if (gameState.isAnimating) return;
    if (type === 'burst' && gameState.braveBurst < gameState.maxBraveBurst) return;
    
    gameState.isAnimating = true;
    
    let damage, animClass, flashIntensity, hitCount;
    
    switch(type) {
        case 'normal':
            damage = 1500 + Math.floor(Math.random() * 500);
            animClass = 'attacking';
            flashIntensity = 0.3;
            hitCount = 1;
            break;
        case 'skill':
            damage = 3000 + Math.floor(Math.random() * 1000);
            animClass = 'skill-cast';
            flashIntensity = 0.5;
            hitCount = 3;
            break;
        case 'burst':
            damage = 8000 + Math.floor(Math.random() * 2000);
            animClass = 'brave-burst';
            flashIntensity = 0.8;
            hitCount = 7;
            gameState.braveBurst = 0;
            break;
    }
    
    // Hero attack animation
    heroSprite.classList.add(animClass);
    
    // Create slash/impact effects during attack
    if (type === 'burst') {
        await sleep(200);
        createMassiveAura();
    }
    
    // Wait for attack to reach enemy
    const attackDelay = type === 'burst' ? 600 : type === 'skill' ? 400 : 200;
    await sleep(attackDelay);
    
    // Multi-hit damage
    for (let i = 0; i < hitCount; i++) {
        const hitDamage = Math.floor(damage / hitCount) + Math.floor(Math.random() * 200);
        const isCritical = Math.random() > 0.7;
        const finalDamage = isCritical ? Math.floor(hitDamage * 1.5) : hitDamage;
        
        // Screen flash
        flashScreen(flashIntensity);
        
        // Screen shake
        battleArena.classList.add('screen-shake');
        
        // Enemy hit animation
        enemySprite.classList.add('hit');
        showHitEffect();
        
        // Create impact particles
        createImpactParticles(type);
        
        // Show damage number
        showDamageNumber(finalDamage, isCritical);
        
        // Deal damage
        gameState.enemyHP = Math.max(0, gameState.enemyHP - finalDamage);
        
        // Increase combo
        gameState.combo++;
        
        // Increase brave burst gauge
        if (type !== 'burst') {
            gameState.braveBurst = Math.min(gameState.maxBraveBurst, gameState.braveBurst + 10);
        }
        
        updateUI();
        
        await sleep(150);
        
        enemySprite.classList.remove('hit');
        battleArena.classList.remove('screen-shake');
    }
    
    // Remove attack animation class
    heroSprite.classList.remove(animClass);
    
    // Check for victory
    if (gameState.enemyHP <= 0) {
        await sleep(500);
        showVictory();
        gameState.isAnimating = false;
        return;
    }
    
    // Enemy counter attack
    await sleep(500);
    await enemyAttack();
    
    gameState.isAnimating = false;
}

// Enemy Attack
async function enemyAttack() {
    const damage = 80 + Math.floor(Math.random() * 40);
    
    // Enemy attack animation
    enemySprite.style.animation = 'none';
    enemySprite.offsetHeight; // Trigger reflow
    enemySprite.style.animation = 'enemyAttack 0.5s ease-out';
    
    await sleep(300);
    
    // Flash and shake
    flashScreen(0.3, '#ff0000');
    battleArena.classList.add('screen-shake');
    
    // Hero takes damage
    gameState.heroHP = Math.max(0, gameState.heroHP - damage);
    heroSprite.style.filter = 'brightness(2)';
    
    // Show damage on hero
    showDamageNumber(damage, false, true);
    
    updateUI();
    
    await sleep(200);
    heroSprite.style.filter = '';
    battleArena.classList.remove('screen-shake');
    
    // Reset combo when enemy attacks
    gameState.combo = 0;
    updateUI();
    
    // Check for defeat
    if (gameState.heroHP <= 0) {
        showDefeat();
    }
}

// Show damage number
function showDamageNumber(damage, isCritical = false, isHeroHit = false) {
    const dmgNum = document.createElement('div');
    dmgNum.className = 'damage-number' + (isCritical ? ' critical' : '');
    dmgNum.textContent = damage.toLocaleString();
    
    if (isHeroHit) {
        dmgNum.style.left = '30%';
        dmgNum.style.top = '60%';
        dmgNum.style.color = '#ff6666';
    } else {
        // Random position near enemy
        dmgNum.style.left = (40 + Math.random() * 20) + '%';
        dmgNum.style.top = (20 + Math.random() * 15) + '%';
    }
    
    damageNumbers.appendChild(dmgNum);
    
    // Remove after animation
    setTimeout(() => dmgNum.remove(), 1000);
}

// Flash screen
function flashScreen(intensity, color = '#ffffff') {
    screenFlash.style.background = color;
    screenFlash.style.opacity = intensity;
    setTimeout(() => {
        screenFlash.style.opacity = 0;
    }, 100);
}

// Show hit effect on enemy
function showHitEffect() {
    const hitEffect = enemySprite.querySelector('#enemy-hit-effect') || document.createElement('div');
    hitEffect.id = 'enemy-hit-effect';
    hitEffect.style.cssText = `
        position: absolute;
        inset: -20px;
        background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, transparent 70%);
        opacity: 1;
        pointer-events: none;
        transition: opacity 0.2s;
    `;
    if (!enemySprite.contains(hitEffect)) {
        enemySprite.appendChild(hitEffect);
    }
    
    setTimeout(() => {
        hitEffect.style.opacity = 0;
    }, 100);
}

// Create impact particles
function createImpactParticles(type) {
    const colors = type === 'burst' ? ['#ffcc00', '#ff6600', '#ff0000'] : 
                   type === 'skill' ? ['#00ffff', '#0088ff', '#ffffff'] :
                   ['#ffffff', '#aaccff', '#88aaff'];
    
    const count = type === 'burst' ? 20 : type === 'skill' ? 12 : 6;
    
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        const color = colors[Math.floor(Math.random() * colors.length)];
        const size = type === 'burst' ? 8 + Math.random() * 8 : 4 + Math.random() * 6;
        const angle = (Math.PI * 2 / count) * i + Math.random() * 0.5;
        const distance = 50 + Math.random() * 100;
        const duration = 0.3 + Math.random() * 0.3;
        
        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            border-radius: 50%;
            left: 50%;
            top: 25%;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 ${size * 2}px ${color};
            pointer-events: none;
            z-index: 50;
        `;
        
        damageNumbers.appendChild(particle);
        
        // Animate outward
        requestAnimationFrame(() => {
            particle.style.transition = `all ${duration}s ease-out`;
            particle.style.transform = `translate(
                calc(-50% + ${Math.cos(angle) * distance}px), 
                calc(-50% + ${Math.sin(angle) * distance}px)
            ) scale(0)`;
            particle.style.opacity = 0;
        });
        
        setTimeout(() => particle.remove(), duration * 1000);
    }
}

// Create massive aura for brave burst
function createMassiveAura() {
    const aura = document.createElement('div');
    aura.style.cssText = `
        position: absolute;
        left: 50%;
        bottom: 15%;
        width: 300px;
        height: 300px;
        transform: translate(-50%, 50%);
        background: radial-gradient(circle, rgba(255,200,0,0.8) 0%, rgba(255,100,0,0.4) 40%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 5;
        animation: auraExpand 1s ease-out forwards;
    `;
    
    // Add keyframes if not exists
    if (!document.getElementById('aura-keyframes')) {
        const style = document.createElement('style');
        style.id = 'aura-keyframes';
        style.textContent = `
            @keyframes auraExpand {
                0% { transform: translate(-50%, 50%) scale(0.5); opacity: 1; }
                50% { transform: translate(-50%, 50%) scale(2); opacity: 0.8; }
                100% { transform: translate(-50%, 50%) scale(3); opacity: 0; }
            }
            @keyframes enemyAttack {
                0% { transform: translateY(0) scale(1); }
                30% { transform: translateY(50px) scale(1.1); }
                60% { transform: translateY(100px) scale(1.2); }
                100% { transform: translateY(0) scale(1); }
            }
        `;
        document.head.appendChild(style);
    }
    
    battleArena.appendChild(aura);
    setTimeout(() => aura.remove(), 1000);
    
    // Also add energy lines
    for (let i = 0; i < 8; i++) {
        const line = document.createElement('div');
        const angle = (360 / 8) * i;
        line.style.cssText = `
            position: absolute;
            left: 50%;
            bottom: 25%;
            width: 4px;
            height: 100px;
            background: linear-gradient(to top, rgba(255,200,0,1), transparent);
            transform-origin: bottom center;
            transform: translateX(-50%) rotate(${angle}deg);
            pointer-events: none;
            z-index: 6;
            animation: lineExpand 0.5s ease-out forwards;
        `;
        
        if (!document.getElementById('line-keyframes')) {
            const style = document.createElement('style');
            style.id = 'line-keyframes';
            style.textContent = `
                @keyframes lineExpand {
                    0% { height: 0; opacity: 1; }
                    50% { height: 200px; opacity: 1; }
                    100% { height: 300px; opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        battleArena.appendChild(line);
        setTimeout(() => line.remove(), 500);
    }
}

// Update UI
function updateUI() {
    // Health bars
    heroHealthFill.style.width = (gameState.heroHP / gameState.heroMaxHP * 100) + '%';
    enemyHealthFill.style.width = (gameState.enemyHP / gameState.enemyMaxHP * 100) + '%';
    enemyHealthText.textContent = `${gameState.enemyHP.toLocaleString()} / ${gameState.enemyMaxHP.toLocaleString()}`;
    
    // Brave burst bar
    braveBurstFill.style.width = (gameState.braveBurst / gameState.maxBraveBurst * 100) + '%';
    
    // Burst button glow when ready
    if (gameState.braveBurst >= gameState.maxBraveBurst) {
        burstBtn.classList.add('ready');
    } else {
        burstBtn.classList.remove('ready');
    }
    
    // Combo counter
    comboNumber.textContent = gameState.combo;
    comboNumber.classList.add('pop');
    setTimeout(() => comboNumber.classList.remove('pop'), 200);
}

// Show Victory
function showVictory() {
    resultTitle.textContent = 'VICTORY!';
    resultTitle.style.color = '#ffcc00';
    resultScreen.classList.add('show');
}

// Show Defeat
function showDefeat() {
    resultTitle.textContent = 'DEFEAT';
    resultTitle.style.color = '#ff4444';
    resultScreen.classList.add('show');
}

// Reset Game
function resetGame() {
    gameState.heroHP = gameState.heroMaxHP;
    gameState.enemyHP = gameState.enemyMaxHP;
    gameState.braveBurst = 0;
    gameState.combo = 0;
    gameState.isAnimating = false;
    resultScreen.classList.remove('show');
    updateUI();
}

// Utility: Sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Start the game
document.addEventListener('DOMContentLoaded', init);

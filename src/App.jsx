import React, { useState } from 'react';
import { GameProvider } from './context/GameContext.jsx';
import { useGameState } from './context/useGameState';
import { monsters } from './data/monsters';
import MonsterCard from './components/MonsterCard';
import MonsterTab from './components/MonsterTab';
import TopUI from './components/TopUI';
import './components/OriginalStyles.css';

// --- BOSS SCREEN ---
const BossScreen = () => {
  const { state, attackBoss, damagePopup, bossShake, isAttacking } = useGameState();
  const hpPercent = state.maxBossHp > 0 ? (state.bossHp / state.maxBossHp) * 100 : 0;

  // Timer Logic
  const [now, setNow] = React.useState(Date.now());
  React.useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);

  const formatTime = (ms) => {
    if (ms < 0) return "00:00:00";
    const h = Math.floor(ms / (1000 * 60 * 60));
    const m = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((ms % (1000 * 60)) / 1000);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  let timerText = "";
  let overlay = null;

  if (state.bossState === 'active') {
    timerText = `Event Ends In: ${formatTime(state.bossEndTime - now)}`;
  } else {
    timerText = `Respawn In: ${formatTime(state.bossRespawnTime - now)}`;
    overlay = (
      <div style={{
        position: 'absolute', inset: 0,
        background: 'rgba(0,0,0,0.7)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        zIndex: 50, color: '#fff'
      }}>
        <h1 style={{ fontSize: '40px', color: '#ff3333', textShadow: '0 0 10px #000' }}>BOSS DEFEATED</h1>
        <h2 style={{ fontSize: '24px', marginTop: '10px' }}>{timerText}</h2>
      </div>
    );
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
      {overlay}

      {/* MONSTER AREA */}
      <div style={{
        height: '70%',
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
        position: 'relative',
        paddingBottom: '0',
        paddingTop: '0',
        backgroundImage: 'url(/assets/electric_bg_final.png)',
        backgroundSize: '100% 100%',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        borderBottom: '2px solid #444'
      }}>
        {/* Floor Shadow */}
        <div style={{
          position: 'absolute', bottom: '15px', width: '80%', height: '40px',
          background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.6) 0%, transparent 70%)',
          zIndex: 1
        }}></div>

        <img
          src="/assets/electric_god_unit_clean.png"
          className={`boss-animation ${bossShake ? 'shake-effect' : ''}`}
          style={{
            width: 'auto',
            height: '92%',
            maxWidth: '95%',
            objectFit: 'contain',
            objectPosition: 'bottom center',
            marginBottom: '0px',
            zIndex: 2,
            filter: 'contrast(1.1)'
          }}
        />

        {/* FLOATING DAMAGE TEXT - PURE CSS CONTROL */}
        {/* FLOATING DAMAGE TEXT */}
        {damagePopup && (
          <div
            className={`damage-number ${damagePopup.isCrit ? 'crit' : (typeof damagePopup.val === 'string' && isNaN(parseFloat(damagePopup.val)) ? 'error' : 'normal')}`}
            key={damagePopup.id}
          >
            {typeof damagePopup.val === 'string' ? damagePopup.val : `-${damagePopup.val.toLocaleString()}`}
          </div>
        )}

      </div>

      {/* CONTROLS */}
      <div style={{
        flexShrink: 0,
        background: '#000',
        position: 'relative',
        zIndex: 10
      }}>

        {/* BOSS HP BAR - FULL WIDTH */}
        <div className="boss-bar-frame" style={{
          margin: '0',
          borderRadius: '0',
          height: '24px',
          width: '100%',
          borderLeft: 'none',
          borderRight: 'none'
        }}>
          <div className="boss-bar-fill" style={{ width: `${hpPercent}%` }}></div>
          <div style={{ position: 'absolute', left: '15px', top: 0, bottom: 0, display: 'flex', alignItems: 'center', fontWeight: 'bold', fontSize: '13px', color: '#fff', textShadow: '0 1px 2px #000', zIndex: 10 }}>HP</div>
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '15px', color: '#fff', textShadow: '0 1px 2px #000', zIndex: 5 }}>Thunder Emperor Zylos</div>
          <div style={{ position: 'absolute', right: '15px', top: 0, bottom: 0, display: 'flex', alignItems: 'center', fontWeight: 'bold', fontSize: '12px', color: '#ffd700', textShadow: '0 1px 2px #000', zIndex: 10, fontFamily: 'monospace' }}>{timerText}</div>
        </div>

        {/* 3-BUTTON ROW (Padded) */}
        <div style={{ padding: '0 10px 10px' }}>
          <div className="btn-row" style={{ padding: '10px 0 0' }}>
            <button className="btn normal" onClick={() => attackBoss(1000)} disabled={isAttacking || state.bossState !== 'active'} style={{ opacity: (isAttacking || state.bossState !== 'active') ? 0.7 : 1 }}>
              <span className="btn-title">ATTACK x1</span>
              <span className="btn-cost"><img className="btn-icon" src="/assets/icon_energy.svg" alt="Energy" /> 1 ENERGY</span>
            </button>
            <button className="btn united" onClick={() => attackBoss(5000)} disabled={isAttacking || state.bossState !== 'active'} style={{ opacity: (isAttacking || state.bossState !== 'active') ? 0.7 : 1 }}>
              <span className="btn-title">ATTACK x5</span>
              <span className="btn-cost"><img className="btn-icon" src="/assets/icon_energy.svg" alt="Energy" /> 5 ENERGY</span>
            </button>
            <button className="btn special" onClick={() => attackBoss(50000)} disabled={isAttacking || state.bossState !== 'active'} style={{ opacity: (isAttacking || state.bossState !== 'active') ? 0.7 : 1 }}>
              <span className="btn-title">ATTACK x50</span>
              <span className="btn-cost"><img className="btn-icon" src="/assets/icon_gem.svg" alt="Gems" /> 10 GEMS</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// ... Inventory same ...
const InventoryScreen = () => (
  <div style={{ padding: '15px' }}>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))', gap: '8px' }}>
      {monsters.map(m => <MonsterCard key={m.id} monster={m} onClick={() => { }} />)}
    </div>
  </div>
);

const GameLayout = () => {
  const [activeTab, setActiveTab] = useState('boss');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      <div style={{ flexShrink: 0 }}>
        <TopUI variant={activeTab === 'boss' ? 'boss' : 'menu'} />
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', background: 'transparent' }}>
        {activeTab === 'boss' && <BossScreen />}
        {activeTab === 'monsters' && <MonsterTab />}
      </div>
      <div style={{
        height: '60px',
        background: 'linear-gradient(180deg, #2d2d38 0%, #1a1a22 100%)',
        borderTop: '2px solid #3d3d48',
        display: 'flex', justifyContent: 'space-around', alignItems: 'center',
        paddingBottom: 'safe-area-inset-bottom',
        flexShrink: 0,
        position: 'relative', zIndex: 50
      }}>
        <NavButton label="HOME" image="/assets/icon_home.png" active={false} onClick={() => { }} />
        <NavButton label="BATTLE" image="/assets/icon_battle.png" active={activeTab === 'boss'} onClick={() => setActiveTab('boss')} />
        <NavButton label="UNIT" image="/assets/icon_monster.png" active={activeTab === 'monsters'} onClick={() => setActiveTab('monsters')} />
        <NavButton label="EQUIP" image="/assets/icon_equip.png" active={activeTab === 'fusion'} onClick={() => alert("Fusion Coming!")} />
        <NavButton label="SHOP" image="/assets/icon_shop.png" active={activeTab === 'shop'} onClick={() => setActiveTab('shop')} />
      </div>
    </div>
  );
};

const NavButton = ({ label, image, active, onClick }) => (
  <button onClick={onClick} style={{ background: 'none', border: 'none', color: active ? '#fff' : '#888', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px', cursor: 'pointer', flex: 1, opacity: active ? 1 : 0.6 }}>
    <img src={image} style={{ width: '28px', height: '28px', objectFit: 'contain', filter: active ? 'drop-shadow(0 0 5px white)' : 'grayscale(0.5)' }} />
    <span style={{ fontSize: '10px', fontWeight: 'bold', letterSpacing: '0.5px', marginTop: '2px' }}>{label}</span>
  </button>
);

export default function App() { return <GameProvider><GameLayout /></GameProvider>; }

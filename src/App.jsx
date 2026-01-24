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
  const { state, attackBoss, damagePopup, bossShake } = useGameState();
  const hpPercent = (state.bossHp / state.maxBossHp) * 100;

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>

      {/* MONSTER AREA */}
      <div style={{
        flex: 1,
        minHeight: 0,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
        position: 'relative',
        paddingBottom: '0',
        paddingTop: '30px'
      }}>
        {/* Floor Shadow */}
        <div style={{
          position: 'absolute', bottom: '20px', width: '80%', height: '40px',
          background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.6) 0%, transparent 70%)',
          zIndex: 1
        }}></div>

        <img
          src="/assets/fire_demon_final.png"
          className={`boss-animation ${bossShake ? 'shake-effect' : ''}`}
          style={{
            width: 'auto',
            height: '98%',
            maxWidth: '95%',
            objectFit: 'contain',
            objectPosition: 'bottom center',
            marginBottom: '0px',
            zIndex: 2,
            filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))'
          }}
        />

        {/* FLOATING DAMAGE TEXT - PURE CSS CONTROL */}
        {damagePopup && (() => {
          const isError = typeof damagePopup.val === 'string';
          const isCrit = !isError && damagePopup.isCrit;
          const baseColor = damagePopup.color || (isError ? '#ff4444' : (isCrit ? '#ff4400' : '#ffcc00'));
          const baseShadow = isError ? '0 1px 2px #000' : '0 0 10px #ff0000';
          const baseFontSize = isError ? '24px' : (isCrit ? '50px' : '40px');
          return (
            <div
              className={`damage-number ${isError ? 'error' : (isCrit ? 'crit' : 'normal')}`}
              key={damagePopup.id}
              style={{
                color: baseColor,
                textShadow: baseShadow,
                fontFamily: 'Cinzel, serif',
                fontWeight: 700,
                fontSize: baseFontSize
              }}
            >
              {isError ? damagePopup.val : `-${damagePopup.val}`}
            </div>
          );
        })()}

      </div>

      {/* CONTROLS */}
      <div style={{
        flexShrink: 0,
        background: 'linear-gradient(to top, #000 80%, transparent 100%)',
        padding: '0 10px 10px',
        position: 'relative',
        zIndex: 10
      }}>

        {/* BOSS HP BAR */}
        <div className="boss-bar-frame" style={{ margin: '0', borderRadius: '4px', height: '22px' }}>
          <div className="boss-bar-fill" style={{ width: `${hpPercent}%` }}></div>
          <div style={{ position: 'absolute', left: '10px', top: 0, bottom: 0, display: 'flex', alignItems: 'center', fontWeight: 'bold', fontSize: '14px', color: '#fff', textShadow: '0 1px 2px #000', zIndex: 10 }}>HP</div>
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '14px', color: '#fff', textShadow: '0 1px 2px #000', zIndex: 5 }}>Overlord</div>
        </div>

        {/* 3-BUTTON ROW */}
        <div className="btn-row" style={{ padding: '10px 0 0' }}>
          <button className="btn normal" onClick={() => attackBoss(1000)}>
            <span className="btn-title">ATTACK x1</span>
            <span className="btn-cost">⚡ 1 STAMINA</span>
          </button>
          <button className="btn united" onClick={() => attackBoss(5000)}>
            <span className="btn-title">ATTACK x5</span>
            <span className="btn-cost">⚡ 5 STAMINA</span>
          </button>
          <button className="btn special" onClick={() => attackBoss(50000)}>
            <span className="btn-title">ATTACK x50</span>
            <span className="btn-cost">💎 10 GEMS</span>
          </button>
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
        <NavButton label="MONSTER" image="/assets/icon_monster.png" active={activeTab === 'monsters'} onClick={() => setActiveTab('monsters')} />
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

import React, { useState, useMemo } from 'react';
import { GameProvider } from './context/GameContext.jsx';
import { useGameState } from './context/useGameState';
import { monsters } from './data/monsters';
import MonsterCard from './components/MonsterCard';
import MonsterTab from './components/MonsterTab';
import QuestScreen from './components/QuestScreen';
import TopUI from './components/TopUI';
import SkillModal from './components/SkillModal';
import BattleMenu from './components/BattleMenu';
import './components/OriginalStyles.css';

import BossSelection from './components/BossSelection';
import BossBattle from './components/BossBattle';
// ... previous imports ...

// REMOVED INLINE BossScreen code ...

const GameLayout = () => {
  const [activeTab, setActiveTab] = useState('boss');
  const [battleMode, setBattleMode] = useState('menu'); // menu, boss-selection, boss-battle, quest
  const [targetBoss, setTargetBoss] = useState('world');
  const { state, skillModalOpen, setSkillModalOpen, dismissLevelUp } = useGameState();

  const handleBattleSelect = (id) => {
    if (id === 'world-boss') setBattleMode('boss-selection');
    if (id === 'quest') setBattleMode('quest');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {state.showLevelUp && (
        <div className="level-up-splash" onClick={dismissLevelUp}>
          <div className="splash-content">
            <h1 className="splash-title">LEVEL UP!</h1>
            <h2 className="splash-subtitle">RANK {state.level} REACHED</h2>
            <div style={{ color: '#aaa', fontSize: '12px', marginTop: '20px' }}>TAP TO CONTINUE</div>
          </div>
        </div>
      )}
      <SkillModal isOpen={skillModalOpen} onClose={() => setSkillModalOpen(false)} />
      <div style={{ flexShrink: 0 }}>
        <TopUI variant={(activeTab === 'boss' && battleMode === 'boss-battle') ? 'boss' : 'menu'} />
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', background: 'transparent' }}>
        {activeTab === 'boss' && (
          battleMode === 'menu' ? (
            <BattleMenu onSelect={handleBattleSelect} />
          ) : battleMode === 'boss-selection' ? (
            <BossSelection
              onBack={() => setBattleMode('menu')}
              onSelectBoss={(type) => {
                setTargetBoss(type);
                setBattleMode('boss-battle');
              }}
            />
          ) : battleMode === 'boss-battle' ? (
            <BossBattle
              bossType={targetBoss}
              onBack={() => setBattleMode('boss-selection')}
            />
          ) : battleMode === 'quest' ? (
            <QuestScreen onBack={() => setBattleMode('menu')} />
          ) : null
        )}
        {activeTab === 'monsters' && <MonsterTab />}
        {activeTab === 'shop' && (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#888' }}>
            SHOP COMING SOON
          </div>
        )}
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
        <NavButton label="BATTLE" image="/assets/icon_battle.png" active={activeTab === 'boss'} onClick={() => { setActiveTab('boss'); setBattleMode('menu'); }} />
        <NavButton label="UNIT" image="/assets/icon_monster.png" active={activeTab === 'monsters'} onClick={() => setActiveTab('monsters')} />
        <NavButton label="FUSION" image="/assets/icon_equip.png" active={activeTab === 'fusion'} onClick={() => alert("Fusion Coming!")} />
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

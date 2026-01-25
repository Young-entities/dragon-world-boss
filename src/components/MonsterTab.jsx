import React, { useMemo, useRef, useState } from 'react';
import { useGameState } from '../context/useGameState';
import { monsters as baseMonsters } from '../data/monsters';
import './MonsterTab.css';

const tierOrder = [
  { key: 'Primordial', tierClass: 'tier-13', color: '#ffd700', rankValue: 13 },
  { key: 'Eternal', tierClass: 'tier-12', color: '#ffffff', rankValue: 12 },
  { key: 'Chaos', tierClass: 'tier-11', color: '#990000', rankValue: 11 },
  { key: 'Deity', tierClass: 'tier-10', color: '#ff00ff', rankValue: 10 },
  { key: 'God', tierClass: 'tier-9', color: '#ff4400', rankValue: 9 },
  { key: 'Demi God', tierClass: 'tier-8', color: '#ffaa00', rankValue: 8 },
  { key: 'Titan', tierClass: 'tier-7', color: '#00ffff', rankValue: 7 },
  { key: 'Mythic', tierClass: 'tier-6', color: '#ff0000', rankValue: 6 },
  { key: 'Myth', tierClass: 'tier-5', color: '#ff8800', rankValue: 5 },
  { key: 'Legendary', tierClass: 'tier-4', color: '#ffff00', rankValue: 4 },
  { key: 'Epic', tierClass: 'tier-3', color: '#aa00ff', rankValue: 3 },
  { key: 'Rare', tierClass: 'tier-2', color: '#44ff44', rankValue: 2 },
  { key: 'Minion', tierClass: 'tier-1', color: '#888888', rankValue: 1 }
];

const fusionMonsters = [
  {
    name: 'Inferno Dragon Knight Kael',
    tier: 'Demi God',
    icon: '/assets/overlord_portrait_v2_clean.png',
    full: '/assets/overlord_absolute_final.png',
    color: '#ffaa00',
    rankValue: 8,
    aura: '#ff3300'
  },
  {
    name: 'Abyssal Sea Deity',
    tier: 'Deity',
    icon: '/assets/water_deity_unit_final.png',
    full: '/assets/water_deity_unit_final.png',
    color: '#ff00ff',
    rankValue: 10,
    aura: '#00ccff'
  }
];

const fusionRecipes = {};

const getFusionCost = (rank, type) => {
  if (type === 'money') return 1000000 * rank;
  if (type === 'gem') return 100 * rank;
  return 0;
};

const rollFusionSuccess = (chance) => Math.random() <= chance;

const getTierColor = (tier) => {
  const match = tierOrder.find((t) => t.key === tier);
  return match?.color || '#ffffff';
};

const formatTierClass = (tier) => tier.toLowerCase().replace(/\s+/g, '-');
const formatElementClass = (element) => (element || 'neutral').toLowerCase().replace(/\s+/g, '-');

const pickFallbackMonster = (monsters, seed) => {
  if (!monsters.length) return null;
  let hash = 0;
  for (let index = 0; index < seed.length; index += 1) {
    hash = (hash * 31 + seed.charCodeAt(index)) | 0;
  }
  const safeIndex = Math.abs(hash) % monsters.length;
  return monsters[safeIndex];
};


const MonsterTab = () => {
  const { state, applyResourceDelta, updateMonsterCollection } = useGameState();
  const [subTab, setSubTab] = useState('fusions');
  const [expandedTiers, setExpandedTiers] = useState({ God: false, 'Demi God': false, Chaos: false, Deity: false });
  const [selectedMonster, setSelectedMonster] = useState(null);
  const monsterInventory = useMemo(() => ({
    'Inferno Dragon Knight Kael': 2,
    'Abyssal Sea Deity': 1,
    ...(state.monsterCollection || {})
  }), [state.monsterCollection]);
  const [fusionSlots, setFusionSlots] = useState({ slot1: null, slot2: null });
  const [fusionModal, setFusionModal] = useState(null);
  const [fusionAnim, setFusionAnim] = useState({
    open: false,
    phase: null,
    ingredient: null,
    result: null,
    success: true
  });
  const animTimeouts = useRef([]);


  const sortedMonsters = useMemo(() => {
    return [...baseMonsters].sort((a, b) => {
      const valA = tierOrder.find((t) => t.key === a.rank)?.rankValue || 0;
      const valB = tierOrder.find((t) => t.key === b.rank)?.rankValue || 0;
      return valB - valA;
    });
  }, []);

  const tierCounts = useMemo(() => {
    const counts = Object.fromEntries(tierOrder.map(t => [t.key, 0]));
    fusionMonsters.forEach((monster) => {
      const qty = monsterInventory[monster.name] || 0;
      if (counts[monster.tier] !== undefined) {
        counts[monster.tier] += qty;
      }
    });
    return counts;
  }, [monsterInventory]);

  const clearFusionSlot = (slot) => {
    setFusionSlots((prev) => ({
      ...prev,
      [slot]: null
    }));
  };

  const clearAllSlots = () => {
    setFusionSlots({ slot1: null, slot2: null });
  };

  const addToFusionSlot = (monster) => {
    const currentQty = monsterInventory[monster.name] || 0;
    const inSlots = [fusionSlots.slot1, fusionSlots.slot2].filter((s) => s?.name === monster.name).length;

    if (currentQty === 0 || inSlots >= currentQty) {
      window.alert(`You only have ${currentQty} ${monster.name} unit(s)!`);
      return;
    }

    setFusionSlots((prev) => {
      if (!prev.slot1) return { ...prev, slot1: monster };
      if (!prev.slot2) return { ...prev, slot2: monster };

      return { slot1: monster, slot2: null };
    });
  };

  const openFusionModal = (type) => {
    if (!fusionSlots.slot1 || !fusionSlots.slot2) {
      window.alert('You need 2 units to fuse!');
      return;
    }

    if (fusionSlots.slot1.name !== fusionSlots.slot2.name) {
      window.alert('You must fuse 2 of the SAME unit!');
      return;
    }

    const rank = fusionSlots.slot1.rankValue || 1;
    const cost = getFusionCost(rank, type);
    const chance = '40%';

    setFusionModal({ type, cost, chance });
  };

  const closeFusionModal = () => setFusionModal(null);

  const executeFusion = () => {
    if (!fusionModal) return;

    const { type, cost } = fusionModal;
    closeFusionModal();

    if (!fusionSlots.slot1 || !fusionSlots.slot2) return;

    const name1 = fusionSlots.slot1.name;
    const name2 = fusionSlots.slot2.name;

    if (name1 !== name2) {
      window.alert('You must fuse 2 of the SAME unit!');
      return;
    }

    const qty = monsterInventory[name1] || 0;
    if (qty < 2) {
      window.alert(`You don't have enough ${name1}s! (Need 2, Have ${qty})`);
      return;
    }

    const resultName = fusionRecipes[name1];
    if (!resultName) {
      window.alert(`${name1} cannot be fused further (No recipe found)!`);
      return;
    }

    const hasFunds = type === 'money' ? state.money >= cost : state.gems >= cost;
    if (!hasFunds) {
      window.alert(`Not enough ${type === 'money' ? 'Money' : 'Gems'}! Need ${cost.toLocaleString()}`);
      return;
    }

    applyResourceDelta(type === 'money' ? { money: -cost } : { gems: -cost });

    const chance = 0.4;
    if (!rollFusionSuccess(chance)) {
      const fallbackTier = fusionSlots.slot1.tier;
      const sameTierMonsters = fusionMonsters.filter((monster) => monster.tier === fallbackTier);
      const fallbackMonster = pickFallbackMonster(sameTierMonsters, name1);

      if (!fallbackMonster) {
        window.alert('No fallback unit found for this tier.');
        return;
      }

      const currentQty = monsterInventory[name1] || 0;
      const nextName1 = Math.max(0, currentQty - 2);

      if (fallbackMonster.name === name1) {
        updateMonsterCollection({
          [name1]: Math.max(0, nextName1 + 1)
        });
      } else {
        updateMonsterCollection({
          [name1]: nextName1,
          [fallbackMonster.name]: (monsterInventory[fallbackMonster.name] || 0) + 1
        });
      }

      startFusionAnimation(name1, fallbackMonster.name, false);
      return;
    }

    const currentQty = monsterInventory[name1] || 0;
    const nextName1 = Math.max(0, currentQty - 2);
    const nextResult = (monsterInventory[resultName] || 0) + 1;

    updateMonsterCollection({
      [name1]: nextName1,
      [resultName]: nextResult
    });

    startFusionAnimation(name1, resultName, true);
  };

  const startFusionAnimation = (ingredientName, resultName, success) => {
    animTimeouts.current.forEach((t) => clearTimeout(t));
    animTimeouts.current = [];

    setFusionAnim({ open: true, phase: 1, ingredient: ingredientName, result: resultName, success });

    animTimeouts.current.push(setTimeout(() => setFusionAnim((prev) => ({ ...prev, phase: 2 })), 1000));
    animTimeouts.current.push(setTimeout(() => setFusionAnim((prev) => ({ ...prev, phase: 3 })), 2500));
    animTimeouts.current.push(setTimeout(() => setFusionAnim((prev) => ({ ...prev, phase: 4 })), 4000));
    animTimeouts.current.push(setTimeout(() => setFusionAnim((prev) => ({ ...prev, phase: 5 })), 5000));
  };

  const closeFusionOverlay = () => {
    setFusionAnim({ open: false, phase: null, ingredient: null, result: null, success: true });
    clearAllSlots();
  };

  const ingredientMonster = fusionMonsters.find((m) => m.name === fusionAnim.ingredient) || fusionSlots.slot1;
  const resultMonster = fusionMonsters.find((m) => m.name === fusionAnim.result) || ingredientMonster;

  const getSlotStyle = (slot) => {
    if (!slot) return undefined;
    return {
      border: 'none',
      background: 'transparent',
      boxShadow: `0 0 15px ${slot.aura || slot.color}`
    };
  };

  return (
    <div className="monster-tab-wrapper">
      <div className="sub-nav-tabs">
        <button className={`sub-tab ${subTab === 'monster' ? 'active' : ''}`} onClick={() => setSubTab('monster')}>Unit</button>
        <button className={`sub-tab ${subTab === 'fusions' ? 'active' : ''}`} onClick={() => setSubTab('fusions')}>Fusion</button>
        <button className={`sub-tab ${subTab === 'pets' ? 'active' : ''}`} onClick={() => setSubTab('pets')}>Pets</button>
        <button className={`sub-tab ${subTab === 'collections' ? 'active' : ''}`} onClick={() => setSubTab('collections')}>Collection</button>
      </div>

      {subTab === 'monster' && (
        <div className="mon-tab-content active">
          {sortedMonsters.map((monster) => (
            <div key={monster.id} className="mon-row" onClick={() => setSelectedMonster(monster)}>
              <div className={`mon-icon-frame tier-${formatTierClass(monster.rank)} element-${formatElementClass(monster.element)}`}>
                <span className="frame-inner" />
                <span className="frame-ornament o1" />
                <span className="frame-ornament o2" />
                <span className="frame-ornament o3" />
                <span className="frame-ornament o4" />
                <span className="frame-rivet r1" />
                <span className="frame-rivet r2" />
                <span className="frame-rivet r3" />
                <span className="frame-rivet r4" />
                <img src={`${monster.image}?v=21`} alt={monster.name} />
              </div>
              <div className="mon-info">
                <div className="mon-name" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <img
                    src={monster.element === 'Fire' ? '/assets/element_fire_v4.png?v=4' : (monster.element === 'Water' ? '/assets/element_water.png?v=12' : `/assets/element_${(monster.element || 'neutral').toLowerCase()}.png`)}
                    alt={monster.element}
                    style={{ width: '18px', height: '18px', objectFit: 'contain' }}
                  />
                  {monster.name}
                </div>
                <div className="mon-stats" style={{ color: getTierColor(monster.rank) }}>Tier: {monster.rank}</div>
                <div className="mon-stats">
                  <span className="stat-attack">ATK {monster.stats.atk.toLocaleString()}</span>
                  <span className="stat-divider"> • </span>
                  <span className="stat-defense">DEF {monster.stats.def.toLocaleString()}</span>
                  <span className="stat-divider"> • </span>
                  <span className="stat-hp">HP {monster.stats.hp.toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {subTab === 'fusions' && (
        <div className="mon-tab-content active fusion-tab">
          <div className="fusion-deck unique-style">
            <div className="fusion-deck-left">
              <div className="fusion-chamber">
                <div className="fusion-slot-wrapper">
                  <div
                    className={`fusion-slot ${fusionSlots.slot1 ? 'filled' : ''}`}
                    style={getSlotStyle(fusionSlots.slot1)}
                    onClick={() => clearFusionSlot('slot1')}
                  >
                    {fusionSlots.slot1 ? (
                      <img src={fusionSlots.slot1.icon} alt={fusionSlots.slot1.name} />
                    ) : (
                      <img src="/assets/fusion_vortex.png" className="vortex-bg" />
                    )}
                  </div>
                  {fusionSlots.slot1 && (
                    <div className="fusion-slot-name" style={{ color: getTierColor(fusionSlots.slot1.tier) }}>
                      {fusionSlots.slot1.name}
                    </div>
                  )}
                </div>

                <div className="fusion-plus">
                  <div className="atom-container">
                    <div className="atom-nucleus">
                      <div className="proton p1" />
                      <div className="proton p2" />
                      <div className="proton p3" />
                      <div className="proton p4" />
                    </div>
                    <div className="atom-ring ring-1" />
                    <div className="atom-ring ring-2" />
                    <div className="atom-ring ring-3" />
                  </div>
                </div>

                <div className="fusion-slot-wrapper">
                  <div
                    className={`fusion-slot ${fusionSlots.slot2 ? 'filled' : ''}`}
                    style={getSlotStyle(fusionSlots.slot2)}
                    onClick={() => clearFusionSlot('slot2')}
                  >
                    {fusionSlots.slot2 ? (
                      <img src={fusionSlots.slot2.icon} alt={fusionSlots.slot2.name} />
                    ) : (
                      <img src="/assets/fusion_vortex.png" className="vortex-bg" />
                    )}
                  </div>
                  {fusionSlots.slot2 && (
                    <div className="fusion-slot-name" style={{ color: getTierColor(fusionSlots.slot2.tier) }}>
                      {fusionSlots.slot2.name}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="fusion-actions">
              <button className="btn-fuse" onClick={() => openFusionModal('money')}>FUSE</button>
              <button className="btn-fuse mass" onClick={() => openFusionModal('gem')}>INSTANT<br />FUSE</button>
            </div>
          </div>

          <div className="rank-list-unique">
            {tierOrder.map((tier) => {
              const isExpandable = tier.key === 'God' || tier.key === 'Demi God' || tier.key === 'Chaos' || tier.key === 'Deity';
              const isExpanded = expandedTiers[tier.key] || false;

              return (
                <div key={tier.key}>
                  <div
                    className={`rank-card ${tier.tierClass}`}
                    onClick={() => {
                      if (!isExpandable) return;
                      setExpandedTiers((prev) => ({ ...prev, [tier.key]: !prev[tier.key] }));
                    }}
                    style={{ cursor: isExpandable ? 'pointer' : 'default' }}
                  >
                    {tier.key}
                    <span className="count">{tierCounts[tier.key] || 0}</span>
                  </div>

                  {isExpandable && isExpanded && (
                    <div className="rank-monsters" style={{ borderLeftColor: tier.color }}>
                      {fusionMonsters.filter((m) => m.tier === tier.key).map((monster) => (
                        <div
                          key={monster.name}
                          className="monster-item"
                          onClick={() => addToFusionSlot(monster)}
                        >
                          <div className="mob-icon-square">
                            <img src={monster.icon} alt={monster.name} />
                          </div>
                          <div className="inv-qty">x{monsterInventory[monster.name] || 0}</div>
                          <div className="monster-name" style={{ color: getTierColor(monster.tier) }}>{monster.name}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {subTab === 'pets' && (
        <div className="mon-tab-content active">
          <div className="tab-placeholder">Pets Coming Soon</div>
        </div>
      )}

      {subTab === 'collections' && (
        <div className="mon-tab-content active">
          <div className="mon-grid">
            {Array.from({ length: 12 }).map((_, idx) => (
              <div key={`slot-${idx}`} className="mon-grid-item">?</div>
            ))}
          </div>
        </div>
      )}

      {fusionModal && (
        <div className="fusion-modal">
          <div className="fusion-modal-content">
            <div className="fusion-modal-header">FUSION CHAMBER</div>
            <div className="fusion-modal-body">
              <div className="fusion-modal-info">Units will be combined.</div>
              <div className="fusion-modal-ingredients">
                <div className="fusion-modal-slot">
                  <div className="fusion-modal-slot-img" dangerouslySetInnerHTML={{ __html: fusionSlots.slot1 ? `<img src='${fusionSlots.slot1.icon}' />` : '' }} />
                  <div className="fusion-modal-qty">1</div>
                </div>
                <div className="fusion-modal-plus">+</div>
                <div className="fusion-modal-slot">
                  <div className="fusion-modal-slot-img" dangerouslySetInnerHTML={{ __html: fusionSlots.slot2 ? `<img src='${fusionSlots.slot2.icon}' />` : '' }} />
                  <div className="fusion-modal-qty">1</div>
                </div>
              </div>
              <div className="fusion-modal-arrow">▼</div>
              <div className="fusion-modal-result">
                <div className="fusion-modal-result-ring" />
                <span>?</span>
              </div>
              <div className="fusion-info">
                <div className="fusion-info-row"><span>Success Rate:</span><span className="fusion-info-value">{fusionModal.chance}</span></div>
                <div className="fusion-info-row"><span>Fusion Cost:</span><span className="fusion-info-cost">{fusionModal.cost.toLocaleString()} {fusionModal.type === 'money' ? 'Gold' : 'Gems'}</span></div>
              </div>
              <div className="fusion-modal-actions">
                <button className="fusion-cancel" onClick={closeFusionModal}>CANCEL</button>
                <button className="fusion-confirm" onClick={executeFusion}>COMBINE</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {fusionAnim.open && (
        <div className={`fusion-anim-overlay ${fusionAnim.phase ? `fusion-phase-${fusionAnim.phase}` : ''}`}>
          <div id="anim-bg" />
          <div id="energy-particles">
            <div className="particle p1" />
            <div className="particle p2" />
            <div className="particle p3" />
            <div className="particle p4" />
            <div className="particle p5" />
            <div className="particle p6" />
          </div>
          <div id="fusion-orb" />
          <div id="light-rays">
            <div />
            <div />
            <div />
            <div />
          </div>
          <img id="anim-left" src={ingredientMonster?.full || ingredientMonster?.icon || ''} alt="" />
          <img id="anim-right" src={ingredientMonster?.full || ingredientMonster?.icon || ''} alt="" />
          <div id="anim-flash" />
          <div id="anim-result-container">
            <div id="success-text">
              {fusionAnim.success ? '✨ FUSION SUCCESS ✨' : '❌ FUSION FAILED ❌'}
            </div>
            <div id="result-glow">
              <div className="result-glow-ring" />
              <img id="anim-result" src={resultMonster?.full || resultMonster?.icon || ''} alt="" />
            </div>
            <button className="fusion-continue" onClick={closeFusionOverlay}>CONTINUE</button>
          </div>
        </div>
      )}

      {selectedMonster && (
        <div className="monster-detail-overlay" onClick={() => setSelectedMonster(null)}>
          <div className="monster-detail-card" onClick={(event) => event.stopPropagation()}>
            <div className="monster-detail-header" style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '6px 0 2px 0', background: 'rgba(0,0,0,0.5)', borderBottom: '1px solid #333' }}>
              <div className="monster-detail-name" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <img
                  src={selectedMonster.element === 'Fire' ? '/assets/element_fire_v4.png?v=4' : (selectedMonster.element === 'Water' ? '/assets/element_water.png?v=12' : `/assets/element_${(selectedMonster.element || 'neutral').toLowerCase()}.png`)}
                  alt={selectedMonster.element}
                  style={{ width: '20px', height: '20px', objectFit: 'contain' }}
                />
                <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>{selectedMonster.name}</span>
              </div>
              <div style={{
                color: getTierColor(selectedMonster.rank),
                fontWeight: 'normal',
                fontSize: '0.95rem',
                marginTop: '1px'
              }}>
                {selectedMonster.rank}
              </div>
              <button className="monster-detail-close" onClick={() => setSelectedMonster(null)} style={{ position: 'absolute', right: '15px', top: '15px' }}>✕</button>
            </div>
            <div className="monster-detail-body">
              <div className="monster-detail-image" style={{
                backgroundImage: `url(${(selectedMonster.cardBackground || '/assets/bg_final_no_mercy.png')}?v=22)`,
                backgroundSize: '100% 100%',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'center',
                paddingBottom: '20px',
                minHeight: '260px',
                borderRadius: '8px',
                border: '1px solid #444',
                position: 'relative'
              }}>
                <img
                  src={`${selectedMonster.fullImage || selectedMonster.image}?v=22`}
                  alt={selectedMonster.name}
                  style={{
                    maxHeight: '90%',
                    maxWidth: '90%',
                    objectFit: 'contain',
                    filter: 'drop-shadow(0 0 15px rgba(255,100,0,0.4))'
                  }}
                />
              </div>
              <div className="monster-detail-stats">

                {selectedMonster.leaderSkill && (
                  <div className="monster-detail-leader-skill" style={{
                    textAlign: 'center',
                    marginBottom: '4px',
                    padding: '0'
                  }}>
                    <span style={{ color: '#ffd700', fontWeight: 'bold', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '1px', display: 'block', marginBottom: '0' }}>
                      Leader Skill
                    </span>
                    <span style={{ color: '#fff', fontSize: '13px', fontStyle: 'italic' }}>
                      {selectedMonster.leaderSkill}
                    </span>
                  </div>
                )}

                <div className="monster-detail-stat-line" style={{ margin: '8px -16px' }}>
                  <span className="stat-attack">ATK {selectedMonster.stats.atk.toLocaleString()}</span>
                  <span className="stat-divider"> • </span>
                  <span className="stat-defense">DEF {selectedMonster.stats.def.toLocaleString()}</span>
                  <span className="stat-divider"> • </span>
                  <span className="stat-hp">HP {selectedMonster.stats.hp.toLocaleString()}</span>
                </div>
                <div className="monster-detail-desc" style={{ marginTop: '4px' }}>{selectedMonster.description}</div>
              </div>
            </div>
          </div>
        </div>
      )
      }
    </div >
  );
};

export default MonsterTab;

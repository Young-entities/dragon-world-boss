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
    color: '#ffaa00',
    rankValue: 8,
    aura: '#ff3300',
    stats: { atk: '52,488', def: '39,366' }
  },
  {
    name: 'Tidal Goddess Elara',
    tier: 'God',
    icon: '/assets/water_god_icon.png',
    full: '/assets/water_god_unit_clean.png',
    color: '#ff4400',
    rankValue: 9,
    aura: '#00ccff',
    stats: { atk: '104,976', def: '177,147' }
  },
  {
    name: 'Abyssal Queen Nereid',
    tier: 'Deity',
    icon: '/assets/water_deity_unit_final.png',
    full: '/assets/water_deity_unit_final.png',
    color: '#ff00ff',
    rankValue: 10,
    aura: '#00ccff',
    stats: { atk: '314,928', def: '531,441' }
  },
  {
    name: 'Dark Deity Azaerth', /* Renamed */
    tier: 'Primordial',
    icon: '/assets/dark_deity_icon.png',
    full: '/assets/dark_deity_unit.png',
    color: '#ff00ff',
    rankValue: 13,
    aura: '#aa00ff',
    stats: { atk: '669,222', def: '255,879' } /* Base Dark * 3^9 */
  }
];

const fusionRecipes = {
  'Tidal Goddess Elara': 'Abyssal Queen Nereid',
  'Abyssal Queen Nereid': 'Dark Deity Azaerth'
};

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
  const { state, applyResourceDelta, updateMonsterCollection, appointLeader } = useGameState();
  const [subTab, setSubTab] = useState('monster');
  const [expandedTiers, setExpandedTiers] = useState({ God: false, 'Demi God': false, Chaos: false, Deity: false });
  const [selectedMonster, setSelectedMonster] = useState(null);
  const [sellModalData, setSellModalData] = useState(null);
  const [sellAmount, setSellAmount] = useState(1);
  const [selectedElement, setSelectedElement] = useState('Fire');
  const activeLeader = useMemo(() => baseMonsters.find(m => m.name === state.leader), [state.leader]);
  const elements = ['Fire', 'Water', 'Electric', 'Earth', 'Void', 'Celestial'];

  const getElementIcon = (el) => {
    const lower = (el || 'neutral').toLowerCase();
    if (lower === 'void') return 'dark';
    if (lower === 'celestial') return 'holy';
    return lower;
  };

  const monsterInventory = useMemo(() => ({
    ...(state.monsterCollection || {}),
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
    const targetElement = selectedElement;

    return baseMonsters
      .filter(m => m.element === targetElement && (monsterInventory[m.name] || 0) > 0)
      .sort((a, b) => {
        const valA = tierOrder.find((t) => t.key === a.rank)?.rankValue || 0;
        const valB = tierOrder.find((t) => t.key === b.rank)?.rankValue || 0;
        return valB - valA;
      });
  }, [selectedElement]);

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

    // Check Tier Compatibility
    if (fusionSlots.slot1 && !fusionSlots.slot2) {
      if (fusionSlots.slot1.tier !== monster.tier) {
        window.alert('You can only fuse units of the same Tier!');
        return;
      }
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
    const chance = type === 'gem' ? '100%' : '40%';

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

    const chance = type === 'gem' ? 1.0 : 0.4;
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
    animTimeouts.current.push(setTimeout(() => setFusionAnim((prev) => ({ ...prev, phase: 6 })), 9000)); /* Auto Pop-up Stats */
  };

  const closeFusionOverlay = () => {
    if (fusionAnim.phase === 5) {
      setFusionAnim((prev) => ({ ...prev, phase: 6 }));
      return;
    }
    setFusionAnim({ open: false, phase: null, ingredient: null, result: null, success: true });
    clearAllSlots();
  };

  const ingredientMonster = fusionMonsters.find((m) => m.name === fusionAnim.ingredient) || fusionSlots.slot1;
  const resultMonster = fusionMonsters.find((m) => m.name === fusionAnim.result) || ingredientMonster;
  const phase6Monster = useMemo(() => baseMonsters.find(m => m.name === resultMonster?.name) || resultMonster, [resultMonster]);

  const getSlotStyle = (slot) => {
    if (!slot) return undefined;
    return {
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
        <>
          <div className="element-tabs">
            {elements.map(el => (
              <div
                key={el}
                className={`element-tab ${el.toLowerCase()} ${selectedElement === el ? 'active' : ''}`}
                onClick={() => setSelectedElement(el)}
              >
                {el}
              </div>
            ))}
          </div>
          <div className="element-header">
            <div className="element-header-text">{selectedElement} Unit</div>
            {activeLeader?.leaderSkill && (
              <div className="active-leader-skill-hud">
                <span className="skill-tag">LEADER</span>
                <span className="skill-desc">{activeLeader.leaderSkill}</span>
              </div>
            )}
            <div style={{ width: '80px' }} />
          </div>
          <div className="mon-tab-content active">
            {sortedMonsters.length > 0 ? sortedMonsters.map((monster) => {
              const qty = monsterInventory[monster.name] || 0;
              const rankItem = tierOrder.find(t => t.key === monster.rank) || { rankValue: 1 };
              const rv = rankItem.rankValue;

              /* getElementIcon moved to top-level */

              // Dynamic Values
              const sellPrice = Math.pow(rv, 4) * 1000000; // Primordial (rv=13) -> ~28B? Maybe too high? rv=8 -> 4B.
              const dissAmount = rv * 5;

              return (
                <div key={monster.id} className="mon-row" onClick={() => setSelectedMonster(monster)}>
                  <div className="mon-icon-box">
                    <img src={monster.icon || monster.image} alt={monster.name} style={{ width: '100%', height: '100%', borderRadius: '8px', objectFit: 'cover' }} />
                  </div>

                  <div className="mon-info">
                    <div className="mon-name">
                      <img
                        src={`/assets/element_${getElementIcon(monster.element)}_circle.png?v=129`}
                        alt={monster.element}
                        className={`mon-element-icon-mini el-${getElementIcon(monster.element)}`}
                        style={{ marginRight: '6px' }}
                      />
                      {monster.name}
                    </div>

                    <div className="mon-tier-label" style={{ color: getTierColor(monster.rank), fontSize: '11px', fontWeight: 'bold' }}>
                      {monster.rank} {state.leader === monster.name && '[LEADER]'}
                    </div>

                    <div className="mon-stats-row">
                      <span className="stat-atk"><span className="stat-label">ATK</span> {monster.stats.atk.toLocaleString()}</span>
                      <span className="stat-def"><span className="stat-label">DEF</span> {monster.stats.def.toLocaleString()}</span>
                      <span className="stat-hp"><span className="stat-label">HP</span> {monster.stats.hp.toLocaleString()}</span>
                    </div>

                    {monster.leaderSkill && (
                      <div className={`mon-leader-skill ${state.leader === monster.name ? 'active' : ''}`}>
                        <span className="skill-label">LEADER SKILL:</span> <span className="skill-desc">{monster.leaderSkill}</span>
                      </div>
                    )}
                  </div>

                  <div className="mon-act" onClick={e => e.stopPropagation()}>
                    <div className="mon-owned-corner">
                      <div className="mon-owned-label">OWNED</div>
                      <div className="mon-owned-val">x{qty}</div>
                    </div>

                    <div className="mon-act-buttons">
                      <button
                        className={`btn-act btn-leader ${state.leader === monster.name ? 'active' : ''}`}
                        disabled={qty <= 0 || state.leader === monster.name}
                        onClick={() => appointLeader(monster.name)}
                      >
                        {state.leader === monster.name ? 'ACTIVE' : (
                          <>
                            <span className="btn-sub-text">SET AS</span>
                            <span className="btn-main-text">LEADER</span>
                          </>
                        )}
                      </button>
                      <button
                        className="btn-act btn-sell"
                        disabled={qty <= 0}
                        onClick={() => {
                          setSellAmount(1);
                          setSellModalData({ monster, qty, sellPrice });
                        }}
                      >
                        SELL
                      </button>
                    </div>
                  </div>
                </div>
              );
            }) : (
              <div className="tab-placeholder">No {selectedElement} units in inventory.</div>
            )}
          </div>
        </>
      )}

      {sellModalData && (
        <div className="monster-detail-overlay sell-modal-overlay" onClick={() => setSellModalData(null)}>
          <div className="monster-detail-card sell-modal-card" onClick={e => e.stopPropagation()}>
            <div className="monster-detail-header">
              <div className="monster-detail-name">SELL {sellModalData.monster.name}</div>
              <button className="monster-detail-close" onClick={() => setSellModalData(null)}>✕</button>
            </div>
            <div className="sell-modal-body">
              <div className="sell-preview-unit">
                <div className={`mon-icon-frame tier-${formatTierClass(sellModalData.monster.rank)}`}>
                  <img src={sellModalData.monster.image} alt="" />
                </div>
                <div className="sell-unit-stats">
                  <div style={{ color: getTierColor(sellModalData.monster.rank), fontWeight: 'bold' }}>{sellModalData.monster.rank}</div>
                  <div style={{ color: '#fff', fontSize: '11px' }}>Owned: {sellModalData.qty}</div>
                </div>
              </div>

              <div className="sell-governor">
                <div className="sell-gov-label">SELECT QUANTITY</div>
                <div className="sell-gov-controls">
                  <button onClick={() => setSellAmount(Math.max(1, sellAmount - 1))}>-</button>
                  <input
                    type="number"
                    value={sellAmount}
                    onChange={e => setSellAmount(Math.min(sellModalData.qty, Math.max(1, parseInt(e.target.value) || 1)))}
                  />
                  <button onClick={() => setSellAmount(Math.min(sellModalData.qty, sellAmount + 1))}>+</button>
                </div>
                <div className="sell-quick-buttons">
                  <button onClick={() => setSellAmount(1)}>1</button>
                  <button onClick={() => setSellAmount(Math.floor(sellModalData.qty / 2))}>50%</button>
                  <button onClick={() => setSellAmount(sellModalData.qty)}>MAX</button>
                </div>
              </div>

              <div className="sell-result-box">
                <div className="sell-result-label">TOTAL GOLD RECEIVE</div>
                <div className="sell-result-value">
                  <img src="/assets/icon_gold.svg" alt="" />
                  {(sellModalData.sellPrice * sellAmount).toLocaleString()}
                </div>
              </div>

              <div className="sell-modal-actions">
                <button className="btn-cancel" onClick={() => setSellModalData(null)}>CANCEL</button>
                <button className="btn-confirm-sell" onClick={() => {
                  updateMonsterCollection({ [sellModalData.monster.name]: sellModalData.qty - sellAmount });
                  applyResourceDelta({ money: sellModalData.sellPrice * sellAmount });
                  setSellModalData(null);
                }}>SELL UNITS</button>
              </div>
            </div>
          </div>
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
                </div>
              </div>
            </div>

            <div className="fusion-actions">
              <button className="btn-fuse" onClick={() => openFusionModal('money')}>FUSE</button>
              <button className="btn-fuse mass" onClick={() => openFusionModal('gem')}>INSTANT<br />FUSE</button>
            </div>
          </div>

          <div className="rank-list-unique">
            {tierOrder.filter(t => t.key !== 'Primordial').map((tier) => {
              const hasUnits = (tierCounts[tier.key] || 0) > 0;
              const isExpandable = (tier.key === 'God' || tier.key === 'Demi God' || tier.key === 'Chaos' || tier.key === 'Deity') && hasUnits;
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
                      {fusionMonsters.filter((m) => m.tier === tier.key && (monsterInventory[m.name] || 0) > 0).map((monster) => (
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

      {
        subTab === 'collections' && (
          <div className="mon-tab-content active">
            <div className="mon-grid">
              {Array.from({ length: 12 }).map((_, idx) => (
                <div key={`slot-${idx}`} className="mon-grid-item">?</div>
              ))}
            </div>
          </div>
        )
      }

      {
        fusionModal && (
          <div className="fusion-modal">
            <div className="fusion-modal-content">
              <div className="fusion-modal-header">FUSION CHAMBER</div>
              <div className="fusion-modal-body">
                <div className="fusion-modal-info">Units will be fused.</div>
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
                <div className="fusion-modal-connectors">
                  <div className="connector-line left" />
                  <div className="connector-line right" />
                </div>
                <div className="fusion-modal-result">
                  <div className="fusion-modal-result-ring" />
                  <span>?</span>
                </div>
                <div className="fusion-info">
                  <div className="fusion-info-row"><span>Success Rate:</span><span className="fusion-info-value">{fusionModal.chance}</span></div>
                  <div className="fusion-info-row"><span>Fusion Cost:</span><span className="fusion-info-cost" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {fusionModal.cost.toLocaleString()}
                    <img src={fusionModal.type === 'money' ? '/assets/icon_gold.svg' : '/assets/icon_gem.svg'} alt={fusionModal.type} style={{ width: '14px', height: '14px' }} />
                  </span></div>
                </div>
                <div className="fusion-modal-actions">
                  <button className="fusion-cancel" onClick={closeFusionModal}>CANCEL</button>
                  <button className="fusion-confirm" onClick={executeFusion}>COMBINE</button>
                </div>
              </div>
            </div>
          </div>
        )
      }

      {
        fusionAnim.open && (
          <div className={`fusion-anim-overlay ${fusionAnim.phase ? `fusion-phase-${fusionAnim.phase}` : ''} ${fusionAnim.phase >= 5 ? 'fusion-phase-5' : ''}`}>
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
            <img id="anim-left" className="boss-animation" src={ingredientMonster?.full || ingredientMonster?.icon || ''} alt="" />
            <img id="anim-right" className="boss-animation" src={ingredientMonster?.full || ingredientMonster?.icon || ''} alt="" />
            <div id="anim-flash" />
            <div id="anim-result-container">
              <div id="success-text">
                {fusionAnim.success ? (
                  <div className="rainbow-text-wrapper">
                    {"FUSION SUCCESS!!".split('').map((char, i) => (
                      <span key={i} className="rainbow-char-clean" style={{ '--delay': `${i * 0.1}s` }}>
                        {char === ' ' ? '\u00A0' : char}
                      </span>
                    ))}
                  </div>
                ) : '❌ FUSION FAILED ❌'}
              </div>
              <div id="result-glow">
                <div className="result-glow-ring" />
                <img id="anim-result" src={resultMonster?.full || resultMonster?.icon || ''} alt="" />
              </div>
              {/* Auto Transition - No Continue Button */}
            </div>

            {fusionAnim.phase === 6 && phase6Monster && (
              <div className="monster-detail-overlay" style={{ zIndex: 21000, background: 'rgba(0,0,0,0.4)', position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <style>{`
                @keyframes scaleIn {
                  from { transform: scale(0.8); opacity: 0; }
                  to { transform: scale(1); opacity: 1; }
                }
              `}</style>
                <div className="monster-detail-card" onClick={(event) => event.stopPropagation()} style={{
                  animation: 'scaleIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                  width: '85%',
                  maxWidth: '300px',
                  background: '#1a1a1a',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  boxShadow: '0 10px 40px rgba(0,0,0,0.8)',
                  border: '1px solid #444',
                  display: 'flex',
                  flexDirection: 'column'
                }}>
                  <div className="monster-detail-header" style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '4px 0', background: 'rgba(0,0,0,0.3)', borderBottom: '1px solid #333' }}>
                    <div className="monster-detail-name" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <img
                        src={`/assets/element_${getElementIcon(phase6Monster.element)}_circle.png?v=129`}
                        alt={phase6Monster.element}
                        style={{ width: '18px', height: '18px', objectFit: 'contain' }}
                      />
                      <span style={{ fontWeight: '900', fontSize: '1.1rem', color: '#fff', fontFamily: "'Inter', sans-serif" }}>{phase6Monster.name}</span>
                    </div>
                    <div style={{ color: getTierColor(phase6Monster.rank || phase6Monster.tier), fontWeight: '800', fontSize: '0.75rem', marginTop: '-2px', textTransform: 'uppercase', letterSpacing: '0.5px', fontFamily: "'Inter', sans-serif", width: '100%', textAlign: 'left', paddingLeft: '32px' }}>
                      {phase6Monster.rank || phase6Monster.tier}
                    </div>
                    <button className="monster-detail-close" onClick={closeFusionOverlay} style={{ position: 'absolute', right: '8px', top: '8px', background: 'none', border: 'none', color: '#666', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
                  </div>

                  <div className="monster-detail-body" style={{ padding: '0', flex: 1 }}>
                    <div className="monster-detail-image" style={{
                      backgroundImage: `url(${(phase6Monster.cardBackground || '/assets/bg_final_no_mercy.png')}?v=119)`,
                      backgroundSize: 'cover',
                      backgroundPosition: 'center',
                      display: 'flex',
                      alignItems: 'flex-end',
                      justifyContent: 'center',
                      paddingBottom: '4px',
                      height: '110px',
                      position: 'relative'
                    }}>
                      <img
                        src={`${phase6Monster.fullImage || phase6Monster.full || phase6Monster.image}?v=119`}
                        alt={phase6Monster.name}
                        style={{ maxHeight: '95%', maxWidth: '95%', objectFit: 'contain', filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))' }}
                      />
                    </div>
                    <div className="monster-detail-stats" style={{ padding: '5px 8px', background: '#222' }}>
                      {phase6Monster.leaderSkill && (
                        <div className="monster-detail-leader-skill" style={{ textAlign: 'center', marginBottom: '4px', paddingBottom: '4px', borderBottom: '1px solid #333', fontSize: '0.65rem', lineHeight: '1.1' }}>
                          <span style={{ color: '#ffd700', fontWeight: 'bold', textTransform: 'uppercase' }}>LEADER:</span> <span style={{ color: '#ddd', fontStyle: 'italic' }}>{phase6Monster.leaderSkill}</span>
                        </div>
                      )}
                      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '8px', padding: '4px 6px', background: 'rgba(0,0,0,0.4)', borderRadius: '6px' }}>
                        <div style={{ textAlign: 'center' }}>
                          <div style={{ color: '#ff5555', fontSize: '0.6rem', fontWeight: 'bold', lineHeight: '1' }}>ATK</div>
                          <div style={{ color: '#fff', fontSize: '0.75rem', fontWeight: 'bold' }}>{(phase6Monster.stats?.atk || '0').toLocaleString()}</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                          <div style={{ color: '#5555ff', fontSize: '0.6rem', fontWeight: 'bold', lineHeight: '1' }}>DEF</div>
                          <div style={{ color: '#fff', fontSize: '0.75rem', fontWeight: 'bold' }}>{(phase6Monster.stats?.def || '0').toLocaleString()}</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                          <div style={{ color: '#55ff55', fontSize: '0.6rem', fontWeight: 'bold', lineHeight: '1' }}>HP</div>
                          <div style={{ color: '#fff', fontSize: '0.75rem', fontWeight: 'bold' }}>{(phase6Monster.stats?.hp || '0').toLocaleString()}</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div style={{ padding: '6px', background: '#222', borderTop: '1px solid #333', textAlign: 'center' }}>
                    <button onClick={closeFusionOverlay} style={{
                      padding: '4px 20px',
                      background: 'linear-gradient(to bottom, #d4af37, #a67c00)',
                      border: '1px solid #8a6d3b',
                      borderRadius: '4px',
                      color: '#222',
                      fontWeight: 'bold',
                      fontSize: '1rem',
                      cursor: 'pointer',
                      boxShadow: '0 2px 5px rgba(0,0,0,0.5)'
                    }}>
                      CLOSE
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )
      }

      {
        selectedMonster && (
          <div className="monster-detail-overlay" onClick={() => setSelectedMonster(null)}>
            <div className="monster-detail-card" onClick={(event) => event.stopPropagation()}>
              <div className="monster-detail-header" style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', padding: '10px 16px', background: 'rgba(0,0,0,0.5)', borderBottom: '1px solid #333' }}>
                <div className="monster-detail-name" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <img
                    src={`/assets/element_${getElementIcon(selectedMonster.element)}_circle.png?v=129`}
                    alt={selectedMonster.element}
                    style={{ width: '22px', height: '22px', objectFit: 'contain' }}
                  />
                  <span style={{ fontWeight: '900', fontSize: '1.4rem', color: '#fff', fontFamily: "'Inter', sans-serif" }}>{selectedMonster.name}</span>
                </div>
                <div style={{
                  color: getTierColor(selectedMonster.rank),
                  fontWeight: '850',
                  fontSize: '0.85rem',
                  marginTop: '-4px',
                  paddingLeft: '30px',
                  textTransform: 'uppercase',
                  fontFamily: "'Inter', sans-serif"
                }}>
                  {selectedMonster.rank}
                </div>
                <button className="monster-detail-close" onClick={() => setSelectedMonster(null)} style={{ position: 'absolute', right: '15px', top: '15px' }}>✕</button>
              </div>
              <div className="monster-detail-body">
                <div className="monster-detail-image" style={{
                  backgroundImage: `url(${(selectedMonster.cardBackground || '/assets/bg_final_no_mercy.png')}?v=119)`,
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
                    src={`${selectedMonster.fullImage || selectedMonster.image}?v=119`}
                    alt={selectedMonster.name}
                    style={{
                      maxHeight: '90%',
                      maxWidth: '90%',
                      objectFit: 'contain',
                      objectFit: 'contain'
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
                      <span style={{ color: '#ffda00', fontWeight: 'bold', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '1px', display: 'block', marginBottom: '0' }}>
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

import React from 'react';
import { useGameState } from '../context/useGameState';
import './TopUI.css';

const fmt = (n) => n.toLocaleString();

const formatTime = (seconds) => {
    if (seconds <= 0) return "";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
};

const TopUI = ({ variant = 'boss' }) => {
    const { state, resourcePopups } = useGameState();
    const xpPercent = (state.xp / state.xpToLevel) * 100;
    const odPercent = (state.overdrive / state.maxOverdrive) * 100;

    return (
        <div className={`top-ui-wrapper ${variant === 'menu' ? 'top-ui-menu' : 'top-ui-boss'}`}>

            {variant === 'boss' && (
                <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%)', zIndex: -1 }}></div>
            )}

            <div className="top-row">
                {/* LEVEL BADGE & XP */}
                <div className="level-badge">
                    <div className="level-number">
                        <span className="level-value">{state.level}</span>
                    </div>

                    {/* XP BAR WRAPPER */}
                    <div className="xp-bar-wrapper">
                        <div className="xp-text-overlay">{fmt(state.xp)}/{fmt(state.xpToLevel)}</div>
                        <div className="xp-fill" style={{ width: `${xpPercent}%` }}></div>
                    </div>

                    {/* XP FLOATERS - MOVED OUTSIDE WRAPPER */}
                    {resourcePopups.filter(p => p.type === 'xp').map(p => (
                        <div key={p.id} className={`res-floater xp ${p.isCrit ? 'crit' : ''}`}>+{fmt(p.val)} XP</div>
                    ))}
                </div>

                {/* GEMS (TOP MIDDLE) */}
                <div className="gems-display">
                    <div className="gems-pill">
                        <img className="res-icon" src="/assets/icon_gem.svg" alt="Gems" />
                        <span className="gems-amount">{fmt(state.gems)}</span>
                    </div>
                </div>

                {/* MONEY */}
                <div className="money-display">
                    <div className="money-pill-wrapper">
                        <div className="gold-coin">
                            <img className="gold-icon" src="/assets/icon_gold.svg" alt="Gold" />
                        </div>
                        <div className="money-amount-pill">{fmt(state.money)}</div>
                    </div>
                    <div className="money-sub">Next Check: 15:00</div>

                    {/* MONEY FLOATERS */}
                    {resourcePopups.filter(p => p.type === 'money').map(p => (
                        <div key={p.id} className={`res-floater ${p.isCrit ? 'crit' : ''}`} style={{ top: '30px', right: '10px' }}>+{fmt(p.val)}</div>
                    ))}
                </div>
            </div>

            {/* RESOURCES ROW */}
            <div className="resource-row pill-design">
                {/* HP */}
                <div className="resource-item pill">
                    <img className="res-icon" src="/assets/icon_hp.svg" alt="HP" />
                    <div className="resource-bar">
                        <div className="resource-fill hp" style={{ width: `${(state.hp / state.maxHp) * 100}%` }}></div>
                    </div>
                    <span className="resource-text">
                        {state.hp}/{state.maxHp}
                        {state.hp < state.maxHp && (
                            <span className="resource-timer">
                                {formatTime(state.hpSeconds)}
                            </span>
                        )}
                    </span>
                </div>

                {/* ENERGY (QUEST) */}
                <div className="resource-item pill">
                    <img className="res-icon" src="/assets/icon_energy.svg" alt="Energy" />
                    <div className="resource-bar">
                        <div className="resource-fill energy" style={{ width: `${(state.energy / state.maxEnergy) * 100}%` }}></div>
                    </div>
                    <span className="resource-text">
                        {state.energy}/{state.maxEnergy}
                        {state.energy < state.maxEnergy && (
                            <span className="resource-timer">
                                {formatTime(state.energySeconds)}
                            </span>
                        )}
                    </span>
                </div>

                {/* STAMINA (ARENA/WORLD BOSS) */}
                <div className="resource-item pill">
                    <img className="res-icon" src="/assets/icon_battle.png" alt="Stamina" />
                    <div className="resource-bar">
                        <div className="resource-fill stamina" style={{ width: `${(state.stamina / state.maxStamina) * 100}%` }}></div>
                    </div>
                    <span className="resource-text">
                        {state.stamina}/{state.maxStamina}
                        {state.stamina < state.maxStamina && (
                            <span className="resource-timer">
                                {formatTime(state.staminaSeconds)}
                            </span>
                        )}
                    </span>
                </div>
            </div>

            {variant === 'boss' && (
                <div className="overdrive-wrapper">
                    <div className="od-bar-frame">
                        <div
                            className={`od-bar-fill ${odPercent >= 100 ? 'full' : ''}`}
                            style={{ width: `${odPercent}%` }}
                        ></div>
                        <div className="od-text-overlay">OVERDRIVE</div>
                    </div>
                </div>
            )}

        </div>
    );
};

export default TopUI;

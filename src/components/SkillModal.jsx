import React, { useState, useEffect } from 'react';
import { useGameState } from '../context/useGameState';
import { monsters as baseMonsters } from '../data/monsters';
import './SkillModal.css';

const SkillModal = ({ isOpen, onClose }) => {
    const { state, bulkUpdateStats, resetStats } = useGameState();
    const [tempStats, setTempStats] = useState(null);
    const [showResetConfirm, setShowResetConfirm] = useState(false);

    // Initialize tempStats when modal opens
    useEffect(() => {
        if (isOpen && !tempStats) {
            setTempStats({ ...state.stats });
        }
    }, [isOpen, tempStats, state.stats]);

    if (!isOpen || !tempStats) return null;

    const pointsSpent = Object.values(tempStats).reduce((a, b) => a + b, 0) -
        Object.values(state.stats).reduce((a, b) => a + b, 0);
    const availablePoints = state.skillPoints - pointsSpent;

    const leaderSkillEffect = (() => {
        const leader = baseMonsters.find(m => m.name === state.leader);
        if (!leader || !leader.leaderSkill) return {};
        const skill = leader.leaderSkill;
        const effect = {};
        if (skill.includes("Increase Attack")) effect.attack = parseInt(skill.match(/\d+/)[0]) / 100;
        if (skill.includes("Overdrive Damage")) effect.od = parseInt(skill.match(/\d+/)[0]) / 100;
        if (skill.includes("Increase Defense")) effect.defense = parseInt(skill.match(/\d+/)[0]) / 100;
        return effect;
    })();

    const statConfigs = {
        health: { label: 'Health', icon: '/assets/icon_hp.svg', short: 'HP', color: '#ff4d4d', getBonus: (v) => `+${v * 10} Max HP` },
        energy: { label: 'Energy', icon: '/assets/icon_energy.svg', short: 'EN', color: '#ffd700', getBonus: (v) => `+${v} Max Energy` },
        stamina: { label: 'Stamina', icon: '/assets/icon_battle.png', short: 'ST', color: '#39b6ff', getBonus: (v) => `+${v} Max Stamina` },
        attack: {
            label: 'Attack',
            icon: '/assets/stat_attack_retro.png',
            isRetro: true,
            getBonus: (v) => {
                const perc = (v * 0.1).toFixed(1);
                const leaderBonus = (leaderSkillEffect.attack || 0) * 100;
                return `+${(parseFloat(perc) + leaderBonus).toFixed(1)}% Total ATK`;
            }
        },
        defense: {
            label: 'Defense',
            icon: '/assets/stat_defense_retro.png',
            isRetro: true,
            getBonus: (v) => {
                const statBonus = v;
                const leaderBonus = (leaderSkillEffect.defense || 0) * 100;
                return `+${statBonus + leaderBonus}% Total DEF`;
            }
        },
        od: {
            label: 'Overdrive DMG',
            icon: '/assets/stat_overdrive_retro.png',
            isRetro: true,
            getBonus: (v) => {
                const perc = (v * 0.1).toFixed(1);
                return `+${perc}% OD DMG`;
            }
        }
    };

    const handleAdjust = (key, delta) => {
        if (delta > 0 && availablePoints <= 0) return;
        if (delta < 0 && tempStats[key] <= state.stats[key]) return;
        setTempStats(prev => ({ ...prev, [key]: prev[key] + delta }));
    };

    const handleConfirm = () => {
        bulkUpdateStats(tempStats, pointsSpent);
        setTempStats(null);
        onClose();
    };

    const handleResetAction = () => {
        resetStats();
        setTempStats(null);
        setShowResetConfirm(false);
        onClose();
    };

    return (
        <div className="skill-modal-overlay">
            <div className="skill-modal-content small-menu">
                {showResetConfirm && (
                    <div className="reset-confirm-overlay">
                        <div className="reset-confirm-title">RESET STATS</div>
                        <div className="reset-confirm-text">
                            Spend 200 Gems to refund all your Skill Points?
                            <br /><br />
                            You will get back all the points you have spent!
                        </div>
                        <div className="confirm-actions">
                            <button className="btn-no" onClick={() => setShowResetConfirm(false)}>CANCEL</button>
                            <button className="btn-yes" onClick={handleResetAction}>RESET</button>
                        </div>
                    </div>
                )}

                <div className="skill-modal-header">
                    <h2>RANK UP</h2>
                    <div className="points-badge">
                        <span className="points-label">SKILL POINTS</span>
                        <span className="points-value">{availablePoints}</span>
                    </div>
                </div>

                <div className="skill-list mini">
                    {Object.entries(statConfigs).map(([key, config]) => (
                        <div key={key} className="skill-item compact">
                            <div className="skill-info">
                                {config.isRetro ? (
                                    <img src={config.icon} alt={config.label} className="stat-boxed-icon-retro" />
                                ) : (
                                    <div className="stat-boxed-icon-virtual" style={{ '--stat-accent': config.color }}>
                                        <div className="boxed-glow"></div>
                                        <div className="boxed-arrow">▲</div>
                                        <img src={config.icon} alt={config.label} className="boxed-icon-img" />
                                        <div className="boxed-label">{config.short}</div>
                                    </div>
                                )}
                                <div className="skill-details">
                                    <div className="skill-name-row">
                                        <span className="skill-name">{config.label}</span>
                                        <span className="skill-lvl">Lv.{tempStats[key]}</span>
                                    </div>
                                    <div className="skill-bonus-bar">
                                        {config.getBonus(tempStats[key])}
                                    </div>
                                </div>
                            </div>
                            <div className="skill-controls">
                                <button
                                    className="ctrl-btn minus"
                                    disabled={tempStats[key] <= state.stats[key]}
                                    onClick={() => handleAdjust(key, -1)}
                                >-</button>
                                <button
                                    className="ctrl-btn plus"
                                    disabled={availablePoints <= 0}
                                    onClick={() => handleAdjust(key, 1)}
                                >+</button>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="modal-actions-top">
                    <button
                        className="btn-reset"
                        onClick={() => setShowResetConfirm(true)}
                        disabled={state.gems < 200 || Object.values(state.stats).reduce((a, b) => a + b, 0) === 0}
                    >
                        <img src="/assets/icon_gem.svg" className="reset-gem-icon" />
                        RESET (200)
                    </button>
                </div>

                <div className="modal-actions">
                    <button className="btn-cancel" onClick={() => { setTempStats(null); onClose(); }}>CLOSE</button>
                    <button className="btn-confirm" onClick={handleConfirm} disabled={pointsSpent === 0}>CONFIRM</button>
                </div>
            </div>
        </div>
    );
};

export default SkillModal;

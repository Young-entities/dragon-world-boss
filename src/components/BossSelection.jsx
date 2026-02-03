import React, { useState, useEffect } from 'react';
import { useGameState } from '../context/useGameState';
import './RarityBorders.css';

const BossSelection = ({ onBack, onSelectBoss }) => {
    const { state } = useGameState();
    const [activeTab, setActiveTab] = useState('world'); // world, elemental, eternal

    // Timer for UI updates
    const [now, setNow] = useState(Date.now());
    useEffect(() => {
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

    const currentBoss = state.bosses ? state.bosses[activeTab] : null;

    // Helper to render Boss Card
    const renderBossCard = (boss, type) => {
        if (!boss) return <div>Loading...</div>;

        const isCooldown = boss.state === 'cooldown';
        const isLocked = boss.state === 'locked';
        const timeLeft = isCooldown ? (boss.respawnTime - now) : (boss.endTime - now);

        let statusText = "Active";
        let statusColor = "#00ff00";
        let btnText = "ENTER";
        let btnDisabled = false;

        if (isCooldown) {
            statusText = "Waiting";
            statusColor = "#888"; // Gray
            btnText = "WAITING"; // or RESULTS
            btnDisabled = true;
        } else if (isLocked) {
            statusText = "Locked";
            statusColor = "#ff0000";
            btnText = "LOCKED";
            btnDisabled = true;
        } else {
            statusText = "Underway";
            statusColor = "#ffa500"; // Orange
        }

        return (
            <div className="boss-select-card" style={{
                background: '#1a1a22',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.1)',
                padding: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '15px',
                marginTop: '15px'
            }}>
                {/* ICON CONTAINER */}
                {type === 'elemental' ? (
                    <div className="rarity-border-primordial" style={{ width: '70px', height: '70px', flexShrink: 0 }}>
                        <img
                            src={boss.img || "/assets/electric_god_unit_clean.png"}
                            style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top 20%' }}
                        />
                    </div>
                ) : (
                    <div style={{
                        width: '60px', height: '60px', borderRadius: '8px', background: '#000',
                        border: '1px solid #ffd700', display: 'flex', justifyContent: 'center', alignItems: 'center', overflow: 'hidden', flexShrink: 0
                    }}>
                        <img
                            src={boss.img || "/assets/icon_monster.png"}
                            style={{ width: '100%', height: '100%', objectFit: (type === 'world' ? 'cover' : 'contain') }}
                        />
                    </div>
                )}

                <div style={{ flex: 1 }}>
                    <div style={{ color: '#ffd700', fontWeight: 'bold', fontSize: '16px' }}>{boss.name}</div>
                    <div style={{
                        height: '6px', width: '100%', background: '#333', borderRadius: '3px', margin: '5px 0',
                        position: 'relative'
                    }}>
                        <div style={{
                            width: isActive(boss) ? `${(boss.hp / boss.maxHp) * 100}%` : '0%',
                            background: '#ff6600', height: '100%', borderRadius: '3px'
                        }}></div>
                    </div>
                    <div style={{ fontSize: '12px', color: '#888', fontFamily: 'monospace' }}>
                        {isCooldown ? `Starting Time : ${formatTime(timeLeft)}` :
                            isLocked ? "Opens Friday" :
                                `Ends In : ${formatTime(timeLeft)}`}
                    </div>
                </div>

                <button
                    onClick={() => onSelectBoss(type)}
                    disabled={btnDisabled}
                    style={{
                        padding: '10px 20px',
                        background: btnDisabled ? '#333' : '#39b6ff',
                        color: btnDisabled ? '#888' : '#000',
                        border: 'none',
                        borderRadius: '6px',
                        fontWeight: 'bold',
                        cursor: btnDisabled ? 'default' : 'pointer'
                    }}
                >
                    {btnText}
                </button>
            </div>
        );
    };

    const isActive = (b) => b && b.state === 'active';

    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: '#0e0e12', overflow: 'hidden' }}>
            {/* HERDER IMAGE */}
            <div style={{ height: '35%', background: 'url(/assets/boss_header_bg.png) center/cover', position: 'relative' }}>
                <div style={{ position: 'absolute', bottom: '10px', left: '20px', fontSize: '36px', fontWeight: '900', color: '#fff', textShadow: '0 2px 4px #000' }}>
                    BOSS RAIDS
                </div>
                <button onClick={onBack} style={{ position: 'absolute', top: '10px', right: '10px', background: 'rgba(0,0,0,0.5)', border: 'none', color: '#fff', fontSize: '20px', width: '30px', height: '30px', borderRadius: '50%', cursor: 'pointer' }}>✕</button>
            </div>

            {/* TABS */}
            <div style={{ display: 'flex', background: '#111', borderBottom: '1px solid #333' }}>
                {['world', 'elemental', 'eternal'].map(tab => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        style={{
                            flex: 1,
                            padding: '15px 0',
                            background: activeTab === tab ? '#39b6ff' : 'transparent',
                            color: activeTab === tab ? '#000' : '#888',
                            border: 'none',
                            fontWeight: 'bold',
                            fontSize: '14px',
                            cursor: 'pointer',
                            textTransform: 'uppercase'
                        }}
                    >
                        {tab} Boss
                    </button>
                ))}
            </div>

            {/* CONTENT AREA */}
            <div style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>

                {/* FILTER BUTTONS (Visual Only) */}
                <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                    <button style={{ flex: 1, padding: '8px', background: 'linear-gradient(to bottom, #39b6ff, #0088cc)', border: '1px solid #fff', borderRadius: '4px', color: '#fff', fontWeight: 'bold' }}>ALL</button>
                    <button style={{ flex: 1, padding: '8px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#888' }}>Lv1 - 160</button>
                    <button style={{ flex: 1, padding: '8px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#888' }}>Lv161+</button>
                </div>

                <div style={{ color: '#aaa', fontSize: '12px', marginBottom: '20px', lineHeight: '1.4' }}>
                    Defeat the powerful {activeTab} boss to earn massive rewards! All players cooperate to bring down these titans.
                </div>

                <div style={{ color: '#00e5ff', fontWeight: 'bold', fontSize: '14px', marginBottom: '5px' }}>
                    Current {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Boss:
                </div>

                {renderBossCard(currentBoss, activeTab)}

                {/* PREVIOUS BOSS (Mockup) */}
                <div style={{ color: '#00e5ff', fontWeight: 'bold', fontSize: '14px', marginTop: '30px', marginBottom: '5px' }}>
                    Previous Boss:
                </div>
                <div className="boss-select-card" style={{
                    background: '#1a1a22', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', padding: '10px',
                    display: 'flex', alignItems: 'center', gap: '15px', opacity: 0.7
                }}>
                    <div style={{ width: '60px', height: '60px', borderRadius: '8px', background: '#000', border: '1px solid #555' }}></div>
                    <div style={{ flex: 1 }}>
                        <div style={{ color: '#888', fontWeight: 'bold' }}>Dead Boss</div>
                        <div style={{ fontSize: '12px', color: '#666' }}>Defeated</div>
                    </div>
                    <button style={{ padding: '8px 15px', background: '#333', color: '#aaa', border: 'none', borderRadius: '6px' }}>Results</button>
                </div>
            </div>
        </div>
    );
};

export default BossSelection;

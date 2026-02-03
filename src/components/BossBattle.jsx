import React, { useMemo, useState, useEffect } from 'react';
import { useGameState } from '../context/useGameState';

const BossBattle = ({ onBack, bossType = 'world' }) => {
    const { state, attackBoss, damagePopup, bossShake, isAttacking } = useGameState();
    const boss = state.bosses ? state.bosses[bossType] : (bossType === 'world' ? { ...state.bosses?.world, hp: state.bossHp, maxHp: state.maxBossHp } : null);

    // Fallback if boss data missing (should be fixed by now)
    const currentHp = boss ? boss.hp : 0;
    const maxHp = boss ? boss.maxHp : 1;
    const hpPercent = maxHp > 0 ? (currentHp / maxHp) * 100 : 0;

    // Timer Logic
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

    if (!boss) return <div style={{ color: 'white' }}>Loading Boss...</div>;

    let timerText = "";
    let overlay = null;

    if (boss.state === 'active') {
        timerText = `Event Ends In: ${formatTime((boss.endTime || 0) - now)}`;
    } else {
        timerText = `Respawn In: ${formatTime((boss.respawnTime || 0) - now)}`;

        // Sort players to find rank (World Boss Only)
        let finalRank = 0;
        if (bossType === 'world') {
            const players = [...(state.worldBossPlayers || []), { name: "YOU", damage: state.worldBossDamage || 0 }];
            players.sort((a, b) => b.damage - a.damage);
            finalRank = players.findIndex(p => p.name === "YOU") + 1;
        }

        overlay = (
            <div style={{
                position: 'absolute', inset: 0,
                background: 'rgba(0,0,0,0.8)',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                zIndex: 50, color: '#fff', textAlign: 'center'
            }}>
                <h1 style={{ fontSize: '40px', color: '#ff3333', textShadow: '0 0 10px #000', margin: 0 }}>BOSS DEFEATED</h1>
                <div style={{ margin: '20px 0', padding: '15px 30px', background: 'rgba(255,215,0,0.1)', border: '1px solid #ffd700', borderRadius: '12px' }}>
                    {bossType === 'world' ? (
                        <>
                            <div style={{ fontSize: '14px', color: '#ffd700', fontWeight: 'bold' }}>FINAL GLOBAL RANK</div>
                            <div style={{ fontSize: '48px', fontWeight: '900', textShadow: '0 0 15px rgba(255,215,0,0.5)' }}>#{finalRank}</div>
                        </>
                    ) : (
                        <div style={{ fontSize: '24px', color: '#ffd700', fontWeight: 'bold' }}>VICTORY</div>
                    )}
                </div>
                <h2 style={{ fontSize: '20px', color: '#888' }}>{timerText}</h2>
            </div>
        );
    }

    const leaderboard = useMemo(() => {
        if (bossType !== 'world') return [];
        const players = [...(state.worldBossPlayers || []), { name: "YOU", damage: state.worldBossDamage || 0 }];
        players.sort((a, b) => b.damage - a.damage);
        return players.slice(0, 5); // Top 5
    }, [state.worldBossPlayers, state.worldBossDamage, bossType]);

    // Dynamic Background based on boss type
    let bgImage = "/assets/electric_bg_final.png";
    if (bossType === 'elemental') bgImage = "/assets/volcanic_bg.png"; // Placeholder
    if (bossType === 'eternal') bgImage = "/assets/void_bg.png"; // Placeholder

    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
            {overlay}

            {/* BACK BUTTON */}
            <button
                onClick={onBack}
                style={{
                    position: 'absolute', top: '10px', right: '10px', zIndex: 100,
                    background: 'rgba(0,0,0,0.6)', border: '2px solid #39b6ff', color: '#fff',
                    padding: '4px 12px', borderRadius: '4px', fontSize: '11px', fontWeight: 'bold',
                    cursor: 'pointer', backdropFilter: 'blur(4px)', textTransform: 'uppercase'
                }}
            >
                BACK TO MENU
            </button>

            <div style={{
                height: '70%',
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'center',
                position: 'relative',
                paddingBottom: '0',
                paddingTop: '0',
                backgroundImage: `url(${bgImage})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                borderBottom: '2px solid #334466'
            }}>
                {/* Cinematic Lighting Overlay */}
                <div style={{
                    position: 'absolute', inset: 0,
                    background: 'linear-gradient(0deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 40%, rgba(0,180,255,0.1) 100%)',
                    zIndex: 1
                }}></div>

                {/* WORLD LEADERBOARD (Only for World Boss) */}
                {bossType === 'world' && (
                    <div style={{
                        position: 'absolute', top: '10px', left: '10px', width: '140px',
                        background: 'rgba(0,0,0,0.6)', borderRadius: '8px', padding: '8px', zIndex: 10,
                        border: '1px solid rgba(255,255,255,0.1)', backdropFilter: 'blur(4px)'
                    }}>
                        <div style={{ fontSize: '9px', color: '#ffd700', fontWeight: '900', marginBottom: '4px', letterSpacing: '1px' }}>WORLD RANKING</div>
                        {leaderboard.map((p, i) => (
                            <div key={i} style={{
                                display: 'flex', justifyContent: 'space-between', fontSize: '10px',
                                color: p.name === 'YOU' ? '#ffd700' : '#fff', opacity: p.name === 'YOU' ? 1 : 0.8,
                                marginBottom: '2px'
                            }}>
                                <span>{i + 1}. {p.name}</span>
                                <span>{(p.damage / 1000000).toFixed(1)}M</span>
                            </div>
                        ))}
                    </div>
                )}

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
                    <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '15px', color: '#fff', textShadow: '0 1px 2px #000', zIndex: 5 }}>{boss.name || 'Boss'}</div>
                    <div style={{ position: 'absolute', right: '15px', top: 0, bottom: 0, display: 'flex', alignItems: 'center', fontWeight: 'bold', fontSize: '12px', color: '#ffd700', textShadow: '0 1px 2px #000', zIndex: 10, fontFamily: 'monospace' }}>{timerText}</div>
                </div>

                {/* 3-BUTTON ROW (Padded) */}
                <div style={{ padding: '0 10px 10px' }}>
                    <div className="btn-row" style={{ padding: '10px 0 0' }}>
                        <button className="btn normal" onClick={() => attackBoss(1000, bossType)} disabled={isAttacking || boss.state !== 'active'} style={{ opacity: (isAttacking || boss.state !== 'active') ? 0.7 : 1 }}>
                            <span className="btn-title">ATTACK x1</span>
                            <span className="btn-cost"><img className="btn-icon" src="/assets/icon_battle.png" alt="Stamina" /> 1 STAMINA</span>
                        </button>
                        <button className="btn united" onClick={() => attackBoss(5000, bossType)} disabled={isAttacking || boss.state !== 'active'} style={{ opacity: (isAttacking || boss.state !== 'active') ? 0.7 : 1 }}>
                            <span className="btn-title">ATTACK x5</span>
                            <span className="btn-cost"><img className="btn-icon" src="/assets/icon_battle.png" alt="Stamina" /> 5 STAMINA</span>
                        </button>
                        <button className="btn special" onClick={() => attackBoss(50000, bossType)} disabled={isAttacking || boss.state !== 'active'} style={{ opacity: (isAttacking || boss.state !== 'active') ? 0.7 : 1 }}>
                            <span className="btn-title">ATTACK x50</span>
                            <span className="btn-cost"><img className="btn-icon" src="/assets/icon_gem.svg" alt="Gems" /> 10 GEMS</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BossBattle;

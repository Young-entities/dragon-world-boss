import React from 'react';
import { motion as Motion } from 'framer-motion';

// Helper for Rank Colors
const getRankColor = (rank) => {
    if (rank === 'God') return 'linear-gradient(135deg, #ffd700, #ffaa00)';
    if (rank === 'Demi God') return 'linear-gradient(135deg, #da70d6, #800080)';
    return '#cccccc';
};

const MonsterCard = ({ monster, onClick }) => {
    return (
        <Motion.div
            onClick={() => onClick(monster)}
            whileHover={{
                scale: 1.05,
                y: -10,
                boxShadow: "0px 10px 20px rgba(0,0,0,0.5)"
            }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            style={{
                position: 'relative',
                background: '#222',
                borderRadius: '15px',
                padding: '10px',
                cursor: 'pointer',
                overflow: 'hidden',
                border: '2px solid transparent',
                backgroundClip: 'padding-box',
                boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                minWidth: '200px'
            }}
        >
            {/* Rank Border Glow */}
            <div
                style={{
                    position: 'absolute',
                    top: 0, left: 0, right: 0, bottom: 0,
                    borderRadius: '15px',
                    padding: '2px',
                    background: getRankColor(monster.rank),
                    mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                    maskComposite: 'exclude',
                    pointerEvents: 'none',
                    zIndex: 1
                }}
            />

            {/* Rank Badge */}
            <div style={{
                background: getRankColor(monster.rank),
                color: '#000',
                fontWeight: 'bold',
                fontSize: '10px',
                padding: '4px 8px',
                borderRadius: '20px',
                marginBottom: '10px',
                textTransform: 'uppercase',
                zIndex: 2
            }}>
                {monster.rank}
            </div>

            {/* Image */}
            <div style={{ height: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 2 }}>
                <Motion.img
                    src={`${monster.image || monster.fullImage}?v=75`}
                    alt={monster.name}
                    animate={{ y: [0, -6, 0], rotate: [0, -1.2, 0], scale: [1, 1.02, 1] }}
                    transition={{ duration: 2.6, repeat: Infinity, ease: 'easeInOut' }}
                    style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))' }}
                />
            </div>

            {/* Name */}
            <h3 style={{ margin: '10px 0 5px', fontSize: '16px', color: '#fff', zIndex: 2 }}>{monster.name}</h3>

            {/* Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px', width: '100%', fontSize: '12px', color: '#aaa', zIndex: 2 }}>
                <div style={{ background: 'rgba(255,0,0,0.1)', color: '#ff4444', padding: '4px', borderRadius: '4px' }}>ATK: {monster.stats.atk}</div>
                <div style={{ background: 'rgba(0,255,0,0.1)', color: '#44ff44', padding: '4px', borderRadius: '4px' }}>HP: {monster.stats.hp}</div>
                <div style={{ background: 'rgba(0,120,255,0.12)', color: '#4da3ff', padding: '4px', borderRadius: '4px' }}>DEF: {monster.stats.def}</div>
            </div>

        </Motion.div>
    );
};

export default MonsterCard;

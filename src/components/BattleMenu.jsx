import React from 'react';
import './BattleMenu.css';

const BattleMenu = ({ onSelect }) => {
    const options = [
        {
            id: 'quest',
            name: 'QUESTS',
            title: 'Greenhaven Chronicles',
            status: 'Continent I',
            bg: '/assets/banners/quest_bg.png',
            className: 'quest-story',
            locked: false
        },
        {
            id: 'world-boss',
            name: 'WORLD BOSS',
            title: 'Thunder Emperor Zylos',
            status: 'Special Event',
            bg: '/assets/electric_bg_final.png',
            className: 'boss-raid',
            locked: false
        },
        {
            id: 'tower',
            name: 'BATTLE TOWER',
            title: 'Celestial Spire',
            status: '100 Floors',
            bg: '/assets/gemini_bg_clean.png',
            className: 'tower-climb',
            locked: false
        },
        {
            id: 'dungeons',
            name: 'DUNGEONS',
            title: 'Enchanted Paradise',
            status: 'Material Farm',
            bg: '/assets/dark_void_bg.png',
            className: 'dungeon-evolver',
            locked: false
        },
        {
            id: 'arena',
            name: 'ARENA',
            title: 'Warlord Colosseum',
            status: 'PVP Combat',
            bg: '/assets/electric_bg_gold.png',
            className: 'arena-rank',
            locked: false
        }
    ];

    return (
        <div className="battle-menu-container">

            <div className="battle-banners-list">
                {options.map((option) => (
                    <div
                        key={option.id}
                        className={`battle-banner-container ${option.className} ${option.locked ? 'locked' : ''}`}
                        onClick={() => !option.locked && onSelect(option.id)}
                    >
                        {/* MAIN BANNER ART */}
                        <div className="banner-art-box" style={{ backgroundImage: `url(${option.bg})` }}>
                            <div className="banner-overlay-gradient"></div>

                            <div className="banner-text-content">
                                <div className="banner-category">{option.name}</div>
                                <div className="banner-main-title">{option.title}</div>
                            </div>
                        </div>

                        {/* BANNER FOOTER STATUS */}
                        <div className="banner-status-bar">
                            <div className="status-label">{option.status}</div>
                        </div>

                        {/* LOCKED OVERLAY */}
                        {option.locked && (
                            <div className="banner-locked-overlay">
                                <div className="lock-icon">🔒</div>
                                <div className="lock-text">LOCKED</div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BattleMenu;

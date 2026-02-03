import React, { useState } from 'react';
import { motion as Motion, AnimatePresence } from 'framer-motion';
import { useGameState } from '../context/useGameState';
import { chapters } from '../data/quests';
import './QuestScreen.css';

const chapterNodePositions = {
    1: [
        { x: 26, y: 80 }, // Stage 1: Waterfall
        { x: 48, y: 71 }, // Stage 2: Ring
        { x: 78, y: 76 }, // Stage 3: Village
        { x: 42, y: 46 }, // Stage 4: Fortress
        { x: 74, y: 28 }, // Stage 5: Lava
        { x: 72, y: 10 }, // Stage 6: Lighthouse (BOSS)
    ]
};

const QuestScreen = ({ onBack }) => {
    const { state, doQuest } = useGameState();
    const [activeChapterId, setActiveChapterId] = useState(1);
    const [selectedStageIdx, setSelectedStageIdx] = useState(null);

    // Calculate Chapter Unlock Status
    const getChapterStatus = (chId) => {
        if (chId === 1) return 'unlocked';
        const prevChapter = chapters.find(c => c.id === chId - 1);
        if (!prevChapter) return 'locked';
        // CHAPTER UNLOCK: Must master (300%) the very last quest (Quest 6) of Stage 6 of previous chapter
        const lastQuestId = prevChapter.stages[5].quests[5].id;
        return (state.questProgress?.[lastQuestId] || 0) >= 300 ? 'unlocked' : 'locked';
    };

    // Calculate Stage Unlock Status (within current chapter)
    const getStageStatus = (chId, sIdx) => {
        if (chId === 1 && sIdx === 0) return 'unlocked';

        if (sIdx === 0) {
            // First stage of a later chapter: check if previous chapter is fully cleared
            return getChapterStatus(chId);
        } else {
            // Check previous stage in same chapter
            const currentChapter = chapters.find(c => c.id === chId);
            const prevStage = currentChapter.stages[sIdx - 1];
            const prevLastQuestId = prevStage.quests[5].id;
            return (state.questProgress?.[prevLastQuestId] || 0) >= 300 ? 'unlocked' : 'locked';
        }
    };

    // Calculate Quest Unlock Status (within stage)
    const getQuestStatus = (questId) => {
        const [c, s, q] = questId.split('-').map(Number);
        if (q === 1) return 'unlocked';
        const prevQuestId = `${c}-${s}-${q - 1}`;
        return (state.questProgress?.[prevQuestId] || 0) >= 100 ? 'unlocked' : 'locked';
    };

    const activeChapter = chapters.find(c => c.id === activeChapterId);

    const generatePath = () => {
        const positions = chapterNodePositions[activeChapterId];
        if (!positions || positions.length < 2) return "";

        let d = `M ${positions[0].x},${positions[0].y}`;
        for (let i = 1; i < positions.length; i++) {
            const prev = positions[i - 1];
            const curr = positions[i];
            // Calculate a control point for a smooth curve
            const cx = (prev.x + curr.x) / 2 + (i % 2 === 0 ? 5 : -5);
            const cy = (prev.y + curr.y) / 2;
            d += ` Q ${cx},${cy} ${curr.x},${curr.y}`;
        }
        return d;
    };

    return (
        <div className="quest-screen-container archero-theme">
            {/* ARCHERO CHAPTER SELECTOR HEADER */}
            <div className="chapter-header">
                <button className="header-back-btn" onClick={onBack}>✕</button>
                <div className="chapter-selector">
                    <button
                        className="nav-arrow"
                        disabled={activeChapterId <= 1}
                        onClick={() => setActiveChapterId(prev => prev - 1)}
                    >◀</button>
                    <div className="active-chapter-info">
                        <div className="ch-label">CHAPTER {activeChapterId}</div>
                        <div className={`ch-title ${getChapterStatus(activeChapterId) === 'locked' ? 'locked' : ''}`}>
                            {getChapterStatus(activeChapterId) === 'locked' ? '???' : activeChapter.name.split(': ')[1]}
                        </div>
                    </div>
                    <button
                        className="nav-arrow"
                        disabled={activeChapterId >= 20}
                        onClick={() => setActiveChapterId(prev => prev + 1)}
                    >▶</button>
                </div>
                <div style={{ width: 40 }} />
            </div>

            {/* BRAVE FRONTIER STYLE STAGE MAP */}
            <div className="stage-map-area">
                {getChapterStatus(activeChapterId) === 'locked' && (
                    <div className="chapter-locked-overlay">
                        <div className="lock-icon-huge">🔒</div>
                        <div className="lock-text">MASTER PREVIOUS CHAPTER TO UNLOCK</div>
                    </div>
                )}

                <div className="stage-map-scroll">
                    <div className="map-board">
                        <img
                            src={activeChapterId === 1 ? "/assets/maps/chapter1_bg.png" : ""}
                            className="map-underlay-img"
                            alt=""
                        />

                        {/* DYNAMIC TACTICAL PATH - SLEEK DOTTED ENERGY */}
                        <svg className="stage-path-svg-new" viewBox="0 0 100 100" preserveAspectRatio="none">
                            <path
                                d={generatePath()}
                                stroke="#00e5ff"
                                strokeWidth="1.2"
                                fill="none"
                                strokeDasharray="0.1 5"
                                opacity="0.8"
                                strokeLinecap="round"
                                className="path-glow-anim"
                            />
                        </svg>

                        {activeChapter.stages.map((stage, idx) => {
                            const status = getStageStatus(activeChapterId, idx);
                            const isCleared = (state.questProgress?.[stage.quests[5].id] || 0) >= 300;
                            const isSelected = selectedStageIdx === idx;

                            const pos = chapterNodePositions[activeChapterId]?.[idx] || {
                                x: 50,
                                y: 50
                            };

                            return (
                                <div
                                    key={stage.id}
                                    className={`stage-node-bf ${status} ${isCleared ? 'cleared' : ''} ${isSelected ? 'active' : ''}`}
                                    style={{ top: `${pos.y}%`, left: `${pos.x}%` }}
                                    onClick={() => status === 'unlocked' && setSelectedStageIdx(idx)}
                                >
                                    <div className="node-glow" />
                                    <div className="node-crown-bf">
                                        {isCleared ? '👑' : idx + 1 === 6 ? '💀' : ''}
                                    </div>
                                    <div className="node-body-bf">
                                        <div className="node-num-bf">{idx + 1}</div>
                                    </div>
                                    <div className="node-label-bf">
                                        {(getChapterStatus(activeChapterId) === 'locked') ? '???' : stage.name.split(': ')[1]}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* MONSTER WARLORD QUEST LIST (SLIDE UP PANEL) */}
            <AnimatePresence>
                {selectedStageIdx !== null && (
                    <Motion.div
                        className="quest-panel-overlay"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setSelectedStageIdx(null)}
                    >
                        <Motion.div
                            className="quest-list-panel"
                            initial={{ y: '100%' }}
                            animate={{ y: 0 }}
                            exit={{ y: '100%' }}
                            onClick={e => e.stopPropagation()}
                        >
                            <div className="panel-header">
                                <div className="panel-desc">
                                    <div className="st-id">STAGE {activeChapterId}-{selectedStageIdx + 1}</div>
                                    <div className="st-name">{activeChapter.stages[selectedStageIdx].name.split(': ')[1]}</div>
                                </div>
                                <button className="panel-close" onClick={() => setSelectedStageIdx(null)}>✕</button>
                            </div>

                            <div className="quest-rows-container">
                                {/* Calculate Stage Min Progress to enforce "All Must Complete Round X before Round X+1" */}
                                {(() => {
                                    const stageQuests = activeChapter.stages[selectedStageIdx].quests;
                                    const stageProgressValues = stageQuests.map(q => state.questProgress?.[q.id] || 0);
                                    const stageMinProgress = Math.min(...stageProgressValues);
                                    // Current Max Cap for any quest is roughly (floor(min / 100) + 1) * 100
                                    // Example: If min is 0, Cap is 100. If min is 100, Cap is 200.
                                    // But we need to handle the transition.
                                    // If strict "All first", then you can't go above 100 if min < 100.
                                    const currentRound = Math.floor(stageMinProgress / 100) + 1;
                                    const roundCap = currentRound * 100;

                                    return stageQuests.map((quest, qIdx) => {
                                        const qStatus = getQuestStatus(quest.id);
                                        let rawProgress = state.questProgress?.[quest.id] || 0;
                                        const mastered = rawProgress >= 300;

                                        let tier = Math.floor(rawProgress / 100) + 1;
                                        if (tier > 3) tier = 3;

                                        let displayPct = rawProgress % 100;

                                        const isRoundCapped = rawProgress >= roundCap && !mastered;
                                        if (isRoundCapped) displayPct = 100;

                                        return (
                                            <div key={quest.id} className={`quest-card ${qStatus} ${mastered ? 'mastered' : ''} ${isRoundCapped ? 'round-done' : ''}`}>
                                                {/* Header: Title + Rank Info */}
                                                <div className="qc-header">
                                                    <div className="qc-title-group">
                                                        <div className="qc-title">{quest.name.split(': ')[1]}</div>
                                                    </div>
                                                    <div className="qc-rank-info">
                                                        {mastered ? 'MASTERED' : `${displayPct}% RANK ${tier}`}
                                                    </div>
                                                </div>

                                                {/* Progress Strip */}
                                                <div className="qc-progress-track">
                                                    <div
                                                        className="qc-progress-fill"
                                                        style={{
                                                            width: `${mastered ? 100 : displayPct}%`,
                                                            background: tier === 2 ? '#ffd700' : tier === 3 ? '#ff4444' : '#39b6ff'
                                                        }}
                                                    />
                                                </div>

                                                {/* Body: Rewards + Action */}
                                                <div className="qc-body">
                                                    <div className="qc-left">
                                                        <div className="qc-rewards-list">
                                                            <div className="qc-rew-item green">
                                                                + {quest.money} Gold
                                                            </div>
                                                            <div className="qc-rew-item white">
                                                                + {quest.xp} XP
                                                            </div>
                                                        </div>

                                                        {/* Energy Requirement */}
                                                        <div className="qc-energy-cost">
                                                            <img src="/assets/icon_energy.svg" alt="E" className="qc-energy-icon" />
                                                            <span>{quest.energy}</span>
                                                        </div>
                                                    </div>

                                                    <div className="qc-right">
                                                        {qStatus === 'unlocked' && !mastered && !isRoundCapped ? (
                                                            <button
                                                                className="qc-btn-go"
                                                                disabled={state.energy < quest.energy}
                                                                onClick={() => doQuest(quest)}
                                                            >
                                                                GO
                                                            </button>
                                                        ) : mastered ? (
                                                            <div className="qc-status-badge mastered">✓</div>
                                                        ) : isRoundCapped ? (
                                                            <div className="qc-status-badge done">DONE</div>
                                                        ) : (
                                                            <div className="qc-status-badge locked">🔒</div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    });
                                })()}
                            </div>
                        </Motion.div>
                    </Motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default QuestScreen;

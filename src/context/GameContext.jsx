import React, { useState, useEffect } from 'react';
import { GameContext } from './gameContext';
import { monsters as baseMonsters } from '../data/monsters';

const buildInitialCollection = () => (
    Object.fromEntries(baseMonsters.map((monster) => [monster.name, 5]))
);

const getLeaderSkillEffect = (leaderName) => {
    if (!leaderName) return {};
    const leader = baseMonsters.find(m => m.name === leaderName);
    if (!leader || !leader.leaderSkill) return {};

    const skill = leader.leaderSkill;
    const effect = {};

    if (skill.includes("Increase Attack")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.atkMult = 1 + (val / 100);
    }
    if (skill.includes("Increase Experience Gain")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.xpMult = 1 + (val / 100);
    }
    if (skill.includes("Overdrive Damage")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.odCritMult = val / 100;
    }
    if (skill.includes("Energy Recharge Time")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.energyReduction = val;
    }
    if (skill.includes("Stamina Recharge Time")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.staminaReduction = val;
    }
    if (skill.includes("Increase Defense")) {
        const val = parseInt(skill.match(/\d+/)[0]);
        effect.defMult = 1 + (val / 100);
    }

    return effect;
};

const getCollectionAttack = (collection) => (
    baseMonsters.reduce((total, monster) => {
        const qty = collection[monster.name] || 0;
        return total + (monster.stats?.atk || 0) * qty;
    }, 0)
);

export const GameProvider = ({ children }) => {
    const [state, setState] = useState(() => {
        const saved = localStorage.getItem('monster_warlord_save');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                const defaultState = {
                    money: 50000,
                    gems: 50000,
                    level: 1,
                    xp: 0,
                    xpToLevel: 1000,
                    hp: 100,
                    maxHp: 100,
                    hpSeconds: 60,
                    energy: 50,
                    maxEnergy: 50,
                    energySeconds: 120,
                    stamina: 50,
                    maxStamina: 50,
                    staminaSeconds: 120,
                    bossHp: 500000000,
                    maxBossHp: 500000000,
                    worldBossDamage: 0,
                    worldBossPlayers: [
                        { name: "Top-G", damage: 150000000 },
                        { name: "Slayer", damage: 120000000 },
                        { name: "Shadow", damage: 90000000 }
                    ],
                    totalDamage: 0,
                    totalAttacks: 0,
                    overdrive: 0,
                    maxOverdrive: 100,
                    skillPoints: 0,
                    stats: {
                        health: 0, energy: 0, stamina: 0, attack: 0, defense: 0, od: 0
                    },
                    monsterCollection: buildInitialCollection(),
                    leader: "Cinderpaw",
                    summonCurrency: 0,
                    showLevelUp: false,
                    bossState: 'active',
                    bossEndTime: Date.now() + 12 * 60 * 60 * 1000,
                    bossRespawnTime: null,
                    questProgress: { '1-1-1': 0 }
                };

                return {
                    ...defaultState,
                    ...parsed,
                    gems: 50000,
                    bossHp: 500000000000,
                    maxBossHp: 500000000000,
                    showLevelUp: false,
                    bossState: 'active',
                    monsterCollection: buildInitialCollection()
                };
            } catch (e) {
                console.error("Save load failed", e);
            }
        }

        return {
            money: 50000,
            gems: 50000,
            level: 1,
            xp: 0,
            xpToLevel: 1000,
            hp: 100,
            maxHp: 100,
            hpSeconds: 60,
            energy: 50,
            maxEnergy: 50,
            energySeconds: 120,
            stamina: 50,
            maxStamina: 50,
            staminaSeconds: 120,
            bossHp: 500000000000,
            maxBossHp: 500000000000,
            worldBossDamage: 0,
            worldBossPlayers: [
                { name: "Top-G", damage: 150000000000 },
                { name: "Slayer", damage: 120000000000 },
                { name: "Shadow", damage: 90000000000 }
            ],
            totalDamage: 0,
            totalAttacks: 0,
            overdrive: 0,
            maxOverdrive: 100,
            skillPoints: 0,
            stats: {
                health: 0,
                energy: 0,
                stamina: 0,
                attack: 0,
                defense: 0,
                od: 0
            },
            monsterCollection: buildInitialCollection(),
            leader: "Cinderpaw",
            summonCurrency: 0,
            showLevelUp: false,
            bossState: 'active',
            bossEndTime: Date.now() + 12 * 60 * 60 * 1000,
            bossRespawnTime: null,
            questProgress: { '1-1-1': 0 }
        };
    });

    useEffect(() => {
        localStorage.setItem('monster_warlord_save', JSON.stringify(state));
    }, [state]);

    const [damagePopup, setDamagePopup] = useState(null);
    const [bossShake, setBossShake] = useState(false);
    const [resourcePopups, setResourcePopups] = useState([]);
    const [skillModalOpen, setSkillModalOpen] = useState(false);
    const [isAttacking, setIsAttacking] = useState(false);

    useEffect(() => {
        const timer = setInterval(() => {
            setState(prev => {
                let updates = {};
                let changed = false;

                const bonusStamina = prev.stats.stamina;
                const bonusHp = prev.stats.health * 10;
                const bonusEnergy = prev.stats.energy;

                const realMaxStamina = 50 + bonusStamina;
                const realMaxHp = 100 + bonusHp;
                const realMaxEnergy = 50 + bonusEnergy;

                // FORCE SYNC MAX STATS
                if (prev.maxHp !== realMaxHp) { updates.maxHp = realMaxHp; changed = true; }
                if (prev.maxEnergy !== realMaxEnergy) { updates.maxEnergy = realMaxEnergy; changed = true; }
                if (prev.maxStamina !== realMaxStamina) { updates.maxStamina = realMaxStamina; changed = true; }

                const leaderEffect = getLeaderSkillEffect(prev.leader);
                const baseWait = 120;
                const energyWait = Math.max(10, baseWait - (leaderEffect.energyReduction || 0));
                const staminaWait = Math.max(10, baseWait - (leaderEffect.staminaReduction || 0));

                if (prev.energy < realMaxEnergy) {
                    if (prev.energySeconds > 0) {
                        updates.energySeconds = Math.min(prev.energySeconds - 1, energyWait);
                        changed = true;
                    } else {
                        updates.energySeconds = energyWait;
                        updates.energy = prev.energy + 1;
                        changed = true;
                    }
                }

                if (prev.stamina < realMaxStamina) {
                    if (prev.staminaSeconds > 0) {
                        updates.staminaSeconds = Math.min(prev.staminaSeconds - 1, staminaWait);
                        changed = true;
                    } else {
                        updates.staminaSeconds = staminaWait;
                        updates.stamina = prev.stamina + 1;
                        changed = true;
                    }
                }

                if (prev.hp < realMaxHp) {
                    if (prev.hpSeconds > 0) {
                        updates.hpSeconds = prev.hpSeconds - 1;
                        changed = true;
                    } else {
                        updates.hpSeconds = 60;
                        updates.hp = prev.hp + 1;
                        changed = true;
                    }
                }

                if (prev.bossState === 'active' && prev.bossHp > 0) {
                    const simulatedDmg = Math.floor(Math.random() * 500000) + 100000;
                    updates.bossHp = Math.max(0, prev.bossHp - simulatedDmg);
                    updates.worldBossPlayers = prev.worldBossPlayers.map(p => ({
                        ...p,
                        damage: p.damage + Math.floor(simulatedDmg * (0.8 + Math.random() * 0.4))
                    }));
                    changed = true;
                }

                const now = Date.now();
                if (prev.bossState === 'active') {
                    if (prev.bossHp <= 0 || now >= prev.bossEndTime) {
                        updates.bossState = 'cooldown';
                        updates.bossRespawnTime = now + 12 * 60 * 60 * 1000;
                        changed = true;
                    }
                } else if (prev.bossState === 'cooldown') {
                    if (now >= prev.bossRespawnTime) {
                        updates.bossState = 'active';
                        updates.bossHp = prev.maxBossHp;
                        updates.bossEndTime = now + 12 * 60 * 60 * 1000;
                        updates.worldBossDamage = 0;
                        updates.worldBossPlayers = [
                            { name: "Top-G", damage: 150000000000 },
                            { name: "Slayer", damage: 120000000000 },
                            { name: "Shadow", damage: 90000000000 }
                        ];
                        changed = true;
                    }
                }

                return changed ? { ...prev, ...updates } : prev;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const triggerResourcePopup = (type, val, isCrit = false) => {
        const id = Date.now() + Math.random();
        setResourcePopups(prev => [...prev, { id, type, val, isCrit }]);
        setTimeout(() => {
            setResourcePopups(prev => prev.filter(p => p.id !== id));
        }, 1000);
    };

    const bulkUpdateStats = (newStats, pointsSpent) => {
        setState(prev => {
            const nextStats = { ...prev.stats, ...newStats };
            return {
                ...prev,
                skillPoints: prev.skillPoints - pointsSpent,
                stats: nextStats,
                maxHp: 100 + (nextStats.health * 10),
                maxEnergy: 50 + nextStats.energy,
                maxStamina: 50 + nextStats.stamina
            };
        });
    };

    const applyResourceDelta = ({ money = 0, gems = 0 }) => {
        if (money === 0 && gems === 0) return;
        setState(prev => ({
            ...prev,
            money: Math.max(0, prev.money + money),
            gems: Math.max(0, prev.gems + gems)
        }));
    };

    const resetStats = () => {
        setState(prev => {
            if (prev.gems < 200) return prev;
            const totalSpent = Object.values(prev.stats).reduce((a, b) => a + b, 0);
            return {
                ...prev,
                gems: prev.gems - 200,
                skillPoints: prev.skillPoints + totalSpent,
                stats: {
                    health: 0, energy: 0, stamina: 0, attack: 0, defense: 0, od: 0
                },
                maxHp: 100,
                maxEnergy: 50,
                maxStamina: 50
            };
        });
    };

    const dismissLevelUp = () => {
        setState(prev => ({ ...prev, showLevelUp: false }));
        setSkillModalOpen(true);
    };

    const updateMonsterCollection = (updates) => {
        if (!updates || typeof updates !== 'object') return;
        setState(prev => {
            const nextCollection = { ...prev.monsterCollection };
            Object.entries(updates).forEach(([name, qty]) => {
                nextCollection[name] = Math.max(0, qty);
            });
            return { ...prev, monsterCollection: nextCollection };
        });
    };

    const appointLeader = (monsterName) => {
        setState(prev => ({ ...prev, leader: monsterName }));
    };

    const attackBoss = (dmgType) => {
        if (state.bossState !== 'active') return;
        if (isAttacking) return;

        let costSt = 1, costGm = 0, baseDmg = 15000, attacks = 1, odGain = 0.8;
        const leaderEffect = getLeaderSkillEffect(state.leader);
        const collectionAttack = Math.max(1, getCollectionAttack(state.monsterCollection || {}));
        const statAtkBonus = 1 + (state.stats.attack * 0.001);
        const totalAttackPower = collectionAttack * (leaderEffect.atkMult || 1) * statAtkBonus;

        let type = 'normal';
        if (dmgType === 5000) type = 'united';
        if (dmgType === 50000) type = 'special';

        if (type === 'normal') { costSt = 1; costGm = 0; baseDmg = totalAttackPower; attacks = 1; odGain = 0.8; }
        if (type === 'united') { costSt = 5; costGm = 0; baseDmg = totalAttackPower * 5; attacks = 5; odGain = 4.0; }
        if (type === 'special') { costSt = 0; costGm = 10; baseDmg = totalAttackPower * 50; attacks = 50; odGain = 10.0; }

        if (type !== 'special') {
            if (state.stamina < costSt) {
                setDamagePopup({ val: "NO STAMINA!", id: Date.now(), isCrit: false, color: '#888' });
                return;
            }
        } else {
            if (state.gems < costGm) {
                setDamagePopup({ val: "NO GEMS!", id: Date.now(), isCrit: false, color: '#888' });
                return;
            }
        }

        setIsAttacking(true);
        setBossShake(true);
        setTimeout(() => {
            setBossShake(false);
            setIsAttacking(false);
        }, 500);

        let roll = baseDmg * (0.9 + Math.random() * 0.2);
        let finalDmg = Math.floor(roll);

        let currentOD = state.overdrive;
        let isCrit = (currentOD >= 100) || (currentOD + odGain >= 100);

        if (isCrit) {
            const statODMult = state.stats.od * 0.001;
            const critMult = 3 + (leaderEffect.odCritMult || 0) + statODMult;
            finalDmg *= critMult;
            currentOD = 0;
        } else {
            currentOD += odGain;
            if (currentOD > 100) currentOD = 100;
        }

        let rewardMult = isCrit ? 2 : 1;
        let xpGain = 10 * attacks * rewardMult * (leaderEffect.xpMult || 1);
        let moneyGain = (15000 + Math.floor(Math.random() * 10000)) * attacks * rewardMult;

        triggerResourcePopup('xp', xpGain, isCrit);
        triggerResourcePopup('money', moneyGain, isCrit);

        setDamagePopup({
            val: finalDmg.toLocaleString(),
            id: Date.now(),
            isCrit: isCrit,
            color: isCrit ? '#ff0000' : '#ffffff'
        });
        setTimeout(() => setDamagePopup(null), 800);

        let leveledUp = false;
        setState(prev => {
            let newXp = prev.xp + xpGain;
            let newLevel = prev.level;
            let newXpToLevel = prev.xpToLevel;
            let tempPoints = prev.skillPoints || 0;
            let tempShowLevelUp = false;
            let tempStamina = (type !== 'special') ? prev.stamina - costSt : prev.stamina;
            let tempGems = (type === 'special') ? prev.gems - costGm : prev.gems;
            let tempHp = prev.hp;
            let tempEnergy = prev.energy;

            if (newXp >= newXpToLevel) {
                newXp -= newXpToLevel;
                newLevel++;
                newXpToLevel = Math.floor(newXpToLevel * 1.1);
                tempPoints += 5;
                tempShowLevelUp = true;
                leveledUp = true;
                tempHp = 100 + (prev.stats.health * 10);
                tempStamina = 50 + prev.stats.stamina;
                tempEnergy = 50 + prev.stats.energy;
            }

            let nextState = prev.bossState;
            let nextRespawn = prev.bossRespawnTime;
            let nextWorldDamage = (prev.worldBossDamage || 0) + finalDmg;
            let newBossHp = Math.max(0, prev.bossHp - finalDmg);

            if (prev.bossState === 'active' && newBossHp <= 0) {
                nextState = 'cooldown';
                nextRespawn = Date.now() + 12 * 60 * 60 * 1000;
                const players = [...prev.worldBossPlayers, { name: "YOU", damage: nextWorldDamage }];
                players.sort((a, b) => b.damage - a.damage);
                const rank = players.findIndex(p => p.name === "YOU") + 1;
                let bonusMoney = 1000000 / rank;
                let bonusGems = Math.max(1, Math.floor(50 / rank));
                moneyGain += bonusMoney;
                tempGems += bonusGems;
            }

            return {
                ...prev,
                stamina: tempStamina,
                energy: tempEnergy,
                gems: tempGems,
                bossHp: newBossHp,
                bossState: nextState,
                bossRespawnTime: nextRespawn,
                totalDamage: prev.totalDamage + finalDmg,
                worldBossDamage: nextWorldDamage,
                totalAttacks: prev.totalAttacks + attacks,
                money: prev.money + moneyGain,
                xp: newXp,
                level: newLevel,
                xpToLevel: newXpToLevel,
                hp: tempHp,
                skillPoints: tempPoints,
                showLevelUp: tempShowLevelUp,
                overdrive: currentOD
            };
        });

        if (leveledUp) {
            setTimeout(() => {
                setState(s => {
                    if (s.showLevelUp) return { ...s, showLevelUp: false };
                    return s;
                });
                setSkillModalOpen(true);
            }, 2500);
        }
    };

    const doQuest = (quest) => {
        const energyCost = quest.energy;
        const xpReward = quest.xp;
        const moneyReward = quest.money;

        if (state.energy < energyCost) return false;

        setState(prev => {
            const progressId = quest.id;
            const currentProgress = prev.questProgress?.[progressId] || 0;
            if (currentProgress >= 100) return prev;

            const nextProgress = Math.min(100, currentProgress + 10);
            const newQuestProgress = { ...prev.questProgress, [progressId]: nextProgress };

            let newXp = prev.xp + xpReward;
            let newLevel = prev.level;
            let newXpToLevel = prev.xpToLevel;
            let tempPoints = prev.skillPoints || 0;
            let tempShowLevelUp = false;
            let tempHp = prev.hp;
            let tempStamina = prev.stamina;
            let tempEnergy = prev.energy - energyCost;

            if (newXp >= newXpToLevel) {
                newXp -= newXpToLevel;
                newLevel++;
                newXpToLevel = Math.floor(newXpToLevel * 1.1);
                tempPoints += 5;
                tempShowLevelUp = true;
                tempHp = 100 + (prev.stats.health * 10);
                tempStamina = 50 + prev.stats.stamina;
                tempEnergy = 50 + prev.stats.energy;
            }

            triggerResourcePopup('xp', xpReward);
            triggerResourcePopup('money', moneyReward);

            return {
                ...prev,
                energy: tempEnergy,
                money: prev.money + moneyReward,
                xp: newXp,
                level: newLevel,
                xpToLevel: newXpToLevel,
                hp: tempHp,
                stamina: tempStamina,
                skillPoints: tempPoints,
                showLevelUp: tempShowLevelUp,
                questProgress: newQuestProgress
            };
        });
        return true;
    };

    return (
        <GameContext.Provider value={{ state, attackBoss, damagePopup, bossShake, resourcePopups, bulkUpdateStats, resetStats, dismissLevelUp, skillModalOpen, setSkillModalOpen, applyResourceDelta, updateMonsterCollection, appointLeader, isAttacking, doQuest }}>
            {children}
        </GameContext.Provider>
    );
};

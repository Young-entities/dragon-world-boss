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
            bosses: {
                world: {
                    name: "World Titan",
                    hp: 500000000000,
                    maxHp: 500000000000,
                    state: 'active',
                    respawnTime: null,
                    endTime: Date.now() + 12 * 60 * 60 * 1000
                },
                elemental: {
                    name: "Elemental Invader",
                    hp: 200000000000,
                    maxHp: 200000000000,
                    state: 'active',
                    respawnTime: null,
                    endTime: Date.now() + 6 * 60 * 60 * 1000
                },
                eternal: {
                    name: "Eternal Void",
                    hp: 1000000000000,
                    maxHp: 1000000000000,
                    state: 'locked', // Logic will unlock if Friday
                    respawnTime: null,
                    endTime: null
                }
            },
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

                // BOSS LOGIC (World, Elemental, Eternal)
                const now = Date.now();
                if (!prev.bosses) {
                    updates.bosses = {
                        world: {
                            name: "World Titan",
                            hp: 500000000000,
                            maxHp: 500000000000,
                            state: 'active',
                            respawnTime: null,
                            endTime: Date.now() + 12 * 60 * 60 * 1000,
                            rotationIndex: 0
                        },
                        elemental: {
                            name: "Elemental Invader",
                            hp: 200000000000,
                            maxHp: 200000000000,
                            state: 'active',
                            respawnTime: null,
                            endTime: Date.now() + 6 * 60 * 60 * 1000
                        },
                        eternal: {
                            name: "Eternal Void",
                            hp: 1000000000000,
                            maxHp: 1000000000000,
                            state: 'locked',
                            respawnTime: null,
                            endTime: null
                        }
                    };
                    changed = true;
                } else {
                    const dayOfWeek = new Date().getDay(); // 0=Sun, 5=Fri
                    const bossTypes = ['world', 'elemental', 'eternal'];

                    bossTypes.forEach(type => {
                        const boss = prev.bosses[type];
                        let nextState = boss.state;
                        let nextHp = boss.hp;
                        let nextEndTime = boss.endTime;
                        let nextRespawn = boss.respawnTime;
                        let bossChanged = false;

                        // 1. ETERNAL BOSS (Friday Only)
                        if (type === 'eternal') {
                            if (dayOfWeek === 5) { // Friday
                                // If locked and not in cooldown (killed), activate
                                if (boss.state === 'locked' && (!boss.respawnTime || now >= boss.respawnTime)) {
                                    nextState = 'active';
                                    nextHp = boss.maxHp;
                                    bossChanged = true;
                                }
                            } else {
                                // Not Friday
                                if (boss.state !== 'locked') {
                                    nextState = 'locked';
                                    bossChanged = true;
                                }
                            }
                        }

                        // 2. ACTIVE BOSS LOGIC
                        if (nextState === 'active') {
                            // Check End Time (Forced Despawn) OR Death
                            if (nextHp <= 0 || (nextEndTime && now >= nextEndTime)) {
                                nextState = 'cooldown';
                                // Respawn Times: World=23h, Elemental=11h, Eternal=Next Friday
                                if (type === 'world') nextRespawn = now + 23 * 60 * 60 * 1000;
                                else if (type === 'elemental') nextRespawn = now + 11 * 60 * 60 * 1000;
                                else if (type === 'eternal') nextRespawn = now + 24 * 60 * 60 * 1000; // Just push it forward, day check handles lock

                                bossChanged = true;
                            } else {
                                // Simulate Damage (World Boss Only)
                                if (type === 'world') {
                                    const simulatedDmg = Math.floor(Math.random() * 500000) + 100000;
                                    nextHp = Math.max(0, nextHp - simulatedDmg);
                                    bossChanged = true;
                                    if (Math.random() > 0.9) { // Occasionally update leaderboard
                                        updates.worldBossPlayers = prev.worldBossPlayers.map(p => ({
                                            ...p,
                                            damage: p.damage + Math.floor(simulatedDmg * (0.8 + Math.random() * 0.4))
                                        }));
                                        changed = true;
                                    }
                                }
                            }
                        }
                        // 3. COOLDOWN LOGIC
                        let rotationUpdate = {};

                        if (nextState === 'cooldown') {
                            if (now >= nextRespawn) {
                                // Respawn
                                nextState = 'active';
                                nextHp = boss.maxHp;

                                if (type === 'world') {
                                    nextEndTime = now + 23 * 60 * 60 * 1000;
                                    // Rotation Logic
                                    const rotation = [
                                        { name: "Primordial Ignis", element: 'fire', img: '/assets/primordial_fire_combined.png' },
                                        { name: "Primordial Tide", element: 'water' },
                                        { name: "Primordial Spark", element: 'electric' },
                                        { name: "Primordial Terra", element: 'earth' },
                                        { name: "Primordial Void", element: 'dark' },
                                        { name: "Primordial Light", element: 'holy' }
                                    ];
                                    const nextIndex = ((boss.rotationIndex || 0) + 1) % rotation.length;
                                    rotationUpdate = {
                                        rotationIndex: nextIndex,
                                        name: rotation[nextIndex].name,
                                        img: rotation[nextIndex].img
                                    };
                                }
                                else if (type === 'elemental') nextEndTime = now + 11 * 60 * 60 * 1000;

                                bossChanged = true;

                                // Reset Leaderboard for World
                                if (type === 'world') {
                                    updates.worldBossDamage = 0;
                                    updates.worldBossPlayers = [
                                        { name: "Top-G", damage: 150000000000 },
                                        { name: "Slayer", damage: 120000000000 },
                                        { name: "Shadow", damage: 90000000000 }
                                    ];
                                    changed = true;
                                }
                            }
                        }

                        if (bossChanged) {
                            updates.bosses = {
                                ...(updates.bosses || prev.bosses),
                                [type]: {
                                    ...boss,
                                    state: nextState,
                                    hp: nextHp,
                                    respawnTime: nextRespawn,
                                    endTime: nextEndTime,
                                    ...rotationUpdate
                                }
                            };
                            changed = true;
                        }
                    });
                }

                // SYNC LEGACY STATE for Compatibility
                if (updates.bosses && updates.bosses.world) {
                    updates.bossHp = updates.bosses.world.hp;
                    updates.bossState = updates.bosses.world.state;
                    updates.bossRespawnTime = updates.bosses.world.respawnTime;
                    changed = true;
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
            const newMaxHp = 100 + (nextStats.health * 10);
            const newMaxEnergy = 50 + nextStats.energy;
            const newMaxStamina = 50 + nextStats.stamina;

            return {
                ...prev,
                skillPoints: prev.skillPoints - pointsSpent,
                stats: nextStats,
                maxHp: newMaxHp,
                maxEnergy: newMaxEnergy,
                maxStamina: newMaxStamina,
                // Add the delta to current values so user doesn't feel they "lost" the fill
                hp: prev.hp + (newMaxHp - prev.maxHp),
                energy: prev.energy + (newMaxEnergy - prev.maxEnergy),
                stamina: prev.stamina + (newMaxStamina - prev.maxStamina)
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

    const attackBoss = (dmgType, targetBoss = 'world') => {
        // Guard against missing boss data
        if (!state.bosses || !state.bosses[targetBoss]) return;
        const target = state.bosses[targetBoss];

        if (target.state !== 'active') return;
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

            // TARGET SPECIFIC BOSS
            const currentBoss = prev.bosses[targetBoss];
            let nextState = currentBoss.state;
            let nextRespawn = currentBoss.respawnTime;
            let newBossHp = Math.max(0, currentBoss.hp - finalDmg);

            // WORLD BOSS LEADERBOARD logic
            let nextWorldDamage = prev.worldBossDamage;
            let nextWorldPlayers = prev.worldBossPlayers;

            if (targetBoss === 'world') {
                nextWorldDamage = (prev.worldBossDamage || 0) + finalDmg;
            }

            if (currentBoss.state === 'active' && newBossHp <= 0) {
                nextState = 'cooldown';
                const now = Date.now();
                if (targetBoss === 'world') nextRespawn = now + 23 * 60 * 60 * 1000;
                else if (targetBoss === 'elemental') nextRespawn = now + 11 * 60 * 60 * 1000;
                else if (targetBoss === 'eternal') nextRespawn = now + 24 * 60 * 60 * 1000;

                // Rewards for kill
                if (targetBoss === 'world') {
                    const players = [...prev.worldBossPlayers, { name: "YOU", damage: nextWorldDamage }];
                    players.sort((a, b) => b.damage - a.damage);
                    const rank = players.findIndex(p => p.name === "YOU") + 1;
                    let bonusMoney = 1000000 / rank;
                    let bonusGems = Math.max(1, Math.floor(50 / rank));
                    moneyGain += bonusMoney;
                    tempGems += bonusGems;
                    nextWorldPlayers = players;
                } else {
                    // Solo Kill Rewards
                    moneyGain += 500000;
                    tempGems += 50;
                }
            }

            return {
                ...prev,
                stamina: tempStamina,
                energy: tempEnergy,
                gems: tempGems,
                totalDamage: prev.totalDamage + finalDmg,
                worldBossDamage: targetBoss === 'world' ? nextWorldDamage : prev.worldBossDamage,
                worldBossPlayers: targetBoss === 'world' ? nextWorldPlayers : prev.worldBossPlayers,
                totalAttacks: prev.totalAttacks + attacks,
                money: prev.money + moneyGain,
                xp: newXp,
                level: newLevel,
                xpToLevel: newXpToLevel,
                hp: tempHp,
                skillPoints: tempPoints,
                showLevelUp: tempShowLevelUp,
                overdrive: currentOD,
                bosses: {
                    ...prev.bosses,
                    [targetBoss]: {
                        ...currentBoss,
                        hp: newBossHp,
                        state: nextState,
                        respawnTime: nextRespawn
                    }
                },
                // Legacy Sync
                bossHp: targetBoss === 'world' ? newBossHp : prev.bossHp,
                bossState: targetBoss === 'world' ? nextState : prev.bossState,
                bossRespawnTime: targetBoss === 'world' ? nextRespawn : prev.bossRespawnTime
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
            if (currentProgress >= 300) return prev;

            const [c, s, q] = progressId.split('-').map(Number);
            // Dynamic Difficulty: Earlier quests are faster (22%), later quests are slower (7%).
            const gain = Math.max(5, 25 - (q * 3));
            let nextProgress = Math.min(300, currentProgress + gain);

            // CLAMP TO TIER START logic:
            // If we cross into a new tier (e.g. 100 or 200), stop exactly there so the next round starts at 0%.
            const currentTier = Math.floor(currentProgress / 100);
            const calculatedTier = Math.floor(nextProgress / 100);

            if (calculatedTier > currentTier && calculatedTier < 3) {
                nextProgress = calculatedTier * 100;
            }

            const newQuestProgress = { ...prev.questProgress, [progressId]: nextProgress };

            let newXp = prev.xp + xpReward;

            // CHECK FOR COMPLETION BURSTS
            const oldTier = Math.floor(currentProgress / 100);
            const newTier = Math.floor(nextProgress / 100);

            if (newTier > oldTier) {
                // 1. QUEST COMPLETION BURST
                const tierMultiplier = newTier; // 1, 2, or 3
                const questBurst = xpReward * 10 * tierMultiplier;
                newXp += questBurst;
                triggerResourcePopup('xp', questBurst, true); // true = Crit (Gold/Big text)

                // 2. STAGE COMPLETION BURST
                // Check if all peers in this stage are also at least newTier * 100
                let allPeersDone = true;
                for (let k = 1; k <= 6; k++) {
                    if (k === q) continue; // Skip self (already checked via nextProgress/newTier)
                    const peerId = `${c}-${s}-${k}`;
                    const peerProgress = prev.questProgress?.[peerId] || 0;
                    if (peerProgress < newTier * 100) {
                        allPeersDone = false;
                        break;
                    }
                }

                if (allPeersDone) {
                    const stageBurst = xpReward * 30 * tierMultiplier;
                    newXp += stageBurst;
                    // Trigger a second popup slightly delayed or just one big one?
                    // Let's rely on the separate trigger
                    setTimeout(() => triggerResourcePopup('xp', stageBurst, true), 300);
                }
            }
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

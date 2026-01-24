import React, { useState, useEffect } from 'react';
import { GameContext } from './gameContext';
import { monsters as baseMonsters } from '../data/monsters';

const buildInitialCollection = () => (
    Object.fromEntries(baseMonsters.map((monster) => [monster.name, monster.owned ?? 1]))
);

const getCollectionAttack = (collection) => (
    baseMonsters.reduce((total, monster) => {
        const qty = collection[monster.name] || 0;
        return total + (monster.stats?.atk || 0) * qty;
    }, 0)
);

export const GameProvider = ({ children }) => {
    const [state, setState] = useState({
        money: 416531953,
        gems: 5717,
        level: 42,
        xp: 4200,
        xpToLevel: 50000,
        hp: 100,
        maxHp: 100,
        hpSeconds: 60,
        energy: 50,
        maxEnergy: 50,
        energySeconds: 120,
        stamina: 50,
        maxStamina: 50,
        staminaSeconds: 120,
        bossHp: 75000000,
        maxBossHp: 75000000,
        totalDamage: 0,
        totalAttacks: 1204,
        overdrive: 0,
        maxOverdrive: 100,
        skillPoints: 0,
        stats: {
            energy: 0,
            stamina: 0,
            attack: 0,
            defense: 0,
            critDmg: 0
        },
        monsterCollection: buildInitialCollection(),
        showLevelUp: false
    });

    const [damagePopup, setDamagePopup] = useState(null);
    const [bossShake, setBossShake] = useState(false);
    const [resourcePopups, setResourcePopups] = useState([]);
    const [skillModalOpen, setSkillModalOpen] = useState(false);

    useEffect(() => {
        const timer = setInterval(() => {
            setState(prev => {
                let updates = {};
                let changed = false;

                // Stat Bonuses
                const bonusStamina = prev.stats.stamina; // +1 Max Stamina per point
                const bonusHp = prev.stats.energy * 10; // +10 Max HP per point 

                const realMaxStamina = 50 + bonusStamina;
                const realMaxHp = 100 + bonusHp;

                if (prev.energy < prev.maxEnergy) {
                    if (prev.energySeconds > 0) {
                        updates.energySeconds = prev.energySeconds - 1;
                        changed = true;
                    } else {
                        updates.energySeconds = 120;
                        updates.energy = prev.energy + 1;
                        changed = true;
                    }
                } else if (prev.energySeconds !== 120) {
                    updates.energySeconds = 120;
                    changed = true;
                }

                if (prev.stamina < realMaxStamina) {
                    if (prev.staminaSeconds > 0) {
                        updates.staminaSeconds = prev.staminaSeconds - 1;
                        changed = true;
                    } else {
                        updates.staminaSeconds = 120;
                        updates.stamina = prev.stamina + 1;
                        changed = true;
                    }
                } else if (prev.staminaSeconds !== 120) {
                    updates.staminaSeconds = 120;
                    changed = true;
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

                // If max values changed due to stats, update them in state for UI consistency
                if (prev.maxStamina !== realMaxStamina) { updates.maxStamina = realMaxStamina; changed = true; }
                if (prev.maxHp !== realMaxHp) { updates.maxHp = realMaxHp; changed = true; }

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

    const spendSkillPoint = (stat) => {
        setState(prev => {
            if (prev.skillPoints <= 0) return prev;
            return {
                ...prev,
                skillPoints: prev.skillPoints - 1,
                stats: {
                    ...prev.stats,
                    [stat]: prev.stats[stat] + 1
                }
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

    const attackBoss = (dmgType) => {
        let costSt = 1, costGm = 0, baseDmg = 15000, attacks = 1, odGain = 0.8;
        const collectionAttack = Math.max(1, getCollectionAttack(state.monsterCollection || {}));

        let type = 'normal';
        if (dmgType === 5000) type = 'united';
        if (dmgType === 50000) type = 'special';

        if (type === 'normal') { costSt = 1; costGm = 0; baseDmg = collectionAttack; attacks = 1; odGain = 0.8; }
        if (type === 'united') { costSt = 5; costGm = 0; baseDmg = collectionAttack * 5; attacks = 5; odGain = 4.0; }
        if (type === 'special') { costSt = 0; costGm = 10; baseDmg = collectionAttack * 50; attacks = 50; odGain = 10.0; }

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

        setBossShake(true);
        setTimeout(() => setBossShake(false), 500);

        let roll = baseDmg * (0.9 + Math.random() * 0.2);
        let finalDmg = Math.floor(roll);

        let currentOD = state.overdrive;
        let isCrit = (currentOD + odGain >= 100);

        if (isCrit) {
            finalDmg *= 5;
            currentOD = 0;
        } else {
            currentOD += odGain;
            if (currentOD > 100) currentOD = 100;
        }

        let rewardMult = isCrit ? 2 : 1;

        let xpGain = 10 * attacks * rewardMult;
        let moneyGain = (15000 + Math.floor(Math.random() * 10000)) * attacks * rewardMult;

        triggerResourcePopup('xp', xpGain, isCrit);
        triggerResourcePopup('money', moneyGain, isCrit);

        setDamagePopup({
            val: finalDmg.toLocaleString(),
            id: Date.now(),
            isCrit: isCrit,
            color: isCrit ? '#ff4400' : '#ffcc00'
        });
        setTimeout(() => setDamagePopup(null), 800);

        setState(prev => {
            let newXp = prev.xp + xpGain;
            let newLevel = prev.level;
            let newXpToLevel = prev.xpToLevel;

            // Adjust stamina/gems costs first to check availability? 
            // Logic above already checked costs, so we just deduct unless level up refilled them?
            // Actually, costs should be deducted first, then level up might refill them.
            // But in HTML: state.stamina -= costSt happens BEFORE attack logic.
            // Level up happens AFTER attack logic.
            // So: deduct cost -> add rewards -> check level up -> refill if needed.

            // Let's calculate newStamina/newGems based on cost first.
            // Note: type 'special' uses gems, others use stamina.

            let tempStamina = (type !== 'special') ? prev.stamina - costSt : prev.stamina;
            let tempGems = (type === 'special') ? prev.gems - costGm : prev.gems;
            let tempHp = prev.hp;
            let tempEnergy = prev.energy;

            if (newXp >= newXpToLevel) {
                newXp -= newXpToLevel;
                newLevel++;
                newXpToLevel = Math.floor(newXpToLevel * 1.1);
                // Refill HP and Stamina on level up
                tempHp = prev.maxHp;
                tempStamina = prev.maxStamina;
                tempEnergy = prev.maxEnergy;
            }

            return {
                ...prev,
                stamina: tempStamina,
                energy: tempEnergy,
                gems: tempGems,
                bossHp: Math.max(0, prev.bossHp - finalDmg),
                totalDamage: prev.totalDamage + finalDmg,
                totalAttacks: prev.totalAttacks + attacks,
                money: prev.money + moneyGain,
                xp: newXp,
                level: newLevel,
                xpToLevel: newXpToLevel,
                hp: tempHp,
                overdrive: currentOD
            };
        });
    };

    return (
        <GameContext.Provider value={{ state, attackBoss, damagePopup, bossShake, resourcePopups, spendSkillPoint, skillModalOpen, setSkillModalOpen, applyResourceDelta }}>
            {children}
        </GameContext.Provider>
    );
};


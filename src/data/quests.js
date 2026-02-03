// 30 Chapters, 6 Stages per Chapter, 6 Quests per Stage
const chapterNames = [
    "Greenhaven Forest", "Volcanic Peaks", "Azure Depths", "Shattered Skies", "Frozen Tundra",
    "Whispering Sands", "Golden Plains", "Obsidian Gorge", "Lunar Valley", "Sun-Drenched Basin",
    "Cursed Marches", "Eternal Spire", "Misty Hollow", "Dragon's Den", "Crystal Caverns",
    "Iron Ridge", "Stormy Cliffs", "Shadow Jungle", "Brimstone Waste", "Ancient Sanctuary",
    "Rift of Chaos", "Celestial Reach", "Abyssal Maw", "Spirit Grove", "Titan's Rest",
    "Forgotten Archive", "Neon Metropolis", "Warped Dimension", "Core of the World", "The End"
];

const generateQuests = () => {
    const chapters = [];
    for (let c = 1; c <= 30; c++) {
        const stages = [];
        for (let s = 1; s <= 6; s++) {
            const quests = [];
            for (let q = 1; q <= 6; q++) {
                quests.push({
                    id: `${c}-${s}-${q}`,
                    name: `Quest ${q}: ${getQuestName(c, s, q)}`,
                    energy: c + Math.floor((s - 1) / 2) + Math.floor(q / 2),
                    xp: (c * 50) + (s * 10) + (q * 15),
                    money: (c * 1000) + (s * 200) + (q * 150)
                });
            }
            stages.push({
                id: `${c}-${s}`,
                name: `Stage ${s}: ${getStageName(c, s)}`,
                quests
            });
        }
        chapters.push({
            id: c,
            name: `CHAPTER ${c}: ${chapterNames[c - 1] || 'Unknown Territory'}`,
            stages
        });
    }
    return chapters;
};

const getStageName = (c, s) => {
    const themes = ["Border", "Heart", "Peak", "Depths", "Ruins", "Sanctuary"];
    return themes[s - 1] || "Wilderness";
};

const getQuestName = (c, s, q) => {
    const actions = ["Scouting", "Hunting", "Defending", "Exploring", "Clearing", "Boss Battle"];
    return actions[q - 1] || "Quest";
};

export const chapters = generateQuests();

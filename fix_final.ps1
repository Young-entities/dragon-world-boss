
$path = "final_boss_v2.html"
$content = Get-Content $path -Raw
# Robust regex to match the end block
$pattern = "(?s)// --- Reparent Overlay.*?</script>"
$replacement = @"
        // --- SAFETY PATCH: Ensure showFusionModal exists ---
        window.showFusionModal = function(type) {
             if (!fusionSlot1Filled || !fusionSlot2Filled) {
                alert('You need 2 monsters to fuse!');
                return;
            }

            // Check Same Monster
            const name1 = slot1Data ? slot1Data.name : null;
            const name2 = slot2Data ? slot2Data.name : null;
            if (!name1 || !name2 || name1 !== name2) {
                alert('You must fuse 2 of the SAME monster!');
                return;
            }
            
            // Populate Modal (Using HTML Clone for Cards)
            const slot1Img = document.getElementById('fusion-slot-1') ? document.getElementById('fusion-slot-1').innerHTML : '';
            const slot2Img = document.getElementById('fusion-slot-2') ? document.getElementById('fusion-slot-2').innerHTML : '';
             
            const mSlot1 = document.getElementById('modal-slot-1');
            const mSlot2 = document.getElementById('modal-slot-2');
            if(mSlot1) mSlot1.innerHTML = slot1Img;
            if(mSlot2) mSlot2.innerHTML = slot2Img;

            // Calculate Cost/Chance
            const rank = slot1Data ? slot1Data.rank : 1;
            const cost = getFusionCost(rank, type);
            const chance = type === 'money' ? '40%' : '100%';
            const costText = type === 'money' ? ` + "`$" + @"{cost.toLocaleString()} Gold` : ` + "`$" + @"{cost.toLocaleString()} Gems`;

            const elChance = document.getElementById('modal-chance');
            const elCost = document.getElementById('modal-cost');
            if(elChance) elChance.innerText = chance;
            if(elCost) elCost.innerText = costText;

            currentFusionType = type;
            
            const modal = document.getElementById('fusion-modal');
            if(modal) modal.style.display = 'flex';
        };

        // Ensure Reparenting (Again)
        (function () {
            const overlay = document.getElementById('fusion-anim-overlay');
            const container = document.getElementById('game-container'); 
            if (overlay && container) {
                container.appendChild(overlay);
                overlay.style.position = 'absolute';
                overlay.style.borderRadius = '0';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.zIndex = '20000'; 
            }
        })();
    </script>
"@

# Note: PowerShell string interpolation requires tweaking for ${} inside matching quotes.
# I used ` + "`$" + @"{...} ` logic above roughly.
# Actually, simpler to just use plain concatenation in JS string inside PS string.
# Fixed costText line:
# const costText = type === 'money' ? `${cost.toLocaleString()} Gold` : `${cost.toLocaleString()} Gems`;
# In PS @"...":
# `${cost...}` will try to resolve PS variable cost.
# I need to escape `$`.
# PS Escape is backtick `.

$replacement = $replacement.Replace("` + "`$" + @"{", "`${") 
# wait, my logic above was messy. Let's rewrite replacement cleanly.

$replacement = @"
        // --- SAFETY PATCH: Ensure showFusionModal exists ---
        window.showFusionModal = function(type) {
             if (!fusionSlot1Filled || !fusionSlot2Filled) {
                alert('You need 2 monsters to fuse!');
                return;
            }

            // Check Same Monster
            const name1 = slot1Data ? slot1Data.name : null;
            const name2 = slot2Data ? slot2Data.name : null;
            if (!name1 || !name2 || name1 !== name2) {
                alert('You must fuse 2 of the SAME monster!');
                return;
            }
            
            // Populate Modal
            const slot1Img = document.getElementById('fusion-slot-1') ? document.getElementById('fusion-slot-1').innerHTML : '';
            const slot2Img = document.getElementById('fusion-slot-2') ? document.getElementById('fusion-slot-2').innerHTML : '';
             
            const mSlot1 = document.getElementById('modal-slot-1');
            const mSlot2 = document.getElementById('modal-slot-2');
            if(mSlot1) mSlot1.innerHTML = slot1Img;
            if(mSlot2) mSlot2.innerHTML = slot2Img;

            // Calculate Cost/Chance
            const rank = slot1Data ? slot1Data.rank : 1;
            const cost = getFusionCost(rank, type);
            const chance = type === 'money' ? '40%' : '100%';
            // Use concat instead of template literal to avoid PS interpolation hell
            const costText = type === 'money' ? cost.toLocaleString() + ' Gold' : cost.toLocaleString() + ' Gems';

            const elChance = document.getElementById('modal-chance');
            const elCost = document.getElementById('modal-cost');
            if(elChance) elChance.innerText = chance;
            if(elCost) elCost.innerText = costText;

            currentFusionType = type;
            
            const modal = document.getElementById('fusion-modal');
            if(modal) modal.style.display = 'flex';
        };

        // Ensure Reparenting
        (function () {
            const overlay = document.getElementById('fusion-anim-overlay');
            const container = document.getElementById('game-container'); 
            if (overlay && container) {
                container.appendChild(overlay);
                overlay.style.position = 'absolute';
                overlay.style.borderRadius = '0';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.zIndex = '20000'; 
            }
        })();
    </script>
"@

$content = $content -replace $pattern, $replacement
Set-Content $path $content -Encoding utf8


(function () {
    // Aggressive Sticky Polyfill
    // Uses a placeholder to track 'flow' position relative to viewport.

    function initSticky() {
        var header = document.querySelector('.unified-sticky-header');
        if (!header) return;

        var container = document.getElementById('game-container');

        // Create Sentinel/Placeholder
        // We ensure it has the same height as the header (Nav 50 + Padding 50 = 100px approx?)
        // Actually Nav is absolute (0 height flow) + Status Padding (50px). So flow height is ~50px?
        // Let's measure.
        var placeholder = document.createElement('div');
        placeholder.id = 'sticky-sentinel';
        placeholder.style.height = header.offsetHeight + 'px';
        placeholder.style.width = '100%';
        placeholder.style.display = 'block'; // Always take space? No, only when fixed?
        // Actually, sticky works by 'replacing' itself.
        // If we switch to fixed, we need the placeholder to take up the space.
        // So initially, placeholder has 0 height or is hidden?
        // Better: Always have placeholder in DOM, but overlapping?

        // Strategy: 
        // 1. Insert placeholder BEFORE header.
        // 2. Placeholder is empty, 0 height initially? 
        // NO. If header is RELATIVE, it takes space. 
        // We only show placeholder when header is FIXED.

        placeholder.style.height = '100px'; // Approx safe guess, or read offsetHeight
        placeholder.style.visibility = 'hidden';
        placeholder.style.display = 'none';

        header.parentNode.insertBefore(placeholder, header);

        function updateSticky() {
            // Measure where the placeholder IS (or where the header IS if not fixed)
            // If header is fixed, we measure placeholder.
            // If header is relative, we measure header.

            var target = (header.style.position === 'fixed') ? placeholder : header;
            var rect = target.getBoundingClientRect();

            // If top of element hits top of viewport (0)
            if (rect.top <= 0) {
                if (header.style.position !== 'fixed') {
                    // Lock it
                    placeholder.style.height = header.offsetHeight + 'px';
                    placeholder.style.display = 'block';

                    header.style.position = 'fixed';
                    header.style.top = '0';
                    header.style.zIndex = '9999';

                    // Match width
                    if (container) {
                        header.style.width = container.offsetWidth + 'px';
                        header.style.left = container.getBoundingClientRect().left + 'px';
                    } else {
                        header.style.width = '100%';
                        header.style.left = '0';
                    }
                }
            } else {
                // Unlock it
                if (header.style.position === 'fixed') {
                    header.style.position = 'relative'; // or static
                    header.style.top = 'auto';
                    header.style.left = 'auto';
                    header.style.width = '100%';
                    placeholder.style.display = 'none';
                }
            }

            // Continuous Width Sync (if resizing or container moves)
            if (header.style.position === 'fixed' && container) {
                header.style.width = container.offsetWidth + 'px';
                header.style.left = container.getBoundingClientRect().left + 'px';
            }
        }

        // Listen to EVERY scroll potential
        window.addEventListener('scroll', updateSticky);
        document.body.addEventListener('scroll', updateSticky);
        if (container) container.addEventListener('scroll', updateSticky);
        window.addEventListener('resize', updateSticky);

        // Initial check
        // updateSticky(); // Wait for load?
        setTimeout(updateSticky, 100);
    }

    // Run when DOM valid
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSticky);
    } else {
        initSticky();
    }

})();

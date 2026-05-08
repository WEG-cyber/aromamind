document.addEventListener('DOMContentLoaded', () => {
    const filterContainer = document.getElementById('filter-container');
    const oilGrid = document.getElementById('oil-grid');
    const recipeList = document.getElementById('recipe-list');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const modal = document.getElementById('oil-modal');
    const modalBody = document.getElementById('modal-body');
    const closeBtn = document.querySelector('.close-btn');
    const resultHeading = document.getElementById('result-heading');
    const greeting = document.getElementById('greeting');

    let currentTab = 'moods';
    let activeFilter = null;

    // --- LIFF Initialization ---
    async function initLiff() {
        try {
            // 請將 'YOUR_LIFF_ID' 替換成您在 LINE Developers 取得的 LIFF ID
            await liff.init({ liffId: "2009990334-b3WXj4PN" }); 
            if (liff.isLoggedIn()) {
                const profile = await liff.getProfile();
                greeting.textContent = `嗨 ${profile.displayName}，找回身心的平衡`;
            }
        } catch (err) {
            console.log('LIFF Initialization failed', err);
        }
    }

    // --- Initialization ---
    function init() {
        renderFilters(currentTab);
        renderOils(aromaData.oils);
        renderRecipes();
        setupEventListeners();
        initLiff();
    }

    // --- Rendering ---
    function renderFilters(type) {
        filterContainer.innerHTML = '';
        const items = aromaData[type];
        
        const allChip = createFilterChip({ id: 'all', name: '全部顯示', icon: '✨' }, true);
        filterContainer.appendChild(allChip);

        items.forEach(item => {
            const chip = createFilterChip(item);
            filterContainer.appendChild(chip);
        });
    }

    function createFilterChip(item, isAll = false) {
        const chip = document.createElement('div');
        chip.className = `filter-chip ${isAll && !activeFilter ? 'active' : ''}`;
        if (activeFilter === item.id) chip.classList.add('active');
        
        chip.innerHTML = `<span>${item.icon}</span> ${item.name}`;
        chip.addEventListener('click', () => {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeFilter = isAll ? null : item.id;
            filterOils();
        });
        return chip;
    }

    function renderOils(oils) {
        oilGrid.innerHTML = '';
        oils.forEach((oil, index) => {
            const card = document.createElement('div');
            card.className = 'oil-card';
            card.style.animationDelay = `${index * 0.1}s`;
            
            card.innerHTML = `
                <div>
                    <h3>${oil.name}</h3>
                    <div class="sci-name">${oil.scientificName}</div>
                    <p>${oil.description}</p>
                </div>
                <div class="tags">
                    ${oil.benefits.slice(0, 3).map(b => `<span class="tag">${b}</span>`).join('')}
                </div>
            `;
            
            card.addEventListener('click', () => openModal(oil));
            oilGrid.appendChild(card);
        });

        if (oils.length === 0) {
            oilGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 2rem;">暫無匹配的精油推薦。</p>';
        }
    }

    function renderRecipes() {
        recipeList.innerHTML = '';
        aromaData.recipes.forEach(recipe => {
            const card = document.createElement('div');
            card.className = 'recipe-card';
            card.innerHTML = `
                <h4>${recipe.title}</h4>
                <ul>
                    ${recipe.oils.map(oil => `<li>• ${oil}</li>`).join('')}
                </ul>
                <p style="font-size: 0.85rem; color: var(--text-light);">${recipe.description}</p>
            `;
            recipeList.appendChild(card);
        });
    }

    function filterOils() {
        let filtered = aromaData.oils;
        if (activeFilter) {
            filtered = aromaData.oils.filter(oil => {
                if (currentTab === 'moods') {
                    return oil.moods.includes(activeFilter);
                } else {
                    return oil.symptoms.includes(activeFilter);
                }
            });
            const filterItem = aromaData[currentTab].find(i => i.id === activeFilter);
            resultHeading.textContent = `針對「${filterItem.name}」的推薦`;
        } else {
            resultHeading.textContent = '所有推薦精油';
        }
        renderOils(filtered);
    }

    function openModal(oil) {
        modalBody.innerHTML = `
            <h2>${oil.name}</h2>
            <div class="sci-name">${oil.scientificName}</div>
            <div class="detail-section">
                <h4>療癒生活儀式</h4>
                <div class="ritual-box">${oil.ritual}</div>
            </div>
            <div class="detail-section">
                <h4>關於此精油</h4>
                <p>${oil.description}</p>
            </div>
            <div class="detail-section">
                <h4>主要功效</h4>
                <div class="benefit-list">
                    ${oil.benefits.map(b => `<span class="benefit-item">${b}</span>`).join('')}
                </div>
            </div>
            <div class="detail-section">
                <h4>建議用法</h4>
                <p>${oil.usage}</p>
            </div>
            <div class="detail-section" style="background: #fff9f0; padding: 1rem; border-radius: 12px; border: 1px solid #ffeeba;">
                <h4 style="color: #856404;">⚠️ 注意事項</h4>
                <p style="color: #856404; font-size: 0.9rem;">${oil.caution}</p>
            </div>
            <div style="margin-top: 2rem; text-align: center;">
                <button id="liff-close-btn" class="filter-chip" style="display: inline-flex; width: auto; background: var(--primary); color: white; border: none;">
                    完成並關閉視窗
                </button>
            </div>
        `;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; 

        // Close LIFF window button
        const liffCloseBtn = document.getElementById('liff-close-btn');
        liffCloseBtn.addEventListener('click', () => {
            if (liff.isInClient()) {
                liff.closeWindow();
            } else {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    function setupEventListeners() {
        // Breathing logic
        const breathingContainer = document.querySelector('.zen-breathing-container');
        const breathingText = document.querySelector('.breathing-text');
        let isBreathing = false;

        breathingContainer.addEventListener('click', () => {
            isBreathing = !isBreathing;
            breathingContainer.classList.toggle('active');
            breathingText.innerHTML = isBreathing ? '吸氣... 吐氣...' : '點擊開始呼吸練習';
        });

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentTab = btn.dataset.tab;
                activeFilter = null;
                renderFilters(currentTab);
                filterOils();
            });
        });

        closeBtn.onclick = () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        };

        window.onclick = (event) => {
            if (event.target == modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        };
    }

    init();
});

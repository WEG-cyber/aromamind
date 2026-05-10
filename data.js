const aromaData = {
    oils: [
        {
            id: "lavender",
            name: "薰衣草 (Lavender)",
            scientificName: "Lavandula angustifolia",
            description: "最廣為人知的精油，具有強大的鎮靜與舒緩力量。它是芳療界的『萬用油』。",
            benefits: ["舒緩壓力", "改善睡眠", "緩解頭痛", "修復皮膚"],
            moods: ["anxiety", "insomnia", "stress", "restless"],
            symptoms: ["headache", "skin_irritation", "muscle_tension", "menstrual_discomfort"],
            usage: "可直接滴於枕頭、加入擴香儀或稀釋後按摩太陽穴。",
            ritual: "在睡前將一滴精油滴在枕頭角，閉上眼，想像每一根緊繃的肌肉都像溶化的雪水一樣流走。",
            caution: "雖然溫和，但低血壓者使用過量可能導致倦怠。",
            color: "#9b8dae"
        },
        {
            id: "peppermint",
            name: "歐薄荷 (Peppermint)",
            scientificName: "Mentha piperita",
            description: "清涼清爽的香氣，能瞬間提神醒腦，並緩解各種身體不適。",
            benefits: ["提升專注力", "緩解鼻塞", "減輕噁心", "清涼止癢"],
            moods: ["fatigue", "confusion", "low_energy"],
            symptoms: ["headache", "nasal_congestion", "digestive_issues", "muscle_tension"],
            usage: "適合日間擴香，或稀釋後塗抹於頸部後方提神。",
            ritual: "將稀釋後的精油塗抹在太陽穴，逆時針輕揉，想像清涼的微風正帶走你腦中的迷霧。",
            caution: "具有強烈清涼感，避開眼睛周圍；嬰幼兒、孕婦與蠶豆症患者應避免使用。",
            color: "#7fb9a2"
        },
        {
            id: "eucalyptus",
            name: "尤加利 (Eucalyptus)",
            scientificName: "Eucalyptus globulus",
            description: "具有強勁的穿透力，是呼吸道的守護者，能淨化空氣並激發活力。",
            benefits: ["淨化呼吸道", "提升免疫力", "清空思緒", "環境除臭"],
            moods: ["mental_fog", "lethargy"],
            symptoms: ["nasal_congestion", "cough", "cold_symptoms", "respiratory_congestion"],
            usage: "最適合用於蒸氣吸入或擴香，幫助呼吸順暢。",
            ritual: "滴在熱水中，用大毛巾蓋住頭部吸入蒸氣。每一次呼吸，都在淨化你的內在森林。",
            caution: "不宜口服；幼童使用需選擇較溫和的澳洲尤加利。",
            color: "#6d8c8e"
        },
        {
            id: "tea_tree",
            name: "茶樹 (Tea Tree)",
            scientificName: "Melaleuca alternifolia",
            description: "強效的天然防護劑，具有清新的木質香氣，是居家必備的淨化之星。",
            benefits: ["天然抑菌", "平衡油脂", "提升防護力", "調理肌膚"],
            moods: ["fatigue", "mental_fog"],
            symptoms: ["skin_blemish", "skin_irritation", "cold_symptoms"],
            usage: "點塗於痘痘處，或加入洗手乳中加強防護。",
            ritual: "在清潔地板時滴入幾滴，感受空氣中瀰漫的潔淨能量，這也是在清理你心中的雜念。",
            caution: "不可口服；氧化後的精油可能導致皮膚過敏。",
            color: "#a3bcb6"
        },
        {
            id: "bergamot",
            name: "佛手柑 (Bergamot)",
            scientificName: "Citrus bergamia",
            description: "兼具柑橘的清新與花香的優雅，是著名的『快樂精油』，能同時提振與安撫情緒。",
            benefits: ["抗憂鬱", "緩解焦慮", "提振精神", "幫助消化"],
            moods: ["depression", "anxiety", "low_confidence", "irritability"],
            symptoms: ["stress_digestive", "loss_of_appetite", "digestive_discomfort"],
            usage: "擴香能營造愉悅氛圍；加入按摩油中能放鬆心情。",
            ritual: "擴香時，對著鏡子深呼吸，告訴自己：『我值得擁有這一刻的快樂與平靜。』",
            caution: "具有光敏性，塗抹於皮膚後 12 小時內避免日曬。",
            color: "#d4af37"
        },
        {
            id: "frankincense",
            name: "乳香 (Frankincense)",
            scientificName: "Boswellia carterii",
            description: "神聖且深沉的木質香調，能讓呼吸變慢、變深，帶領心靈進入平靜。",
            benefits: ["深層放鬆", "平撫情緒", "抗老修護", "加深呼吸"],
            moods: ["stress", "grief", "panic", "meditation", "grounding_meditation"],
            symptoms: ["respiratory_distress", "aging_skin", "joint_stiffness"],
            usage: "非常適合冥想時擴香，或加入面霜中護理肌膚。",
            ritual: "盤腿坐下，隨著香氣加深你的呼吸。感受氣息從鼻尖深入到腹部，穩定你的重心。",
            caution: "孕期使用請諮詢專業意見。",
            color: "#c2b280"
        },
        {
            id: "clary_sage",
            name: "快樂鼠尾草 (Clary Sage)",
            scientificName: "Salvia sclarea",
            description: "溫暖、帶點堅果味的草本香，是女性的好隊友，能舒緩週期帶來的不適。",
            benefits: ["平衡情緒", "放鬆肌肉", "女性週期支持", "幫助入夢"],
            moods: ["mood_swings", "anxiety", "stress"],
            symptoms: ["menstrual_discomfort", "muscle_tension"],
            usage: "加入底油按摩下腹部，或在睡前小量擴香。",
            ritual: "將雙手放在腹部，感受快樂鼠尾草的溫暖能量，釋放累積在那裡的壓力與委屈。",
            caution: "懷孕期間禁用；使用後避免飲酒以免造成強烈醉意感。",
            color: "#b09787"
        },
        {
            id: "sweet_orange",
            name: "甜橙 (Sweet Orange)",
            scientificName: "Citrus sinensis",
            description: "溫暖陽光的香氣，像是在寒冬中的擁抱，能帶來純粹的喜悅感。",
            benefits: ["驅散憂鬱", "緩解壓力", "幫助入睡", "改善食慾"],
            moods: ["sadness", "stress", "insomnia", "pessimism"],
            symptoms: ["digestive_sluggishness", "digestive_discomfort"],
            usage: "非常適合與薰衣草搭配睡前擴香，大人小孩都喜愛。",
            ritual: "在溫暖的室內擴香，閉上眼，感受這股金色的暖流包圍著你，趕走所有的孤單。",
            caution: "具輕微光敏性。",
            color: "#f28500"
        },
        {
            id: "rosemary",
            name: "迷迭香 (Rosemary)",
            scientificName: "Rosmarinus officinalis",
            description: "強勁的草本香氣，被稱為『記憶之草』，能激發大腦活力。",
            benefits: ["增強記憶", "提高專注力", "促進循環", "緩解肌肉痠痛"],
            moods: ["confusion", "exam_stress", "mental_exhaustion"],
            symptoms: ["muscle_pain", "low_blood_pressure", "muscle_soreness"],
            usage: "學習或工作時擴香；加入洗髮精中護理頭皮。",
            ritual: "在工作桌旁擴香，挺直脊椎，每一次吸氣都想像氧氣正在點亮你大腦中的每一個細胞。",
            caution: "高血壓與癲癇患者應避免使用；懷孕期間不建議使用。",
            color: "#4a5d4e"
        }
    ],
    symptoms: [
        { id: "headache", name: "頭痛與頸肩緊繃", icon: "🧠" },
        { id: "nasal_congestion", name: "鼻塞 / 呼吸道悶塞", icon: "👃" },
        { id: "insomnia", name: "睡眠困難 / 失眠", icon: "🌙" },
        { id: "muscle_soreness", name: "肌肉痠痛 / 運動後", icon: "💪" },
        { id: "menstrual_discomfort", name: "經期不適 / 暖腹", icon: "🌸" },
        { id: "digestive_discomfort", name: "消化不適 / 順暢", icon: "🍵" },
        { id: "skin_blemish", name: "肌膚瑕疵 / 調理", icon: "✨" },
        { id: "joint_stiffness", name: "關節僵硬 / 靈活", icon: "🦴" }
    ],
    moods: [
        { id: "stress_anxiety", name: "壓力與焦慮", icon: "😟" },
        { id: "fatigue_low_mood", name: "疲勞與低落", icon: "🔋" },
        { id: "grounding_meditation", name: "冥想與安定", icon: "🧘" },
        { id: "insomnia", name: "難以入睡", icon: "🌙" }
    ],
    oils: [
        {
            id: "lavender",
            name: "薰衣草 (Lavender)",
            scientificName: "Lavandula angustifolia",
            description: "最廣為人知的精油，具有強大的鎮靜與舒緩力量。它是芳療界的『萬用油』。",
            benefits: ["舒緩壓力", "改善睡眠", "緩解頭痛", "修復皮膚"],
            moods: ["anxiety", "insomnia", "stress", "restless"],
            symptoms: ["headache", "skin_irritation", "muscle_tension", "menstrual_discomfort"],
            usage: "可直接滴於枕頭、加入擴香儀或稀釋後按摩太陽穴。",
            ritual: "在睡前將一滴精油滴在枕頭角，閉上眼，想像每一根緊繃的肌肉都像溶化的雪水一樣流走。",
            caution: "雖然溫和，但低血壓者使用過量可能導致倦怠。",
            color: "#9b8dae"
        },
        {
            id: "peppermint",
            name: "歐薄荷 (Peppermint)",
            scientificName: "Mentha piperita",
            description: "清涼清爽的香氣，能瞬間提神醒腦，並緩解各種身體不適。",
            benefits: ["提升專注力", "緩解鼻塞", "減輕噁心", "清涼止癢"],
            moods: ["fatigue", "confusion", "low_energy"],
            symptoms: ["headache", "nasal_congestion", "digestive_issues", "muscle_tension"],
            usage: "適合日間擴香，或稀釋後塗抹於頸部後方提神。",
            ritual: "將稀釋後的精油塗抹在太陽穴，逆時針輕揉，想像清涼的微風正帶走你腦中的迷霧。",
            caution: "具有強烈清涼感，避開眼睛周圍；嬰幼兒、孕婦與蠶豆症患者應避免使用。",
            color: "#7fb9a2"
        },
        {
            id: "eucalyptus",
            name: "尤加利 (Eucalyptus)",
            scientificName: "Eucalyptus globulus",
            description: "具有強勁的穿透力，是呼吸道的守護者，能淨化空氣並激發活力。",
            benefits: ["淨化呼吸道", "提升免疫力", "清空思緒", "環境除臭"],
            moods: ["mental_fog", "lethargy"],
            symptoms: ["nasal_congestion", "cough", "cold_symptoms", "respiratory_congestion"],
            usage: "最適合用於蒸氣吸入或擴香，幫助呼吸順暢。",
            ritual: "滴在熱水中，用大毛巾蓋住頭部吸入蒸氣。每一次呼吸，都在淨化你的內在森林。",
            caution: "不宜口服；幼童使用需選擇較溫和的澳洲尤加利。",
            color: "#6d8c8e"
        },
        {
            id: "tea_tree",
            name: "茶樹 (Tea Tree)",
            scientificName: "Melaleuca alternifolia",
            description: "強效的天然防護劑，具有清新的木質香氣，是居家必備的淨化之星。",
            benefits: ["天然抑菌", "平衡油脂", "提升防護力", "調理肌膚"],
            moods: ["fatigue", "mental_fog"],
            symptoms: ["skin_blemish", "skin_irritation", "cold_symptoms"],
            usage: "點塗於痘痘處，或加入洗手乳中加強防護。",
            ritual: "滴一滴在口罩扣或領口，想像一層純淨的防護罩正保護著你。",
            caution: "雖然溫和，但大面積使用仍需稀釋。",
            color: "#a3bcb6"
        },
        {
            id: "clarysage",
            name: "快樂鼠尾草 (Clary Sage)",
            scientificName: "Salvia sclarea",
            description: "具有獨特的堅果木質香氣，是著名的『女性精油』，能平衡情緒，帶來深層的放鬆感。",
            benefits: ["平衡荷爾蒙", "緩解焦慮", "放鬆肌肉", "提升幸福感"],
            moods: ["anxiety", "stress", "depression", "mood_swings"],
            symptoms: ["menstrual_discomfort", "muscle_tension", "insomnia"],
            usage: "適合擴香使用，或稀釋後輕輕按摩於腹部。",
            ritual: "在溫暖的掌心中搓熱精油，深深吸氣。想像溫暖的月光正包圍著你，融化所有的不安。",
            caution: "使用後應避免飲酒；懷孕期間請避免使用。",
            color: "#8da3ae"
        }
    ],
    recipes: [
        {
            title: "放鬆舒壓按摩油",
            oils: ["薰衣草 5滴", "佛手柑 4滴", "乳香 3滴"],
            description: "稀釋於 30ml 荷荷芭油中。適用於肩頸、胸口，能有效緩解高壓下的緊繃感。"
        },
        {
            title: "經期暖腹按摩油",
            oils: ["快樂鼠尾草 4滴", "薰衣草 4滴", "甜馬鬱蘭 4滴"],
            description: "稀釋於 30ml 甜杏仁油中。經期前或經期中少量按摩下腹，溫暖安撫身心。"
        },
        {
            title: "運動後肌肉舒緩油",
            oils: ["迷迭香 5滴", "尤加利 5滴", "歐薄荷 5滴"],
            description: "稀釋於 30ml 葡萄籽油中。運動後淋浴後按摩局部肌肉，帶動循環並釋放痠痛。"
        },
        {
            title: "睡前安眠按摩油",
            oils: ["羅馬洋甘菊 2滴", "薰衣草 4滴"],
            description: "稀釋於 30ml 分餾椰子油中。睡前 30 分鐘少量按摩足底與肩頸，幫助進入深度睡眠。"
        }
    ]
};

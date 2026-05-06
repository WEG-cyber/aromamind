const aromaData = {
    oils: [
        {
            id: "lavender",
            name: "薰衣草 (Lavender)",
            scientificName: "Lavandula angustifolia",
            description: "最廣為人知的精油，具有強大的鎮靜與舒緩力量。它是芳療界的『萬用油』。",
            benefits: ["舒緩壓力", "改善睡眠", "緩解頭痛", "修復皮膚"],
            moods: ["anxiety", "insomnia", "stress", "restless"],
            symptoms: ["headache", "skin_irritation", "muscle_tension"],
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
            symptoms: ["headache", "nasal_congestion", "digestive_issues"],
            usage: "適合日間擴香，或稀釋後塗抹於頸部後方提神。",
            ritual: "將稀釋後的精油塗抹在太陽穴，逆時針輕揉，想像清涼的微風正帶走你腦中的迷霧。",
            caution: "具有強烈清涼感，避開眼睛周圍；嬰幼兒與蠶豆症患者應避免使用。",
            color: "#7fb9a2"
        },
        {
            id: "eucalyptus",
            name: "尤加利 (Eucalyptus)",
            scientificName: "Eucalyptus globulus",
            description: "具有強勁的穿透力，是呼吸道的守護者，能淨化空氣並激發活力。",
            benefits: ["淨化呼吸道", "提升免疫力", "清空思緒", "環境除臭"],
            moods: ["mental_fog", "lethargy"],
            symptoms: ["nasal_congestion", "cough", "cold_symptoms"],
            usage: "最適合用於蒸氣吸入或擴香，幫助呼吸順暢。",
            ritual: "滴在熱水中，用大毛巾蓋住頭部吸入蒸氣。每一次呼吸，都在淨化你的內在森林。",
            caution: "不宜口服；幼童使用需選擇較溫和的澳洲尤加利。",
            color: "#6d8c8e"
        },
        {
            id: "bergamot",
            name: "佛手柑 (Bergamot)",
            scientificName: "Citrus bergamia",
            description: "兼具柑橘的清新與花香的優雅，是著名的『快樂精油』，能同時提振與安撫情緒。",
            benefits: ["抗憂鬱", "緩解焦慮", "提振精神", "幫助消化"],
            moods: ["depression", "anxiety", "low_confidence", "irritability"],
            symptoms: ["stress_digestive", "loss_of_appetite"],
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
            moods: ["stress", "grief", "panic", "meditation"],
            symptoms: ["respiratory_distress", "aging_skin"],
            usage: "非常適合冥想時擴香，或加入面霜中護理肌膚。",
            ritual: "盤腿坐下，隨著香氣加深你的呼吸。感受氣息從鼻尖深入到腹部，穩定你的重心。",
            caution: "孕期使用請諮詢專業意見。",
            color: "#c2b280"
        },
        {
            id: "sweet_orange",
            name: "甜橙 (Sweet Orange)",
            scientificName: "Citrus sinensis",
            description: "溫暖陽光的香氣，像是在寒冬中的擁抱，能帶來純粹的喜悅感。",
            benefits: ["驅散憂鬱", "緩解壓力", "幫助入睡", "改善食慾"],
            moods: ["sadness", "stress", "insomnia", "pessimism"],
            symptoms: ["digestive_sluggishness"],
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
            symptoms: ["muscle_pain", "low_blood_pressure"],
            usage: "學習或工作時擴香；加入洗髮精中護理頭皮。",
            ritual: "在工作桌旁擴香，挺直脊椎，每一次吸氣都想像氧氣正在點亮你大腦中的每一個細胞。",
            caution: "高血壓與癲癇患者應避免使用；懷孕初期不建議使用。",
            color: "#4a5d4e"
        }
    ],
    symptoms: [
        { id: "headache", name: "頭痛 / 偏頭痛", icon: "🧠" },
        { id: "nasal_congestion", name: "鼻塞 / 呼吸不暢", icon: "👃" },
        { id: "insomnia", name: "失眠 / 難以入睡", icon: "🌙" },
        { id: "muscle_tension", name: "肌肉緊繃 / 酸痛", icon: "💪" },
        { id: "skin_irritation", name: "皮膚敏感 / 癢", icon: "✨" },
        { id: "digestive_issues", name: "消化不良 / 脹氣", icon: "🍵" }
    ],
    moods: [
        { id: "anxiety", name: "焦慮 / 緊張", icon: "😟" },
        { id: "stress", name: "壓力過大", icon: "😫" },
        { id: "fatigue", name: "疲勞 / 沒精神", icon: "🔋" },
        { id: "depression", name: "情緒低落 / 憂鬱", icon: "☁️" },
        { id: "confusion", name: "思緒混亂 / 分心", icon: "🌀" },
        { id: "sadness", name: "悲傷 / 難過", icon: "💧" }
    ],
    recipes: [
        {
            title: "深度助眠配方",
            oils: ["薰衣草 3滴", "佛手柑 2滴"],
            description: "適合在睡前 30 分鐘進行擴香，營造寧靜的睡眠環境。"
        },
        {
            title: "高效辦公配方",
            oils: ["歐薄荷 2滴", "迷迭香 2滴", "甜橙 1滴"],
            description: "提升專注力，保持頭腦清醒，同時緩解工作帶來的緊繃感。"
        },
        {
            title: "呼吸道淨化配方",
            oils: ["尤加利 3滴", "乳香 2滴"],
            description: "在感冒流行期間或空氣不佳時使用，能幫助呼吸順暢並淨化空間。"
        },
        {
            title: "陽光好心情配方",
            oils: ["甜橙 3滴", "佛手柑 2滴"],
            description: "驅散陰霾心情，帶來溫暖與喜悅的氛圍。"
        }
    ]
};

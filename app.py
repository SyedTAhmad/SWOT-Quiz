import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ------------------ PAGE STATE ------------------
if "page" not in st.session_state:
  st.session_state.page = "main"
if "score" not in st.session_state:
  st.session_state.score = 0

# Navigation callbacks
def go_main():
    st.session_state.page = "main"

def go_q1():
    st.session_state.page = "question1"

def go_q2():
    st.session_state.page = "question2"

def go_q3():
    st.session_state.page = "question3"

def go_summary():
    st.session_state.page = "summary"

# ===================== MAIN PAGE =====================
def main_page():

    if "q1Score" in st.session_state:
       st.session_state.q1Score = None
       st.session_state.q2Score = None
       st.session_state.q3Score = None
    
    if "totalScore" not in st.session_state:
        score = 0
    else:
        score = st.session_state.totalScore
    
    st.title("Main Menu")
    st.write("")
    st.write("")
    st.button("Lesson 1: SWOT Analysis", on_click=go_q1)
    if score<13:
        st.button("Lesson 2:...", disabled=True)
    else:
        st.button("Lesson 2: Setting Strategic Goals")
    
    if score<18:
        st.button("Lesson 3:...", disabled=True)
    else:
        st.button("Lesson 3: Advanced Competitive Strategy")
    st.button("Lesson 4: ...", disabled=True)
    st.button("Lesson 5: ...", disabled=True)
    st.button("Lesson 6: ...", disabled=True)
    st.write("")
    st.button("Next Module", disabled=True)

# ===================== QUESTION 1 PAGE =====================

def question1_page():
    q1_component = st.components.v2.component(
        "q1",
        html="""
    <div id="root"></div>

    <style>
    body { background-color: #fff; color: #000; font-family: sans-serif; }
    .outer-row { width: 100%; display:flex; justify-content:center; margin-bottom:20px; }
    .box-row { display:flex; align-items:center; gap:12px; }
    .label { font-weight:600; width:20px; text-align:right; }
    .drop-box { width:150px; height:56px; background:#e0e0e0; border-radius:6px; display:flex;
                justify-content:center; align-items:center; padding:4px; }
    #pool {
        background:#e0e0e0;
        padding:12px;
        border-radius:6px;
        display:flex; flex-wrap:wrap; gap:12px;
        justify-content: center; align-items: center;
        min-height:100px; margin-top:20px;
    }
    .item {
        background:#b0b0b0;
        color:#000;
        font-weight:bold;
        min-width:100px; height:48px;
        border-radius:6px;
        display:flex; justify-content:center; align-items:center;
        cursor:grab; user-select:none;
        padding:0 10px; transition: background-color 0.2s ease;
        position: relative; /* allow z-index if needed */
    }
    .correct { background:#2ecc71 !important; cursor: default !important; }
    .wrong { background:#e74c3c !important; cursor: default !important; }
    #submit-btn { margin-top:20px; padding:10px 20px; font-size:16px; border-radius:6px; border:none;
                    background:#6e8575; cursor:pointer; }
    #submit-btn:disabled { background:#cccccc; cursor: not-allowed; }
    #answer-key { margin-top:20px; font-weight:bold; font-size:20px; }
    .swot-description { font-size:16px; margin-bottom:12px; }
    </style>

    <div id="content">
    <div class="outer-row">
        <div class="box-row">
        <div class="label">S:</div> <div id="box_S" class="drop-box"></div>
        <div class="label">W:</div> <div id="box_W" class="drop-box"></div>
        <div class="label">O:</div> <div id="box_O" class="drop-box"></div>
        <div class="label">T:</div> <div id="box_T" class="drop-box"></div>
        </div>
    </div>

    <h4 style="margin-top: 50px; font-size: 20px;">What does SWOT stand for</h4>
    <div id="pool"></div>

    <button id="submit-btn" disabled>Submit</button>
    <div id="answer-key"></div>
    </div>
        """,

        js="""
    import Sortable from "https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/modular/sortable.esm.js";

    export default function(component) {
        const { setTriggerValue } = component;

        const correctMap = {
            "S": "Strengths",
            "W": "Weaknesses",
            "O": "Opportunities",
            "T": "Threats"
        };

        const items = ["Strategy", "Weaknesses", "Opportunities", "Outlook", "Threats",
            "Team", "Objectives", "Strengths", "Tactics"];

        const pool = component.parentElement.querySelector("#pool");

        // Create items
        items.forEach(t => {
            const el = document.createElement("div");
            el.className = "item";
            el.setAttribute("draggable", "true");
            el.innerText = t;
            pool.appendChild(el);
        });

        const boxLabels = ["S", "W", "O", "T"];

        function elementChildren(el) {
            return Array.from(el.children).filter(n => n.nodeType === 1);
        }

        function checkAllFull() {
            return boxLabels.every(l => elementChildren(component.parentElement.querySelector("#box_" + l)).length > 0);
        }

        function refreshButton() {
            component.parentElement.querySelector("#submit-btn").disabled = !checkAllFull();
        }

        function handleBoxAdd(evt) {
            const box = evt.to;
            const kids = elementChildren(box);
            if (kids.length > 1) {
                const newItem = evt.item;
                kids.forEach(el => {
                    if (el !== newItem) pool.appendChild(el);
                });
            }
            refreshButton();
        }

        // Pool sortable
        const poolSortable = new Sortable(pool, {
            group: { name: "shared", pull: true, put: true },
            animation: 150,
            onAdd: refreshButton,
            onRemove: refreshButton
        });

        // Box sortables
        const boxSortables = {};
        boxLabels.forEach(l => {
            boxSortables[l] = new Sortable(component.parentElement.querySelector("#box_" + l), {
                group: { name: "shared", pull: true, put: true },
                animation: 150,
                onAdd: handleBoxAdd
            });
        });

        component.parentElement.querySelector("#submit-btn").addEventListener("click", () => {
            let score = 0;

            // Lock all cards and mark correct/wrong
            boxLabels.forEach(l => {
                const box = component.parentElement.querySelector("#box_" + l);
                const child = elementChildren(box)[0];
                if (!child) return;

                if (child.textContent.trim() === correctMap[l]) {
                    child.classList.add("correct");
                    score += 1;
                } else {
                    child.classList.add("wrong");
                }
                child.removeAttribute("draggable");
            });

            // Lock all pool items
            elementChildren(pool).forEach(k => k.removeAttribute("draggable"));

            // Disable all Sortable instances
            poolSortable.option("disabled", true);
            boxLabels.forEach(l => boxSortables[l].option("disabled", true));

            setTriggerValue("score", score);
        });
    }
        """
    )

    # ---------------------------------------------------------------------
    # Use component inside Streamlit
    # ---------------------------------------------------------------------
    st.title("Level 1: What does SWOT stand for?")
    st.write("")  # adds small vertical spacing
    st.write("")  # repeat for more spacing
    st.write("")  # adds small vertical spacing

    response = q1_component(key="q1")

    if response and hasattr(response, "score"):
        st.session_state.q1Score = response.score
    #Print Score
    if st.session_state.get("q1Score", None)==None:
       st.write("Score: -/4")
    else:
      st.write("Score:", str(st.session_state.get("q1Score", None))+"/4")
    #Button Logic
    st.button("Continue", on_click=go_q2, disabled=st.session_state.get("q1Score", None) is None)

# ===================== QUESTION 2 PAGE =====================

def question2_page():

    # ---------------------------------------------------------------------
    # Define Component
    # ---------------------------------------------------------------------
    q2_component = st.components.v2.component(
        "q2",
        html="""
    <div id="root"></div>

    <style>
    body { background-color: #fff; color: #000; font-family: sans-serif; }


    .box-label {
    position: relative;
    z-index: 1; /* Ensure it appears above the background emoji */
    font-size: 16px;
    margin-bottom: 10px;
    text-align: center;
    padding: 2px;
    }

    .outer-row {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .box-row {
        display: flex;
        align-items: stretch;
        gap: 10px;
    }

    .drop-box {
        width: 280px;
        min-height: 300px;
        display:flex;
        flex-direction: column;
        justify-content:center; /* Center vertically */
        align-items:center;
        border-radius:14px;
        padding:10px;
        text-align:center;
        font-size:16px;
        position: relative;
    }

    /* Pastel colors */
    #box_S { background:#aecbff; }   /* Soft blue */
    #box_W { background:#ffb3b3; }   /* Light red */
    #box_O { background:#c4f4c2; }   /* Pastel green */
    #box_T { background:#fff5a8; }   /* Pastel yellow */

    /* White star on blue square */
    #box_S::after {
        content: "★";
        color: white;
        font-size: 200px; /* Larger size */
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Center perfectly */
        pointer-events: none;
        z-index: 0;
    }
    #box_W::after {
        content: "⛓️‍💥";
        font-size: 200px; /* Adjust size as needed */
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Center perfectly */
        pointer-events: none;
        filter: brightness(0) invert(1); /* Makes the emoji white */
        z-index: 0;
    }
    #box_O::after {
        content: "☀️";
        font-size: 200px; /* Adjust size as needed */
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Center perfectly */
        pointer-events: none;
        filter: brightness(0) invert(1); /* Makes the emoji white */
        z-index: 0;
    }
    #box_T::after {
        content: "❗";
        font-size: 200px; /* Adjust size as needed */
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Center perfectly */
        pointer-events: none;
        filter: brightness(0) invert(1); /* Makes the emoji white */
        z-index: 0;
    }
    #pool {
        background:#f0f0f0;
        padding:16px;
        border-radius:6px;
        display:flex;
        flex-wrap:wrap;
        gap:18px;
        justify-content:center;
        align-items:center;
        min-height:200px;
        margin-top:30px;
    }

    .item {
        background:#dedede;
        color:#000;
        font-weight:bold;
        font-size:16px;
        min-width:200px;
        max-width:220px;
        height:auto;
        border-radius:10px;
        display:flex;
        justify-content:center;
        align-items:center;
        cursor:grab;
        user-select:none;
        padding:12px;
        margin-bottom:10px;
        transition: background-color 0.2s ease;
        word-wrap: break-word;
        z-index: 1;
    }

    .correct { background:#8be39a !important; cursor: default !important; }
    .wrong { background:#f28b82 !important; cursor: default !important; }

    #submit-btn {
        margin-top:26px;
        padding:12px 22px;
        font-size:18px;
        border-radius:10px;
        border:none;
        background:#6e8575;
        cursor:pointer;
    }

    #submit-btn:disabled { background:#cccccc; cursor: not-allowed; }
    </style>

    <div id="content">
        <div class="outer-row">
            <div class="outer-row">
                <div class="box-row">
                    <div class="box-wrapper">
                        <div class="box-label"><strong>Strengths:</strong> Positive attributes and resources inside your business that you can control.</div>
                        <div id="box_S" class="drop-box"></div>
                    </div>
                    <div class="box-wrapper">
                        <div class="box-label"><strong>Weaknesses:</strong> Negative factors inside your business that are in your control to improve.</div>
                        <div id="box_W" class="drop-box"></div>
                    </div>
                    <div class="box-wrapper">
                        <div class="box-label"><strong>Opportunities:</strong> Favorable factors in the world you could use to your advantage.</div>
                        <div id="box_O" class="drop-box"></div>
                    </div>
                    <div class="box-wrapper">
                        <div class="box-label"><strong>Threats:</strong> Unfavorable factors in the outside world that could harm your business.</div>
                        <div id="box_T" class="drop-box"></div>
                    </div>
                </div>
            </div>
        </div>


        <h4 style="margin-top: 50px; font-size: 20px;">Drag the statements into the correct squares (2 per square)</h4>
        <div id="pool"></div>
        <button id="submit-btn" disabled>Submit</button>
    </div>
        """,

        js="""
    import Sortable from "https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/modular/sortable.esm.js";

    export default function(component) {
        const { setTriggerValue } = component;
        const boxLabels = ["S", "W", "O", "T"];

        // Cards and their correct boxes
        const cardMap = {
            "Our company has a strong, recognizable brand name and loyal customer base.": "S",
            "A new government regulation will increase the cost of our raw materials.": "T",
            "A new social media trend is making our type of product very popular.": "O",
            "Our company's website is outdated and difficult for customers to use.": "W",
            "A major competitor in our area just went out of business.": "O",
            "Our team has proprietary, patented technology that nobody else has.": "S",
            "A new, well-funded competitor is entering the market.": "T",
            "We have a high level of debt and struggle with cash flow.": "W"
        };

        const items = Object.keys(cardMap);
        const pool = component.parentElement.querySelector("#pool");

        // Create cards
        items.forEach(t => {
            const el = document.createElement("div");
            el.className = "item";
            el.setAttribute("draggable", "true");
            el.innerText = t;
            pool.appendChild(el);
        });

        function elementChildren(el) {
            return Array.from(el.children).filter(n => n.nodeType === 1);
        }

        function checkAllFull() {
            const allBoxesFull = boxLabels.every(l =>
                elementChildren(component.parentElement.querySelector("#box_" + l)).length === 2
            );
            const allCardsUsed = elementChildren(pool).length === 0;
            return allBoxesFull && allCardsUsed;
        }

        function refreshButton() {
            component.parentElement.querySelector("#submit-btn").disabled = !checkAllFull();
        }

        function handleBoxAdd(evt) {
            const box = evt.to;
            const kids = elementChildren(box);

            // Reject if more than 2 cards
            if (kids.length > 2) {
                const newItem = evt.item;
                pool.appendChild(newItem);
            }
            refreshButton();
        }

        // Pool sortable
        const poolSortable = new Sortable(pool, {
            group: { name: "shared", pull: true, put: true },
            animation: 150,
            onAdd: refreshButton,
            onRemove: refreshButton
        });

        // Box sortables
        const boxSortables = {};
        boxLabels.forEach(l => {
            boxSortables[l] = new Sortable(component.parentElement.querySelector("#box_" + l), {
                group: { name: "shared", pull: true, put: true },
                animation: 150,
                onAdd: handleBoxAdd
            });
        });

        // Submit button
        component.parentElement.querySelector("#submit-btn").addEventListener("click", () => {
            let score = 0;
            boxLabels.forEach(l => {
                const box = component.parentElement.querySelector("#box_" + l);
                const kids = elementChildren(box);
                kids.forEach(k => {
                    k.removeAttribute("draggable");
                    if (cardMap[k.innerText] === l) {
                        k.classList.add("correct");
                        score += 1;
                    } else {
                        k.classList.add("wrong");
                    }
                });
            });

            // Lock pool and boxes
            elementChildren(pool).forEach(k => k.removeAttribute("draggable"));
            poolSortable.option("disabled", true);
            boxLabels.forEach(l => boxSortables[l].option("disabled", true));

            // Send score
            setTriggerValue("score", score);
        });
    }
        """
    )

    # ---------------------------------------------------------------------
    # Use component inside Streamlit
    # ---------------------------------------------------------------------
    st.title("Level 2: Know the Matrix")
    st.write("")  # adds small vertical spacing
    st.write("")  # repeat for more spacing
    st.write("")  # adds small vertical spacing
    st.write("")  # repeat for more spacing

    if "q2Score" not in st.session_state:
        st.session_state.q2Score = None

    response = q2_component(key="q2")

    if response and hasattr(response, "score"):
        st.session_state.q2Score = response.score

    #Print Score
    if st.session_state.get("q2Score", None)==None:
       st.write("Score: -/8")
    else:
      st.write("Score:", str(st.session_state.get("q2Score", None))+"/8")

    st.button("Continue", on_click=go_q3,
        disabled=(st.session_state.get("q2Score", None) is None))

# ===================== QUESTION 3 PAGE =====================

def question3_page():

    # -------------------------
    # COMPONENT
    # -------------------------
    q3_component = st.components.v2.component(
        "q3",
        html="""
<div id="root"></div>

<style>
body { background-color: #fff; color: #000; font-family: sans-serif; margin:0; }

.container {
    display: flex;
    gap: 20px;
    width: 100%;
    margin-top: 20px;
    height: 90vh;
}

#left-section {
    flex: 1.5;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

#top-dossier, #bottom-drag {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    border: 1px solid #ccc;
    border-radius: 6px;
}

#top-dossier .title {
    font-weight: bold;
    margin-bottom: 8px;
}

#bottom-drag {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: flex-start;
}

.drag-item {
    cursor: grab;
    user-select: none;
    font-weight: bold;
    font-size:16px;
    padding: 8px 12px;
    background: #dedede;
    border-radius: 6px;
    min-width: 150px;
    text-align: center;
    margin: 4px;
    border: 2px solid transparent;
}

.correct { background:#8be39a !important; cursor: default !important; border-color:#4caf50 !important; }
.wrong { background:#f28b82 !important; cursor: default !important; border-color:#e53935 !important; }

#sections {
    flex: 3;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    width: 100%;
    height: 100%;
}

.box-wrapper {
    position: relative;
}

.drop-box {
    width: 100%;
    height: 100%;
    padding-top: 30px;
    box-sizing: border-box;
    position: relative;
}

.box-label {
    position: absolute;
    top: 0;
    width: 100%;
    text-align: center;
    font-weight: bold;
    font-size: 20px;
    padding: 4px 0;
    pointer-events: none;
}

.drop-box-inner {
    width: 100%;
    height: 100%;
    padding: 12px;
    box-sizing: border-box;
}

#box_S { background:#aecbff; }
#box_W { background:#ffb3b3; }
#box_O { background:#c4f4c2; }
#box_T { background:#fff5a8; }

#submit-btn {
    margin-top:20px;
    padding:10px 20px;
    font-size:16px;
    border-radius:6px;
    border:none;
    background:#6e8575;
    cursor:pointer;
}
#submit-btn:disabled { background:#cccccc; cursor: not-allowed; }
</style>

<div class="container">
    <div id="left-section">
        <div id="top-dossier">
            <div class="title">Dossier</div>
            <p><b>Company Profile:</b> Wanderlust Coffee is a single-location coffee shop in a busy downtown area, known for its ethically sourced beans and cozy atmosphere.</p>
            <p><b>Internal Memo:</b> Team Morale Report: Our baristas are highly trained and have a great rapport with customers. However, our point-of-sale system is slow and frequently crashes, leading to long lines during peak hours.</p>
            <p><b>Market News:</b> Industry Trend Report: There is a growing city-wide demand for mobile app ordering and delivery. Additionally, the city council recently approved a new office tower development two blocks away.</p>
            <p><b>Competitor Alert:</b> A large, international coffee chain, GlobalBean, is planning to open a new location on the same street within six months.</p>
        </div>
    <div id="bottom-drag"></div>
</div>

    <div id="sections">
        <div class="box-wrapper">
            <div id="box_S" class="drop-box">
                <div class="box-label">Strengths</div>
                <div class="drop-box-inner"></div>
            </div>
        </div>

        <div class="box-wrapper">
            <div id="box_W" class="drop-box">
                <div class="box-label">Weaknesses</div>
                <div class="drop-box-inner"></div>
            </div>
        </div>

        <div class="box-wrapper">
            <div id="box_O" class="drop-box">
                <div class="box-label">Opportunities</div>
                <div class="drop-box-inner"></div>
            </div>
        </div>

        <div class="box-wrapper">
            <div id="box_T" class="drop-box">
                <div class="box-label">Threats</div>
                <div class="drop-box-inner"></div>
            </div>
        </div>
    </div>
</div>

<button id="submit-btn" disabled>Submit</button>
        """,

        js=r"""
import Sortable from "https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/modular/sortable.esm.js";

export default function(component) {
    // use key/value setTriggerValue form (same as your working q2)
    const { setTriggerValue } = component;

    const phrases = [
        "Highly trained baristas",
        "Cozy atmosphere and loyal customers",
        "Slow and outdated point-of-sale system",
        "No mobile app or delivery option",
        "New office tower being built nearby",
        "Growing demand for mobile ordering",
        "GlobalBean chain opening on the same street",
        "Rising cost of ethically sourced beans"
    ];

    const correctMap = {
        "Growing demand for mobile ordering": "O",
        "Highly trained baristas": "S",
        "Slow and outdated point-of-sale system": "W",
        "Cozy atmosphere and loyal customers": "S",
        "No mobile app or delivery option": "W",
        "GlobalBean chain opening on the same street": "T",
        "New office tower being built nearby": "O",
        "Rising cost of ethically sourced beans": "T"
    };

    const bottom = component.parentElement.querySelector("#bottom-drag");

    // Create draggable items
    phrases.forEach(t => {
        const el = document.createElement("div");
        el.className = "drag-item";
        el.innerText = t;
        el.setAttribute("draggable", "true");
        bottom.appendChild(el);
    });

    const labels = ["S","W","O","T"];

    const countCards = box =>
        Array.from(box.children).filter(el => el.classList && el.classList.contains("drag-item")).length;

    const refresh = () => {
        const placed =
            labels.reduce((acc,l)=> acc + countCards(component.parentElement.querySelector("#box_" + l + " .drop-box-inner")), 0);
        component.parentElement.querySelector("#submit-btn").disabled = (placed !== phrases.length);
    };

    // Make pool sortable and keep reference so we can disable later
    const poolSortable = new Sortable(bottom, {
        group: { name:"swot", pull:true, put:true },
        animation:150,
        onAdd: refresh,
        onRemove: refresh
    });

    // Make boxes sortable and save references
    const boxSortables = {};
    labels.forEach(l => {
        boxSortables[l] = new Sortable(
            component.parentElement.querySelector("#box_" + l + " .drop-box-inner"),
            {
                group:{ name:"swot", pull:true, put:true },
                animation:150,
                onAdd: refresh,
                onRemove: refresh
            }
        );
    });

    // Submit handler with colouring + lock
    component.parentElement.querySelector("#submit-btn").addEventListener("click", () => {
        let score = 0;

        labels.forEach(l => {
            const box = component.parentElement.querySelector("#box_" + l + " .drop-box-inner");

            Array.from(box.children).forEach(card => {
                const text = card.innerText.trim();
                if (correctMap[text] === l) {
                    score += 1;
                    card.classList.add("correct");
                } else {
                    card.classList.add("wrong");
                }

                // lock visual + draggable
                card.removeAttribute("draggable");
                card.style.cursor = "default";
            });
        });

        // disable dragging entirely
        poolSortable.option("disabled", true);
        labels.forEach(l => boxSortables[l].option("disabled", true));

        // send the score using key/value style identical to q2
        setTriggerValue("score", score);
    });
}
        """
    )

    # -------------------------
    # STREAMLIT SIDE
    # -------------------------
    st.title("Level 3: The Strategist Challenge")
    st.write("")
    st.write("")
    st.write("""
<span style="font-size:20px;">
<strong>Scenario:</strong> You have been hired as a consultant for Wanderlust Coffee, a local coffee shop. 
Your first task is to analyze their business and present a full SWOT analysis. Read the briefing materials carefully.
</span>
""", unsafe_allow_html=True)

    if "q3Score" not in st.session_state:
        st.session_state.q3Score = None

    response = q3_component(key="q3")

    # q2 used response.score style; here we mirror that
    if response and hasattr(response, "score"):
        st.session_state.q3Score = response.score

    #Print Score
    if st.session_state.get("q3Score", None)==None:
       st.write("Score: -/8")
    else:
      st.write("Score:", str(st.session_state.get("q3Score", None))+"/8")
    #Button Logic
    st.button("Continue", on_click=go_summary, disabled=st.session_state.get("q3Score", None) is None)

# ===================== SUMMARY PAGE ========================

def summary_page():
    st.title("Summary")
    st.write("")  # spacing

    st.session_state.totalScore = st.session_state.q1Score + st.session_state.q2Score + st.session_state.q3Score
    totalScore = st.session_state.totalScore
    # Determine message based on score
    if totalScore <= 12:
        result_message = """
        You have built a great starting point. This path focused on reinforcing the core building blocks of the SWOT analysis to set you up for success. 
        Reviewing the levels again is a great next step to solidify your knowledge.
        """
    elif 13 <= totalScore <= 17:
        result_message = """
        Great job! You have a solid grasp of the SWOT framework. You are now ready to learn how to turn your analysis into action. 
        Your recommended next module is Setting Strategic Goals.
        """
    else:  # 18-20
        result_message = """
        Exceptional work! You have mastered strategic analysis and are ready for a new challenge. 
        Your recommended next module is Advanced Competitive Strategy.
        """

    # Create two columns: Scores | Result
    col1, col2 = st.columns([1, 2])

    # --------------------------
    # Left column: Scores
    # --------------------------
    with col1:
        st.markdown(f"""
        <div style='
            background-color:#f0f0f0;
            padding:20px;
            border-radius:12px;
            text-align:center;
        '>
            <h3 style='font-size:22px; margin-bottom:15px;'>Your Scores</h3>
            <p style='font-size:20px; margin:5px 0;'>Level 1: <strong>{st.session_state.q1Score}</strong> / 4</p>
            <p style='font-size:20px; margin:5px 0;'>Level 2: <strong>{st.session_state.q2Score}</strong> / 8</p>
            <p style='font-size:20px; margin:5px 0;'>Level 3: <strong>{st.session_state.q3Score}</strong> / 8</p>
            <hr style='margin:10px 0;'>
            <p style='font-size:22px; font-weight:bold;'>Total: {totalScore} / 20</p>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------
    # Right column: Result Message
    # --------------------------
    with col2:
        st.markdown(f"""
        <div style='
            background-color:#ffffff;
            padding:20px;
            border-radius:12px;
            border:1px solid #ccc;
        '>
            <h3 style='font-size:22px; margin-bottom:15px;'>Result</h3>
            <p style='font-size:20px;'>{result_message}</p>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.button("Main Menue", on_click=go_main)

# ===================== ROUTER =====================
if st.session_state.page == "main":
  main_page()
elif st.session_state.page == "question1":
  question1_page()
elif st.session_state.page == "question2":
  question2_page()
elif st.session_state.page == "question3":
  question3_page()
elif st.session_state.page == "summary":
  summary_page()

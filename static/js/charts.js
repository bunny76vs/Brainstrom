// =====================================================
// READ URL PARAMETERS
// =====================================================
const params = new URLSearchParams(window.location.search);
const stream = params.get("stream");        // science / commerce / arts
const percentage = parseFloat(params.get("percentage"));

console.log("Stream:", stream);
console.log("Percentage:", percentage);

// =====================================================
// LOAD COURSES BASED ON STREAM
// =====================================================
const courseSelect = document.getElementById("courseSelect");
const output = document.getElementById("output");

fetch(`/api/courses/${stream}`)
    .then(res => res.json())
    .then(courses => {
        courseSelect.innerHTML = `<option value="">Select Course</option>`;

        courses.forEach(course => {
            const opt = document.createElement("option");
            opt.value = course;
            opt.textContent = course;
            courseSelect.appendChild(opt);
        });
    })
    .catch(err => {
        console.error("Error loading courses:", err);
        courseSelect.innerHTML = `<option>Error loading courses</option>`;
    });

// =====================================================
// ON COURSE CHANGE → LOAD COLLEGES & DRAW CHARTS
// =====================================================
courseSelect.addEventListener("change", async function () {

    const course = this.value;
    if (!course) return;

    output.innerHTML = ""; // clear previous cards

    const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            stream: stream,
            course: course,
            percentage: percentage
        })
    });

    const colleges = await res.json();

    if (!Array.isArray(colleges) || colleges.length === 0) {
        output.innerHTML = `<p>No colleges found for this selection.</p>`;
        return;
    }

    // =====================================================
    // CREATE COLLEGE CARDS & PIE CHARTS (SAFE METHOD)
    // =====================================================
    colleges.forEach((c, i) => {

        // ---- card ----
        const card = document.createElement("div");
        card.className = "college-card";

        // ---- title ----
        const title = document.createElement("h3");
        title.textContent = c.college;

        // ---- canvas ----
        const canvas = document.createElement("canvas");
        canvas.width = 240;
        canvas.height = 240;

        card.appendChild(title);
        card.appendChild(canvas);
        output.appendChild(card);

        // ---- chart ----
        new Chart(canvas, {
            type: "pie",
            data: {
                labels: ["Fees", "Infrastructure", "Placements"],
                datasets: [{
                    data: [c.fees, c.infra, c.placement],
                    backgroundColor: [
                        "#ef4444", // fees
                        "#3b82f6", // infra
                        "#22c55e"  // placement
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    });
});

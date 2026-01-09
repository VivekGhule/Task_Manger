//Task_Manager\static\meeting.js
document.addEventListener("DOMContentLoaded", () => {
    setupTabs();
    loadMeetings();

    const form = document.getElementById("addMeetingForm");
    if (form) {
        form.addEventListener("submit", handleMeetingSubmit);
    }

    // Meeting filter buttons
    document.querySelectorAll(".meeting-filter-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".meeting-filter-btn")
                .forEach((b) => b.classList.remove("bg-purple-600", "text-white"));

            btn.classList.add("bg-purple-600", "text-white");
            loadMeetings(btn.dataset.filter);
        });
    });
});

/* ---------------- CATEGORY BADGE ---------------- */
function getCategoryBadge(category) {
    const safeCategory = (category || "other").toLowerCase();
    const categories = {
        work: "💼 Work",
        personal: "👤 Personal",
        team: "👥 Team",
        client: "🤝 Client",
        other: "📌 Other"
    };
    const label = categories[safeCategory] || categories.other;

    return `
        <span class="inline-block px-3 py-1 bg-gray-100 dark:bg-gray-700
            text-gray-700 dark:text-gray-300 rounded-full text-xs font-semibold">
            ${label}
        </span>
    `;
}

/* ---------------- TAB SYSTEM ---------------- */
function setupTabs() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetTab = btn.dataset.tab;

            tabButtons.forEach((b) => {
                b.classList.remove("active", "text-indigo-600", "border-b-2", "border-indigo-600");
                b.classList.add("text-gray-600");
            });

            btn.classList.add("active", "text-indigo-600", "border-b-2", "border-indigo-600");
            btn.classList.remove("text-gray-600");

            tabContents.forEach((content) => (content.style.display = "none"));
            const targetContent = document.getElementById(`${targetTab}-content`);
            if (targetContent) targetContent.style.display = "block";
        });
    });
}

/* ---------------- CREATE MEETING ---------------- */
async function handleMeetingSubmit(e) {
    e.preventDefault();

    const payload = {
        title: document.getElementById("meetingTitle").value.trim(),
        category: document.getElementById("meetingCategory").value,
        meeting_date: document.getElementById("meetingDate").value,
        meeting_time: document.getElementById("meetingTime").value,
        duration: parseInt(document.getElementById("meetingDuration").value || 60),
        meeting_link: document.getElementById("meetingLink").value.trim(),
        description: document.getElementById("meetingDescription").value.trim()
    };

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

    try {
        const response = await fetch("/meetings/api/meetings/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            alert("Meeting scheduled successfully");
            e.target.reset();
            loadMeetings(); // Refresh list
        } else {
            alert(data.error || "Failed to create meeting");
        }
    } catch (err) {
        console.error(err);
        alert("Server error occurred");
    }
}

/* ---------------- DELETE MEETING ---------------- */
// Fix: Exposed to window so the 'onclick' in HTML string can find it
window.deleteMeeting = async function(meetingId) {
    if (!confirm("Are you sure you want to delete this meeting?")) return;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

    try {
        const response = await fetch(`/meetings/api/meetings/${meetingId}/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": csrfToken }
        });

        if (response.ok) {
            loadMeetings(); 
        } else {
            const data = await response.json();
            alert(data.error || "Failed to delete meeting");
        }
    } catch (err) {
        console.error("Delete error:", err);
    }
};

/* ---------------- LOAD MEETINGS ---------------- */
function loadMeetings(filter = "all") {
    fetch("/meetings/api/meetings/")
        .then((res) => res.json())
        .then((data) => {
            const container = document.getElementById("meetingsContainer");
            const emptyState = document.getElementById("emptyStateMeetings");

            const meetings = data.meetings || data || [];
            container.innerHTML = "";

            const now = new Date();
            let counts = { total: 0, upcoming: 0, past: 0, visible: 0 };

            meetings.forEach((m) => {
                // Handle different ID formats (Django vs MongoDB)
                const id = m.id || m._id;
                
                // Better Date Parsing (ISO replacement for Safari compatibility)
                const meetingDateTime = new Date(`${m.meeting_date}T${m.meeting_time}`);
                
                const isPast = meetingDateTime < now;
                const isUpcoming = meetingDateTime >= now;

                // Update Stats
                counts.total++;
                if (isUpcoming) counts.upcoming++;
                if (isPast) counts.past++;

                // Apply Filtering
                if (filter === "upcoming" && !isUpcoming) return;
                if (filter === "past" && !isPast) return;

                counts.visible++;

                const div = document.createElement("div");
                div.className = "bg-white dark:bg-gray-800 p-5 rounded-2xl shadow-sm border flex flex-col gap-3 mb-4";

               div.innerHTML = `
  <div class="flex justify-between items-start gap-4">
    <!-- Left Content -->
    <div class="flex-1 min-w-0">
      <div class="flex flex-wrap items-center gap-2 mb-1">
        <h4 class="font-semibold text-lg text-gray-800 dark:text-white truncate">
          ${m.title}
        </h4>
        ${getCategoryBadge(m.category)}
      </div>

      <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mt-1">
        <span class="flex items-center gap-1">📅 ${m.meeting_date}</span>
        <span class="flex items-center gap-1">⏰ ${m.meeting_time}</span>
        ${
          m.duration
            ? `<span class="flex items-center gap-1">⏱️ ${m.duration} min</span>`
            : ""
        }
      </div>

      ${
        m.description
          ? `
            <p class="mt-3 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
              ${m.description}
            </p>
          `
          : `
            <p class="mt-3 text-xs italic text-gray-400">
              No description provided
            </p>
          `
      }
    </div>

    <!-- Actions -->
    <div class="flex gap-2 shrink-0">
      ${
        m.meeting_link
          ? `
            <a href="${m.meeting_link}" target="_blank"
              class="inline-flex items-center gap-1 bg-purple-600 hover:bg-purple-700
                     text-white px-4 py-2 rounded-lg text-sm font-medium transition">
              Join
            </a>
          `
          : ""
      }

      <button
        onclick="deleteMeeting('${id}')"
        class="inline-flex items-center gap-1 bg-red-500 hover:bg-red-600
               text-white px-4 py-2 rounded-lg text-sm font-medium transition">
        Delete
      </button>
    </div>
  </div>
`;

                container.appendChild(div);
            });

            // Update UI Counters
            if(document.getElementById("totalMeetings")) document.getElementById("totalMeetings").innerText = counts.total;
            if(document.getElementById("upcomingMeetings")) document.getElementById("upcomingMeetings").innerText = counts.upcoming;
            if(document.getElementById("pastMeetings")) document.getElementById("pastMeetings").innerText = counts.past;

            // Toggle Empty State
            if (emptyState) {
                counts.visible === 0 ? emptyState.classList.remove("hidden") : emptyState.classList.add("hidden");
            }
        })
        .catch((err) => console.error("Fetch error:", err));
}
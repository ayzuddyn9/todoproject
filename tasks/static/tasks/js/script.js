document.addEventListener("DOMContentLoaded", () => {
  const csrftoken = getCookie("csrftoken");

  document.querySelectorAll("li").forEach(item => {
    item.addEventListener("click", () => {
      const id = item.dataset.id;

      fetch(`/toggle/${id}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          const isComplete = data.complete;

          // Toggle visual state
          item.classList.toggle("completed", isComplete);

          // Find and replace the emoji
          let emoji = item.querySelector(".emoji");
          if (emoji) {
            emoji.textContent = isComplete ? "✅" : "❌";
          }
        } else {
          console.error("Error:", data.message);
        }
      })
      .catch(err => console.error("Error:", err));
    });
  });
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

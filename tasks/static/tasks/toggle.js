document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toggle-task").forEach((icon) => {
    icon.addEventListener("click", async () => {
      const li = icon.closest("li");
      const taskId = li.dataset.taskId;

      try {
        const response = await fetch(`/toggle/${taskId}/`);
        const data = await response.json();

        // Update the icon without refreshing
        icon.textContent = data.complete ? "✅" : "❌";
      } catch (error) {
        console.error("Error toggling task:", error);
      }
    });
  });
});

document.getElementById("careerForm").addEventListener("submit", function(e) {
  e.preventDefault();

  let education = document.getElementById("education").value;
  let stream = document.getElementById("stream").value;
  let percentage = document.getElementById("percentage").value;

  let url = `result.html?education=${education}&stream=${stream}&percentage=${percentage}`;
  window.open(url, "_blank");
});

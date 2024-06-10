document.getElementById("surveyForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission

  const email = document.getElementById("email").value.trim();
  const resultsDiv = document.getElementById("results");

  // Basic email validation
  if (!validateEmail(email)) {
      resultsDiv.innerHTML = "Por favor, ingrese un correo electrónico válido.";
      return;
  }

  // Check if a team was selected
  if (!document.querySelector('input[name="team"]:checked')) {
      resultsDiv.innerHTML = "Por favor, seleccione un equipo.";
      return;
  }

  this.submit(); // If validation passes, submit the form
});

function validateEmail(email) {
  if (email.length < 7 || email.indexOf("@") === -1 || email.indexOf(".") === -1 ||
      email.startsWith("@") || email.endsWith("@") ||
      email.startsWith(".") || email.endsWith(".") ||
      /[!#%$]/.test(email)) {
      return false;
  }
  return true;
}

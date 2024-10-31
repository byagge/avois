document.getElementById("registerForm").onsubmit = async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const response = await fetch("{% url 'register' %}", {
    method: "POST",
    body: formData,
    headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
  });

  if (response.redirected) {
    window.location.href = response.url;
  } else {
    const html = await response.text();
    document.querySelector(".wrapper").innerHTML = html;
  }
};
  
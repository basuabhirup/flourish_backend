document.addEventListener("DOMContentLoaded", () => {
  const hostEventModal = document.querySelector('#hostEventModal');

  hostEventModal.addEventListener('shown.bs.modal', function () {
    // populate event category with relevant options from db
  });
});


// const openEvent = (e) =>{
//     const eventId = e.target.closest(".event").dataset.eventId
//     window.location = `/event/${eventId}`
// }

const backToHome = () => {
  window.location = "/";
};

const logIn = () => {
  form = document.querySelector("#loginForm");
  username = document.getElementById("loginUsername").value;
  password = document.getElementById("loginPassword").value;
  csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
  data.append("username", username);
  data.append("password", password);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  // console.log(data.get('csrfmiddlewaretoken')

  // API Call
  fetch("/login", {
    method: "POST",
    body: data,
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 200) {
      res.json().then((json) => {
        console.log(json.message);
        window.location.reload();
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
};

const signUp = () => {
  form = document.querySelector("#signUpForm");

  username = document.getElementById("signupUsername").value;
  email = document.getElementById("signupEmail").value;
  password = document.getElementById("signupPassword").value;
  confirmation = document.getElementById("signupConfirmation").value;

  csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;
  
  const data = new FormData()
  data.append("username", username);
  data.append("email", email);
  data.append("password", password);
  data.append("confirmation", confirmation);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  
  // API Call
  fetch("/register", {
    method: "POST",
    body: data,
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 200) {
      res.json().then((json) => {
        console.log(json.message);
        window.location.reload();
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
};

const logOut = () => {
  fetch("/logout", {
    method: "POST",
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 200) {
      res.json().then((json) => {
        console.log(json.message);
        window.location = '/'
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
}

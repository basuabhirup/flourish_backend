document.addEventListener("DOMContentLoaded", () => {
  const hostEventModal = document.querySelector("#hostEventModal");

  hostEventModal.addEventListener("shown.bs.modal", function () {
    // populate event category with relevant options from db
    fetch("/categories").then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          json.categories.forEach(
            (category) =>
              (hostEventModal.querySelector(
                "#eventCategory"
              ).innerHTML += `<option value=${category.id}>${category.name}</option>`)
          );
        });
      }
    });
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
  const form = document.querySelector("#loginForm");
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;
  const csrfmiddlewaretoken = form.querySelector(
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
  const form = document.querySelector("#signUpForm");

  const username = document.getElementById("signupUsername").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;
  const confirmation = document.getElementById("signupConfirmation").value;

  const csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
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
        window.location = "/";
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
};

const hostEvent = () => {
  const form = document.querySelector("#hostEventForm");

  const title = document.getElementById("eventName").value;
  const description = document.getElementById("eventDescription").value;
  const date = document.getElementById("eventDate").value;
  const time = document.getElementById("eventTime").value;
  const location = document.getElementById("eventLocation").value;
  const category = document.getElementById("eventCategory").value;
  const capacity = document.getElementById("eventCapacity").value;
  const image_url = document.getElementById("eventImage").value;

  const csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
  data.append("title", title);
  data.append("description", description);
  data.append("date", date);
  data.append("time", time);
  data.append("location", location);
  data.append("category", category);
  data.append("capacity", capacity);
  data.append("image", image_url);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  // API Call
  fetch("/create_event", {
    method: "POST",
    body: data,
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 201) {
      res.json().then((json) => {
        console.log(json.message);
        window.location = `/events/${json.event.id}`;
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
};

const createGroup = () => {
  const form = document.getElementById("createGroupForm");
  const name = document.getElementById("groupName").value;
  const description = document.getElementById("groupDescription").value;
  const privacySetting = document.getElementById("privacySetting").value;
  const image_url = document.getElementById("groupImage").value;
  const csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
  data.append("name", name);
  data.append("description", description);
  data.append("privacy_setting", privacySetting);
  data.append("image_url", image_url);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  fetch("/create_group", {
    method: "POST",
    body: data,
    credentials: "same-origin",
  })
    .then((res) => {
      if (res.status === 201) {
        res.json().then((json) => {
          console.log(json.message);
          // Close modal and potentially update UI
          window.location.reload();
        });
      } else {
        res.json().then((json) => {
          alert(json.error);
        });
      }
    })
    .catch((error) => {
      console.error(error);
      alert("An error occurred. Please try again.");
    });
};

const editGroup = () => {
  const form = document.getElementById("editGroupForm");
  const name = document.getElementById("groupName").value;
  const description = document.getElementById("groupDescription").value;
  const privacySetting = document.getElementById("privacySetting").value;
  const image_url = document.getElementById("groupImage").value;


  const groupId = document.getElementById("groupId").value;

  const data = {
    name,
    description,
    privacy_setting: privacySetting,
    image_url,
  };

  const jsonData = JSON.stringify(data);

  fetch(`/edit_group/${groupId}`, {
    method: "PUT",
    body: jsonData,
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "same-origin",
  })
    .then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          console.log(json.message);
          // Close modal and potentially update UI
          window.location = `/groups/${json.group.id}`;
        });
      } else {
        res.json().then((json) => {
          alert(json.error);
        });
      }
    })
    .catch((error) => {
      console.error(error);
      alert("An error occurred. Please try again.");
    });
};

const openInNewTab = (e) => {
  const url = e.target.closest(".bi").dataset.url
  // console.log(url)
  window.open(url, '_blank').focus()
}

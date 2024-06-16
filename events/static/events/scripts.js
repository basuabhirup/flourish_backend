document.addEventListener("DOMContentLoaded", () => {
  const hostEventModal = document.querySelector("#hostEventModal");
  const editEventModal = document.querySelector("#editEventModal");
  const inviteMemberModal = document.querySelector("#inviteMemberModal");
  const attendeeListModal = document.getElementById("attendeeListModal");
  const allEvents = document.getElementById("all-events");
  const allGroups = document.getElementById("all-groups");

  const usernameInput = document.getElementById("username");
  const addMemberButton = document.getElementById("add-member-btn");
  const suggestionList = document.getElementById("username-suggestions");
  const selectedUsersList = document.getElementById("selected-users-list");

  if (!!hostEventModal) {
    // hostEventModal.addEventListener("shown.bs.modal", function () {
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

    // populate group names with all of the user's groups
    fetch("/groups").then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          json.groups.forEach(
            (group) =>
              (hostEventModal.querySelector(
                "#hostGroupName"
              ).innerHTML += `<option value=${group.id}>${group.name}</option>`)
          );
        });
      }
    });
    // });

    hostEventModal.addEventListener("change", function (event) {
      // console.log(event.target)
      if (event.target.matches("#hostEventModal input[type='radio']")) {
        // Check if clicked element is a radio button inside the modal
        const selectedValue = event.target.value;
        const groupField = document.getElementById("groupField");
        if (selectedValue === "group") {
          groupField.style.display = "block"; // Show group field
        } else {
          groupField.style.display = "none"; // Hide group field
        }
      }
    });
  }

  if (!!editEventModal) {
    const dateInput = document.getElementById("editEventDate");
    const timeInput = document.getElementById("editEventTime");
    const date = dateInput.dataset.dateValue;
    const time = timeInput.dataset.timeValue;
    dateInput.value = new Date(
      new Date(date).getTime() - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .split("T")[0];

    timeInput.value = new Date(date)
      .toISOString()
      .split("T")[1]
      .split(":00.00")[0];

    fetch("/categories").then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          json.categories.forEach(
            (category) =>
              (editEventModal.querySelector(
                "#editEventCategory"
              ).innerHTML += `<option value=${category.id}>${category.name}</option>`)
          );
        });
      }
    });
  }

  if (!!inviteMemberModal) {
    let selectedUsernames = [];
    let usernames = [];
    const groupId = document.querySelector("#groupId").value;

    // inviteMemberModal.addEventListener("shown.bs.modal", function () {
    fetch(`/users-not-in-group/${groupId}`).then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          json.users.forEach((user) => usernames.push(user.username));
          usernameInput.addEventListener("input", handleUserInput);
        });
      } else {
        res.json(),
          then((json) => {
            alert(json.error);
          });
      }
    });
    // });

    addMemberButton.addEventListener("click", function () {
      const groupId = document.getElementById("groupId").value;

      const data = { usernames: selectedUsernames };

      // console.log(data)

      const jsonData = JSON.stringify(data);

      // console.log(jsonData)

      // API Call
      fetch(`/add-user-to-group/${groupId}`, {
        method: "POST",
        body: jsonData,
        credentials: "same-origin",
      })
        .then((res) => {
          if (res.status === 200) {
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
    });

    function handleUserInput(event) {
      const typedUsername = event.target.value.toLowerCase();
      const suggestions = usernames.filter(
        (username) =>
          username.toLowerCase().startsWith(typedUsername) &&
          !selectedUsernames.includes(username)
      );

      // Clear previous suggestions
      suggestionList.innerHTML = "";

      if (suggestions.length > 0) {
        suggestionList.classList.add("show"); // Add Bootstrap class to show dropdown
        for (const suggestion of suggestions) {
          const suggestionItem = document.createElement("li");
          suggestionItem.innerText = suggestion;
          suggestionItem.addEventListener("click", function () {
            const username = this.innerText;
            if (!selectedUsernames.includes(username)) {
              selectedUsernames.push(username);
              // Add username to selected list
              const selectedUserListItem = document.createElement("span");
              selectedUserListItem.innerText = username;
              selectedUserListItem.classList.add("px-2");
              selectedUserListItem.classList.add("py-1");
              selectedUserListItem.classList.add("me-2");
              selectedUserListItem.classList.add("mb-2");
              selectedUserListItem.classList.add("text-bg-secondary");
              selectedUserListItem.classList.add("rounded");
              selectedUserListItem.classList.add("selected-user");
              selectedUsersList.appendChild(selectedUserListItem);
              suggestionList.classList.remove("show");
              usernameInput.value = "";

              for (
                let i = 0;
                i < document.querySelectorAll(".selected-user").length;
                i++
              ) {
                document
                  .querySelectorAll(".selected-user")
                  [i].removeEventListener("click", deleteUser);
                document
                  .querySelectorAll(".selected-user")
                  [i].addEventListener("click", deleteUser);
              }
            }
          });
          suggestionList.appendChild(suggestionItem);
        }
      } else {
        suggestionList.classList.remove("show"); // Hide dropdown if no suggestions
      }
    }

    function deleteUser() {
      const index = selectedUsernames.indexOf(this.textContent);
      selectedUsernames.splice(index, 1);
      selectedUsersList.removeChild(selectedUsersList.children[index]);
    }
  }

  if (!!attendeeListModal) {
    const eventId = document.getElementById("editEventId").value;
    fetch(`/get_registered_users/${eventId}`)
      .then((response) => response.json())
      .then((json) => {
        const attendeesTableBody =
          document.getElementById("attendeesTableBody");
        attendeesTableBody.innerHTML = ""; // Clear existing content
        const data = json.data;

        data.forEach((attendee) => {
          const tableRow = document.createElement("tr");
          const fullNameCell = document.createElement("td");
          fullNameCell.textContent = attendee.full_name; // Use textContent for vanilla JS
          const emailCell = document.createElement("td");
          emailCell.textContent = attendee.email;
          const contactNumberCell = document.createElement("td");
          contactNumberCell.textContent = attendee.contact_number;

          tableRow.appendChild(fullNameCell);
          tableRow.appendChild(emailCell);
          tableRow.appendChild(contactNumberCell);

          attendeesTableBody.appendChild(tableRow);
        });
      })
      .catch((error) => {
        console.error("Error fetching attendees:", error);
        // Handle errors appropriately (e.g., display an error message)
      });
  }

  if (!!allEvents) {
    const params = new URLSearchParams(window.location.search);

    const tab = params.get("tab");
    const searchQuery = params.get("search");
    const categoryId = params.get("category_id");
    const categoryFilterInput = document.querySelector("#eventCategoryFilter");

    // populate event category with relevant options from db
    fetch("/categories").then((res) => {
      if (res.status === 200) {
        res.json().then((json) => {
          json.categories.forEach((category) => {
            if (!!categoryId && Number(categoryId) === category.id) {
              categoryFilterInput.innerHTML += `<option value=${category.id} selected>${category.name}</option>`;
            } else {
              categoryFilterInput.innerHTML += `<option value=${category.id}>${category.name}</option>`;
            }
          });
        });
      }
    });

    if (tab === "groups") {
      document.getElementById("all-events").classList.remove("show");
      document.getElementById("all-events").classList.remove("active");
      document.getElementById("all-events-button").classList.remove("active");

      document.getElementById("all-groups").classList.add("show");
      document.getElementById("all-groups").classList.add("active");
      document.getElementById("all-groups-button").classList.add("active");

      document.getElementById("categoryFilterContainer").style.display = "none";
    } else {
      document.getElementById("all-groups").classList.remove("show");
      document.getElementById("all-groups").classList.remove("active");
      document.getElementById("all-groups-button").classList.remove("active");

      document.getElementById("all-events").classList.add("show");
      document.getElementById("all-events").classList.add("active");
      document.getElementById("all-events-button").classList.add("active");

      document.getElementById("categoryFilterContainer").style.display = "flex";
    }

    if (!!searchQuery) {
      document.querySelector("#events-subtitle").innerHTML = `
        Displaying search results for query: <strong>"${searchQuery}"</strong>
        <br>
        <span role="button" class="badge text-bg-light fw-normal fs-6 mt-3" onclick="removeSearchQuery()">
          <i class="bi bi-arrow-left-square"></i>
          View all ${!!tab ? tab : "results"}
        </span>
      `;
    }
  }
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
  const first_name = document.getElementById("signupFirstName").value;
  const last_name = document.getElementById("signupLastName").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;
  const confirmation = document.getElementById("signupConfirmation").value;

  const csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
  data.append("username", username);
  data.append("first_name", first_name);
  data.append("last_name", last_name);
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
  const group = document.getElementById("hostGroupName").value;
  const category = document.getElementById("eventCategory").value;
  // const capacity = document.getElementById("eventCapacity").value;
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
  // data.append("capacity", capacity);
  data.append("image", image_url);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  if (!!groupName) {
    data.append("group", group);
  }

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
  // const form = document.getElementById("editGroupForm");
  const name = document.getElementById("editGroupName").value;
  const description = document.getElementById("editGroupDescription").value;
  const privacySetting = document.getElementById("editPrivacySetting").value;
  const image_url = document.getElementById("editGroupImage").value;

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
  const url = e.target.closest(".bi").dataset.url;
  // console.log(url)
  window.open(url, "_blank").focus();
};

const editProfile = () => {
  // const form = document.querySelector("#editProfileForm");

  const first_name = document.getElementById("editFirstName").value;
  const last_name = document.getElementById("editLastName").value;
  const bio = document.getElementById("editBio").value;
  const instagram_url = document.getElementById("editInstagramUrl").value;
  const facebook_url = document.getElementById("editFacebookUrl").value;
  const twitter_url = document.getElementById("editTwitterUrl").value;
  const linkedin_url = document.getElementById("editLinkedinUrl").value;
  const userName = document.getElementById("editUsername").value;

  const data = {
    first_name,
    last_name,
    bio,
    instagram_url,
    facebook_url,
    twitter_url,
    linkedin_url,
  };

  console.log(data);

  const jsonData = JSON.stringify(data);

  // API Call
  fetch(`/edit_profile/${userName}`, {
    method: "PUT",
    body: jsonData,
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 200) {
      res.json().then((json) => {
        console.log(json.message);
        window.location = `/profile/${json.user.username}`;
      });
    } else {
      res.json().then((json) => {
        alert(json.error);
      });
    }
  });
};

const deleteMemberFromGroup = (e) => {
  const btn = e.target.closest(".delete-member");
  // console.log(btn)
  const memberId = btn.dataset.memberId;
  // console.log(memberId)

  const groupId = document.querySelector("#groupId").value;
  console.log(groupId);

  const data = {
    memberId,
  };

  console.log(data);

  const jsonData = JSON.stringify(data);

  // API Call
  fetch(`/delete_member_from_group/${groupId}`, {
    method: "DELETE",
    body: jsonData,
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

const editEvent = () => {
  // const form = document.querySelector("#editEventForm");
  const eventId = document.getElementById("editEventId").value;
  const title = document.getElementById("editEventName").value;
  const description = document.getElementById("editEventDescription").value;
  const date = document.getElementById("editEventDate").value;
  const time = document.getElementById("editEventTime").value;
  const location = document.getElementById("editEventLocation").value;
  const category = document.getElementById("editEventCategory").value;
  // const capacity = document.getElementById("editEventCapacity").value;
  const image_url = document.getElementById("editEventImage").value;

  const data = {
    title,
    description,
    date,
    time,
    location,
    category,
    image_url,
  };

  console.log(data);

  const jsonData = JSON.stringify(data);

  // API Call
  fetch(`/edit_event/${eventId}`, {
    method: "PUT",
    body: jsonData,
    credentials: "same-origin",
  }).then((res) => {
    if (res.status === 200) {
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

const attendEvent = () => {
  const form = document.querySelector("#attendEventForm");
  const eventId = document.getElementById("attendEventId").value;
  const email = document.getElementById("attendEmail").value;
  const contact_number = document.getElementById("attendContactNumber").value;

  const csrfmiddlewaretoken = form.querySelector(
    "input[name='csrfmiddlewaretoken'][type='hidden']"
  ).value;

  const data = new FormData();
  data.append("email", email);
  data.append("contact_number", contact_number);
  data.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

  console.log(data);

  // API Call
  fetch(`/attend_event/${eventId}`, {
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

const changeTabTo = (tab) => {
  const params = new URLSearchParams(window.location.search);
  params.delete("page");
  params.set("tab", tab);
  window.location.search = params.toString();
};

const searchQuery = (e) => {
  e.preventDefault();
  const query = document.getElementById("search-query").value;
  if (window.location.pathname === "/events-and-groups") {
    const params = new URLSearchParams(window.location.search);
    const page = params.get("page");
    if (!!page) {
      params.delete("page");
    }
    params.set("search", query);
    // console.log(params)
    window.location.search = params.toString();
  } else {
    window.location = `/events-and-groups?search=${query}`;
  }
};

const removeSearchQuery = () => {
  const params = new URLSearchParams(window.location.search);
  const page = params.get("page");
  const search = params.get("search");
  if (!!page) {
    params.delete("page");
  }
  if (!!search) {
    params.delete("search");
  }
  window.location.search = params.toString();
};

const handleCategoryFilterSelection = () => {
  const categoryFilter = document.getElementById("eventCategoryFilter");
  const params = new URLSearchParams(window.location.search);
  const categoryId = params.get("category_id");
  const categoryIdInput = categoryFilter.value;
  if (categoryIdInput === "0" && !!categoryId) {
    if (!!categoryId) {
      params.delete("category_id");
    }
  } else {
    params.set("category_id", categoryIdInput);
  }
  window.location.search = params.toString();
};

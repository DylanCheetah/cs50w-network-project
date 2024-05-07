// Add page load listener
document.addEventListener("DOMContentLoaded", () => {
    // Add click handler to like buttons
    document.querySelectorAll(".btn-like").forEach((btn) => {
        btn.onclick = (event) => {
            // Like/unlike post
            if(event.target.innerHTML.indexOf("🤍") != -1) {
                fetch("/like-post", {
                    method: "POST",
                    body: JSON.stringify({
                        id: event.target.dataset.id
                    })
                })
                .then((response) => response.json())
                .then((data) => {
                    // Error?
                    if(data["error"]) {
                        console.log("Failed to like post.");
                        return;
                    }

                    // Update button emoji and like count
                    event.target.innerHTML = `❤️ ${data["likes"]}`;
                })
                .catch((error) => {
                    console.log("Failed to like post.");
                });
            } else {
                fetch("/unlike-post", {
                    method: "POST",
                    body: JSON.stringify({
                        id: event.target.dataset.id
                    })
                })
                .then((response) => response.json())
                .then((data) => {
                    // Error?
                    if(data["error"]) {
                        console.log("Failed to unlike post.");
                        return;
                    }

                    // Update button emoji and like count
                    event.target.innerHTML = `🤍 ${data["likes"]}`;
                })
                .catch((error) => {
                    console.log("Failed to like post.");
                });
            }
        };
    })

    // Add click handler to follow buttons
    document.querySelectorAll(".btn-follow").forEach((btn) => {
        btn.onclick = (event) => {
            // Follow/unfollow the user
            if(event.target.innerHTML == "Follow") {
                fetch("/profile/follow", {
                    method: "POST",
                    body: JSON.stringify({
                        id: event.target.dataset.id
                    })
                })
                .then((response) => response.json())
                .then((data) => {
                    // Error?
                    if(data["error"]) {
                        console.log("Failed to follow user.");
                        return;
                    }

                    // Update follow button and follower count
                    event.target.innerHTML = "Unfollow";
                    document.querySelector("#follower-count").innerHTML = `<strong>Followers:</strong> ${data["follower_count"]}`;
                })
                .catch((error) => {
                    console.log("Failed to follow user.");
                });
            } else {
                fetch("/profile/unfollow", {
                    method: "POST",
                    body: JSON.stringify({
                        id: event.target.dataset.id
                    })
                })
                .then((response) => response.json())
                .then((data) => {
                    // Error?
                    if(data["error"]) {
                        console.log("Failed to unfollow user.");
                        return;
                    }

                    // Update unfollow button and follower count
                    event.target.innerHTML = "Follow";
                    document.querySelector("#follower-count").innerHTML = `<strong>Followers:</strong> ${data["follower_count"]}`;
                })
                .catch((error) => {
                    console.log("Failed to unfollow user.");
                });
            }
        };
    });

    // Add click handler to edit post buttons
    document.querySelectorAll(".btn-edit").forEach((btn) => {
        btn.onclick = (event) => {
            // Edit/save post
            const post_text = document.querySelector(`#post-${event.target.dataset.id}`);
            const post_editor = document.querySelector(`#post-editor-${event.target.dataset.id}`);

            if(event.target.innerHTML == "Edit Post") {
                // Copy post text to post editor, hide post text, and show post editor
                post_editor.innerHTML = post_text.innerHTML;
                post_text.style.display = "none";
                post_editor.style.display = "block";
                post_editor.focus();

                // Change button text
                event.target.innerHTML = "Save Post";
            } else {
                // Save the modified post
                console.log("Saving post...");
                fetch("/edit-post", {
                    method: "POST",
                    body: JSON.stringify({
                        id: event.target.dataset.id,
                        content: post_editor.value
                    })
                })
                .then((response) => response.json())
                .then((data) => {
                    // Did an error occur?
                    if(data["error"]) {
                        console.log("Failed to edit post.");
                        return;
                    }

                    // Update post text, hide post editor, and show post text
                    post_text.innerHTML = post_editor.value;
                    post_editor.style.display = "none";
                    post_text.style.display = "block";

                    // Change button text
                    event.target.innerHTML = "Edit Post";
                    console.log("Post saved.");
                })
                .catch((error) => {
                    console.log(error);
                });
            }
        };
    });
});
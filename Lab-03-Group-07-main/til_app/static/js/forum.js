document.addEventListener("DOMContentLoaded", function() {
    const createPostBtn = document.getElementById("createPostBtn");
    const createPostFormContainer = document.getElementById("createPostFormContainer");
    const cancelPostBtn = document.getElementById("cancelPostBtn");
    const createPostForm = document.querySelector('.create-post-form');
    const postListContainer = document.querySelector('.post-list');

    createPostBtn.addEventListener("click", function() {
        createPostFormContainer.style.display = "block";
    });

    cancelPostBtn.addEventListener("click", function() {
        createPostFormContainer.style.display = "none";
    });

    $(createPostForm).on('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const url = this.action; // Ensure this is correctly set in the form's HTML

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                if (data.success) {
                    const newPost = `
                        <a href="/til_app/post/${data.post.id}/" class="post-box-link">
                            <div class="post-box">
                                <h3>${data.post.title}</h3>
                                <div class="post-meta">
                                    <p>by ${data.post.creator} on ${new Date(data.post.created_at).toLocaleDateString("en-US")}</p>
                                </div>
                                <div class="post-stats">
                                    <span class="like-count">❤️ 0</span>
                                    <span class="comment-count">💬 0</span>
                                </div>
                            </div>
                        </a>`;

                    const firstPost = $(postListContainer).children().first();
                    if (firstPost.length && firstPost.find('.post-box').hasClass('pinned')) {
                        firstPost.after(newPost);
                    } else {
                        $(postListContainer).prepend(newPost);
                    }

                    createPostFormContainer.style.display = "none";
                    createPostForm.reset();

                } else {
                    alert(data.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred while creating the post.');
            }
        });
    });
});

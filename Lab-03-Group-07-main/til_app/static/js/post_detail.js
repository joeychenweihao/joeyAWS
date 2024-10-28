document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = getCookie('csrftoken');

   
    function toggleLike(type, id) {
        const url = type === 'post'
            ? document.querySelector(`#like-button-post-${id}`).getAttribute('data-url')
            : document.querySelector(`#like-button-comment-${id}`).getAttribute('data-url');
        const likeButton = type === 'post'
            ? document.querySelector(`#like-button-post-${id}`)
            : document.querySelector(`#like-button-comment-${id}`);
        const likeCount = type === 'post'
            ? document.querySelector(`#like-count-post-${id}`)
            : document.querySelector(`#like-count-comment-${id}`);

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                likeButton.textContent = data.liked ? 'Unlike' : 'Like';
                likeCount.textContent = `${data.likes} likes`;
            }
        })
        .catch(error => console.error('Error:', error));
    }

    
    function bindLikeButtons() {
        document.body.addEventListener('click', function (event) {
            if (event.target.classList.contains('like-btn')) {
                const postId = event.target.getAttribute('data-post-id');
                toggleLike('post', postId);
            } else if (event.target.classList.contains('like-comment-btn')) {
                const commentId = event.target.getAttribute('data-comment-id');
                toggleLike('comment', commentId);
            }
        });
    }

 
    function bindQuoteButtons() {
        document.body.addEventListener('click', function (event) {
            if (event.target.classList.contains('quote-btn')) {
                const creator = event.target.getAttribute('data-creator');
                const commentTextArea = document.querySelector('.comment-form textarea');
                const quoteText = `@${creator} `;
                commentTextArea.value += quoteText;
                commentTextArea.focus();
            }
        });
    }


    function deleteComment(url, commentElement) {
        if (confirm("Are you sure you want to delete this comment?")) {
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    commentElement.remove();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }


    function bindDeleteCommentButtons() {
        document.body.addEventListener('click', function (event) {
            if (event.target.classList.contains('delete-comment-btn')) {
                const url = event.target.getAttribute('data-url');
                deleteComment(url, event.target.closest('.comment'));
            }
        });
    }

  
    function handleCommentSubmission() {
        const commentForm = document.querySelector('.comment-form');
        const commentsContainer = document.querySelector('.comments');

        if (commentForm) {
            commentForm.addEventListener('submit', function (event) {
                event.preventDefault();

                const formData = new FormData(commentForm);
                const url = commentForm.getAttribute('action');

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const newComment = `
                            <div class="comment">
                                <p><strong>${data.comment.creator}</strong>: ${data.comment.content}</p>
                                <p><small>${data.comment.created_at}</small></p>
                                <button class="like-comment-btn" id="like-button-comment-${data.comment.id}" data-comment-id="${data.comment.id}" data-url="${data.comment.like_url}">
                                    Like
                                </button>
                                <span id="like-count-comment-${data.comment.id}">0 Likes</span>
                                <button class="delete-btn quote-btn" data-creator="${data.comment.creator}" data-comment-id="${data.comment.id}">
                                    Quote
                                </button>
                                <button class="delete-comment-btn delete-btn" data-url="${data.comment.delete_url}">Delete</button>
                            </div>
                        `;
                        commentsContainer.insertAdjacentHTML('beforeend', newComment);
                        commentForm.reset();
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        }
    }


    const deletePostButton = document.querySelector('.delete-post-btn');
    if (deletePostButton) {
        deletePostButton.addEventListener('click', function (event) {
            event.preventDefault();

            const url = this.getAttribute('data-url');
            const forumUrl = document.getElementById('forum-url').getAttribute('data-url');

            if (confirm("Are you sure you want to delete this post?")) {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = forumUrl;
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }


    handleCommentSubmission();
    bindLikeButtons();
    bindQuoteButtons();
    bindDeleteCommentButtons();
});

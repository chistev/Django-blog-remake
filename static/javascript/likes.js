document.addEventListener('DOMContentLoaded', function(){
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(e){
            // If user is not logged in, the onclick attribute handles redirect
            if(this.hasAttribute('onclick')){
                return;
            }

            e.preventDefault()
            // A JavaScript object containing all data-* attributes
            const articleId = this.dataset.articleId
            // closest() - Goes UP the DOM tree
            const likeContainer = this.closest('.like-container')
            // querySelector() - Goes DOWN the DOM tree
            const likeCountSpan = this.querySelector('.like-count')

            const csrftoken = getCookie('csrftoken')

            fetch('/toggle-like/', {
                method:'POST',
                headers:{
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken
                },
                body: 'article_id=' + articleId
            })
            .then(response => response.json())
            .then(data => {
                if(data.error){
                    console.log('Error:', data.error)
                    return
                }

                likeCountSpan.textContent = data.total_likes;

                if (data.liked){
                    this.classList.add('liked')
                } else{
                    this.classList.remove('liked')
                }
            })
            .catch(error => {
                console.log('Error:', error)
            })
        })
    })
})

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
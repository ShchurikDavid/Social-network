let currentPage = 1;
let isLoading = false;

const postList = document.getElementById('post_content_main')
const sentinel = document.getElementById('post_loader')

const obeserve = new IntersectionObserver(async (entries)=>{
    if (entries[0].isIntersecting && isLoading === false){
        isLoading = true
        currentPage += 1
        
        const response = await fetch (
            `${window.location.pathname}?page=${currentPage}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        )

        const objectRespone = await response.json()

        if (objectRespone.posts_html){
            postList.insertAdjacentHTML("beforeend", objectRespone.posts_html)
        }

        if (!objectRespone.has_next){
            obeserve.disconnect()
        }

        isLoading = false
    }
}, {rootMargin: "50px"})

obeserve.observe(sentinel)
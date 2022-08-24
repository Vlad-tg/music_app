
const button_hidden = document.getElementById('button-index-line-top-search-button');
function SearchHiddenScript() {
    const img_search = document.querySelector('.img-index-line-top-button')
    const button_hidden = document.getElementById('button-index-line-top-search-button');
    const search_hidden = document.getElementById('div-index-line-top-search');
    const data_button = button_hidden.getAttribute('data-active')
    if (data_button === 'hidden') {
        search_hidden.style.transform = 'scale(.9)';
        search_hidden.style.display = 'block';
        search_hidden.style.transition = 'all .3s ease-in-out';
        button_hidden.style.display = 'none';
        button_hidden.style.marginLeft = '365px';
        button_hidden.style.display = 'block';
        button_hidden.setAttribute('data-active', 'active');
        img_search.setAttribute("src", "/static/core/img/close.svg");
    } else {
        button_hidden.style.marginLeft = '0';
        search_hidden.style.display = 'none';
        search_hidden.style.transform = 'scale(.0)';
        button_hidden.setAttribute('data-active', 'hidden');
        img_search.setAttribute("src", "/static/core/img/search.svg");
    }
}

button_hidden.addEventListener('click', SearchHiddenScript)



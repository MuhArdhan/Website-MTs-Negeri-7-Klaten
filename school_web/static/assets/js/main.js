function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
        let config = JSON.parse(
            swiperElement.querySelector(".swiper-config").innerHTML.trim()
        );

        if (swiperElement.classList.contains("swiper-tab")) {
            initSwiperWithCustomPagination(swiperElement, config);
        } else {
            new Swiper(swiperElement, config);
        }
    });
}

window.addEventListener("load", initSwiper);

document.addEventListener("DOMContentLoaded", function () {
    if (window.location.hash) {
        const target = document.querySelector(window.location.hash);
        if (target) {
            setTimeout(() => {
                target.scrollIntoView({ behavior: 'smooth' });
            }, 100); // Delay sedikit supaya pasti ketangkap
        }
    }
});
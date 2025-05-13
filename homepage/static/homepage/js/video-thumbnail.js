document.addEventListener("DOMContentLoaded", () => {
    const videoPlayer = document.querySelector(".main-video video");
    const thumbnails = document.querySelectorAll(".thumbnail-item");
    let currentIndex = 0;

    function playVideoAt(index) {
        const selected = thumbnails[index];
        const src = selected.getAttribute("data-src");

        if (!src) {
            console.error("Video source is null for index", index);
            return;
        }

        videoPlayer.src = src;
        videoPlayer.muted = true;  // Tắt tiếng để được phép autoplay
        videoPlayer.play().catch(err => {
            console.warn("Autoplay bị chặn:", err);
        });

        thumbnails.forEach(t => t.classList.remove("active"));
        selected.classList.add("active");

        currentIndex = index;
    }

    videoPlayer.addEventListener("ended", () => {
        let nextIndex = (currentIndex + 1) % thumbnails.length;
        playVideoAt(nextIndex);
    });

    thumbnails.forEach((thumb, idx) => {
        thumb.addEventListener("click", () => {
            playVideoAt(idx);  // vẫn giữ muted
        });
    });

    // Tự động phát video đầu tiên (tắt tiếng)
    playVideoAt(0);
});
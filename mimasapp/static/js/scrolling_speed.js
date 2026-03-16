document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.message-container');
    const scroller = document.querySelector('.scrolling-messages');
    const speed = 90; // Pixels per second
    const width = scroller.offsetWidth;
    const duration = width / speed;

    // Ensure content is duplicated in Django template for seamlessness
    // <div class="marquee-content"> {% for message in h_messages %} <span>{{ message.message }}</span> {% endfor %} {% for message in h_messages %} <span>{{ message.message }}</span> {% endfor %} </div>

    scroller.style.animation = `marquee ${duration}s linear infinite`;
    scroller.style.animationName = 'marquee'; // Define animation name in JS if needed
    scroller.style.animationDuration = `${duration}s`;
    scroller.style.animationTimingFunction = 'linear';
    scroller.style.animationIterationCount = 'infinite';
});
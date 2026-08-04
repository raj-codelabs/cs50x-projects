document.addEventListener('DOMContentLoaded', function() {
    const welcomeButton=document.getElementById('welcomeButton');
    if (welcomeButton){
        welcomeButton.addEventListener('click', function(){
            alert('Thanks for visiting!');
        });
    }

    const greetingLine=document.getElementById('greetingLine');
    if (greetingLine) {
        const hour=new Date().getHours();
        let message='Hello';
        if (hour<12) message='Good morning - happy coding!';
        else if (hour<18) message='Good afternoon - keep learning!';
        else message='Good evening - nice to see you!';
        greetingLine.textContent=message;
    }

    const clock=document.getElementById('clock');
    if (clock) {
        function updateClock() {
            clock.textContent=new Date().toLocaleTimeString();
        }
        updateClock();
        setInterval(updateClock, 1000);
    }

    const contactForm=document.getElementById('contactForm')
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const name=(document.getElementById('name') || {}).value || 'friend';
            alert('Thank you, ' + name + '! I will read your message soon.');
            contactForm.reset();
        });
    }
});

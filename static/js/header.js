document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.getElementById('profileDropdownToggle');
    const dropdownMenu = document.getElementById('profileDropdownMenu');

    dropdownToggle.addEventListener('click', function(e) {
        e.preventDefault(); // Предотвращаем переход по ссылке
        dropdownMenu.classList.toggle('show');
    });

    // Закрываем dropdown при клике вне его
    document.addEventListener('click', function(e) {
        if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});




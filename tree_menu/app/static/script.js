$(document).ready(function() {
  $('li:has(ul)').click(function(event) {
    if (event.target !== this) {
      return; // Избегаем реакции на нажатие на ссылку внутри элемента
    }

    $(this).toggleClass('expanded');
    $(this).find('ul').toggle();
  });

  // Закрываем подменю, если оно не активно
  $('li:not(.active)').find('ul').hide();
});
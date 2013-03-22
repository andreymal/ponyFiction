/**
 * Обработка AJAX-подгрузки комментариев
 * 
 * @param comments_array
 *            array JSON-массив переданных комментариев
 * @param request
 *            mixed Указатель текущей страницы комментариев
 */
function processComments(comments, page_current, num_pages) {
	// Проставляем текущий номер страницы в зависимости от указателя
	$('#page_current').val(page_current);
	// Обновляем плейсхолдер и текущий номер страницы
	$('#comments_goto_page').val('');
	$('#comments_goto_page').attr('placeholder',
			page_current + ' / ' + num_pages);
	// Очищаем предыдущие комментарии
	$('#comments-list').fadeOut('slow');
	$('#comments-list').empty();
	// Вставляем комментарии
	$('#comments-list').append(comments);
	// Показываем комментарии
	$('#comments-list').fadeIn();
	// Скрываем ненужные элементы управления
	if (page_current == 1) {
		$('#ajax_prev_comment').addClass('hidden');
		$('#ajax_next_comment').removeClass('hidden');
	} else if (page_current == num_pages) {
		$('#ajax_next_comment').addClass('hidden');
		$('#ajax_prev_comment').removeClass('hidden');
	} else {
		$('#ajax_next_comment').removeClass('hidden');
		$('#ajax_prev_comment').removeClass('hidden');
	}

}

/**
 * Подгрузка комментариев по AJAX
 */
function getComments(request) {
	var page_current = $('#page_current').val() | 0;
	var num_pages = $('#num_pages').val() | 0;
	switch (request) {
	case 'prev':
		page_current--;
		var go_page = (page_current > 0) ? page_current : 1;
		break;
	case 'next':
		page_current++;
		var go_page = (page_current <= num_pages) ? page_current : num_pages;
		break;
	default:
		var go_page = (0 < request | 0 <= num_pages) ? request | 0 : 1;
		break;
	}
	$.ajax({
		dataType : 'html',
		success : function(response) {
			processComments(response, go_page, num_pages);
		},
		error : getAjaxErrorHandler,
		type : 'GET',
		url : 'ajax/comments/page/' + go_page + '/'
	});
}

/**
 * Обработчик ошибок AJAX-подгрузки
 * 
 * @param XMLHttpRequest
 *            object Объект XMLHttpRequest
 * @param ajaxOptions
 *            string Строка, описывающая тип случившейся ошибки
 * @param thrownError
 *            object Объект исключений
 */
function getAjaxErrorHandler(XMLHttpRequest, ajaxOptions, thrownError) {
	console.warn(XMLHttpRequest);
	console.warn(ajaxOptions);
	console.warn(thrownError);
}

// Функция проверки CRSF-безопасности
function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * Голосование за рассказ по AJAX
 */
requestRunning = false;
function voteStory(request) {
	if (requestRunning) { // don't do anything if an AJAX request is pending
		return;
	}
	requestRunning = true;
	// Читаем CSRF Cookie
	var csrftoken = $.cookie('csrftoken');
	// Конфигурируем заголовок AJAX-запроса
	$.ajaxSetup({
		crossDomain : false,
		beforeSend : function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$.ajax({
		cache : false,
		data : {
			vote : request
		},
		dataType : 'json',
		error : getAjaxErrorHandler,
		success : changeVote,
		complete : function() {
			requestRunning = false;
		},
		type : 'POST',
		url : 'vote'
	});
}
// Обработка смены количества голосов
function changeVote(response) {
	$('#vote-up').text(response[0]);
	$('#vote-down').text(response[1]);
	$('#vote-msg').html(
			'<span class="alert alert-success">Ваш голос учтен!</span>');
	$('#vote-msg span').animate({
		opacity : 0.1
	}, 3500, function() {
		$('#vote-msg span').remove();
	});
}
/**
 * Добавление-удаление из избранного по AJAX
 */
function favoriteStory() {
	// Читаем CSRF Cookie
	var csrftoken = $.cookie('csrftoken');
	// Конфигурируем заголовок AJAX-запроса
	$.ajaxSetup({
		crossDomain : false,
		beforeSend : function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$.ajax({
		cache : false,
		error : getAjaxErrorHandler,
		success : changeFavorite,
		type : 'POST',
		url : 'favorite'
	});
}
// Обработка добавления-удаления из избранного
function changeFavorite(response) {
	$('#favstar').toggleClass('faved');
	if (response == '0') {
		var text = 'Рассказ удален из избранного';
	} else if (response == '1') {
		var text = 'Рассказ добавлен в избранное';
	}
	$('#fav-msg').append(
			'<span class="alert alert-success">' + text + '</span>')
	$('#fav-msg span').animate({
		opacity : 0.1
	}, 3500, function() {
		$('#fav-msg span').remove();
	});
}

// При загрузке страницы
$(function() {
	// Включаем карусель
	$('#myCarousel').slides({
		generatePagination : false,
		play : 5000,
		pause : 2500,
		hoverPause : true,
	});
	// Включаем обработку BootStrap Buttons
	// TODO: Всерьёз заняться оптимизированием кода!
	$('.bootstrap').each(
			function() {
				var group = $(this);
				var buttons_container = $('.buttons-visible', group)
				var data_container = $('.buttons-data', group)

				if (group.hasClass('checkboxes')) {
					var type = 'checkboxes'
				} else if (group.hasClass('radio')) {
					var type = 'radio'
				}
				// Обработка проставленных заранее чекбоксов и радиоселектов
				$('input', data_container).each(
						function() {
							var input = $(this);
							value = input.attr('value')
							checked = Boolean(input.attr('checked'))
							if (checked) {
								buttons_container.children(
										'button[value=' + value + ']')
										.addClass('active');
							}
						});
				// Onclick-обработчик
				$('button', buttons_container).each(
						function() {
							var button = $(this);
							button.live('click',
									function() {
										value = button.attr('value');
										if (type == 'checkboxes') {
											input = $('input:checkbox[value='
													+ value + ']',
													data_container);
											selected = Boolean($(
													'input:checked[value='
															+ value + ']',
													data_container).length);
											selected ? input
													.removeAttr('checked')
													: input.attr('checked',
															'checked');
										} else if (type == 'radio') {
											input = $('input:radio[value='
													+ value + ']',
													data_container);
											all_inputs = $('input:radio',
													data_container);
											all_inputs.removeAttr('checked');
											input.attr('checked', 'checked');
										}
									});
						});
			});
	// Подключаем обработку выбора персонажей
	$(".character-item").click(function() {
		if (Boolean($(this).children('input:checked').length)) {
			$(this).children('img').removeClass('ui-selected');
			$(this).children('input').removeAttr('checked');
		} else {
			$(this).children('img').addClass("ui-selected");
			$(this).children('input').attr('checked', 'checked');
		}
	});
	// Очистка формы поиска
	$("#reset_search").click(
			function() {
				$('input:checked').removeAttr('checked');
				$('button').removeClass('active');
				$('img').removeClass('ui-selected');
				document.getElementById('appendedInputButtons').setAttribute(
						'value', '');
				$('.span8').slideUp();
			});
	// На странице поиска...
	var re_search = new RegExp('/search/(.+)?');
	if (re_search.test(window.location.pathname)) {
		// ...проставляем классы изображениям персонажей, в зависимости от
		// выбранных скрытых чекбоксов.
		$('input[name="characters_select"][checked="checked"]').parent()
				.children('img').addClass('ui-selected');
	}
	// На странице редактирования истории...
	var re_storyedit = new RegExp('/story/[0-9]+/edit/')
	if (re_storyedit.test(window.location.pathname)) {
		// ...подключаем markItUp!
		$('#id_notes').markItUp(mySettings);
		// ...проставляем классы изображениям персонажей, в зависимости от
		// выбранных скрытых чекбоксов.
		$('.character-item input[checked="checked"]').prev().addClass(
				'ui-selected');
		// ...подключаем возможность сортировки глав "на лету"
		$('#sortable_chapters').sortable({
			// Действия при обновлении
			update : function() {
				// Читаем CSRF Cookie
				var csrftoken = $.cookie('csrftoken');
				// Конфигурируем заголовок AJAX-запроса
				$.ajaxSetup({
					crossDomain : false,
					beforeSend : function(xhr, settings) {
						if (!csrfSafeMethod(settings.type)) {
							xhr.setRequestHeader("X-CSRFToken", csrftoken);
						}
					}
				});
				// Посылаем AJAX-запрос
				$.ajax({
					cache : false,
					data : $('#sortable_chapters').sortable('serialize'),
					error : getAjaxErrorHandler,
					type : 'POST',
					url : 'ajax'
				});
			}
		});
	}
	// На странице добавления или редактирования главы
	var re_chapteredit = new RegExp('/story/[0-9]+/chapter/[0-9]+/edit/')
	var re_chapteradd = new RegExp('/story/[0-9]+/chapter/add/')
	if (re_chapteredit.test(window.location.pathname)
			|| re_chapteradd.test(window.location.pathname)) {
		$('.chapter-textarea').markItUp(mySettings);
		$('#id_notes').markItUp(mySettings);
	}
	// Голосование
	$('#vote-up').click(function() {
		voteStory('1');
	});
	$('#vote-down').click(function() {
		voteStory('-1');
	});
	$('#favstar').click(function() {
		favoriteStory()
	});
	// Переключение размера и типа шрифта
	$('.select-font').change(function() {
		if ($('.select-font').val() == '1')
			$('.chapter-text').removeClass('mono-font serif-font')
		else if ($('.select-font').val() == '2')
			$('.chapter-text').removeClass('mono-font').addClass('serif-font')
		else if ($('.select-font').val() == '3')
			$('.chapter-text').removeClass('serif-font').addClass('mono-font')
	});
	$('.select-size').change(function() {
		if ($('.select-size').val() == '1')
			$('.chapter-text').removeClass('small-font big-font')
		else if ($('.select-size').val() == '2')
			$('.chapter-text').removeClass('big-font').addClass('small-font')
		else if ($('.select-size').val() == '3')
			$('.chapter-text').removeClass('small-font').addClass('big-font')
	});
	// Управление AJAX-пагинацией
	$('#ajax_next_comment').click(function() {
		getComments('next');
	});
	$('#ajax_prev_comment').click(function() {
		getComments('prev');
	});
	$('#comments_goto_page').change(function() {
		getComments($(this).val() | 0);
	});
	// Ещё какая-то ерунда
	// ---
});
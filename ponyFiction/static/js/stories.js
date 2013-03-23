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
	$('#comments_goto_page').val('').attr('placeholder',
			page_current + ' / ' + num_pages);
	// Очищаем предыдущие комментарии, вставляем, показываем.
	$('#comments-list').fadeOut('slow').empty().append(comments).fadeIn();
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
	var re_story = new RegExp('/story/[0-9]+/');
	var story_id = window.location.pathname.match(re_story)[1];
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
		type : 'GET',
		url : '/ajax/comments/story/' + story_id + '/page/' + go_page + '/'
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
	if (requestRunning) {
		return;
	}
	requestRunning = true;

	$.ajax({
		data : {
			vote : request
		},
		dataType : 'json',
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
	$.ajax({
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
	// Конфигурируем заголовок AJAX-запроса с CSRF Cookie
	$.ajaxSetup({
		cache : false,
		crossDomain : false,
		error : getAjaxErrorHandler,
		beforeSend : function(request) {
			request.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
		}
	});
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
	var current_path = window.location.pathname;
	var re_storyadd = new RegExp('/story/add/')
	var re_storyedit = new RegExp('/story/[0-9]+/edit/')
	var re_search = new RegExp('/search/(.+)?');
	var re_chapteredit = new RegExp('/story/[0-9]+/chapter/[0-9]+/edit/');
	var re_chapteradd = new RegExp('/story/[0-9]+/chapter/add/');
	var re_story = new RegExp('/story/[0-9]+/');

	// На странице поиска...
	if (re_search.test(window.location.pathname)) {
		$('input[name="characters_select"][checked="checked"]').parent()
				.children('img').addClass('ui-selected');
	}
	// На странице добавления или редактирования истории...
	if (re_storyedit.test(current_path) || re_storyadd.test(current_path)) {
		$('#id_notes').markItUp(mySettings);
		$('.character-item input[checked="checked"]').prev().addClass(
				'ui-selected');
		// ...подключаем возможность сортировки глав "на лету"
		$('#sortable_chapters').sortable({
			// Действия при обновлении
			update : function() {
				// Посылаем AJAX-запрос
				$.ajax({
					data : $('#sortable_chapters').sortable('serialize'),
					type : 'POST',
					url : 'ajax'
				});
			}
		});
	}
	// На странице добавления или редактирования главы
	if (re_chapteredit.test(current_path) || re_chapteradd.test(current_path)) {
		$('.chapter-textarea').markItUp(mySettings);
		$('#id_notes').markItUp(mySettings);
	}
	// На странице рассказа
	if (re_story.test(current_path)) {
		$('#id_text').markItUp(mySettings);
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
	var font_selector = $('.select-font');
	var size_selector = $('.select-size');
	var chapter_text = $('.chapter-text');
	font_selector.change(function() {
		if (font_selector.val() == '1')
			chapter_text.removeClass('mono-font serif-font');
		else if (font_selector.val() == '2')
			chapter_text.removeClass('mono-font').addClass('serif-font');
		else if (font_selector.val() == '3')
			chapter_text.removeClass('serif-font').addClass('mono-font');
	});
	size_selector.change(function() {
		if (size_selector.val() == '1')
			chapter_text.removeClass('small-font big-font');
		else if (size_selector.val() == '2')
			chapter_text.removeClass('big-font').addClass('small-font');
		else if (size_selector.val() == '3')
			chapter_text.removeClass('small-font').addClass('big-font');
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
	// AJAX-удаление рассказа
	$('.story_delete').live('click', function(self) {
		if (!(re_story.test(current_path))) {
			self.stopImmediatePropagation();
			self.preventDefault();
			var url = '/ajax' + $(this).attr('href');
			$.post(url, function(data) {
				$('#story_' + data).slideUp('slow').remove();
			}).success(function() {
				$('.modal').modal('hide').remove();
			});
		} else {
			$('.modal').modal('hide').remove();
		}
	});
	// Отображение модального окна подтверждения
	$('.story_delete_confirm').click(function(self) {
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href') + 'confirm/';
		if (url.indexOf('#') == 0) {
			$(url).modal('open');
		} else {
			$.get(url, function(data) {
				$('<div class="modal hide fade">' + data + '</div>').modal();
			}).success(function() {
				$('input:text:visible:first').focus();
			});
		}
	});
	// Одобрение глав по AJAX
	$('.story_approve').click(function(self) {
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, function(data) {
			var btn = $('#story_' + data + ' .story_approve');
			if (btn.hasClass('btn-success')) {
				btn.removeClass('btn-success').text('Отменить');
			} else {
				btn.addClass('btn-success').text('Одобрить');
			}
		});
	});
	// Публикация глав по AJAX
	$('.story_publish').click(function(self) {
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, function(data) {
			var btn = $('#story_' + data + ' .story_publish');
			if (btn.hasClass('btn-primary')) {
				btn.removeClass('btn-primary').text('В черновики');
			} else {
				btn.addClass('btn-primary').text('Опубликовать');
			}
		});

	});
	// Ещё какая-то ерунда
	// ---
});
// Глобальные регулярки и прочий нужный почти везде стафф
current_path = window.location.pathname;
re_story = new RegExp('^/story/[0-9]+/(?:comments/page/[0-9]+/)?$');
re_chapter = new RegExp('^/story/[0-9]+/chapter/[0-9]+/$');
re_story_add = new RegExp('^/story/add/$');
re_story_edit = new RegExp('^/story/[0-9]+/edit/$');
re_chapter_edit = new RegExp('^/chapter/[0-9]+/edit/$');
re_chapter_add = new RegExp('^/story/[0-9]+/chapter/add/$');
re_author_overview = new RegExp('^/accounts/[0-9]+/(?:comments/page/[0-9]+/)?$');
re_author_dashboard = new RegExp(
		'^/accounts/profile/(?:comments/page/[0-9]+/)?$');
re_registration = new RegExp('^/accounts/registration/(.+)?');
re_search = new RegExp('^/search/(.+)?');
re_favorites = new RegExp('^/accounts/[0-9]+/favorites/(.+)?');
re_bookmarks = new RegExp('^/bookmarks/(.+)?');
re_submitted = new RegExp('^/submitted/(.+)?');
re_help = new RegExp('^/help/$');
re_terms = new RegExp('^/terms/$');
requestRunning = false;
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

/**
 * Обработка AJAX-подгрузки комментариев
 * 
 * @param comments
 *            string HTML-код переданных комментариев
 * @param page_current
 *            int Текущая страница комментариев
 * @param num_pages
 *            int Число страниц комментариев
 */
function processComments(comments, page_current) {
	var num_pages = $('#num_pages').val();
	var prev_link = $('#ajax_prev_comment');
	var next_link = $('#ajax_next_comment');
	var re_link = new RegExp('(.+)comments/page/[0-9]+/$');
	var new_href_prev_link = prev_link.attr('href').match(re_link)[1]
			+ 'comments/page/' + (page_current - 1) + '/';
	var new_href_next_link = next_link.attr('href').match(re_link)[1]
			+ 'comments/page/' + (page_current + 1) + '/';
	prev_link.attr('href', new_href_prev_link);
	next_link.attr('href', new_href_next_link);
	$('#comments-list').fadeOut('slow').empty().append(comments).fadeIn();
	$('#ajax_pages_comment').text(page_current + '/' + num_pages);
	if (page_current == 1) {
		prev_link.addClass('hidden');
		next_link.removeClass('hidden');
	} else if (page_current == num_pages) {
		next_link.addClass('hidden');
		prev_link.removeClass('hidden');
	} else {
		next_link.removeClass('hidden');
		prev_link.removeClass('hidden');
	}

}

/**
 * Обработка AJAX-изменения публикации рассказа
 * 
 * @param response
 *            int ID рассказа
 */
function processPublish(response) {
	if (re_story.test(current_path)) {
		var btn = $('.story_publish');
	} else {
		var btn = $('#story_' + response + ' .story_publish');
	}
	if (btn.hasClass('btn-primary')) {
		var text = 'В черновики';
	} else {
		var text = 'Опубликовать';
	}
	btn.text(text).toggleClass('btn-primary');
}
/**
 * Обработка AJAX-изменения одобрения рассказа
 * 
 * @param response
 *            int ID рассказа
 */
function processApprove(response) {
	if (re_story.test(current_path)) {
		var btn = $('.story_approve');
	} else {
		var btn = $('#story_' + response + ' .story_approve');
	}
	if (btn.hasClass('btn-primary')) {
		var text = 'Отменить';
	} else {
		var text = 'Одобрить';
	}
	btn.text(text).toggleClass('btn-primary');
}
/**
 * Обработка AJAX-изменения одобрения автора
 * 
 * @param response
 *            int ID рассказа
 */
function processAuthorApprove(response) {
	var btn = $('#author_approve');
	if (btn.hasClass('btn-primary')) {
		var text = 'Не проверен';
	} else {
		var text = 'Проверен';
	}
	btn.text(text).toggleClass('btn-primary');
}
/**
 * Обработка AJAX-изменения закладки рассказа
 * 
 * @param response
 *            int ID рассказа
 */
function processBookmark(response) {
	if (re_story.test(current_path)) {
		var btn = $('.story_bookmark');
		var msg_container = $('.story_bookmark ~ .story_bookmark_msg');
	} else {
		var btn = $('#story_' + response + ' .story_bookmark');
		var msg_container = $('#story_' + response
				+ ' .story_bookmark ~ .story_bookmark_msg');
	}
	if (btn.hasClass('bookmarked')) {
		var text = 'Рассказ удален из закладок';
	} else {
		var text = 'Рассказ добавлен в закладки';
	}
	btn.toggleClass('bookmarked');
	msg_container.append('<span class="alert alert-warning alert-mini">' + text
			+ '</span>');
	msg_container.children().animate({
		opacity : 0.01
	}, 3000, function() {
		msg_container.children().remove();
	});

}

/**
 * Обработка AJAX-изменения избранности рассказа
 * 
 * @param response
 *            int ID рассказа
 */
function processFavorite(response) {
	if (re_story.test(current_path)) {
		var btn = $('.story_favorite');
		var msg_container = $('.story_favorite ~ .story_favorite_msg');
	} else {
		var btn = $('#story_' + response + ' .story_favorite');
		var msg_container = $('#story_' + response
				+ ' .story_favorite ~ .story_favorite_msg');
	}
	if (btn.hasClass('favorited')) {
		var text = 'Рассказ удален из избранного';
	} else {
		var text = 'Рассказ добавлен в избранное';
	}
	btn.toggleClass('favorited');
	msg_container.append('<span class="alert alert-warning alert-mini">' + text
			+ '</span>');
	msg_container.children().animate({
		opacity : 0.01
	}, 3000, function() {
		msg_container.children().remove();
	});

}

/**
 * Подгрузка комментариев по AJAX
 * 
 * @param request
 *            int Адрес страницы подгрузки
 */
function getComments(url) {
	var re_page = new RegExp('/comments/page/([0-9]+)/$');
	var go_page = url.match(re_page)[1] | 0;
	$.ajax({
		type : 'GET',
		dataType : 'html',
		success : function(response) {
			processComments(response, go_page);
		},
		url : url
	});
}
/**
 * Удаление рассказа по AJAX
 * 
 * @param self
 *            object Кнопка удаления
 */
function processStoryDelete(self) {
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
}
/**
 * Удаление главы по AJAX
 * 
 * @param self
 *            object Кнопка удаления
 */
function processChapterDelete(self) {
	self.stopImmediatePropagation();
	self.preventDefault();
	var url = '/ajax' + $(this).attr('href');
	$('#sortable_chapters').sortable('destroy');
	$.post(url, function(data) {
		$('#chapters_' + data).slideUp('slow').remove();
	}).success(function() {
		$('.modal').modal('hide').remove();
		$('#sortable_chapters').sortable({
			// Действия при обновлении
			update : function() {
				$.ajax({
					data : $('#sortable_chapters').sortable('serialize'),
					type : 'POST',
					url : 'ajax'
				});
			}
		});
	});
}

/**
 * Декорация меню навигации в зависимости от текущей страницы
 */
function decorateNavbar() {
	if (current_path == '/') {
		$('#nav_index').addClass('active');
	} else if (re_search.test(current_path)) {
		$('#nav_search').addClass('active');
	} else if (re_help.test(current_path)) {
		$('#nav_help').addClass('active');
	} else if (re_favorites.test(current_path)) {
		$('#nav_favorites').addClass('active');
	} else if (re_bookmarks.test(current_path)) {
		$('#nav_bookmarks').addClass('active');
	} else if (re_submitted.test(current_path)) {
		$('#nav_submitted').addClass('active');
	} else if (re_story_add.test(current_path)) {
		$('#nav_story_add').addClass('active');
	} else if (re_author_dashboard.test(current_path)) {
		$('#nav_author_dashboard').addClass('active');
	} else if (re_author_overview.test(current_path)) {
		$('#nav_author_overview').addClass('active');
	} else if (re_registration.test(current_path)) {
		$('#nav_registration').addClass('active');
	} else if (re_terms.test(current_path)) {
		$('#nav_terms').addClass('active');
	}
}

/**
 * Голосование за рассказ по AJAX
 */
function processVote(url) {
	if (requestRunning) {
		return;
	}
	requestRunning = true;
	$.ajax({
		dataType : 'json',
		success : changeVote,
		complete : function() {
			requestRunning = false;
		},
		type : 'POST',
		url : url
	});
}
/**
 * Обработка смены количества голосов
 */
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
 * Ротатор шапок
 */
function rotateLogo() {
	var len = 9
	if ($.cookie('stories_gr') == null) {
		var stories_gr = Math.floor(Math.random() * len) + 1;
		$.cookie('stories_gr', stories_gr, {
			expires : 1
		});
	} else {
		var stories_gr = $.cookie('stories_gr');
	}
	var new_image = "url(/static/i/logopics/logopic-" + stories_gr + ".jpg)";
	$('.logopic').css('background-image', new_image);
}
/**
 * Плавающая панелька
 */
function floatingPanel() {
	var storypanel = $('#story_panel');
	var storypanelHomeY = storypanel.offset().top;
	var isFixed = false;
	var $w = $(window);
	$w.scroll(function() {
		var scrollTop = $w.scrollTop();
		var shouldBeFixed = scrollTop > storypanelHomeY;
		$('#story_panel').css('opacity: 1');
		$("#wrapper").hover(function() {
			if (isFixed) {
				$(this).find("#story_panel").stop().animate({
					opacity : 1
				});
			}
		}, function() {
			if (isFixed) {
				$(this).find("#story_panel").stop().animate({
					opacity : 0
				});
			}
		});
		// Когда скролл есть
		if (shouldBeFixed && !isFixed) {
			storypanel.css({
				position : 'fixed',
				top : 0,
				left : storypanel.offset().left + 12,
				width : storypanel.width(),
				opacity : 0
			});
			isFixed = true;
		}
		// Когда скролла нет
		else if (!shouldBeFixed && isFixed) {
			storypanel.css({
				position : 'static',
				opacity : 1.0
			});
			isFixed = false;
		}
	});
}
/**
 * Обработка состояний BootStrap Elements
 * 
 * @TODO Всерьёз заняться оптимизированием кода!
 */
function activateBootstrap() {
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
					buttons_container.children('button[value=' + value + ']')
							.addClass('active');
				}
			});
	// Onclick-обработчик
	$('button', buttons_container).each(
			function() {
				var button = $(this);
				button.live('click', function() {
					value = button.attr('value');
					if (type == 'checkboxes') {
						input = $('input:checkbox[value=' + value + ']',
								data_container);
						selected = Boolean($('input:checked[value=' + value
								+ ']', data_container).length);
						selected ? input.removeAttr('checked') : input.attr(
								'checked', 'checked');
					} else if (type == 'radio') {
						input = $('input:radio[value=' + value + ']',
								data_container);
						all_inputs = $('input:radio', data_container);
						all_inputs.removeAttr('checked');
						input.attr('checked', 'checked');
					}
				});
			});
}
// При загрузке страницы
$(function() {
	// Декорируем навигацию
	decorateNavbar();
	// Включаем ротатор шапок
	rotateLogo();
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
	$('.bootstrap').each(activateBootstrap);
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
	if (re_search.test(window.location.pathname)) {
		$('input[name="characters_select"][checked="checked"]').parent()
				.children('img').addClass('ui-selected');
	}
	// На странице добавления или редактирования рассказа
	if (re_story_edit.test(current_path) || re_story_add.test(current_path)) {
		$('#id_notes').markItUp(mySettings);
		// Простановка классов для изображений персонажей
		$('.character-item input[checked="checked"]').prev().addClass(
				'ui-selected');
		// Сортировка глав
		$('#sortable_chapters').sortable({
			// Действия при обновлении
			update : function() {
				$.ajax({
					data : $('#sortable_chapters').sortable('serialize'),
					type : 'POST',
					url : 'ajax'
				});
			}
		});
		// Отображение модального окна подтверждения удаления главы
		$('.chapter_delete_confirm').click(
				function(self) {
					self.stopImmediatePropagation();
					self.preventDefault();
					var url = '/ajax' + $(this).attr('href') + 'confirm/';
					if (url.indexOf('#') == 0) {
						$(url).modal('open');
					} else {
						$.get(
								url,
								function(data) {
									$(
											'<div class="modal hide fade">'
													+ data + '</div>').modal();
								}).success(function() {
							$('input:text:visible:first').focus();
						});
					}
				});
		// AJAX-удаление главы
		$('.chapter_delete').live('click', processChapterDelete);
	}
	// На странице справки
	if (re_help.test(current_path)) {
		$('a.tab_inline[data-toggle="tab"]').click(
				function() {
					var href = $($(this)['context']).attr('href');
					$('.nav-simple li').removeClass('active');
					$('.nav-simple li a[href="' + href + '"]').parent()
							.addClass('active');

				});
	}
	// На странице добавления или редактирования главы
	if (re_chapter_edit.test(current_path) || re_chapter_add.test(current_path)) {
		$('#id_text').markItUp(mySettings);
		$('#id_notes').markItUp(mySettings);
	}
	// На странице рассказа
	if (re_story.test(current_path)) {
		$('#id_text').markItUp(mySettings);
		// Голосование
		$('#vote-up').click(function(self) {
			self.stopImmediatePropagation();
			self.preventDefault();
			var url = '/ajax' + $(this).attr('href');
			processVote(url);
		});
		$('#vote-down').click(function(self) {
			self.stopImmediatePropagation();
			self.preventDefault();
			var url = '/ajax' + $(this).attr('href');
			processVote(url);
		});
	}
	// На странице рассказа или главы
	if (re_story.test(current_path) || re_chapter.test(current_path)) {
		// Подключаем динамическое состояние панели
		floatingPanel();
	}
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
	$('#ajax_next_comment').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		getComments(url);
	});
	$('#ajax_prev_comment').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		getComments(url);
	});
	// AJAX-удаление рассказа
	$('.story_delete').live('click', processStoryDelete);
	// Отображение модального окна подтверждения удаления рассказа
	$('.story_delete_confirm').click(function(self) {
		self.stopImmediatePropagation();
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
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, processApprove);
	});
	// Публикация глав по AJAX
	$('.story_publish').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, processPublish);
	});
	// Добавление в закладки по AJAX
	$('.story_bookmark').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, processBookmark);
	});
	// Добавление в избранное по AJAX
	$('.story_favorite').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, processFavorite);
	});
	// Одобрение автора по AJAX
	$('#author_approve').click(function(self) {
		self.stopImmediatePropagation();
		self.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, processAuthorApprove);
	});
	// Ещё какая-то ерунда
	// ---
});
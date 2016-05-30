fotuto.directive("fMenu", function () {
	return {
		restrict: 'E',
		replace: false,
		templateUrl: '/static/spa/components/fmenus/menu.html',
		controller: 'fttMenuController'
	}
});

fotuto.controller('fttMenuController', ['$scope', '$http', '$attrs', function ($scope, $http, $attrs) {
	$http.get('/api/menus/?position=' + $attrs.position).success(function (data) {
		$scope.menus = data.results
	});

	/* Provide scopes for some string used in template because a problem in html2js-processor:
		 Error: [$parse:lexerr] Lexer Error: Unexpected next character  at columns 13-13 [\] in expression [menu.mode == \'text\'].
		 check this question: http://stackoverflow.com/q/33563247/2343488
	*/
	$scope.icon_value = 'icon';
	$scope.text_value = 'text';

	$scope.open_menu = function (has_submenu, $mdOpenMenu, $event) {
		if (has_submenu) {
			$event.preventDefault();
			$mdOpenMenu($event)
		}
	}
}]);
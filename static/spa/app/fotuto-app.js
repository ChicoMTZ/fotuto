var fotuto = angular.module('fotuto', ['ngRoute', 'ngCookies', 'ngMaterial', 'ngSanitize']);

// TODO: Refactor urls by components
fotuto.config(['$routeProvider', function ($routeProvider) {
	$routeProvider
	// Component: Dashboard
		.when('/dashboard', {
			title: "Dashboard",
			templateUrl: '/static/spa/components/dashboard/index.html'
		})
		.when('/mimics', {
			title: "Mimics",
			templateUrl: '/static/spa/components/dashboard/index.html'
		})
		// Component: config-wizard
		.when('/config/intro', {
			title: "Configuration Wizard",
			templateUrl: '/static/spa/components/config-wizard/intro.html'
		})
		.when('/config/steps/1', {
			title: "Configuration Wizard | Step 1",
			templateUrl: '/static/spa/components/config-wizard/step-devices.html',
			controller: 'DeviceController'
		})
		.when('/config/steps/2', {
			title: "Configuration Wizard | Step 2",
			templateUrl: '/static/spa/components/config-wizard/step-vars.html',
		})
		.when('/config/steps/3', {
			title: "Configuration Wizard | Step 3",
			templateUrl: '/static/spa/components/config-wizard/step-scenes.html',
		})
		.when('/config/steps/4', {
			title: "Configuration Wizard | Step 4",
			templateUrl: '/static/spa/components/config-wizard/step-mimics.html',
		})
		.otherwise({
			redirectTo: '/dashboard'
		});
}]);

fotuto.config(function ($mdThemingProvider) {
	$mdThemingProvider.theme('default')
		.primaryPalette('light-green')
		.accentPalette('blue');
});

fotuto.config(function ($mdIconProvider) {
	$mdIconProvider.defaultIconSet('assets/midi/mdi.svg')
});

fotuto.run(['$rootScope', '$log', '$http', '$cookies', function ($rootScope, $log, $http, $cookies) {
	// Add header param in url requests to use CSRF token
	$http.defaults.xsrfCookieName = 'csrftoken';
	$http.defaults.xsrfHeaderName = 'X-CSRFToken';
	csrftoken = $cookies.get('csrftoken');
	if (csrftoken) {
		$http.defaults.headers.common['Authorization'] = 'Token ' + csrftoken;
	}

	// Set the page title
	$rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
		$rootScope.title = current.title;
	});
}]);

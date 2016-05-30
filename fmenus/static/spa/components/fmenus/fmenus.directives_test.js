describe('fmenus directive', function () {
	var $compile, $controller, $scope, $httpBackend;
	var template;

	beforeEach(module('fotuto'));

	beforeEach(module('templates'));

	beforeEach(inject(function (_$compile_, _$controller_, _$rootScope_, _$httpBackend_) {
		$compile = _$compile_;
		$httpBackend = _$httpBackend_;
		$controller = _$controller_;
		$scope = _$rootScope_.$new();

		// Test data to filter menu
		var position = 'view';

		/* Load mocks of the fmenus API
		 a root external menu in main position
		 a root internal menu in main position
		 a child menu to the first parent in main position
		 other child menu to the first parent in main position
		 a root menu to user position
		 */
		// TODO: Load fixtures from fmenus.fixtures.json
		//jasmine.getJSONFixtures().fixturesPath='/absolute/home/juliocesar/work/me/fotuto/fotuto/fmenus/static/spa/components/fmenus';
		// jasmine.getJSONFixtures().fixturesPath='/base/../fmenus/static/spa/components/fmenus';
		//$httpBackend.expectGET("/api/menus/").respond(getJSONFixture('fmenus.fixtures.json'));
		menu_fixtures = [
			{
				"id": 1,
				"has_submenu": false,
				"active": true,
				"order": 0,
				"home": true,
				"position": "view",
				"text": "Dashboard",
				"icon": "dashboard",
				"link": "/",
				"mode": "icon-text",
				"class_name": "",
				"style": "",
				"target": "",
				"parent": null
			},
			{
				"id": 2,
				"has_submenu": true,
				"active": true,
				"order": 1,
				"home": false,
				"position": "view",
				"text": "Social links",
				"icon": "share",
				"link": "",
				"mode": "icon-text",
				"class_name": "",
				"style": "",
				"target": "",
				"parent": null
			},
			{
				"id": 3,
				"has_submenu": false,
				"active": true,
				"order": 0,
				"home": false,
				"position": "view",
				"text": "Fotuto on Github",
				"icon": "settings",
				"link": "https://github.com/cesarcruz/fotuto",
				"mode": "icon-text",
				"class_name": "",
				"style": "",
				"target": "",
				"parent": 2
			},
			{
				"id": 4,
				"has_submenu": false,
				"active": true,
				"order": 0,
				"home": false,
				"position": "view",
				"text": "Fotuto on Facebook",
				"icon": "thumb_up",
				"link": "https://www.facebook.com/fotutoscada/",
				"mode": "icon-text",
				"class_name": "",
				"style": "",
				"target": "",
				"parent": 2
			},
			{
				"id": 5,
				"has_submenu": false,
				"active": true,
				"order": 0,
				"home": false,
				"position": "user",
				"text": "Log In",
				"icon": "login",
				"link": "#/login",
				"mode": "icon-text",
				"class_name": "",
				"style": "",
				"target": "",
				"parent": null
			}
		];
		$httpBackend.when('GET', '/api/menus/?position=' + position).respond(
			{
				"results": menu_fixtures.filter(
					function (menu) {
						return menu.position == position
					}
				)
			}
		);
		$controller('fttMenuController', {$scope: $scope, $attrs: {'position': position}});

		// Compile some HTML that uses the directive
		var element = angular.element('<f-menu position="' + position + '"></f-menu>');
		template = $compile(element)($scope);
		$httpBackend.flush();
		$scope.$digest();
	}));

	afterEach(function () {
		$httpBackend.verifyNoOutstandingExpectation();
		$httpBackend.verifyNoOutstandingRequest();
	});

	it('It should display the two root menu in position view', function () {
		var menus = template.find('md-menu');

		expect(menus.length).toEqual(2);
		expect(menus.eq(0).find('md-icon').eq(0).text()).toEqual('dashboard');  // icon
		expect(menus.eq(0).text()).toContain('Dashboard');  // text
		expect(menus.eq(1).find('md-icon').eq(0).text()).toEqual('share'); // icon
		expect(menus.eq(1).text()).toContain('Social links');  // text
	});

	it('It should display subemenu on click on first root menu', function () {
		var menus = template.find('md-menu');
		/* TODO: find a better way to find 'md-menu' in second menu on menus, menus.find('md-menu') doesn't work on jqlite,
		   see note on https://docs.angularjs.org/api/ng/function/angular.element
		*/
		var submenus = menus.eq(1).children().eq(1).children().eq(0).children();

		expect(submenus.length).toEqual(2);
		expect(submenus.eq(0).find('md-icon').eq(0).text()).toEqual('settings');  // icon
		expect(submenus.eq(0).text()).toContain('Fotuto on Github');  // text
		expect(submenus.eq(1).text()).toContain('thumb_up'); // icon
		expect(submenus.eq(1).text()).toContain('Fotuto on Facebook');  // text
	});

	// TODO: Test if all menu params

});

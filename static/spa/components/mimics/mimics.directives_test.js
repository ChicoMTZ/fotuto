describe("Mimics directives", function () {

	var $scope, $controller, $compile, $interpolate;
	var template, element;

	beforeEach(module('fotuto'));
	beforeEach(module('templates'));

	beforeEach(inject(function (_$rootScope_, _$controller_, _$compile_, _$interpolate_) {
		$scope = _$rootScope_.$new();
		$controller = _$controller_;
		$compile = _$compile_;
		$interpolate = _$interpolate_;

		$scope.mimic = {
			x: 10,
			y: 15,
			width: 20,
			height: 30,
			graphic: '<circle r="{{ (mimic.vars | getItem: \'alarm_state\').value }}" cx="10" cy="10">',
			vars: [
				{id: 1, slug: 'door_sensor', value: 0},
				{id: 2, slug: 'alarm_state', value: 'red'},
			],
			rules: []
		};

		$controller('fttMimicGraphicController', {$scope: $scope, $interpolate: $interpolate});

		// Compile some HTML that uses the directive
		element = angular.element('<ftt-mimic-graphic mimic="mimic"></ftt-mimic-graphic>');
		template = $compile(element)($scope);
		$scope.$digest();
	}));

	it("Should use svg tag for the mimic with svg graphic type", function () {
		expect(template.length).toEqual(1);
		var mimic_container = template.eq(0);
		expect(mimic_container.attr('width')).toEqual('20');
		expect(mimic_container.attr('height')).toEqual('30');
	});

	it("Should display the mimic graphic", function () {
		var mimic_graphic = template.eq(0).find('circle');
		expect(mimic_graphic.length).toEqual(1);
		expect(mimic_graphic.attr('r')).toEqual('red')
		expect(mimic_graphic.attr('cx')).toEqual('10')
	});

	it("Should change graphic with a change in a variable", function () {
		var mimic_graphic = template.eq(0).find('circle');
		expect(mimic_graphic.attr('r')).toEqual('red');
		expect($scope.mimic.graphic_rendered).toEqual('<circle r="red" cx="10" cy="10">');
		// Change variable
		/* TODO: Checks against template not working, even using isolateScope
					var isolated_scope = template.isolateScope();
					var isolated_scope = template.children().scope();
					isolated_scope.mimic.vars[1].value = 'green';
					isolated_scope.$digest();
					expect(mimic_graphic.attr('r')).toEqual('green')
		 */
		$scope.mimic.vars[1].value = 'green';
		$scope.$digest();
		// Attribute should change
		expect($scope.mimic.graphic_rendered).toEqual('<circle r="green" cx="10" cy="10">');
	});

});
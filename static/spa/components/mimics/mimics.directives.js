/**
 * Directive to display a mimic graphic
 *
 * It loads the mimic template and use the controller to observe changes in mimic vars, if so it renders the mimic
 * graphic with new values
 *
 * Usage format:
 *
 *    <ftt_mimic_graphic mimic="<MIMIC_OBJECT>">
 *
 */
fotuto.directive('fttMimicGraphic', [
	function () {
		return {
			restrict: 'E',
			replace: true,
			templateUrl: '/static/spa/components/mimics/mimic_svg.html', // TODO: Use mimic.graphic type to use the corresponding template
			controller: 'fttMimicGraphicController',
		}
	}
]);

fotuto.controller('fttMimicGraphicController', ['$scope', '$interpolate',
	function ($scope, $interpolate) {
		$scope.$watch("mimic.vars", function (value) {
			$scope.mimic.graphic_rendered = $interpolate($scope.mimic.graphic)($scope);
		}, true);
	}
]);
